---
name: khan-academy
description: Find a Khan Academy video fast and add it only on a strong match.
---

# Khan Academy Video Finder

This skill finds one Khan Academy video for one lesson step.
Find content with two searches: Khan first (Door 1), YouTube second (Door 2).
Add the video only for an exact topic match.
You need no MCP server. You need no transcript.

## When to Use and When to Skip

Use this skill for a single topic that needs a video.
An example query is `Bayes theorem`.
Another query is `linear transformations`.
Skip when the lesson already teaches the step.
Skip when no candidate clearly teaches the exact topic.
Use length only to choose a clip, never to reject a topic match.

## Find the Video in Four Steps

### Step 1 Find Names on Khan

Run the finder script with your query.

```bash
python3 skills/khan-academy/scripts/video_finder.py /tmp/khan-report.md "Bayes theorem"
```

The script calls Khan GraphQL and returns titles with contentIds.
Pick the title that matches your exact topic.
An example pick is `Conditional probability with Bayes' Theorem`.
Save its contentId and parent path.

### Step 2 Find Videos on YouTube

The same script feeds each exact Khan title to YouTube.
It searches YouTube for Khan Academy plus the quoted title.
It keeps two or three hits per title with channel and duration.
An example hit is a Khan Academy video near five minutes.

### Step 3 Join on Title and Duration

Match the Khan title to the YouTube title.
Allow only small word differences.
Match a Khan-owned channel: the name without spaces starts with `khanacademy`.
Note the duration so you can pick a clip later; length alone never rejects a match.
The script labels each pair as a strong candidate or a weak candidate.
Stop if nothing scores strong.
Read `references/selection.md` to judge direct, prerequisite-only, or partial coverage before you add the video.

### Step 4 Add the Video or Stop

Add the video only on a strong match.
If you have not confirmed the ID, link the Khan page instead.
One known page is below.

`https://www.khanacademy.org/math/ap-statistics/probability-ap/stats-conditional-probability/v/bayes-theorem-visualized`

Confirm the YouTube ID in a browser.
Confirm playback through the local HTTP server, never through `file://`.
A `file://` page sends no origin, and YouTube returns Error 153
for every embed even when the ID is correct.
Read `references/embedding.md` before you render or inspect.
Then use a video block with that ID.
Stop and report no match if unsure.

## Use a Video Block Only on an Exact Match

The video must teach the exact topic.
A close topic is not enough.
A playlist or part two is not enough.
Link the Khan page if you cannot confirm the ID.
Do not guess an ID.
Do not embed an unconfirmed ID.

## Record the Check

Save these eight items for each pick.

- Title
- Khan page URL
- contentId
- YouTube ID
- Duration
- Confidence
- Check date
- Placer name

Store URLs and IDs in code spans.
Read `references/finder-workflow.md` for endpoints and failures.
Read `references/selection.md` for coverage judgments.
Read `references/incorporation.md` for placement and prompts.
Read `references/embedding.md` for the iframe markup and the serve-over-HTTP playback check.
