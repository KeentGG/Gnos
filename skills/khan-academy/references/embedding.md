# Embed and inspect a Khan lesson block

Use the existing [course source contract](../../course-design/references/course-contract.md)
and [lesson contract](../../lesson-design/references/lesson-contract.md).
Khan video is external source media, not a downloaded/generated video artifact.
Do not register a thumbnail as the video or paste the finder report as HTML.

## Author the source and block

Put the checked item in `course.json.sources` with `type: "khan-video"`, its
exact canonical Khan `/v/` URL, verified 11-character `youtube_id`, title,
`checked_on`, `sections`, and `verification_notes`. Notes should distinguish
what was confirmed through GraphQL finder report, yt-dlp match, browser playback,
and transcript, and state
any coverage limit. Add its ID to the topic's `resource_ids`; add
`skills/khan-academy/SKILL.md` to the topic and lesson `skill_routes`.
Validate the revised course and refresh the lesson's design receipt through
the normal lesson-design workflow.

The `khan-video` block needs `source_id`, lesson concepts, a concrete purpose,
`text` with a watch prompt, and a production brief using this skill route.
Use optional `clip_start_seconds` and `clip_end_seconds` together: integers,
`0 <= start < end`, within the verified video duration. Omit both when the
whole video is the right unit. Bounds belong to the block, so one checked
source can serve distinct sections. If a legacy topic has a representation
plan, use its `khan` entry and `representation_id`; new lessons need no plan.

A structure example, using the item inspected on 2026-09-27:

```json
{
  "id": "constant-ratio", "type": "khan-video",
  "concepts": ["math.derivative"],
  "purpose": "Review constant rise/run before contrasting a curved graph.",
  "text": "The magenta line rises two units for one unit right. Predict its rise for three units right; watch whether the ratio changes.",
  "source_id": "khan-intro-slope",
  "clip_start_seconds": 78, "clip_end_seconds": 195,
  "production": {
    "skill_route": "skills/khan-academy/SKILL.md",
    "brief": "Use the inspected constant-slope demonstration as a prerequisite bridge.",
    "must_include": ["The comparison of 2/1 and 6/3"],
    "continuity": ["Vertical is y; horizontal is x. Introduce the magenta line before viewing."],
    "acceptance_checks": ["The interval contains both step sizes and the conclusion; the next block returns to the GNOS example."],
    "depends_on_block_ids": ["slope-prediction"]
  }
}
```

This fragment requires its real source, preceding block, declared concepts,
and following application; it is not a complete publishable lesson. Recheck
before reuse. The inspected page's ID was `MeU-KzdCBps`, with duration 415
seconds. Its timestamped transcript starts the magenta-line example at 1:18,
compares the two ratios around 2:38, and names the slope at 3:10–3:13 before
changing context at 3:15. The interval teaches constant slope, not the limit
definition of a derivative. The example's boundaries come from that content,
not the unrelated synthetic IDs/times used in renderer unit tests.

## What actually embeds

The finder never emits an iframe. It returns titles with contentIds plus
YouTube IDs with durations. Confirm the ID in a browser. The GNOS renderer creates a responsive 16:9 YouTube privacy-enhanced
iframe at `https://www.youtube-nocookie.com/embed/<youtube_id>`, with `start`
and `end` query parameters for a segment. The card shows its time range, title,
watch prompt, and direct Khan link. It requires network access and supported
playback; a rendered iframe or thumbnail alone does not establish playback.

The iframe uses `referrerpolicy="strict-origin-when-cross-origin"` to send only
the site's origin to YouTube, not the learner or lesson path. This overrides
the course server's default `no-referrer` for this embed only. YouTube requires
client identification; suppressing it can cause Error 153. See
[YouTube's client-identification requirement](https://developers.google.com/youtube/terms/required-minimum-functionality).
Some embedded browsers may still block or suppress external player requests;
check actual playback instead of treating this attribute as proof of success.

Never open a page with embeds through `file://`. A `file://` page sends a
null origin, so YouTube answers every player with a black frame reading
`Video player configuration error` and `Error 153`, even when every video ID
is correct. Always serve first, then open the `http://127.0.0.1` address:

```bash
.venv/bin/python skills/course-viewer/scripts/serve_course.py learners/<learner>/courses/<course-id> --port 8080
# visit http://127.0.0.1:8080/portal/
```

When every embed on a page shows Error 153 at once, suspect serving, not
the IDs. When one embed fails while its neighbors play, suspect that ID:
a public embeddable video answers HTTP 200 at
`https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=<youtube_id>&format=json`,
while a private, deleted, or embedding-disabled video does not.

Both bounds are seconds measured from the beginning of the whole video.
YouTube's `end` is not a duration relative to `start`; seeking may begin near
a keyframe. Treat the interval as a viewing aid, not an exact edit or access
restriction. Users can operate the player themselves. See the official
[YouTube player parameter reference](https://developers.google.com/youtube/player_parameters)
and [embedding guidance](https://support.google.com/youtube/answer/171780).

Articles and exercises use an exact Khan link in a `source` block, with a
purpose and return task. They are not iframed into the video player. In chat,
give the descriptive Khan link, the time range, and what to notice; do not
promise an inline player if the host only shows a link or thumbnail.

## Render and inspect

Run `review_video_blocks.py --course … --lesson …` from this skill's scripts
for structural validation and placement review. Then validate/publish the
lesson and render it through the normal course-viewer workflow:

```bash
python3 skills/course-viewer/scripts/render_viewer.py path/to/course-workspace
```

Serve the portal over localhost with the course viewer's server, then inspect:

1. The title, exact source link, prompt, interval, and surrounding explanation
   belong to the chosen item and section. The fallback source link is visible.
2. At desktop and narrow/mobile widths, the 16:9 player, text, and link fit
   without clipping or horizontal overflow. Capture screenshots of both.
3. Click play. Inspect the start, a frame containing the target relation, and
   the end behavior. Check captions/readability if needed for this learner.
   Do not equate loading the player with successful playback.
4. Follow the Khan link and verify it opens the intended page. Complete the
   GNOS follow-up interaction when the demonstration includes one.
5. Report rendering and playback separately. A blocked embed, consent gate,
    network failure, or unavailable captions calls for a usable alternative
    and the source link, not an invented success claim.

Use temporary/synthetic course workspaces for harness tests. Do not fabricate
real learner evidence to make a sample lesson or screenshot.
