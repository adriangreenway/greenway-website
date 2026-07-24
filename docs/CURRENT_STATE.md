# CURRENT STATE: The Greenway Band Website

**Last updated:** 2026-07-24
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
- 2026-07-24 Template v7+v8 (D14 v7/v8). v7 = targeted rollback per Adrian's strict spec: original per-package two-column itemization + five original labels restored, shared "Included With Every…" section removed, subtitles retired for one secondary benefit sentence each, closing back to Schedule-a-Call primary + quiet Move-Forward email secondary; all v5/v6 approved improvements kept. Adrian: "this actually looks really good." v8 same day on his feedback: 10-Piece ALWAYS leads Recommended (hinojosa realigned, v5 flag 1 closed), desktop ≥900px side-by-side bordered comparison cards (mobile stacked unchanged, print untouched), video section trimmed to label + player + caption. Names stay 6/10-Piece Band (naming CLOSED). Browser-verified both breakpoints, console clean; docs synced. Nothing committed, prod untouched.
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
Template SETTLED through v9 and committed 2026-07-24 (D14 v9): the 50%
deposit line is the ONLY copy cut (policy lives in PRICING_AND_CONTENT
"Reservation + payment flow", contract/invoice use only, never on a page);
Adrian restored the helper lines a broader sweep had cut ("that one was
fine") and locked "Two Ways to Fill the Room" ("i love that one"). Final
draft, verified: `6a63654a839ef42d67904902--greenway-proposals.netlify.app
/hinojosa/`. Branch ahead 1 after the v9 commit — his "push" backs it up.
Open: does Marli's live page get the reworked version? (prod = her
2026-07-21 original; his explicit ask + prod deploy.) Deferred at his word:
"next steps" reply email for EMAIL_TEMPLATES.md. Proposals repo still
uncommitted (normal). Gate 3 frozen (D13).
