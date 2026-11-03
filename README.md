# echoes-social

Social media content for **echoes — leave your mark** (Instagram, TikTok, Facebook @theechoes.app), scheduled through Metricool.

- `render.py` — renders the 9:16 brand videos (neon-cyan orb, topographic lines, echo rings, original ambient sound). `python3 render.py weekN_posts.json videos`
- `weekN_posts.json` — each week's posts: on-screen text, captions, hashtags per network.
- `videos/` — rendered MP4s. Metricool pulls them from their public raw GitHub URLs.
- `log.md` — what was scheduled, when, and how it performed.

Rules for the content: English, global audience, about the app only (no token / presale promotion), facts only from thesocialecho.app.
