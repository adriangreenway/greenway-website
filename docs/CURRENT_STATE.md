# CURRENT STATE: The Greenway Band Website

**Last updated:** 2026-07-23
**Last verified build:** PASS on 2026-07-03 (`npm run build`, 6 pages, clean; no test/typecheck scripts exist in this repo to run).

Rules for this file (Claude Code, obey these):
- Keep it under 60 lines. This file gets read every session, so it must stay cheap.
- Only the current truth lives here. Deep verified detail with evidence lives in `PROJECT_STATE.md`, `ARCHITECTURE.md`, `INTEGRATIONS.md`; fold new findings in, don't duplicate them here.
- Never delete a Known Issue without fixing it or moving it to ROADMAP.md as deferred.

## Working version
Working tree on branch `docs/build-context`, up to date with `origin`. The site itself lives on two diverged branches: `dev` (deployed — strong inference from the netlify.app redirect existing only there) and `main` (has Reviews + FAQ committed, not deployed). Neither is checked out right now; this branch carries documentation only.

## Active task
**Two separate tracks. Only one is paused.**

1. **The Astro rebuild is PAUSED**, cross-project decision. Adrian decided 2026-07-03 (in the separate Growth Hour project) that greenwayband.com stays on Squarespace; this Astro rebuild (~70% done) resumes after Growth Hour's M3 ships. Source: `~/greenway-growth-hour/docs/{CURRENT_STATE,ROADMAP,DECISIONS}.md`, `START_HERE.md`, and `WEBSITE_PLAN_2026-07-03.md`. No new Astro features, deploys, or DNS changes until Adrian lifts this.
2. **The Squarespace lead-form embed: Gates 0-2 CLOSED, Gate 3 ON HOLD (not just paused on a "go").** Growth Hour's `POST /api/lead-intake` is deployed and live. v3 (premium dark redesign, `docs/squarespace/lead-form-embed.html` + `README.md`) is live and dark at `greenwayband.com/inquiry-test`. **2026-07-03: all 5 previously-deferred fields added** (`event_type`, `cocktail_hour_interest`, `budget_range`, `planner_name`, `message`) now that Growth Hour's endpoint accepts them, and the iOS Safari date-field height bug Adrian spotted is fixed and phone-confirmed. Gates 0-2 fully closed on the full 13-field form.
   **2026-07-03, same day: Adrian said "go" on Gate 3, then reconsidered before anything was touched in Squarespace (nothing was actually changed there — Claude has no Squarespace access).** He wants nothing live on greenwayband.com until BOTH this website's build and the separate Growth Hour app are entirely finished, not just at a milestone. Reason: a past form went live early and lost real submissions. See `docs/DECISIONS.md` D13 (controlling) and the memory note `greenway_golive_hold`. **Do not propose or execute Gate 3 again until Adrian says both builds are done.**

## Recently completed (last 5 max, then archive)
- 2026-07-23 Proposal template upgrade v1+v2+v3 built, locally verified, **not yet committed** (D14 + amendments, see DECISIONS.md): every new wedding proposal defaults to two performance-photo bands, a self-hosted click-to-load video (`assets/uptown-funk-2026a.mp4`, 720p, no Vimeo/watermark), the three-hours contract line, and two Schedule-a-Call CTAs. Palette is the hybrid "C" (dark cover+closing, cream `#F5F2ED` body on the site's own tokens) — a 3-judge panel voted it unanimously over full-dark/full-cream. Venue strip built then dropped (Adrian: low value). Built a real preview of Marli Hinojosa's actual proposal on the new template (real facts, no live page touched); Adrian called it "a good first pass" and flagged 3 items, all now fixed: (1) **FIXED 2026-07-23 (D14 v4, Adrian's "you decide")** — photo bands show the whole 3:2 frame on wide screens (the strip crop was cutting the musicians out); phones keep the immersive 68vh/52vh crop via a 560px media query. (2) **FIXED** — perceived font/weight difference between palette zones was a real optical effect (dark-on-light reads thinner than light-on-dark at equal weight); compensated with a `-webkit-text-stroke` on the cream body, cancelled in `.cover`/`.closing`. (3) **FIXED** — the hard-edge cut after the first photo felt too abrupt to him; reinstated a gradient (dark top → cream bottom) overriding the judge panel's hard-edge recommendation, per Adrian's direct instruction. **Nothing in either repo is committed** — Adrian: "I don't want to commit it just yet."
- 2026-07-23 Proposal live: `proposals.greenwayband.com/campbell` (Kate Campbell wedding 2027-03-13, Evelyn's Park, Bellaire; 10-Piece $14,375 recommended + 6-Piece $10,350 + cocktail add-on cards). **New defaults set this build (Adrian, 2026-07-23):** the 10-Piece now always leads Recommended regardless of what the client asked for, and the Cocktail Hour cards are on by default on every wedding proposal (both were previously conditional; docs/skill updated). Template 4.1 email SENT to katercampbell111@gmail.com, links verified clean in Sent. Proposals repo commit `0f33446`; rollback deploy `6a5fe15d2d011fbb9622cc16`.
- 2026-07-21 Proposal live: `proposals.greenwayband.com/hinojosa` (Marli Hinojosa wedding 2027-07-17, The Junior League of Houston, 100-200 guests, reception 7-11 PM; 6-Piece $10,350 recommended + 10-Piece $14,375 + cocktail add-on cards, no timeline). Template 4.1 email SENT to Marlihinojosa13@gmail.com same day with an Adrian-approved apology line (her Jul 5 form sat 16 days, came from a different address than her Jun 23 yahoo email); links verified clean in Sent 2026-07-23 (correction — the 2026-07-21 end-of-session note wrongly called this a pending draft; it was already sent). Proposals repo commit `c5a5845`; rollback deploy `6a569f09a251fd14726df077`.

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
Proposals track: turner, giulia-costantini, hinojosa, and campbell all live
under the OLD template. The NEW template (v4: hybrid palette + self-hosted
video + gradient seam + text-weight fix + whole-frame photos on wide screens)
is built and verified on real Hinojosa content with all review items closed,
but uncommitted by Adrian's explicit choice — do not commit either repo
without him saying so again. Next: get Adrian's go to commit, and his call on
whether Hinojosa's live page gets the new look or the template just becomes
the default going forward. Nothing to build on Astro/Squarespace — Gate 3
stays frozen until Adrian confirms both builds are entirely done (D13).
