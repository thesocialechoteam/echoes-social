# Weekly playbook

Weeks run Wednesday → Tuesday. The weekly run (Mondays) prepares the next Wednesday–Tuesday.

1. Read `log.md` and the previous `weekN_posts.json` so themes don't repeat.
2. Re-check https://thesocialecho.app for features/news. Only state facts the site states. No $ECHO token / presale promotion.
3. Pull last week's results from Metricool (brand 7851174, timezone Europe/Bucharest); note what worked in `log.md`.
4. Write `weekN_posts.json` (same structure as week1: 7 posts, 3–4 on-screen text screens + end card, caption, hashtags per network, cta).
5. `python3 render.py weekN_posts.json videos` → look at a few frames before pushing.
6. Commit + push videos. Media URL: `https://raw.githubusercontent.com/thesocialechoteam/echoes-social/main/videos/<file>.mp4`
7. Schedule one Metricool post per network per day (21 total), checking getScheduledPosts first to avoid duplicates:
   - Instagram: `instagramData.type = "REEL"`, 10:00
   - Facebook: `facebookData.type = "REEL"`, 12:00
   - TikTok: 18:00, **`tiktokData.title` is required** — set it to the full caption text
   - `videoCoverMilliseconds: 1500`, `autoPublish: true`
   - text = caption + "\n\n" + cta[network] + "\n\n" + hashtags[network]
   - Download link: https://thesocialecho.app/#get (Facebook clickable; Instagram/TikTok "link in bio")
8. Append the schedule table (with Metricool post ids) to `log.md`, commit, push.
