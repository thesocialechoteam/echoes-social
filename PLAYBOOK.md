# Weekly playbook

Weeks run Wednesday → Tuesday. The weekly run (Mondays) prepares the next Wednesday–Tuesday.

1. Read `log.md` and the previous `weekN_posts.json` so themes don't repeat.
2. Re-check https://thesocialecho.app for features/news. Only state facts the site states. No $ECHO token / presale promotion.
3. Pull last week's results from Metricool (brand 7851174, timezone Europe/Bucharest), then run **Method A (growth audit)** below and write it into `log.md`.
4. Hook rule: every video opens with a QUESTION. The first screen is that question (2–3 short lines, ≤ ~22 characters each), shown large from frame 0 with no fade, so nobody scrolls past. The caption's first line is the same question.
5. Write `weekN_posts.json` (same structure as week1: 7 posts, hook + 2–3 screens, a "shots" list per screen, caption, hashtags per network, cta) using **Methods B, C, D, E** below.
6. Real app look: check assets/library.json → app_reference. AI clips must not contradict the real UI; prefer mixing AI footage with at least one real app shot per video. Choose the end card per post with "end": "end_card" or "end_card_b".
   `python3 render2.py weekN_posts.json videos` (real-footage style; see assets/library.json and week1_posts.json. render.py is the old cyan animation style, don't use it) → look at a few frames before pushing.
7. Commit + push videos. Media URL: `https://raw.githubusercontent.com/thesocialechoteam/echoes-social/main/videos/<file>.mp4`
8. Schedule one Metricool post per network per day (21 total), checking getScheduledPosts first to avoid duplicates:
   - Instagram: `instagramData.type = "REEL"`, 10:00
   - Facebook: `facebookData.type = "REEL"`, 12:00
   - TikTok: 18:00, **`tiktokData.title` is required** — set it to the full caption text
   - `videoCoverMilliseconds: 1500`, `autoPublish: true`
   - text = caption + "\n\n" + cta[network] + "\n\n" + hashtags[network]
   - Hashtags: Instagram max 5 (Instagram cap since Dec 2025, caption + first comment combined), TikTok 3–5, Facebook 1–2. Specific beats generic.
   - AI label: if the post's shots use any asset with "ai": true in assets/library.json (render2.py prints ai_label=True), set instagramData.isAiGenerated=true and tiktokData.isAigc=true. Facebook has no field for it.
   - Download link: https://thesocialecho.app/#get (Facebook clickable; Instagram/TikTok "link in bio")
9. Append the schedule table (with Metricool post ids) to `log.md`, commit, push.

## Content method (George's 5 prompts — apply every week)

**A. Growth audit** — act as an Instagram growth analyst who studies why accounts in the same niche grow at very different rates. Using last week's numbers per post and network, name the **three patterns making the account invisible**: not just saturated formats, but the specific ways the content fails to give a reason to *follow* rather than just like. Write them in `log.md` with one concrete fix each, and apply the fixes this week.

**B. Scroll-stopping hooks** — the first line is the only line that matters. For each of the 7 posts, draft **12 opening lines across four modes** (3 each): (1) immediate tension, (2) a counterintuitive claim, (3) naming a specific person's exact feeling, (4) an open loop the viewer can't close without watching to the end. Keep George's rule — the final hook is phrased as a question — and pick the strongest. Note the winning mode per post in `log.md` so results can be compared by mode.

**C. Faceless formats** — think like a faceless producer who grew accounts past 100K without showing a face or relying on trending audio. Each post is a text-led reel with scene-by-scene direction (screens + shots). When carousels are added to the mix, the same idea becomes a 7-slide carousel with exact on-screen text per slide.

**D. Retention edit** — before rendering, go through every reel line by line like a retention editor with a stopwatch. Flag each moment a viewer would swipe away and why, then rewrite so every line creates enough tension to pull the next. No filler screens; the payoff comes on the last text screen, right before the end card.

**E. Positioning** — make echoes look like the obvious authority in place-based voice without vanity metrics or guru signals. For each caption write three versions — (1) authority through specificity and precision, (2) confident simplicity, (3) a point of view strong enough that disagreeing feels like a choice — and pick the best. Rotate styles across the week and track which style performs in `log.md`.

Brand voice for all of it: calm, intimate, curious; places and voices, not tech jargon. English, global audience.
