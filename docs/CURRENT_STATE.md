# CURRENT STATE: The Greenway Band Website

**Last updated:** 2026-07-24
**Last verified build:** PASS on 2026-07-24 (`npm run build`, 6 pages, clean; no test/typecheck scripts exist in this repo to run).

Rules for this file (Claude Code, obey these):
- Keep it under 60 lines. This file gets read every session, so it must stay cheap.
- Only the current truth lives here. Deep verified detail with evidence lives in `PROJECT_STATE.md`, `ARCHITECTURE.md`, `INTEGRATIONS.md`; fold new findings in, don't duplicate them here.
- Never delete a Known Issue without fixing it or moving it to ROADMAP.md as deferred.

## Working version
Working tree on branch `docs/build-context`, ahead of `origin` (latest: `8762b1d` Adrian EPK build 01; push pending Adrian's word). The site itself lives on two diverged branches: `dev` (deployed — strong inference from the netlify.app redirect existing only there) and `main` (has Reviews + FAQ committed, not deployed). Neither is checked out right now; this branch carries documentation only.
## Active task
**Three separate tracks. Only one is paused.**

1. **The Astro rebuild is PAUSED**, cross-project decision. Adrian decided 2026-07-03 (in the separate Growth Hour project) that greenwayband.com stays on Squarespace; this Astro rebuild (~70% done) resumes after Growth Hour's M3 ships. Source: `~/greenway-growth-hour/docs/{CURRENT_STATE,ROADMAP,DECISIONS}.md`, `START_HERE.md`, and `WEBSITE_PLAN_2026-07-03.md`. No new Astro features, deploys, or DNS changes until Adrian lifts this.
2. **The Squarespace lead-form embed: Gates 0-2 CLOSED, Gate 3 ON HOLD (not just paused on a "go").** Growth Hour's `POST /api/lead-intake` is deployed and live. v3 (premium dark redesign, `docs/squarespace/lead-form-embed.html` + `README.md`) is live and dark at `greenwayband.com/inquiry-test`. **2026-07-03: all 5 previously-deferred fields added** (`event_type`, `cocktail_hour_interest`, `budget_range`, `planner_name`, `message`) now that Growth Hour's endpoint accepts them, and the iOS Safari date-field height bug Adrian spotted is fixed and phone-confirmed. Gates 0-2 fully closed on the full 13-field form.
   **2026-07-03, same day: Adrian said "go" on Gate 3, then reconsidered before anything was touched in Squarespace (nothing was actually changed there — Claude has no Squarespace access).** He wants nothing live on greenwayband.com until BOTH this website's build and the separate Growth Hour app are entirely finished, not just at a milestone. Reason: a past form went live early and lost real submissions. See `docs/DECISIONS.md` D13 (controlling) and the memory note `greenway_golive_hold`. **Do not propose or execute Gate 3 again until Adrian says both builds are done.**
3. **Adrian Michael EPK (Boston) — IN PROGRESS, build 01 done, "build 02" is next.** Personal EPK for his Boston outreach at `proposals.greenwayband.com/adrian` (+`/solo`, `/vocalist`), built in `docs/adrian-epk/`. Independent of both tracks above: touches no `src/` file, no nav, no `netlify.toml`, so the Astro hold is intact. Committed `8762b1d`, local only, nothing deployed. Adrian has an audit zip on his Desktop for a ChatGPT review and has reconsiderations to raise in the next session. See `docs/adrian-epk/README.md` + `MEDIA_MANIFEST.md`.

## Recently completed (last 5 max, then archive)
- 2026-07-24 **Adrian Michael EPK build 01** (D16), committed `8762b1d`, local only. Three generated pages from `content.json` + the song-list authority, brand tokens mirrored from `global.css`, `noindex`. His calls during the build: **no Vimeo** (self-hosted mp4 behind a poster facade, the proposal template's pattern), 9pc promo **excluded everywhere** (it fronts a different vocalist), reel v4 (2:21) cut from **all thirteen of his own clip windows** at full length, harmony vocals kept in the positioning, electric guitar left out until there's footage. Real gotcha found and fixed: `python -m http.server` ignores HTTP Range, which makes every previewed `<video>` unseekable and looks like a broken player — `tools/range_server.py` + the `adrian-epk` launch entry fix it; Netlify serves Range fine in prod. `dist/` is gitignored (repo-wide build-output rule), README documents the three commands that regenerate it.
- 2026-07-24 **Marli's live page updated again**: Adrian approved v10+v11 (sparkler-exit closing photo + greenhouse/crowd duo). Committed (website `7a46178`; proposals `ae36217`) and production-deployed — verified live on the real domain (HTTP 200, both new assets 200, package order/photo-duo/closing-photo all present). Rollback deploy `6a6367378403325dac860b82` (the v9 state, before these two photos) if ever needed. Print/PDF unaffected by design (screen-only additions).
- 2026-07-24 **Song list LIVE** at `proposals.greenwayband.com/song-list` (D15 v2-v5), 434 songs. Deployed `6a63bad71958589cd9312bc4`; rollback `6a6380672aa2910b840c6fb5`. Proposals repo `d251da3`; website repo pushed through `23e8a12`. History: v2 green rejected ("our color scheme isn't green") → rebuilt via 16-agent workflow on the proposal motif (charcoal cover, cream body, stripped copy). v3 `embed.html` added, a Squarespace Code Block paste-in using the scoping convention proven in `docs/squarespace/lead-form-embed.html` (`#greenway-songlist` wrapper, `gw-` prefixes, literal colors); adversarial-harness verified, zero CSS leakage either way. v4 genre nav switched to middot dividers matching `SocialProofStrip.astro`'s venue strip. v5 "Is This Love" (Bob Marley) added. **Squarespace copy is Adrian's to paste** (no access here); the old unstyled list still sits at `greenwayband.com/song-list` until he does. **Repertoire updates: Adrian just says what changed, Claude edits the xlsx + rebuilds + resyncs** — convention documented in `docs/song-list/README.md` (single A→Z list tagged by genre, insert at the right row, exact genre string).
- 2026-07-24 **Near-miss caught by the pre-deploy safety diff:** `assets/uptown-funk-2026a.mp4` had been moved to `~/Desktop/EPK` during EPK Phase 0 but was still live and still referenced by `hinojosa/index.html`. The song-list deploy would have deleted it and broken the video on Marli's live proposal. Restored before deploying (EPK keeps its copy); hazard written up in `docs/proposals/PROPOSAL_SYSTEM.md` step 1.
- 2026-07-24 **Marli's live page updated in place** (Adrian's explicit ask): `proposals.greenwayband.com/hinojosa` now serves the full v5-v9 redesign — production deploy verified live (HTTP 200, correct package order, no deposit copy, badge on 10-Piece, real domain screenshot-checked). Proposals repo commit `59716b4`; rollback deploy `6a569f09a251fd14726df077` (her July 21 original) if ever needed.

## Known issues
| Issue | Severity | Notes |
|---|---|---|
| Staging URL self-redirects to Squarespace | Medium | `netlify.toml` 301s `greenway-website.netlify.app/*` → `greenwayband.com`, which is still Squarespace. The new build isn't viewable at its own staging URL. Use `npm run dev` or a Netlify deploy-preview link. Fix is a one-line redirect removal, owner-approved only. |
| `dev`/`main` branch split | Medium | `dev` (deployed) lacks committed Reviews/FAQ; `main` has them committed but isn't deployed. Working tree currently has them uncommitted on `dev`. See `PROJECT_STATE.md` for full evidence. |
| `published` flag in `site.ts` is dead metadata | Low | Nothing reads `pages[].published`; nav is a hardcoded array in `Header.astro`. Publishing a page needs a nav edit + a page file, not just a flag flip. |
| FAQ AI assistant never built | Low | FAQ shipped as a static 12-question accordion instead. Revisit only if Adrian still wants it. |
| Reviews page has no real content | Low | Three "Review coming soon" placeholders; copy-integrity compliant, just incomplete. Blocked on Adrian supplying real, attributed testimonials. |
| Vocalist Showcase page missing | Low | No `vocalists.astro` exists; `/vocalists` 404s. Blocked on content. |
| Minor design-token deviations | Low | A few `#ffffff` button-hover states and an off-token gray in `Logo.astro`; dead boxed `.book-form__input` CSS rule in `global.css`. See `DESIGN_SYSTEM.md`. |

## Blockers
- Astro rebuild: none technical, self-paused per Active task note above.
- Squarespace lead-form embed: on hold at Gate 3 by Adrian's request (D13); not code-blocked, don't raise going-live until he says both builds are done.

## Technical warnings
- No test script and no `astro check` configured. Verification = `npm run build` clean + manual browser check.
- Do not commit, push, deploy, or touch Cloudflare DNS without Adrian's explicit approval (hard stop, see `docs/CODE_WORKFLOW.md`).
- Do not discard the uncommitted working-tree changes on `dev` (Reviews/FAQ publish edits) without checking `PROJECT_STATE.md` first — it may be unfinished, unpushed work.
- `PROJECT_STATE.md`, `ARCHITECTURE.md`, and `INTEGRATIONS.md` hold the deep, evidence-backed detail behind every line above; this file is the quick truth only.

## Next recommended action
**Adrian EPK "build 02"** — he ended build 01 saying there are things he wants
to reconsider, and deliberately saved them for a fresh session. Start by asking
what they are. He also took `~/Desktop/adrian-epk-audit-2026-07-24.zip` to
ChatGPT for an outside audit, so expect a second list of findings; treat both as
input to scope build 02 before touching anything. Already known candidates: reel
length (2:21), more photos he has on hand (a wide horizontal hero, a
restaurant/lounge shot for the solo lane), the testimonial pull quote. Nothing
about the EPK is deployed, so all of this is safely reversible.
Also open, unchanged: proposal-template arc closed and live; push to origin
pending Adrian's word; a canned "next steps" reply email deferred at his word.
Gate 3 frozen (D13); Astro rebuild still paused on Growth Hour M3.
