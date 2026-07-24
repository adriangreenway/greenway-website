# Adrian Michael EPK (Boston outreach)

Personal EPK for Adrian's Boston work: solo singer-guitarist and lead/harmony
vocalist lanes. Independent track, same pattern as `docs/song-list/`: source of
truth lives here, the built page deploys to the proposals site. Handoff spec:
`BOSTON_75_ADRIAN_EPK_CLAUDE_HANDOFF_V1.md` (Adrian's Desktop EPK folder).
Nothing here touches the Astro site, its nav, or any `src/` file.

## Pages

- `dist/adrian/index.html` — lane chooser (general)
- `dist/adrian/solo/index.html` — solo singer-guitarist
- `dist/adrian/vocalist/index.html` — lead/harmony vocalist
- `dist/adrian/assets/` — responsive images (`img/`) + email cards (`email/`)

Live target: `proposals.greenwayband.com/adrian` (+`/solo`, `/vocalist`).
Pages carry `noindex` until Adrian approves indexing.

## Build

- `python3 build.py` regenerates `dist/adrian/` from `content.json` +
  `../song-list/songs.json`. Every song title on the page comes from the
  songs.json authority; nothing is hand-typed, so nothing can be invented.
- `python3 build.py --mode preview --out <dir>` writes the same pages with
  assets copied alongside. Preview root is session-scratch with a
  `adrian/media` symlink to `~/Desktop/EPK/renders/web/`; serve with the
  `adrian-epk` entry in `.claude/launch.json` (port 8894). That entry runs
  `range_server.py`, NOT `python3 -m http.server` — the stock module ignores
  HTTP Range, which makes every preview video unseekable and looks like a
  broken player. Netlify handles Range correctly in production.
- `tools/` holds the media scripts, all reading from `~/Desktop/EPK` and
  writing outside this repo. Rerun only when source media changes:
  - `tools/assets_build.py` — hero/poster derivatives into `dist/adrian/assets/img/`
  - `tools/cards_build.py` — the two email cards
  - `tools/reel_build.py` — renders the reel to `~/Desktop/EPK/renders/`
    (SEGS at the top is the edit decision list) and the web encodes
  - `tools/range_server.py` — the preview server, see below
  Rendered video is never committed; this repo is public.

## Video hosting (self-hosted, Adrian's call 2026-07-24; NO Vimeo)

Same pattern as the proposal template's `../assets/uptown-funk-2026a.mp4`:
poster facade, click swaps in a native `<video controls autoplay playsinline>`
pointing at `/adrian/media/*.mp4` on the proposals site. Nothing loads until
click. Web encodes live OUTSIDE this public repo in `~/Desktop/EPK/renders/web/`
(x264 CRF23, faststart): `adrian-reel.mp4` 31MB, `neon-moon.mp4` 12MB,
`big-spring-wedding.mp4` 70MB, `testimonial-nov-2022.mp4` 2MB. (Precedent for
size: the proposal template already ships a 73MB mp4.) The 9pc promo is
excluded everywhere per Adrian (it showcases another vocalist).

## Deploy (Phase 2/3, only on Adrian's go)

**`dist/` is NOT in git** — the repo-wide `.gitignore` rule for build output
covers it. Everything in it is reproducible from the committed sources, so
regenerate before deploying:

```
python3 tools/assets_build.py     # heroes + posters  (needs ~/Desktop/EPK)
python3 tools/cards_build.py      # email cards + reel end card
python3 build.py                  # the three pages
```

Then:

1. `cp -R dist/adrian ~/Desktop/greenway-proposals/` then
   `mkdir -p ~/Desktop/greenway-proposals/adrian/media && cp ~/Desktop/EPK/renders/web/*.mp4 ~/Desktop/greenway-proposals/adrian/media/`
2. Check `git -C ~/Desktop/greenway-proposals status` first; a prod deploy
   publishes EVERYTHING staged in that folder (song-list, proposal edits from
   other sessions). Sequence deploys deliberately.
3. From a neutral cwd: `netlify deploy --dir ~/Desktop/greenway-proposals --site c6041c94-c26c-4ab8-ae5f-96c43addb081`
   (draft URL = preview; add `--prod` only on Adrian's explicit go).
4. Rollback: re-publish the previous deploy in the Netlify UI; note the
   pre-EPK DEPLOY_ID before going prod.

## Email cards

`dist/adrian/assets/email/card-solo.jpg` and `card-vocalist.jpg` (1200x675).
Once deployed, the outreach snippet is: linked image (the card) pointing at the
lane URL, with a visible text link under it for image-blocked recipients:

    [card image] -> https://proposals.greenwayband.com/adrian/solo/
    Watch Adrian solo: https://proposals.greenwayband.com/adrian/solo/

Alt text: "Adrian Michael, solo vocals and acoustic guitar, Boston" /
"Adrian Michael, 60-second live reel, Boston".

## Open items before production

- Adrian's ear and eye on reel v4 (2:21, every window from his own timestamp
  pass at full length; crossfades chosen by waveform stats, not by listening).
- Testimonial exact quote if he ever wants it as on-page text (video plays
  as-is today; nothing paraphrased, nothing fabricated).
- Commit this folder, then Phase 2 draft deploy on his go.
