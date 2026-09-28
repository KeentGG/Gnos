#!/usr/bin/env python3
"""Khan video finder -- two open doors only.

Door 1 is Khan GraphQL GET getContentSearchResults (hash 1013100632).
It returns titles with contentIds. It never returns slug or relativeUrl.
Door 2 is yt-dlp YouTube search (flat playlist, no API key).
It returns titles with 11 char IDs plus channel and duration.

Wiring. Every exact GraphQL translatedTitle of kind Video feeds YouTube as
Khan Academy "<exact title>". Non-video hits (Article, Exercise, Topic)
never feed Door 2; they need a source block, not a player. Each pair
scores on title overlap plus Khan-owned channel match plus duration
plausibility. Strong additionally requires query fit: more than half the
query words must appear in the Khan title, or the pair caps at weak.
Each pair labels as strong candidate or weak candidate. Nothing here claims
verified Khan provenance. Confirm in a browser before embedding.

Failure policy. Every door failure returns an error row. Nothing
raises past the door boundary. Timeouts are 20s GraphQL and 90s
yt-dlp. Rate limit is 0.6s between Khan calls.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from typing import TypedDict

GRAPHQL_ENDPOINT = "https://www.khanacademy.org/api/internal/graphql/getContentSearchResults"
SEARCH_HASH = "1013100632"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
KHAN_TIMEOUT_S = 20
YT_TIMEOUT_S = 90
KHAN_RATE_LIMIT_S = 0.6
YT_PRINT_FORMAT = "%(title)s ||| %(id)s ||| %(channel)s ||| %(duration_string)s ||| %(webpage_url)s"
ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")
TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
TITLE_WEIGHT = 60.0
CHANNEL_WEIGHT = 30.0
DURATION_WEIGHT = 10.0
STRONG_THRESHOLD = 70.0
QUERY_FIT_MIN = 0.5
VIDEO_KIND = "video"


class KhanHit(TypedDict):
    title: str
    kind: str
    contentId: str
    description: str
    parent: str


class YtHit(TypedDict):
    title: str
    id: str
    channel: str
    dur: str
    url: str


class ScoredPair(TypedDict):
    yt: YtHit
    overlap: float
    channel_match: bool
    duration_secs: int | None
    score: float
    verdict: str


def tokenize(title: str) -> set[str]:
    """Lowercase alphanumeric tokens. This makes overlap case proof."""
    return set(TOKEN_PATTERN.findall(title.lower()))


def overlap_ratio(khan_title: str, yt_title: str) -> float:
    """Fraction of Khan title tokens found in the YouTube title."""
    khan_tokens = tokenize(khan_title)
    if not khan_tokens:
        return 0.0
    yt_tokens = tokenize(yt_title)
    return len(khan_tokens & yt_tokens) / len(khan_tokens)


def is_khan_academy_channel(channel: str) -> bool:
    """Khan-owned channel. Spaceless prefix match covers the main channel
    plus official variants (medicine, India, Xhosa, dubs). A squatter
    starting its name with Khan Academy could pass, so title overlap
    must still carry the pair to strong."""
    squashed = re.sub(r"\s+", "", channel.strip().lower())
    return squashed.startswith("khanacademy")


def query_fit_ratio(query: str, khan_title: str) -> float:
    """Fraction of query tokens found in the Khan title. Guards the
    query-to-Khan direction, which title-overlap alone never checks."""
    return overlap_ratio(query, khan_title)


def missing_query_tokens(query: str, khan_title: str) -> list[str]:
    """Query tokens absent from the Khan title, in query order."""
    title_tokens = tokenize(khan_title)
    seen: set[str] = set()
    missing: list[str] = []
    for tok in TOKEN_PATTERN.findall(query.lower()):
        if tok not in title_tokens and tok not in seen:
            seen.add(tok)
            missing.append(tok)
    return missing


def parse_duration_to_seconds(raw: str) -> int | None:
    """Parse H:MM:SS or M:SS or S to seconds. None when unparseable."""
    text = (raw or "").strip().lower()
    if not text or text in {"na", "n/a", "none", "live"}:
        return None
    try:
        parts = [int(p) for p in text.split(":")]
    except ValueError:
        try:
            return int(float(text))
        except ValueError:
            return None
    total = 0
    for part in parts:
        total = total * 60 + part
    return total


def duration_points(raw: str) -> tuple[float, int | None]:
    """Plausibility only. GraphQL sends no duration to compare against."""
    secs = parse_duration_to_seconds(raw)
    if secs is None:
        return 0.0, None
    if 60 <= secs <= 2400:
        return DURATION_WEIGHT, secs
    if 30 <= secs < 60 or 2400 < secs <= 7200:
        return DURATION_WEIGHT / 2, secs
    return 0.0, secs


def score_pair(khan_title: str, yt: YtHit) -> ScoredPair:
    """Score one pair. Pure function. Never raises on bad input."""
    try:
        overlap = overlap_ratio(khan_title, yt.get("title", ""))
        channel_match = is_khan_academy_channel(yt.get("channel", ""))
        dpts, secs = duration_points(yt.get("dur", ""))
        score = round(overlap * TITLE_WEIGHT + (CHANNEL_WEIGHT if channel_match else 0.0) + dpts, 1)
        verdict = "strong candidate" if score >= STRONG_THRESHOLD else "weak candidate"
        return {"yt": yt, "overlap": round(overlap, 3), "channel_match": channel_match,
                "duration_secs": secs, "score": score, "verdict": verdict}
    except Exception:
        fallback: YtHit = {"title": yt.get("title", ""), "id": yt.get("id", ""),
                           "channel": yt.get("channel", ""), "dur": yt.get("dur", ""),
                           "url": yt.get("url", "")}
        return {"yt": fallback, "overlap": 0.0, "channel_match": False,
                "duration_secs": None, "score": 0.0, "verdict": "weak candidate"}


def parent_chain_text(learnable: dict) -> str:
    """Walk parentTopic to parent. Cap at 4 since the chain is unbounded."""
    chain: list[str] = []
    node = learnable.get("parentTopic") if isinstance(learnable, dict) else None
    depth = 0
    while isinstance(node, dict) and depth < 4:
        title = node.get("translatedTitle")
        if isinstance(title, str) and title.strip():
            chain.append(title.strip())
        node = node.get("parent")
        depth += 1
    return " > ".join(reversed(chain))


def khan_search(query: str, num_results: int) -> tuple[bool, list[KhanHit] | str]:
    """Door 1 GET. Returns ok flag with hits or error. Never raises."""
    variables = json.dumps({"query": query, "numResults": num_results})
    url = GRAPHQL_ENDPOINT + "?hash=" + SEARCH_HASH + "&variables=" + urllib.parse.quote(variables)
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=KHAN_TIMEOUT_S) as resp:
            data = json.load(resp)
    except Exception as exc:
        return False, "request failed: " + str(exc)[:300]
    try:
        results = data["data"]["searchPage"]["results"]
        if not isinstance(results, list):
            raise TypeError("results is not a list")
    except (KeyError, TypeError, AttributeError) as exc:
        shape = str(data)[:300] if isinstance(data, dict) else type(data).__name__
        return False, "unexpected shape (" + str(exc)[:120] + "): " + shape
    hits: list[KhanHit] = []
    try:
        for row in results:
            if not isinstance(row, dict):
                continue
            learnable = row.get("learnableContent") or {}
            if not isinstance(learnable, dict):
                learnable = {}
            # Slug and relativeUrl stay unread on purpose. This endpoint
            # no longer sends them. Expecting them caused empty links.
            title = learnable.get("translatedTitle") or ""
            desc = learnable.get("translatedDescription") or ""
            hits.append({
                "title": str(title),
                "kind": str(row.get("kind") or ""),
                "contentId": str(row.get("contentId") or ""),
                "description": str(desc)[:220].replace("\n", " ").replace("\r", " "),
                "parent": parent_chain_text(learnable),
            })
    except Exception as exc:
        return False, "parse failed: " + str(exc)[:200]
    return True, hits


def yt_search_for_title(khan_title: str, per_title: int) -> tuple[bool, list[YtHit] | str]:
    """Door 2. Search Khan Academy plus exact title. Never raises."""
    clean = (khan_title or "").replace('"', "'").strip()
    if not clean:
        return False, "skipped: empty translatedTitle, no YouTube query issued"
    query = 'Khan Academy "' + clean + '"'
    arg = "ytsearch" + str(per_title) + ":" + query
    cmd = ["yt-dlp", arg, "--print", YT_PRINT_FORMAT,
           "--flat-playlist", "--no-warnings", "--skip-download"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=YT_TIMEOUT_S)
    except FileNotFoundError:
        return False, "yt-dlp not installed"
    except subprocess.TimeoutExpired:
        return False, "yt-dlp search timed out after " + str(YT_TIMEOUT_S) + "s"
    except Exception as exc:
        return False, "yt-dlp launch failed: " + str(exc)[:200]
    if proc.returncode != 0:
        err = (proc.stderr or "").strip()[:300] or "yt-dlp failed"
        return False, err
    rows: list[YtHit] = []
    try:
        for line in (proc.stdout or "").strip().splitlines():
            parts = [p.strip() for p in line.split("|||")]
            if len(parts) < 5:
                continue
            title, vid, channel, dur, page_url = parts[:5]
            if not ID_PATTERN.fullmatch(vid):
                continue
            rows.append({"title": title, "id": vid, "channel": channel, "dur": dur, "url": page_url})
    except Exception as exc:
        return False, "output parse failed: " + str(exc)[:200]
    if not rows:
        return False, "no parseable results (all IDs filtered or empty output)"
    return True, rows


def escape_md(cell: str, limit: int = 0) -> str:
    """Make one pipe safe table cell. Raw pipes break Markdown tables."""
    text = (cell or "").replace("|", "/").replace("\n", " ").replace("\r", " ")
    text = re.sub(r"\s+", " ", text).strip()
    if limit and len(text) > limit:
        text = text[:limit].rstrip() + "…"
    return text


def build_report(queries: list[str], num_results: int, per_title: int) -> tuple[str, dict[str, str | int]]:
    """Run both doors per query. Collect error rows. Never raises."""
    lines: list[str] = []
    khan_ok = 0
    khan_fail = 0
    yt_ok = 0
    yt_fail = 0
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append("# Khan video finder report")
    lines.append("")
    lines.append("Generated: " + now + " | queries: " + str(len(queries))
                 + " | Khan numResults=" + str(num_results) + " | YouTube per-title=" + str(per_title))
    lines.append("")
    lines.append("Method (two open doors only, no bot wall bypass). Door 1 is Khan GraphQL"
                 " getContentSearchResults (hash 1013100632) for titles with contentIds."
                 " Door 2 is yt-dlp YouTube search for IDs with durations."
                 " ContentForPath is stale and HTML scraping is challenge walled, so neither runs here.")
    lines.append("")
    lines.append("Status key. Every Khan Video title with YouTube hit pair is a strong candidate"
                 " or weak candidate by title overlap plus Khan-owned channel match"
                 " plus duration plausibility, capped at weak unless more than half"
                 " the query words appear in the Khan title. Non-video Khan hits"
                 " never feed Door 2. Nothing here is verified Khan provenance."
                 " Confirm in a browser before embedding. Khan GraphQL sends no slug,"
                 " relativeUrl, or duration, so no watch URL or duration cross check is claimed.")
    lines.append("")
    for q in queries:
        lines.append("## Query: " + q)
        lines.append("")
        try:
            ok, res = khan_search(q, num_results)
        except Exception as exc:
            ok, res = False, "unexpected: " + str(exc)[:200]
        if ok:
            assert isinstance(res, list)
            khan_ok += 1
            lines.append("### Door 1 Khan GraphQL `" + escape_md(q, 80) + "` with " + str(len(res)) + " hits")
            lines.append("")
            lines.append("| # | Title | Kind | contentId | Parent path | Description |")
            lines.append("|---|-------|------|-----------|-------------|-------------|")
            if not res:
                lines.append("| — | _no hits_ | — | — | — | — |")
            for i, hit in enumerate(res, 1):
                lines.append("| " + str(i) + " | " + escape_md(hit["title"], 90) + " | "
                             + escape_md(hit["kind"], 20) + " | `" + escape_md(hit["contentId"], 40) + "` | "
                             + escape_md(hit["parent"], 90) + " | _" + escape_md(hit["description"], 140) + "_ |")
        else:
            assert isinstance(res, str)
            khan_fail += 1
            lines.append("### Door 1 Khan GraphQL `" + escape_md(q, 80) + "` FAILED")
            lines.append("")
            lines.append("| # | Title | Kind | contentId | Parent path | Description |")
            lines.append("|---|-------|------|-----------|-------------|-------------|")
            lines.append("| — | _error: " + escape_md(str(res), 200) + "_ | — | — | — | — |")
            lines.append("")
            lines.append("Door 2 skipped for this query. No exact translatedTitle exists to feed it.")
            lines.append("")
            time.sleep(KHAN_RATE_LIMIT_S)
            continue
        lines.append("")
        time.sleep(KHAN_RATE_LIMIT_S)
        assert isinstance(res, list)
        lines.append("### Door 2 YouTube cross check (exact title feeds Khan Academy query)")
        lines.append("")
        if not res:
            lines.append("_No Khan titles to cross check._")
            lines.append("")
            continue
        for hit in res:
            kt = hit.get("title", "")
            kind = (hit.get("kind", "") or "").strip().lower()
            lines.append('#### Khan title "' + escape_md(kt, 100) + '"')
            lines.append("")
            if not kt.strip():
                yt_fail += 1
                lines.append("| Khan title | YouTube title | Channel | Dur | ID | Score | Verdict |")
                lines.append("|---|---|---|---|---|---|---|")
                lines.append("| _empty_ | _error: skipped, empty translatedTitle_ | — | — | — | 0.0 | weak candidate |")
                lines.append("")
                continue
            if kind != VIDEO_KIND:
                yt_fail += 1
                lines.append("| Khan title | YouTube title | Channel | Dur | ID | Score | Verdict |")
                lines.append("|---|---|---|---|---|---|---|")
                lines.append("| " + escape_md(kt, 60) + " | _skipped: kind is "
                             + escape_md(hit.get("kind", ""), 20)
                             + ", not a video; use a source block, not a player_ | — | — | — | 0.0 | weak candidate |")
                lines.append("")
                continue
            fit = query_fit_ratio(q, kt)
            if fit <= QUERY_FIT_MIN:
                missing = ", ".join(missing_query_tokens(q, kt)[:6]) or "—"
                lines.append("_Query fit " + str(round(fit, 3)) + " — missing from Khan title: "
                             + escape_md(missing, 80) + ". Strong is blocked:"
                             " more than half the query words must appear in the Khan title._")
                lines.append("")
            try:
                yok, yres = yt_search_for_title(kt, per_title)
            except Exception as exc:
                yok, yres = False, "unexpected: " + str(exc)[:200]
            if not yok:
                assert isinstance(yres, str)
                yt_fail += 1
                lines.append("| Khan title | YouTube title | Channel | Dur | ID | Score | Verdict |")
                lines.append("|---|---|---|---|---|---|---|")
                lines.append("| " + escape_md(kt, 60) + " | _error: " + escape_md(str(yres), 200)
                             + "_ | — | — | — | 0.0 | weak candidate |")
                lines.append("")
                continue
            assert isinstance(yres, list)
            yt_ok += 1
            scored = [score_pair(kt, row) for row in yres]
            if fit <= QUERY_FIT_MIN:
                for sp in scored:
                    if sp["score"] >= STRONG_THRESHOLD:
                        sp["score"] = STRONG_THRESHOLD - 0.1
                        sp["verdict"] = "weak candidate"
            scored.sort(key=lambda s: s["score"], reverse=True)
            lines.append("| # | YouTube title | Channel | Dur | ID | Link | Overlap | Khan channel | Score | Verdict |")
            lines.append("|---|---|---|---|---|---|---|---|---|---|")
            for j, sp in enumerate(scored, 1):
                yt = sp["yt"]
                lines.append("| " + str(j) + " | " + escape_md(yt["title"], 80) + " | "
                             + escape_md(yt["channel"], 30) + " | " + escape_md(yt["dur"], 12) + " | `"
                             + escape_md(yt["id"], 15) + "` | " + escape_md(yt["url"], 60) + " | "
                             + str(sp["overlap"]) + " | " + ("yes" if sp["channel_match"] else "no")
                             + " | " + str(sp["score"]) + " | " + sp["verdict"] + " |")
            lines.append("")
    yt_version = "missing"
    try:
        found = shutil.which("yt-dlp")
        if found:
            ver = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True, timeout=15)
            yt_version = (ver.stdout or "").strip().splitlines()[0][:40] if ver.stdout.strip() else "installed, version unknown"
        else:
            yt_version = "not installed"
    except Exception as exc:
        yt_version = "check failed: " + str(exc)[:120]
    lines.append("## Methods health")
    lines.append("")
    lines.append("| Door | Check | Status | Detail |")
    lines.append("|------|-------|--------|--------|")
    lines.append("| 1 Khan GraphQL getContentSearchResults hash 1013100632 | queries ok or failed | "
                 + ("OK" if khan_fail == 0 else "PARTIAL") + " | " + str(khan_ok) + " ok with "
                 + str(khan_fail) + " failed, timeout " + str(KHAN_TIMEOUT_S) + "s, gap "
                 + str(KHAN_RATE_LIMIT_S) + "s |")
    lines.append("| 2 yt-dlp flat playlist search | title feeds ok or failed | "
                 + ("OK" if yt_fail == 0 else "PARTIAL") + " | " + str(yt_ok) + " ok with "
                 + str(yt_fail) + " failed, timeout " + str(YT_TIMEOUT_S) + "s, yt-dlp "
                 + escape_md(yt_version, 40) + " |")
    lines.append("| policy | failure handling | OK | every door failure is an error row and the script never raises past doors |")
    lines.append("| policy | provenance | OK | strong or weak CANDIDATE only and never verified Khan provenance |")
    lines.append("")
    health = {"khan_ok": khan_ok, "khan_fail": khan_fail, "yt_ok": yt_ok, "yt_fail": yt_fail, "yt_version": yt_version}
    return "\n".join(lines) + "\n", health


def parse_args(argv: list[str]) -> argparse.Namespace:
    """CLI. Report path plus optional queries. Example script REPORT query."""
    parser = argparse.ArgumentParser(description="Khan video finder with two open doors. Writes a Markdown report.")
    parser.add_argument("report", help="Path of the Markdown report to write")
    parser.add_argument("queries", nargs="*", help="Search queries (default Bayes theorem)")
    parser.add_argument("--num-results", type=int, default=4, help="Khan hits per query from 1 to 10")
    parser.add_argument("--yt-per-title", type=int, default=3, help="YouTube hits per exact Khan title from 1 to 5")
    args = parser.parse_args(argv)
    if not args.queries:
        args.queries = ["Bayes theorem"]
    if not (1 <= args.num_results <= 10):
        parser.error("--num-results must be 1..10")
    if not (1 <= args.yt_per_title <= 5):
        parser.error("--yt-per-title must be 1..5")
    if not args.report.strip():
        parser.error("report path must not be empty")
    return args


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns 0 on report write and 2 on CLI or IO failure."""
    try:
        args = parse_args(argv if argv is not None else sys.argv[1:])
    except SystemExit as exc:
        code = exc.code
        if code is None:
            return 0
        return code if isinstance(code, int) else 2
    try:
        markdown, _health = build_report(args.queries, args.num_results, args.yt_per_title)
    except Exception as exc:
        print("error: report build failed: " + str(exc)[:300], file=sys.stderr)
        return 2
    report_path = os.path.abspath(os.path.expanduser(args.report))
    try:
        parent = os.path.dirname(report_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        retest_q = " ".join('"' + q.replace('"', "'") + '"' for q in args.queries)
        retest = ("```bash\npython3 \"" + sys.argv[0] + "\" \"" + report_path + "\" " + retest_q
                  + " --num-results " + str(args.num_results) + " --yt-per-title " + str(args.yt_per_title) + "\n```\n")
        full = markdown + "## Retest\n\n" + retest
        tmp_path = report_path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as fh:
            fh.write(full)
        os.replace(tmp_path, report_path)
    except Exception as exc:
        print("error: cannot write report '" + report_path + "': " + str(exc)[:300], file=sys.stderr)
        return 2
    print("Wrote " + report_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
