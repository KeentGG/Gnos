# Finder Workflow for Khan Academy Content

Find content with two searches: Khan first (Door 1), YouTube second (Door 2).
You need no KhanAcademy MCP server.

## 1 Door 1 Khan GraphQL Search

Send a GET request to the address below.

`https://www.khanacademy.org/api/internal/graphql/getContentSearchResults`

Add two query params. Set hash to `1013100632`.
Set variables to JSON with query and numResults.

```bash
curl 'https://www.khanacademy.org/api/internal/graphql/getContentSearchResults?hash=1013100632&variables=%7B%22query%22%3A%22bayes%20theorem%22%2C%22numResults%22%3A4%7D' -H "Accept: application/json"
```

Set the Accept header to `application/json`.
Use a normal browser User Agent.
Read results at `data.searchPage.results`.
Keep these keys for each hit.

- contentId
- kind
- learnableContent
- translatedTitle
- translatedDescription
- parentTopic

Responses never include `slug` or `relativeUrl`.
You save translatedTitle exactly as returned.
You use it later for YouTube search.
If the hash stops working you log the error.
You move to Door 2 with websearch page URLs.

## 2 Dead End ContentForPath

Hash is `45296627`. Status is stale.
Server returns No query found for this hash.
You do not use this hash for lookup.
You record it as stale in your notes.
You do not retry it in a loop.
You move on to supported methods.

## 3 Walled HTML

Lesson pages return Client Challenge.
Robots and sitemap return the same challenge page.
You do not scrape lesson HTML directly.
You do not bypass the challenge.
You use websearch for canonical page URLs instead.
You store the found URL without fetching full HTML.
You mark HTML scraping as blocked.

## 4 Door 2 YouTube With yt-dlp

You query YouTube by exact translatedTitle.
Keep only 11-character video IDs.
You search candidates with this command.

```bash
yt-dlp "ytsearch3:Khan Academy \"Conditional probability with Bayes' Theorem\"" --print "%(title)s ||| %(id)s ||| %(channel)s ||| %(duration_string)s ||| %(webpage_url)s" --flat-playlist --no-warnings --skip-download
```

You dump a Khan playlist with this command.

```bash
yt-dlp --flat-playlist --print "%(title)s ||| %(id)s" "https://www.youtube.com/playlist?list=PLSQl0a2vh4HAmK-7h0ut3elL4bCuuIfFx" --no-warnings --skip-download
```

You check metadata for one ID with this command.

```bash
yt-dlp --print "%(title)s ||| %(channel)s ||| %(duration_string)s" "https://www.youtube.com/watch?v=Zxm4Xxvzohk" --no-warnings --skip-download
```

Save the title, channel, duration, and watch URL.

## 5 Join Rule

You start each YouTube query from translatedTitle.
You add Khan Academy to the query text.
Only hits where `kind` is `Video` go to Door 2.
An Article, Exercise, or Topic hit needs a source block, not a player.
You check title overlap. You check Khan-owned channel.
Khan-owned means the spaceless lowercase name starts with `khanacademy`.
This covers the main channel plus medicine, India, Xhosa, and dubs.
Note the duration for clip picking. Duration points only add; length never rejects a match.
The script scores overlap up to 60 and channel at 30.
It adds duration plausibility up to 10.
A strong match also requires query fit: more than half the query words
must appear in the Khan title. Below that fit, a pair is at most
a weak candidate, no matter its score.
It labels 70 and above as a strong candidate, and below 70 as a weak candidate.
You never claim verified provenance (proof the upload is Khan's own).
State candidate status in output.

## 6 Failure Table

| Method | Status | Next Action |
| --- | --- | --- |
| GraphQL search | works | You save hits for Door 2 |
| ContentForPath | blocked | You record stale hash and stop |
| HTML scrape | blocked | You use websearch for URL only |
| yt-dlp search | partial | You filter to 11 char IDs |
| yt-dlp playlist | partial | You keep flat list for review |
| Join scoring | partial | You label strong candidate or weak candidate |
