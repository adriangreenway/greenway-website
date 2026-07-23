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

Reconciliation debt on the Astro rebuild, open whenever Adrian wants it tackled (not urgent, unaffected by the Squarespace track): `dev` vs `main` branch split, the uncommitted "April work" on `dev`'s working tree (publishes Reviews + FAQ), and the staging self-redirect. Full detail in `PROJECT_STATE.md`.

## Recently completed (last 5 max, then archive)
- 2026-07-23 Proposal live: `proposals.greenwayband.com/campbell` (Kate Campbell wedding 2027-03-13, Evelyn's Park, Bellaire; 10-Piece $14,375 recommended + 6-Piece $10,350 + cocktail add-on cards). **New defaults set this build (Adrian, 2026-07-23):** the 10-Piece now always leads Recommended regardless of what the client asked for, and the Cocktail Hour cards are on by default on every wedding proposal (both were previously conditional; docs/skill updated). Template 4.1 email SENT to katercampbell111@gmail.com, links verified clean in Sent. Proposals repo commit `0f33446`; rollback deploy `6a5fe15d2d011fbb9622cc16`.
- 2026-07-21 Proposal live: `proposals.greenwayband.com/hinojosa` (Marli Hinojosa wedding 2027-07-17, The Junior League of Houston, 100-200 guests, reception 7-11 PM; 6-Piece $10,350 recommended + 10-Piece $14,375 + cocktail add-on cards, no timeline). Template 4.1 draft in Gmail to Marlihinojosa13@gmail.com with an Adrian-approved apology line (her Jul 5 form sat 16 days, came from a different address than her Jun 23 yahoo email). Draft NOT sent; Adrian to click-test both links first. Proposals repo commit `c5a5845`; rollback deploy `6a569f09a251fd14726df077`.
- 2026-07-14 Proposal live: `proposals.greenwayband.com/turner` (Garrett Turner wedding 2027-10-23, Le Tesserae, Houston; 6-Piece $10,350 recommended + 10-Piece $14,375 + cocktail add-on cards). Intro section REMOVED same day (repetitive with the Template 4.1 email, now in `docs/proposals/EMAIL_TEMPLATES.md`); **no-intro is the locked standard** for new proposals (see PRICING_AND_CONTENT.md). Template 4.1 email SENT to Garrett 2026-07-14 with clean direct links (17hats `#`-URL trips a Google Redirect Notice inside Gmail — gotcha noted in EMAIL_TEMPLATES.md). Page client-visible, 30-day validity running. Proposals repo commits `4d6f93a` + `706cef4`; this repo's doc edits uncommitted.
- 2026-07-13 Proposal live: `proposals.greenwayband.com/giulia-costantini` (wedding 2027-05-29, The Houstonian Hotel; 10-Piece $14,375 recommended + 6-Piece $10,350 + cocktail add-on cards). Adrian's proposal style rules locked into `docs/proposals/` (commit `09f5b3a` on this branch, not pushed). Third track, unaffected by any hold.
- 2026-07-03 Squarespace lead-form embed v3: premium dark redesign ported from the Chat 1.3 "CSS Branded Forms" session (Bodoni Moda, charcoal shadowed fields, cream button, phone auto-format, staggered reveal); wrapper carries its own background so section color can't cause invisible text again. Same 8-field payload, schema-matched. Adrian's phone test from `/inquiry-test` succeeded earlier the same day (browser-side confirmed; Growth Hour record check still pending — Claude has no dashboard login). Awaiting re-paste of v3 + one re-test. Gate 3 still needs Adrian's "go". Extra old-form fields (event type, budget, cocktail hour, planner) deferred — need a Growth Hour schema change first.

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
- Squarespace lead-form embed: intentionally on hold at Gate 3 by Adrian's explicit request (see D13). Not blocked on anything code-side; do not raise going-live again until he says both builds are done.

## Technical warnings
- No test script and no `astro check` configured. Verification = `npm run build` clean + manual browser check.
- Do not commit, push, deploy, or touch Cloudflare DNS without Adrian's explicit approval (hard stop, see `docs/CODE_WORKFLOW.md`).
- Do not discard the uncommitted working-tree changes on `dev` (Reviews/FAQ publish edits) without checking `PROJECT_STATE.md` first — it may be unfinished, unpushed work.
- `PROJECT_STATE.md`, `ARCHITECTURE.md`, and `INTEGRATIONS.md` hold the deep, evidence-backed detail behind every line above; this file is the quick truth only.

## Next recommended action
Proposals track: turner, giulia-costantini, and campbell live and emailed;
hinojosa live 2026-07-21 with its Template 4.1 email still waiting in Gmail
Drafts for Adrian to click-test links and send. Awaiting client replies,
nothing queued. If Adrian brings a ChatGPT-locked page-copy spec, fold it
into TEMPLATE.html. Open one-word offers: shortening the proposals site's
1-hour cache, and moving the GitHub token out of the proposals repo's
remote URL into the keychain.
Nothing to build right now on either site track. Gates 0-2 are fully closed and phone-tested on the Squarespace embed, but Gate 3 (going live) is deliberately on hold until Adrian confirms both this website's build and the Growth Hour app are entirely done (see D13). The Astro rebuild stays paused behind Growth Hour's M3. Do not propose go-live steps for either track until Adrian raises it himself.
