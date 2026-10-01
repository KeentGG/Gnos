#!/usr/bin/env python3
"""GNOS visual-levels harness: 41 prompts (E/P/S/V x L01-10), scaffold + gallery + auto-score.

Owns mechanics for the visual stress tests. Lightweight: everything lives under
tests/visual-levels/, no learner records, no course.json edits.
MCP fallback is honest: excalidraw/pinepaper servers are configured in .mcp.json
but may not be connected in a given host. There is NO svg fallback: E produces
a real Excalidraw scene via the excalidraw MCP server (read_me -> create_view ->
inspected scene + exported PNG + view link), and P produces a real Pinepaper
export via the pinepaper MCP server (agent_start_job -> batch_execute ->
validate_scene -> export). If a server is unavailable the worker makes one
error-based correction, then marks the item failed with the diagnostic — never
a substituted SVG claimed as the real thing.
"""
import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VDIR = ROOT / "tests" / "visual-levels"

MATRIX = [
    # ---- Excalidraw track (E): static inspectable sketch, output.svg ----
    dict(id="E01", track="excalidraw", level=1, subject="math", title="Slope triangle y=2x",
         claim="A learner can see rise over run for y=2x.",
         brief="Draw axes, line y=2x, one slope triangle with rise/run labeled.",
         must_include=["x axis", "y axis", "y=2x", "rise=2", "run=1"],
         continuity=["math symbols", "blue axes, black line, red triangle"],
         acceptance=["all 5 labels verbatim in SVG", "no overlap at 800px wide"],
         skill_route="skills/excalidraw/SKILL.md", output="output.png"),
    dict(id="E02", track="excalidraw", level=2, subject="physics", title="Pendulum forces at 20 deg",
         claim="A learner can see gravity vs tension at 20 deg displacement.",
         brief="Draw pivot, string at 20 deg, bob, gravity arrow down, tension arrow along string.",
         must_include=["pivot", "20 deg", "mg", "T", "bob"],
         continuity=["physics units deg", "red gravity, blue tension"],
         acceptance=["arrow directions correct", "labels verbatim"],
         skill_route="skills/excalidraw/SKILL.md", output="output.png"),
    dict(id="E03", track="excalidraw", level=3, subject="computer-science", title="BFS visit order 3 nodes",
         claim="A learner can see BFS visits A then B,C.",
         brief="Draw nodes A,B,C with directed edges A->B, A->C, numbered visit badges 1,2,3.",
         must_include=["A", "B", "C", "visit 1", "visit 2"],
         continuity=["CS graph layout left-to-right"],
         acceptance=["edges directed", "order badges present"],
         skill_route="skills/excalidraw/SKILL.md", output="output.png"),
    dict(id="E04", track="excalidraw", level=4, subject="biology", title="Cell boundary + organelles",
         claim="A learner can see what is inside vs outside the cell.",
         brief="Draw membrane boundary containing nucleus, mitochondria, ribosome; label outside.",
         must_include=["membrane", "nucleus", "mitochondria", "ribosome", "outside"],
         continuity=["bio terms, containment behind objects"],
         acceptance=["boundary contains 3 parts", "outside label present"],
         skill_route="skills/excalidraw/SKILL.md", output="output.png"),
    dict(id="E05", track="excalidraw", level=5, subject="physics", title="Two force vectors to scale",
         claim="A learner can compare 10N vs 20N vectors drawn to scale.",
         brief="Draw two horizontal arrows with 1:2 length ratio, labeled 10N and 20N with scale note.",
         must_include=["10N", "20N", "scale", "N"],
         continuity=["SI units N, same baseline"],
         acceptance=["length ratio ~2x", "units on both"],
         skill_route="skills/excalidraw/SKILL.md", output="output.png"),
    dict(id="E06", track="excalidraw", level=6, subject="history", title="Dated timeline + boundary map",
         claim="A learner can place 3 dated decisions on time and place.",
         brief="Draw timeline 1939,1941,1945 with matching map pins A,B,C and one boundary line.",
         must_include=["1939", "1941", "1945", "boundary"],
         continuity=["dates identical in both views"],
         acceptance=["3 dates + boundary present"],
         skill_route="skills/excalidraw/SKILL.md", output="output.png"),
    dict(id="E07", track="excalidraw", level=7, subject="economics", title="Supply/demand equilibrium",
         claim="A learner can read equilibrium P*,Q* off crossing curves.",
         brief="Draw S/D curves crossing, dashed lines to P*=5, Q*=100, dense but non-overlapping labels.",
         must_include=["Supply", "Demand", "P*=5", "Q*=100", "equilibrium"],
         continuity=["econ color: blue demand, orange supply"],
         acceptance=["crossing + dashed guides", "labels legible"],
         skill_route="skills/excalidraw/SKILL.md", output="output.png"),
    dict(id="E08", track="excalidraw", level=8, subject="economics", title="Two linked markets",
         claim="A learner can compare equilibrium across two side-by-side markets.",
         brief="Draw two S/D panels with same color meanings, link arrow showing spillover.",
         must_include=["Market A", "Market B", "spillover", "P*", "Q*"],
         continuity=["same colors both panels"],
         acceptance=["two panels + link arrow"],
         skill_route="skills/excalidraw/SKILL.md", output="output.png"),
    dict(id="E09", track="excalidraw", level=9, subject="chemical-engineering", title="Reactor boundary flows",
         claim="A learner can trace mass+energy across the reactor boundary.",
         brief="Draw system boundary, inflow, outflow, heat arrow, reactor vessel with stirrer.",
         must_include=["system boundary", "inflow", "outflow", "Q heat", "reactor"],
         continuity=["transport arrows: green in, purple out, red heat"],
         acceptance=["boundary + 3 crossings labeled"],
         skill_route="skills/excalidraw/SKILL.md", output="output.png"),
    dict(id="E10", track="excalidraw", level=10, subject="artificial-intelligence", title="Training pipeline + leakage boundary",
         claim="A learner can see where test leakage crosses the eval boundary.",
         brief="Draw pipeline data->train->eval with trust boundary, red leakage arrow crossing it, metric label.",
         must_include=["train", "test", "eval boundary", "leakage", "accuracy"],
         continuity=["red=violation, gray=boundary"],
         acceptance=["boundary + violation arrow distinct"],
         skill_route="skills/excalidraw/SKILL.md", output="output.png"),
    # ---- Pinepaper track (P): linked/chart/motion/interactive, self-contained HTML ----
    dict(id="P01", track="pinepaper", level=1, subject="math", title="Fixed triangle sides",
         claim="A learner can read three labeled sides of one triangle.",
         brief="Diagram: triangle with sides a,b,c labeled; caption states relation to inspect.",
         must_include=["side a", "side b", "side c", "triangle"],
         continuity=["math symbols italic"],
         acceptance=["3 side labels verbatim", "renders in iframe"],
         skill_route="skills/pinepaper/SKILL.md", output="output.html"),
    dict(id="P02", track="pinepaper", level=2, subject="physics", title="Free-body + value table",
         claim="A learner can match arrows to numbers in the table.",
         brief="Diagram plus table: same mg=9.8N, T=9.2N values in both.",
         must_include=["mg=9.8N", "T=9.2N", "table"],
         continuity=["same numbers diagram+table"],
         acceptance=["values agree", "units present"],
         skill_route="skills/pinepaper/SKILL.md", output="output.html"),
    dict(id="P03", track="pinepaper", level=3, subject="computer-science", title="Queue states + length chart",
         claim="A learner can link queue states to a length-over-time chart.",
         brief="Ordered states q0..q3 plus bar chart of lengths 0,1,2,1 tied to same steps.",
         must_include=["q0", "q3", "length chart", "enqueue", "dequeue"],
         continuity=["same step labels both views"],
         acceptance=["chart bars match states"],
         skill_route="skills/pinepaper/SKILL.md", output="output.html"),
    dict(id="P04", track="pinepaper", level=4, subject="economics", title="Demand curve + exact table",
         claim="A learner can verify each plotted point against the table.",
         brief="Curve through (1,10),(2,8),(3,6) with table of identical points; sourced-data label.",
         must_include=["(1,10)", "(2,8)", "(3,6)", "sourced data"],
         continuity=["exact values, no smoothing lie"],
         acceptance=["3 points match table"],
         skill_route="skills/pinepaper/SKILL.md", output="output.html"),
    dict(id="P05", track="pinepaper", level=5, subject="physics", title="Pendulum motion + linked chart",
         claim="A learner can see position and velocity change together.",
         brief="Animated bob + linked sine chart with moving dot; play/pause; same angle state.",
         must_include=["angle", "velocity", "play", "chart"],
         continuity=["same pendulum, rad units"],
         acceptance=["motion and chart agree", "controls work sandboxed"],
         skill_route="skills/pinepaper/SKILL.md", output="output.html"),
    dict(id="P06", track="pinepaper", level=6, subject="biology", title="Diffusion gradient + profile",
         claim="A learner can connect particle spread to concentration profile.",
         brief="Animated particles + concentration curve updating together; assumption label.",
         must_include=["high C", "low C", "flux", "simulated output"],
         continuity=["simulated vs measured labeled"],
         acceptance=["both views update together"],
         skill_route="skills/pinepaper/SKILL.md", output="output.html"),
    dict(id="P07", track="pinepaper", level=7, subject="physics", title="Driven oscillation no clipping",
         claim="A learner can inspect resonance without clipped labels.",
         brief="Motion + amplitude-vs-frequency chart, drive slider, all labels in frame at 1280x800.",
         must_include=["drive f", "amplitude", "resonance", "Hz"],
         continuity=["Hz everywhere"],
         acceptance=["no clipping", "slider rewires chart+motion"],
         skill_route="skills/pinepaper/SKILL.md", output="output.html"),
    dict(id="P08", track="pinepaper", level=8, subject="chemical-engineering", title="Heat model + field + graph",
         claim="A learner can tie heat input to field and time graph.",
         brief="Heater slider drives 1D rod field colors + T(t) graph; model assumptions shown.",
         must_include=["heater W", "T(t)", "assumptions", "degC"],
         continuity=["degC, watts labeled"],
         acceptance=["three views share state"],
         skill_route="skills/pinepaper/SKILL.md", output="output.html"),
    dict(id="P09", track="pinepaper", level=9, subject="economics", title="Policy slider + export-safe controls",
         claim="A learner can test a tax policy and keep controls after export.",
         brief="Tax slider shifts equilibrium, surplus readout; controls survive sandboxed iframe export.",
         must_include=["tax", "surplus", "equilibrium", "reset"],
         continuity=["USD units"],
         acceptance=["controls work in viewer iframe", "reset restores"],
         skill_route="skills/pinepaper/SKILL.md", output="output.html"),
    dict(id="P10", track="pinepaper", level=10, subject="physics", title="Wave + spectrum + controls",
         claim="A learner can vary a wave and read its spectrum.",
         brief="String motion + spectrum bars + frequency/amplitude sliders; prediction question.",
         must_include=["frequency", "amplitude", "spectrum", "prediction"],
         continuity=["Hz, m units"],
         acceptance=["spectrum follows sliders", "all labels consistent"],
         skill_route="skills/pinepaper/SKILL.md", output="output.html"),
    # ---- Simulation track (S): self-contained HTML learner-controlled ----
    dict(id="S01", track="simulation", level=1, subject="math", title="Slope slider",
         claim="Learner predicts sign of change before moving slope slider.",
         brief="One slider m in y=mx; readout; prediction prompt; reset.",
         must_include=["slope m", "reset", "prediction", "y=mx"],
         continuity=["math notation KaTeX-style"],
         acceptance=["slider rewires line+readout", "reset works", "no network fetch"],
         skill_route="skills/subject/SKILL.md", output="sim.html"),
    dict(id="S02", track="simulation", level=2, subject="physics", title="Pendulum angle+length",
         claim="Learner tests how length changes period.",
         brief="Sliders angle, length; period readout T=2pi sqrt(L/g); reset.",
         must_include=["angle deg", "length m", "period s", "reset"],
         continuity=["SI units on all controls"],
         acceptance=["T formula correct", "responsive 1280x800"],
         skill_route="skills/subject/SKILL.md", output="sim.html"),
    dict(id="S03", track="simulation", level=3, subject="computer-science", title="BFS stepper",
         claim="Learner steps through BFS and predicts next visit.",
         brief="Buttons next/reset, visited list, queue display; prediction prompt.",
         must_include=["next", "reset", "queue", "visited"],
         continuity=["same graph A-B-C"],
         acceptance=["step order correct", "reset clears"],
         skill_route="skills/subject/SKILL.md", output="sim.html"),
    dict(id="S04", track="simulation", level=4, subject="math", title="Threshold + sampling histogram",
         claim="Learner varies threshold and sample size, reads histogram.",
         brief="Sliders threshold, n; histogram of 100 draws; reset; assumptions shown.",
         must_include=["threshold", "n", "histogram", "assumptions"],
         continuity=["probability units"],
         acceptance=["histogram updates", "reset works"],
         skill_route="skills/subject/SKILL.md", output="sim.html"),
    dict(id="S05", track="simulation", level=5, subject="physics", title="Projectile range",
         claim="Learner finds angle maximizing range at fixed v0.",
         brief="Sliders v0, angle; range readout; trajectory canvas; reset.",
         must_include=["v0 m/s", "angle deg", "range m", "g=9.81"],
         continuity=["SI units, g stated"],
         acceptance=["range math correct", "canvas in frame"],
         skill_route="skills/subject/SKILL.md", output="sim.html"),
    dict(id="S06", track="simulation", level=6, subject="biology", title="Logistic growth r/K",
         claim="Learner separates growth rate from carrying capacity.",
         brief="Sliders r,K; population curve; N0 fixed; reset; model shown.",
         must_include=["r", "K", "N0", "dN/dt"],
         continuity=["bio model labeled as model"],
         acceptance=["curve follows logistic", "K asymptote visible"],
         skill_route="skills/subject/SKILL.md", output="sim.html"),
    dict(id="S07", track="simulation", level=7, subject="economics", title="Stochastic demand trials",
         claim="Learner repeats trials to distinguish noise from shift.",
         brief="Buttons run-100/reset, mean/sd readout, histogram; seed note.",
         must_include=["run 100", "mean", "sd", "histogram"],
         continuity=["USD units"],
         acceptance=["repeatable", "stats update"],
         skill_route="skills/subject/SKILL.md", output="sim.html"),
    dict(id="S08", track="simulation", level=8, subject="physics", title="Damping + drive phase plot",
         claim="Learner maps drive to phase portrait.",
         brief="Sliders damping, drive; phase canvas + amplitude readout; reset.",
         must_include=["damping", "drive", "phase", "amplitude"],
         continuity=["same oscillator state both views"],
         acceptance=["phase responds", "no overflow"],
         skill_route="skills/subject/SKILL.md", output="sim.html"),
    dict(id="S09", track="simulation", level=9, subject="computer-science", title="Policy-rule retry sim",
         claim="Learner tests a retry threshold policy under failures.",
         brief="Threshold slider, step/run, success-rate readout; tempting-bad-policy trap explained.",
         must_include=["threshold", "success rate", "retry", "prediction"],
         continuity=["policy rule stated"],
         acceptance=["policy changes outcome", "trap documented"],
         skill_route="skills/subject/SKILL.md", output="sim.html"),
    dict(id="S10", track="simulation", level=10, subject="chemical-engineering", title="Reactor T/C control + alarms",
         claim="Learner keeps reactor in limits with T/C controls.",
         brief="Sliders coolant, feed; T/C readouts, alarm banner, limits table; reset; responsive.",
         must_include=["coolant", "feed", "alarm", "limits", "reset"],
         continuity=["degC, mol/L units"],
         acceptance=["alarm triggers out-of-limit", "readable at phone width"],
         skill_route="skills/subject/SKILL.md", output="sim.html"),
    # ---- Video track (V): manim storyboard + animated HTML preview ----
    dict(id="V01", track="video", level=1, subject="math", title="Dot along line 1 cue",
         claim="Learner watches one change: dot moves along y=2x.",
         brief="1 cue, exact narration, dot + line, clean first/ending frames.",
         must_include=["cue v01a", "dot", "y=2x", "narration"],
         continuity=["silent preview; authored duration"],
         acceptance=["storyboard valid", "preview plays", "labels in frame"],
         skill_route="skills/manim-voice-animation/SKILL.md", output="preview.mp4"),
    dict(id="V02", track="video", level=2, subject="math", title="Secant to tangent 2 cues",
         claim="Learner watches secant tend to tangent.",
         brief="2 cues, secant slope readout approaching 4 at x=2 for x^2.",
         must_include=["cue v02a", "cue v02b", "secant", "tangent"],
         continuity=["same axes both cues"],
         acceptance=["slope converges", "each cue played once conceptually"],
         skill_route="skills/manim-voice-animation/SKILL.md", output="preview.mp4"),
    dict(id="V03", track="video", level=3, subject="computer-science", title="BFS animation 3 cues",
         claim="Learner follows visit order over time.",
         brief="3 cues visiting A,B,C with narration per cue.",
         must_include=["cue v03a", "cue v03b", "cue v03c", "queue"],
         continuity=["node colors stable"],
         acceptance=["3 cues ordered", "final frame readable silent"],
         skill_route="skills/manim-voice-animation/SKILL.md", output="preview.mp4"),
    dict(id="V04", track="video", level=4, subject="math", title="Basis transform ValueTracker",
         claim="Learner sees basis vectors rotate together.",
         brief="ValueTracker-style tween of basis, determinant readout.",
         must_include=["e1", "e2", "det", "tracker"],
         continuity=["matrix symbols consistent"],
         acceptance=["vectors + det agree"],
         skill_route="skills/manim-voice-animation/SKILL.md", output="preview.mp4"),
    dict(id="V05", track="video", level=5, subject="physics", title="Pendulum numbers tied to geometry",
         claim="Learner checks displayed angle equals drawn angle.",
         brief="Swung bob with DecimalNumber angle readout driven by same state.",
         must_include=["theta", "readout", "pivot", "L"],
         continuity=["deg units both"],
         acceptance=["readout matches geometry"],
         skill_route="skills/manim-voice-animation/SKILL.md", output="preview.mp4"),
    dict(id="V06", track="video", level=6, subject="math", title="Area accumulation cleanup",
         claim="Learner sees Riemann sum refine without leftover updaters.",
         brief="Bars refine 4->8->16, error readout shrinks, no ghost objects.",
         must_include=["n=4", "n=16", "error", "integral"],
         continuity=["same function x^2"],
         acceptance=["error decreases", "ending clean"],
         skill_route="skills/manim-voice-animation/SKILL.md", output="preview.mp4"),
    dict(id="V07", track="video", level=7, subject="computer-science", title="Dijkstra 5 cues + subtitles",
         claim="Learner tracks relaxations with subtitle timing.",
         brief="5 cues, per-cue subtitle lines, distance labels update.",
         must_include=["dist", "relax", "subtitle", "5 cues"],
         continuity=["graph layout fixed"],
         acceptance=["subtitles align to cues", "distances correct"],
         skill_route="skills/manim-voice-animation/SKILL.md", output="preview.mp4"),
    dict(id="V08", track="video", level=8, subject="physics", title="Projectile cue-timed motion",
         claim="Spoken timing coordinates apex callout with motion.",
         brief="Cue-timed apex marker + velocity components; cue_player concept.",
         must_include=["apex", "vx", "vy", "cue timing"],
         continuity=["SI units"],
         acceptance=["callout at apex frame", "no cue reused conceptually"],
         skill_route="skills/manim-voice-animation/SKILL.md", output="preview.mp4"),
    dict(id="V09", track="video", level=9, subject="physics", title="Wave propagation stable camera",
         claim="Learner follows propagation without decorative camera motion.",
         brief="Traveling wave, fixed camera, wavelength callout moves with crest.",
         must_include=["lambda", "crest", "fixed camera", "direction"],
         continuity=["stable frame"],
         acceptance=["camera static", "callout tracks crest"],
         skill_route="skills/manim-voice-animation/SKILL.md", output="preview.mp4"),
    dict(id="V10", track="video", level=10, subject="math", title="Surface + gradient path camera reveals",
         claim="Learner sees gradient path descend on 3D surface where camera move reveals structure.",
         brief="Contour-projected surface, path dots, one justified camera orbit, final readable frame.",
         must_include=["contour", "path", "orbit", "minimum"],
         continuity=["same f(x,y) throughout"],
         acceptance=["orbit justified", "path descends", "ending legible"],
         skill_route="skills/manim-voice-animation/SKILL.md", output="preview.mp4"),
]


def scaffold():
    VDIR.mkdir(parents=True, exist_ok=True)
    (VDIR / "matrix.json").write_text(json.dumps(MATRIX, indent=2))
    for m in MATRIX:
        d = VDIR / m["id"]
        d.mkdir(parents=True, exist_ok=True)
        prompt = (
            f"# {m['id']} L{m['level']:02d} [{m['track']}] — {m['title']}\n\n"
            f"Subject: {m['subject']} | Skill route: `{m['skill_route']}`\n\n"
            f"Claim: {m['claim']}\n\nBrief: {m['brief']}\n\n"
            f"Must include: {', '.join(m['must_include'])}\n\n"
            f"Continuity: {', '.join(m['continuity'])}\n\n"
            f"Acceptance: {'; '.join(m['acceptance'])}\n\n"
            f"Learner prediction: predict the result before running/moving, then compare.\n"
        )
        (d / "prompt.md").write_text(prompt)
        meta = dict(m, producer="excalidraw-mcp" if m["track"]=="excalidraw" else ("pinepaper-mcp" if m["track"]=="pinepaper" else "local"),
                    fallback="" if m["track"] in ("excalidraw", "pinepaper") else "manim storyboard + silent preview; audio only on explicit request",
                    status="scaffolded")
        (d / "meta.json").write_text(json.dumps(meta, indent=2))
    print(f"Scaffolded {len(MATRIX)} prompts under {VDIR}")


def auto_score():
    import math
    results = {}
    for m in MATRIX:
        d = VDIR / m["id"]
        out = d / m["output"]
        score, notes = 1, []
        if out.exists() and out.stat().st_size > 500:
            score += 1
            notes.append("exists+nontrivial")
        else:
            notes.append("missing/tiny")
            results[m["id"]] = dict(auto_1_5=score, notes="; ".join(notes))
            continue
        if out.suffix in (".png", ".mp4"):
            side = d / ("scene.excalidraw.json" if m["track"] == "excalidraw" else "storyboard.json")
            txt = (side.read_text(errors="ignore") if side.exists() else "") + (d / "prompt.md").read_text(errors="ignore")
        else:
            txt = out.read_text(errors="ignore")
        hits = sum(1 for s in m["must_include"] if s.split()[0].lower() in txt.lower())
        if hits >= math.ceil(len(m["must_include"]) / 2):
            score += 1
            notes.append(f"labels {hits}/{len(m['must_include'])}")
        if len(txt) > 2000:
            score += 1
            notes.append(f"length {len(txt)}")
        if m["track"] in ("simulation", "pinepaper") and ("reset" in txt.lower()) or (m["track"] not in ("simulation", "pinepaper")):
            score += 1
            notes.append("controls-or-n/a ok")
        results[m["id"]] = dict(auto_1_5=min(score, 5), notes="; ".join(notes))
    (VDIR / "scores.auto.json").write_text(json.dumps(results, indent=2))
    print(f"Auto-scored {len(results)} -> scores.auto.json")


ESC = html.escape


def build_gallery():
    auto = json.loads((VDIR / "scores.auto.json").read_text()) if (VDIR / "scores.auto.json").exists() else {}
    llm = json.loads((VDIR / "scores.llm.json").read_text()) if (VDIR / "scores.llm.json").exists() else {}
    cards = []
    # The saved matrix includes added cases such as P11.
    matrix_path = VDIR / "matrix.json"
    matrix = json.loads(matrix_path.read_text()) if matrix_path.exists() else MATRIX
    for m in matrix:
        pid = m["id"]
        prompt = (VDIR / pid / "prompt.md").read_text() if (VDIR / pid / "prompt.md").exists() else ""
        out = m["output"]
        rel = f"{pid}/{out}"
        if m["track"] == "video":
            sb = f"{pid}/storyboard.json"
            media = (f'<video controls preload="metadata" style="max-width:100%;border:1px solid #445D48" src="{rel}"></video>'
                     f'<div><a href="{rel}" target="_blank">open {rel} (with audio)</a> · <a href="{sb}" target="_blank">storyboard.json</a></div>')
        elif out.endswith(".html"):
            media = f'<iframe loading="lazy" src="{rel}" sandbox="allow-scripts" style="width:100%;height:800px;border:1px solid #445D48;background:#FDE5D4"></iframe><div><a href="{rel}" target="_blank">open {rel} fullscreen</a></div>'
        else:
            media = f'<img loading="lazy" src="{rel}" alt="{pid}" style="max-width:100%;border:1px solid #445D48;background:#FDE5D4"><div><a href="{rel}" target="_blank">open {rel}</a></div>'
        a = auto.get(pid, {})
        l = llm.get(pid, {})
        cards.append(f"""
<section id="{pid}" style="border:1px solid #445D48;border-radius:3px;padding:16px;margin:24px 0;background:#FDE5D4">
<h2>{pid} · L{m['level']:02d} · {ESC(m['track'])} · {ESC(m['subject'])} — {ESC(m['title'])}</h2>
<p><b>Skill:</b> <code>{ESC(m['skill_route'])}</code> · <b>Claim:</b> {ESC(m['claim'])}</p>
<details open><summary><b>Prompt</b></summary><pre style="white-space:pre-wrap;background:#FDE5D4;padding:12px;border:1px solid #445D48">{ESC(prompt)}</pre></details>
<h3>Result</h3>{media}
<h3>Scores</h3>
<div>Auto (1-5): <b>{a.get('auto_1_5','—')}</b> <small>{ESC(str(a.get('notes','run visual_levels.py auto-score')))}</small></div>
<div style="background:#FDE5D4;border-radius:3px;height:10px;max-width:300px"><div style="background:#445D48;height:10px;border-radius:3px;width:{(a.get('auto_1_5',0)/5*100) if a else 0}%"></div></div>
<div>LLM (1-10): <b>{l.get('llm_1_10','—')}</b> <small>{ESC(str(l.get('reason','pending image review')))}</small></div>
<div style="background:#FDE5D4;border-radius:3px;height:10px;max-width:300px"><div style="background:#5E3023;height:10px;border-radius:3px;width:{(l.get('llm_1_10',0)/10*100) if l else 0}%"></div></div>
<div>Total fair/10 = (human+llm+auto*2)/3 → <b data-total="{pid}">—</b></div>
<h3>Your rating (1-10)</h3>
<label>Score <input type="number" min="1" max="10" step="1" data-human="{pid}" style="width:64px"></label>
<br><label>Feedback<br><textarea data-feedback="{pid}" rows="2" style="width:100%"></textarea></label>
</section>""")
    page = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GNOS visual-levels gallery (41)</title></head><body style="background:#FDE5D4;color:#001524;font-family:system-ui;max-width:1000px;margin:auto;padding:16px">
<h1>GNOS visual-levels — 41 prompts, scroll + rate</h1>
<p>Videos play inline, sims/Pinepaper run inline in iframes, Excalidraw shows as image. Rate each 1-10 + feedback. Scores save to browser + Export JSON.</p>
<p><button onclick="exp()">Export scores.json</button> <span id="st"></span></p>
""" + "\n".join(cards) + """
<script>
try{Object.assign(window.__s||={},JSON.parse(localStorage.getItem('gnos-vl')||'{}'))}catch(e){window.__s={}}
document.querySelectorAll('[data-human]').forEach(i=>{i.value=window.__s[i.dataset.human]?.h||'';i.oninput=save});
document.querySelectorAll('[data-feedback]').forEach(t=>{t.value=window.__s[t.dataset.feedback]?.f||'';t.oninput=save});
function save(){document.querySelectorAll('[data-human]').forEach(i=>{window.__s[i.dataset.human]=window.__s[i.dataset.human]||{};window.__s[i.dataset.human].h=i.value});
document.querySelectorAll('[data-feedback]').forEach(t=>{window.__s[t.dataset.feedback]=window.__s[t.dataset.feedback]||{};window.__s[t.dataset.feedback].f=t.value});
localStorage.setItem('gnos-vl',JSON.stringify(window.__s));document.getElementById('st').textContent='saved '+new Date().toLocaleTimeString()}
function exp(){const b=new Blob([JSON.stringify(window.__s,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='scores.human.json';a.click()}
</script></body></html>"""
    (VDIR / "index.html").write_text(page)
    print(f"Built gallery {VDIR/'index.html'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["scaffold", "auto-score", "build-gallery", "all"])
    args = ap.parse_args()
    if args.cmd in ("scaffold", "all"):
        scaffold()
    if args.cmd in ("auto-score", "all"):
        auto_score()
    if args.cmd in ("build-gallery", "all"):
        build_gallery()
