# CURRENT STATE: The Greenway Band Website

**Last updated:** 2026-07-24
**Last verified build:** PASS on 2026-07-24 (`npm run build`, 6 pages, clean; no test/typecheck scripts exist in this repo to run).

Rules for this file (Claude Code, obey these):
- Keep it under 60 lines. This file gets read every session, so it must stay cheap.
- Only the current truth lives here. Deep verified detail with evidence lives in `PROJECT_STATE.md`, `ARCHITECTURE.md`, `INTEGRATIONS.md`; fold new findings in, don't duplicate them here.
- Never delete a Known Issue without fixing it or moving it to ROADMAP.md as deferred.

## Working version
Working tree on branch `docs/build-context`, ahead of `origin` by 3 (hinojosa record, end-session pass, song-list D15; push pending Adrian's word). The site itself lives on two diverged branches: `dev` (deployed — strong inference from the netlify.app redirect existing only there) and `main` (has Reviews + FAQ committed, not deployed). Neither is checked out right now; this branch carries documentation only.
## Active task
**Two separate tracks. Only one is paused.**

1. **The Astro rebuild is PAUSED**, cross-project decision. Adrian decided 2026-07-03 (in the separate Growth Hour project) that greenwayband.com stays on Squarespace; this Astro rebuild (~70% done) resumes after Growth Hour's M3 ships. Source: `~/greenway-growth-hour/docs/{CURRENT_STATE,ROADMAP,DECISIONS}.md`, `START_HERE.md`, and `WEBSITE_PLAN_2026-07-03.md`. No new Astro features, deploys, or DNS changes until Adrian lifts this.
2. **The Squarespace lead-form embed: Gates 0-2 CLOSED, Gate 3 ON HOLD (not just paused on a "go").** Growth Hour's `POST /api/lead-intake` is deployed and live. v3 (premium dark redesign, `docs/squarespace/lead-form-embed.html` + `README.md`) is live and dark at `greenwayband.com/inquiry-test`. **2026-07-03: all 5 previously-deferred fields added** (`event_type`, `cocktail_hour_interest`, `budget_range`, `planner_name`, `message`) now that Growth Hour's endpoint accepts them, and the iOS Safari date-field height bug Adrian spotted is fixed and phone-confirmed. Gates 0-2 fully closed on the full 13-field form.
   **2026-07-03, same day: Adrian said "go" on Gate 3, then reconsidered before anything was touched in Squarespace (nothing was actually changed there — Claude has no Squarespace access).** He wants nothing live on greenwayband.com until BOTH this website's build and the separate Growth Hour app are entirely finished, not just at a milestone. Reason: a past form went live early and lost real submissions. See `docs/DECISIONS.md` D13 (controlling) and the memory note `greenway_golive_hold`. **Do not propose or execute Gate 3 again until Adrian says both builds are done.**

## Recently completed (last 5 max, then archive)
- 2026-07-24 **Marli's live page updated again**: Adrian approved v10+v11 (sparkler-exit closing photo + greenhouse/crowd duo). Committed (website `7a46178`; proposals `ae36217`) and production-deployed — verified live on the real domain (HTTP 200, both new assets 200, package order/photo-duo/closing-photo all present). Rollback deploy `6a6367378403325dac860b82` (the v9 state, before these two photos) if ever needed. Print/PDF unaffected by design (screen-only additions).
- 2026-07-24 Song list page (D15, v2, v3): client xlsx v4 → `docs/song-list/` → 433 songs + songs.json. v2: green rejected ("our color scheme isn't green"), rebuilt via 16-agent workflow strictly on the proposal motif (charcoal cover, cream body, stripped copy). v3: Adrian wants it on greenwayband.com directly, not just proposals — added `embed.html`, a Squarespace Code Block paste-in following the exact scoping convention already live in `docs/squarespace/lead-form-embed.html` (`#greenway-songlist` wrapper, `gw-` prefixed everything, literal colors). Verified with an adversarial harness (colliding tag/class names) — zero CSS leakage either direction. `greenwayband.com/song-list` already has an old unstyled list live; Adrian pastes the new code himself when ready (no Squarespace access here). `index.html` still staged for proposals.greenwayband.com/song-list, deploy on his go.
- 2026-07-24 **Marli's live page updated in place** (Adrian's explicit ask): `proposals.greenwayband.com/hinojosa` now serves the full v5-v9 redesign — production deploy verified live (HTTP 200, correct package order, no deposit copy, badge on 10-Piece, real domain screenshot-checked). Proposals repo commit `59716b4`; rollback deploy `6a569f09a251fd14726df077` (her July 21 original) if ever needed.
- 2026-07-24 Template v7+v8+v9 (D14 v7-v9), committed + pushed to website repo (`1198ee3`, `c6ae119`). v7 = Adrian's strict rollback spec: original per-package two-column itemization restored, shared services section removed, subtitles → one benefit sentence, closing back to Schedule-a-Call primary. v8 (same day, his feedback): 10-Piece ALWAYS leads Recommended, desktop ≥900px side-by-side comparison cards, video trimmed to label + player + caption. v9: the one payment-copy line (50% deposit) removed for good — the only cut he wanted; all established helper lines (inline CTA, closing note, "Ready now?") kept verbatim, "Two Ways to Fill the Room" locked ("i love that one"). Naming CLOSED: 6-Piece/10-Piece Band.
- 2026-07-23 (session 3) Template `a7884bd` (v4) was extended to v5 (dedicated 7-page print/PDF layout; crowd photo height-capped everywhere; fixed a real phone CSS bug) then v6 (a ChatGPT correction pass: shared services, Move Forward CTA, video click fix, contrast floors). A package-rename experiment was tried and rejected. Adrian's verdict on v6: "I'm not liking these changes" — superseded by the 2026-07-24 v7 rollback above. Nothing beyond `a7884bd` is committed.
- 2026-07-23 Proposal live: `proposals.greenwayband.com/campbell` (Kate Campbell wedding 2027-03-13, Evelyn's Park, Bellaire; 10-Piece $14,375 recommended + 6-Piece $10,350 + cocktail cards). New defaults: 10-Piece always leads Recommended, cocktail cards on by default. Template 4.1 email sent, links clean. Proposals repo commit `0f33446`; rollback deploy `6a5fe15d2d011fbb9622cc16`.

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
Proposal-template arc (v5-v11) closed: committed, pushed is pending Adrian's
word, and live on Marli's real page — see Recently completed. Also pending:
song-list deploy on Adrian's go (D15/v2). Deferred at his word: a canned
"next steps" reply email (contract → invoice → payment methods) for
EMAIL_TEMPLATES.md. Session's likely next start: a fresh ask, the song-list
go-live, or the Astro-rebuild pause lifting (still gated on Growth Hour M3 —
check `~/greenway-growth-hour`). Gate 3 frozen (D13).
