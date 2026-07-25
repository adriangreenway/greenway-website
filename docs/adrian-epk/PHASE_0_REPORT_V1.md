# Adrian EPK — Phase 0 Report (answers Correction Brief v1)

Date: 2026-07-24
Scope: read-only inspection only, per `CORRECTION_BRIEF_V1.md`. No files edited. No deploy.

## 1. Current repository state

- Branch `docs/build-context`; `docs/adrian-epk/` itself has zero uncommitted changes (all committed at `8762b1d`). The unrelated uncommitted changes elsewhere in the tree (`Header.astro`, `site.ts`, `faq.astro`, `reviews.astro`, `public/proposals/`) are pre-existing "April work" from a different task and do not touch this folder.
- Route structure today: 3 generated pages — `dist/adrian/index.html` (lane chooser), `dist/adrian/solo/index.html`, `dist/adrian/vocalist/index.html`.
- Build scripts: `content.json` (all copy) + `build.py` (generator) → `dist/adrian/*` (gitignored, rebuilt before every deploy). `tools/assets_build.py`, `tools/cards_build.py`, `tools/reel_build.py`, `tools/range_server.py` handle media.
- Media locations: source footage in `~/Desktop/EPK` (never committed, repo is public); encoded web copies in `~/Desktop/EPK/renders/web/`; deploy destination is `/adrian/media/` on the proposals site.
- Deployment config: a **separate** repo, `~/Desktop/greenway-proposals` (its own `netlify.toml`, Netlify site `c6041c94-c26c-4ab8-ae5f-96c43addb081`). Checked: no `adrian/` folder exists there yet — **this EPK has never been deployed, draft or otherwise.** Nothing public anywhere today.
- Redirects: the proposals site's `netlify.toml` has no `[[redirects]]` block of any kind today.

## 2. Files that change in Phase 1

| File | Change |
|---|---|
| `content.json` | Full restructure. Drop `lanes`, `solo`, `vocalist`, `role_points`, `repertoire` blocks. Add one unified schema: hero, credibility strip, single reel, experience, contact, footer disclosure. |
| `build.py` | Replace `build_root()` + `build_lane()` with one `build_page()`. Delete `pick_songs()` and the `SONGS_JSON` dependency. Drop `topbar()`'s Solo/Vocalist/Song List links → Reel/Experience/Contact anchors only. Drop `greenway_section()` and `testimonial_section()` as rendered sections. Output shrinks to one `dist/adrian/index.html`. |
| `tools/cards_build.py` | One universal 1200×675 email card instead of `card-solo.jpg` + `card-vocalist.jpg`. |
| `README.md` | Update page list, deploy steps, email-card section. |
| `MEDIA_MANIFEST.md` | Reconcile per the brief's Required Correction #11: mark which videos are on-page (reel only) vs. preserved-but-unused (Neon Moon, Big Spring film, testimonial); note reel is still the 2:21 draft. |
| `~/Desktop/greenway-proposals/netlify.toml` (separate repo, Phase 2/3 only) | Add two redirect rules for the retired `/adrian/solo/*` and `/adrian/vocalist/*` paths. |

No `src/` file, nav, or this repo's `netlify.toml` is touched. Confirmed by grep.

## 3. Isolation confirmation

- **Astro site / nav / this repo's `netlify.toml`:** untouched, confirmed by grep for `adrian` across `src/`.
- **Command Center / Growth Hour:** no references anywhere in `docs/adrian-epk/`.
- **"Boston 75 CRM":** the phrase appears only inside this EPK's own docs (the brief and `README.md`), naming the handoff spec it was built from. It is not a codebase present in this repo or this session — there is nothing here that could touch it.
- **Greenway client proposals:** share the same Netlify **site** and deploy folder (`~/Desktop/greenway-proposals`) as a neighbor, not the same code. Known hazard already on record: a `--prod` deploy publishes everything staged in that folder. Phase 2/3 must run the existing pre-deploy live-file diff first, same as every other proposals deploy.

## 4. Final reel status

Only the 2:21 (141s) v4 draft exists — all 13 of Adrian's own timestamp windows, full length, per his explicit build-01 instruction not to trim them. **No 50–60s cut and no new timestamps exist.**

Per the brief's own instruction (§Reel direction), Phase 1 will not invent a new cut order. The 2:21 draft will be marked a clearly temporary asset, and the real 50–60s reel will be listed as the one open launch blocker.

## 5. `/solo` and `/vocalist` redirect plan

Nothing has ever been deployed, so no live visitor or bookmark depends on these paths today. Phase 1 plan: stop generating `solo/` and `vocalist/` output, and add to the proposals site's `netlify.toml` (which has no redirects today):

```
[[redirects]]
  from = "/adrian/solo/*"
  to = "/adrian/"
  status = 301
[[redirects]]
  from = "/adrian/vocalist/*"
  to = "/adrian/"
  status = 301
```

Takes effect the first time this EPK is deployed at all, draft or prod.

## 6. Conflicts with the brief / with what's already on record

1. **Video hosting — real conflict.** The brief says "Use the final Vimeo reel when Adrian supplies its link." Adrian explicitly ruled out Vimeo for this EPK on 2026-07-24 (self-hosted mp4, no third-party logo, same pattern as the proposal template) — recorded in `DECISIONS.md` D16 and `README.md`. Recommend staying self-hosted; flagged below for Adrian to confirm.
2. **Two-lane architecture — deliberate, not silent, reversal.** `content.json`/`build.py`/`README.md` are all built around the solo-vs-vocalist split Adrian approved as D16's v1 direction. The brief explicitly supersedes it. Since a recorded decision is changing, this gets logged as a `DECISIONS.md` amendment once Phase 1 is approved and built, not silently overwritten.
3. **Repertoire / song-list dependency removal — simplification, not a conflict.** Today's build refuses to invent song titles by sourcing them live from `song-list/songs.json`. The brief removes the repertoire section entirely, so that dependency just goes away. Nothing to resolve.
4. **Reel length vs. "don't trim" instruction — already resolved, not a live conflict.** See §4: the brief's own fallback (treat as draft, list as blocker) matches Adrian's prior instruction rather than overriding it.

## Open decisions for Adrian (not technical — his call)

1. Video hosting: keep self-hosted mp4 (no logo, matches precedent) or switch to Vimeo as the brief assumes?
2. Reel: proceed with the 2:21 draft marked "temporary" and treat the real 50–60s cut as the launch blocker, or does Adrian already have new timestamps for a tight cut?
3. Hero/email-card image: use the existing vocalist hero (him singing, not acoustic-only) for both the page hero and the new single email card, per the brief's "not exclusively acoustic" instruction?

## Decisions (2026-07-24)

Adrian confirmed all three recommended defaults:

1. **Video stays self-hosted.** No Vimeo. Ignore the brief's Vimeo line.
2. **2:21 draft ships marked temporary.** Final 50–60s reel is the one open launch blocker; no trim gets invented.
3. **Vocalist hero (him singing) is the single hero/email-card image.** Solo/acoustic hero is not used.

Phase 1 is scoped and ready to build pending Adrian's go. The two-lane → one-page reversal (Controlling direction #1–4) supersedes `DECISIONS.md` D16's approved v1 structure; log the D16 amendment once Phase 1 is built, not before.
