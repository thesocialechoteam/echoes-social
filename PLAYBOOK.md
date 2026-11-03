# Weekly playbook

Weeks run Wednesday → Tuesday. The weekly run (Mondays) prepares the next Wednesday–Tuesday.

1. Read `log.md` and the previous `weekN_posts.json` so themes don't repeat.
2. Re-check https://thesocialecho.app for features/news. Only state facts the site states. No $ECHO token / presale promotion.
3. Pull last week's results from Metricool (brand 7851174, timezone Europe/Bucharest); note what worked in `log.md`.
4. Hook rule: every video opens with a QUESTION. The first screen is that question (2–3 short lines, ≤ ~22 characters each); render.py shows it large from frame 0 with no fade, so nobody scrolls past a black frame. The caption's first line is the same question.
5. Write `weekN_posts.json` (same structure as week1: 7 posts, 3–4 on-screen text screens + end card, caption, hashtags per network, cta).
6. `python3 render.py weekN_posts.json videos` → look at a few frames before pushing.
7. Commit + push videos. Media URL: `https://raw.githubusercontent.com/thesocialechoteam/echoes-social/main/videos/<file>.mp4`
8. Schedule one Metricool post per network per day (21 total), checking getScheduledPosts first to avoid duplicates:
   - Instagram: `instagramData.type = "REEL"`, 10:00
   - Facebook: `facebookData.type = "REEL"`, 12:00
   - TikTok: 18:00, **`tiktokData.title` is required** — set it to the full caption text
   - `videoCoverMilliseconds: 1500`, `autoPublish: true`
   - text = caption + "\n\n" + cta[network] + "\n\n" + hashtags[network]
   - Hashtags: Instagram max 5 (Instagram cap since Dec 2025, caption + first comment combined), TikTok 3–5, Facebook 1–2. Specific beats generic.
   - Download link: https://thesocialecho.app/#get (Facebook clickable; Instagram/TikTok "link in bio")
9. Append the schedule table (with Metricool post ids) to `log.md`, commit, push.
