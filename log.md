# Posting log

## Week 1 (2026-11-04 → 2026-11-10)
Schedule (Europe/Bucharest): Instagram Reel 10:00 · Facebook Reel 12:00 · TikTok 18:00 — from Metricool best-time data.

All 21 posts scheduled on 2026-11-03 (Metricool brand 7851174), status PENDING:

| Date | Post (hook) | Instagram Reel 10:00 | Facebook Reel 12:00 | TikTok 18:00 |
|---|---|---|---|---|
| Wed 11-04 | w1-01 "What if your voice could stay somewhere?" | 415947713 | 415947727 | 415947776 |
| Thu 11-05 | w1-02 "Why does everything you post scroll away forever?" | 415947801 | 415947824 | 415947880 |
| Fri 11-06 | w1-03 "What did someone leave on the corner you just passed?" | 415947971 | 415948003 | 415948039 |
| Sat 11-07 | w1-04 "Where would you leave your voice this weekend?" | 415948072 | 415948112 | 415948160 |
| Sun 11-08 | w1-05 "What if a video only played where you filmed it?" | 415948242 | 415948271 | 415948328 |
| Mon 11-09 | w1-06 "Who should hear your voice?" | 415948362 | 415948379 | 415948416 |
| Tue 11-10 | w1-07 "What would you say if you could leave it anywhere?" | 415948475 | 415948498 | 415948542 |

Captions updated the same evening to use the download link https://thesocialecho.app/#get (smart link: App Store or Google Play by device). Instagram captions trimmed to 5 hashtags (Instagram's cap). Then all videos re-rendered (_v2) to open with a question hook visible from frame 0, and caption first lines changed to the same question. Then George rejected the cyan animation style: all videos re-made (_v3) with render2.py from his real app footage + promo assets in the app's own look (navy/amber/cream), ending on his brand end card. On 2026-11-04 the Instagram + TikTok posts of w1-01/02/03/04/07 got the AI label (they use AI-generated footage; w1-05/06 are real app footage only). Library extended with George's AI clips (OpenArt/Veo), see assets/library.json. Then (2026-11-04, 02:15) all 7 re-made as _v4 mixing George's new AI clips with real app footage, alternating end_card / end_card_b; all 7 now carry the AI label on Instagram + TikTok. Ids above are the latest ids.

Performance (Metricool, pulled 2026-11-09 ~11:30; w1-06/07 not yet published or not yet synced):

| Post | Hook mode (retro-tagged) | Caption style (retro) | IG views / reach / avg watch / 3s-view rate | FB views | TikTok views |
|---|---|---|---|---|---|
| w1-01 "What if your voice could stay somewhere?" | counterintuitive ("what if") | simplicity | 19 / 13 / 3.7s / 28.6% | 17 | **1719** |
| w1-02 "Why does everything you post scroll away forever?" | tension | POV | 18 / 14 / 2.8s / 35.7% | 20 | 749 (1 like) |
| w1-03 "What did someone leave on the corner you just passed?" | open loop | specificity | 42 / 38 / 3.4s / 34.2% | 50 | 738 |
| w1-04 "Where would you leave your voice this weekend?" | generic prompt | simplicity | 10 / 8 / 2.3s / 0% | 21 | 690 |
| w1-05 "What if a video only played where you filmed it?" | counterintuitive | specificity | **124 / 102 / 4.0s / 35.9%** | 49 | not synced yet |

Totals: ~5.9k views, 1 like, 0 comments, 0 saves, 0 shares across all networks. Instagram followers flat at 12 (2 gained on 11-08).

### Growth audit (Method A) — week 1
Best: concrete, visual-mechanic hooks (w1-05 Reflections, w1-03 "the corner you just passed") on IG/FB; TikTok gave the first post a launch push, then flattened at ~700. Worst: the open "where would you…" prompt (w1-04: 0% of IG views passed 3s). Average watch is 2.3–4.0s of ~13s videos: people leave right after the hook.

1. **Feature brochure, no reason to follow.** Every post explains one feature and ends on "download" — nothing tells a viewer there's more coming. Fix: a named recurring series, *If this place could talk* (one place every Friday, numbered episodes, "follow for the next place").
2. **Hypothetical hooks + an explanation right after.** "What if…/Where would you…" asks the viewer to imagine; screen 2 then switches to a feature definition, which is where they swipe (3–4s). Fix: concrete scenes/feelings or counterintuitive claims, no "what if"; screen 2 must escalate the question (raise "then where/how?"), the explanation only on the last text screen.
3. **Nothing to do in the comments, nothing worth saving.** The only ask was "tell us where you left yours", which requires having the app → 0 comments. Fix: every caption ends with a one-tap, no-app-needed prompt (pick a language, name a city, tag a friend, one word) and two posts are built as interactive games (spot your language, pick the city).



## Week 2 (2026-11-11 → 2026-11-17)
Applied the audit: series launch (w2-03), no "what if" hooks, escalation screen before the reveal, no-app comment prompt on every caption. 12 hook drafts per post (4 modes × 3), 3 caption versions and retention notes are stored per post in week2_posts.json. All posts mix AI + real app footage → AI label on IG + TikTok. Scheduled 2026-11-09 (Metricool brand 7851174), status PENDING:

| Date | Post (hook) | Hook mode | Caption style | Instagram Reel 10:00 | Facebook Reel 12:00 | TikTok 18:00 |
|---|---|---|---|---|---|---|
| Wed 11-11 | w2-01 "Why won't this video play at home?" | counterintuitive | specificity | 421556931 | 421556953 | 421556985 |
| Thu 11-12 | w2-02 "Ever read “nice” and felt nothing?" | feeling | simplicity | 421557516 | 421557541 | 421557575 |
| Fri 11-13 | w2-03 "If this bench could talk, what would it say?" (series #1) | open loop | POV | 421557622 | 421557653 | 421557688 |
| Sat 11-14 | w2-04 "Can you spot your language in 3 seconds?" | open loop | specificity | 421558284 | 421558320 | 421558354 |
| Sun 11-15 | w2-05 "Ever waited all day for one birthday message?" | feeling | simplicity | 421558395 | 421558443 | 421558483 |
| Mon 11-16 | w2-06 "Would you follow a trail of voices across your city?" | tension | POV | 421558889 | 421558900 | 421558913 |
| Tue 11-17 | w2-07 "Is the room you're in really empty?" | counterintuitive | specificity | 421558945 | 421558980 | 421558999 |

Mode mix: counterintuitive 2, feeling 2, open loop 2, tension 1. Styles: specificity 3, simplicity 2, POV 2. Compare next Monday.
Footage note: the library is now repeating (ar_reflection, ar_voicecard, map_2d/3d, ai_beanie_raise used in both weeks); asked George for new screen recordings.

Performance (Metricool, pulled 2026-11-16 11:30): **none of week 2 was published.** All 16 posts from 11-11 10:00 to 11-16 10:00 are status ERROR in Metricool: "You have reached your Metricool account limit." (also likely w1-07 on TikTok, 11-10 18:00, which never appeared in analytics). The 5 still-pending posts (11-16 FB/TikTok, 11-17 ×3) will hit the same limit. George notified 2026-11-16 11:30 to raise the Metricool plan limit. Week 2 has no data → hook modes / caption styles can't be compared yet.


## Week 3 (2026-11-18 → 2026-11-24)

### Results feeding this week (final week-1 numbers, pulled 2026-11-16)
| Post | IG views / reach / avg watch / 3s-view rate | FB views | TikTok views |
|---|---|---|---|
| w1-05 "What if a video only played where you filmed it?" | 125 / 104 / 4.0s / 35.6% | 52 | 772 |
| w1-06 "Who should hear your voice?" | 16 / 10 / 3.9s / 36.4% (1 like) | 22 | 761 (2 likes) |
| w1-07 "What would you say if you could leave it anywhere?" | 13 / 10 / 2.2s / 10.0% | 30 | not published |
Instagram followers: 12, flat all week (0 gained / 0 lost). 0 comments, 0 saves, 0 shares on all 14 published posts.

### Growth audit (Method A) — week 3
1. **The account went silent for 6 days right after the launch push.** Week 2 never published (Metricool account limit), so the algorithm saw 0 posts after w1's ~700/post TikTok baseline. Fix: George raises the Metricool limit; this agent stops re-rendering/updating already-scheduled posts (each update creates a new post id and may count toward the limit) and schedules each week exactly once.
2. **Open "you" prompts lose 90% of viewers in 3 seconds.** w1-04 ("Where would you leave your voice…") and w1-07 ("What would you say if…") got 0% / 10% 3s-view rate on IG, while hooks that name a concrete thing (w1-05 a video that only plays at its spot, w1-03 the corner you passed) held 33–36%. Fix: every week-3 hook names a concrete object, place or person (one person, a river, your city, a café, a stranger) and frame 0 shows it.
3. **Feature lessons, no story, so nothing to follow.** TikTok sits at ~700–770 views on every post whatever the hook (the default test pool), 0 follows, 0 comments: the videos teach a feature and end. Fix: screens are story beats (proposals, goodbyes, late-night calls; their laugh, the way they said your name), the feature appears only as the payoff on the last screen, the series *If this place could talk* restarts on Friday (the bench episode never aired, so the river is Episode 1), and every caption ends with a no-app, few-word comment prompt.

Facts re-checked on thesocialecho.app 2026-11-16 (places can be attached to echoes/Reflections; echoes for everyone/friends/specific people/only you; free to leave/listen/comment/message; 3 free Reflections per 30 days, extra credits in-app; "Now: growing the first cities"; trails/hunts and a portal for local places planned, no dates). New angles only: one specific person, cost, river (series), first voice in your city, a loved one's voice, a stranger, places/cafés.

12 hook drafts per post, 3 caption versions and retention notes are in week3_posts.json. All use AI + real footage → AI label on IG + TikTok. Videos pushed to videos/ (commit cd1c6d2).

**NOT SCHEDULED** — Metricool account limit reached (see week 2). Ready to schedule as soon as the limit is raised (IG Reel 10:00 · FB Reel 12:00 · TikTok 18:00, Europe/Bucharest):

| Date | Post (hook) | Hook mode | Caption style | Video | Instagram | Facebook | TikTok |
|---|---|---|---|---|---|---|---|
| Wed 11-18 | w3-01 "Ever posted something just for one person?" | feeling | simplicity | w3-01_oneperson_v1.mp4 | – | – | – |
| Thu 11-19 | w3-02 "What does it cost to leave your voice here?" | counterintuitive | specificity | w3-02_free_v1.mp4 | – | – | – |
| Fri 11-20 | w3-03 "If this river could talk, who would it miss?" (series ep. 1) | open loop | POV | w3-03_river_v1.mp4 | – | – | – |
| Sat 11-21 | w3-04 "Is your city still silent?" | tension | simplicity | w3-04_firstvoice_v1.mp4 | – | – | – |
| Sun 11-22 | w3-05 "Whose voice do you wish you'd saved?" | feeling | specificity | w3-05_voices_v1.mp4 | – | – | – |
| Mon 11-23 | w3-06 "Would you leave a voice note for a stranger?" | tension | POV | w3-06_stranger_v1.mp4 | – | – | – |
| Tue 11-24 | w3-07 "What's been said about your favourite café?" | open loop | specificity | w3-07_cafe_v1.mp4 | – | – | – |

Mode mix: feeling 2, open loop 2, tension 2, counterintuitive 1. Styles: specificity 3, simplicity 2, POV 2.
Footage note: still no new recordings; the 21 library assets are now in their third week (map_2d/3d, ar_voicecard, ar_portals, ar_reflection in nearly every video). Asked George again for new screen recordings.
