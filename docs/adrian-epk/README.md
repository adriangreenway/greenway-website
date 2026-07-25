# Adrian Michael EPK (Boston outreach)

Personal EPK for Adrian's Boston work: one unified vocalist/live-performer
page (solo, duo, trio, private-event, hospitality, and full-band work are all
booking options on the same page, not separate lanes). Independent track,
same pattern as `docs/song-list/`: source of truth lives here, the built page
deploys to the proposals site. Nothing here touches the Astro site, its nav,
or any `src/` file.

**2026-07-24 correction (v1):** the original three-page solo-vs-vocalist
architecture (handoff spec `BOSTON_75_ADRIAN_EPK_CLAUDE_HANDOFF_V1.md`) was
superseded by `CORRECTION_BRIEF_V1.md`, a ChatGPT audit Adrian brought back.
Read-only findings are in `PHASE_0_REPORT_V1.md`; this README reflects the
corrected, single-page build.

## Page

- `dist/adrian/index.html` — the one canonical page
- `dist/adrian/assets/` — responsive images (`img/`) + the universal email card (`email/`)

Live target: `proposals.greenwayband.com/adrian`. Carries `noindex` until
Adrian approves indexing. The retired `/solo` and `/vocalist` child routes
redirect here at the Netlify level (see Deploy).

## Build

- `python3 build.py` regenerates `dist/adrian/index.html` from `content.json`
  alone. No external data dependency (the song-list link and repertoire grid
  were removed in the v1 correction, so `../song-list/songs.json` is no
  longer read).
- `python3 build.py --mode preview --out <dir>` writes the same page with
  assets copied alongside. Preview root is session-scratch with a
  `adrian/media` symlink to `~/Desktop/EPK/renders/web/`; serve with the
  `adrian-epk` entry in `.claude/launch.json` (port 8894). That entry runs
  `range_server.py`, NOT `python3 -m http.server` — the stock module ignores
  HTTP Range, which makes every preview video unseekable and looks like a
  broken player. Netlify handles Range correctly in production.
- `tools/` holds the media scripts, all reading from `~/Desktop/EPK` and
  writing outside this repo. Rerun only when source media changes:
  - `tools/assets_build.py` — hero/poster derivatives into `dist/adrian/assets/img/`
    (still generates the solo-lane and unused-video posters too; kept on hand
    rather than deleted, cheap to keep, not referenced by the current page)
  - `tools/cards_build.py` — the one universal email card
  - `tools/reel_build.py` — renders the reel to `~/Desktop/EPK/renders/`
    (SEGS at the top is the edit decision list) and the web encodes
  - `tools/range_server.py` — the preview server, see below
  Rendered video is never committed; this repo is public.

## Video hosting (self-hosted, Adrian's call 2026-07-24; NO Vimeo)

Confirmed again in the v1 correction (the brief assumed Vimeo; Adrian's prior
no-Vimeo call stands). Same pattern as the proposal template's
`../assets/uptown-funk-2026a.mp4`: poster facade, click swaps in a native
`<video controls autoplay playsinline>` pointing at `/adrian/media/*.mp4` on
the proposals site. Nothing loads until click. The facade JS now also carries
a loading state, a playback-error state with a retry action, and a direct
fallback link to the mp4 (Required Technical Correction #6).

**Only the reel (`adrian-reel.mp4`) is embedded on the page today.** Neon
Moon, the Big Spring Ranch film, and the testimonial are cut from the first
release per the brief, but their web encodes are preserved (not deleted) in
`~/Desktop/EPK/renders/web/`: `neon-moon.mp4` 12MB, `big-spring-wedding.mp4`
70MB, `testimonial-nov-2022.mp4` 2MB, `adrian-reel.mp4` 31MB. The 9pc promo
stays excluded everywhere per Adrian (it showcases another vocalist).

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
3. `~/Desktop/greenway-proposals/netlify.toml` carries two redirect rules
   sending the retired `/adrian/solo/*` and `/adrian/vocalist/*` paths to
   `/adrian/` (301). Added 2026-07-24; takes effect the first time this EPK is
   ever deployed, draft or prod.
4. From a neutral cwd: `netlify deploy --dir ~/Desktop/greenway-proposals --site c6041c94-c26c-4ab8-ae5f-96c43addb081`
   (draft URL = preview; add `--prod` only on Adrian's explicit go).
5. Rollback: re-publish the previous deploy in the Netlify UI; note the
   pre-EPK DEPLOY_ID before going prod.

## Email card

One universal card, `dist/adrian/assets/email/card-universal.jpg` (1200x675),
vocalist hero image, replacing the prior card-solo/card-vocalist pair. Copy is
fixed: `ADRIAN MICHAEL` / `BOSTON VOCALIST & LIVE PERFORMER` /
`WATCH THE LIVE REEL`. Once deployed, the outreach snippet is a linked image
pointing at the page, with a visible text link under it for image-blocked
recipients:

    [card image] -> https://proposals.greenwayband.com/adrian/
    Watch the live reel: https://proposals.greenwayband.com/adrian/

Alt text: "Adrian Michael, Boston vocalist and live performer."
It also serves as the page's Open Graph image (Required Technical
Correction #7).

## Open items before production

- **Reel: SETTLED at 2:21 by Adrian's final call (v6).** He tried a 55s
  5-moment cut (v5), then decided the same day to keep all thirteen of his
  clip windows at full length — "if they don't want to scroll through the
  whole thing, they don't have to." v6 is the v4 edit exactly, with the one
  v5 improvement kept: the end card now reads "BOSTON VOCALIST & LIVE
  PERFORMER." This consciously overrides the correction brief's 50-60s
  requirement — owner's call beats auditor's brief. Watch-item if real
  Boston replies suggest it's too long (already noted in DECISIONS D16).
- Adrian still reviewing the rest of the page copy (his note when settling
  the reel).
- Testimonial exact quote if Adrian ever wants it as on-page text (dropped
  from the first release entirely per the brief; video preserved, unused).
- Commit this folder, then Phase 2 draft deploy on his go.
