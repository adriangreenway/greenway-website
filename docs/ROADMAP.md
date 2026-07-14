# ROADMAP: The Greenway Band Website

The plan, split by when. Claude Code: update statuses when items ship. New ideas from Adrian go into Later unless he says otherwise.

Statuses: PLANNED, APPROVED (plan exists), IN PROGRESS, SHIPPED, DEFERRED, PAUSED

**Note on sequencing:** the Astro rebuild items below are PAUSED at the project level per the 2026-07-03 cross-project decision (see `CURRENT_STATE.md` "Active task"). Nothing there is urgent until Adrian lifts the pause. The **Squarespace lead-form embed** (below) is the one exception — it's a separate, unblocked track per `WEBSITE_PLAN_2026-07-03.md` and moves independently of the pause.

## In progress (unblocked — not part of the Astro pause)
| Item | Size | Status | Depends on | Done means |
|---|---|---|---|---|
| Squarespace lead-form embed (Gates 0-3) | S | Gates 0-2 SHIPPED 2026-07-03; Gate 3 PLANNED | Adrian's explicit "go" | Gates 0-2 done: v3 premium-dark embed live and dark at `greenwayband.com/inquiry-test`, real phone test confirmed landing correctly in Growth Hour Contacts. Gate 3 (actually going live — publish or link from the real Book page) needs Adrian's explicit "go," plus a same-day and one-week-later canary check. |

## Now (Astro reconciliation hygiene — paused, optional, do only if Adrian asks)
| Item | Size | Status | Depends on | Done means |
|---|---|---|---|---|
| Reconcile `dev` vs `main` and the uncommitted April work | S | PLANNED | Owner approval to commit/push | Either `main`'s Reviews/FAQ are merged into the deploy branch, or the working-tree April work on `dev` is committed and pushed. One canonical branch going forward. |
| Decide the staging self-redirect | S | PLANNED | Owner approval | `netlify.toml`'s netlify.app→greenwayband.com redirect is either removed (so staging shows the new build) or explicitly kept, with the tradeoff stated to Adrian. |
| Confirm the Netlify deploy branch in the dashboard | S | PLANNED | none | Netlify UI confirms which branch actually deploys (inferred to be `dev`, unverified). |

## Next (real content — blocked on Adrian)
| Item | Size | Status | Depends on | Done means |
|---|---|---|---|---|
| Reviews content | S | PLANNED | Adrian supplies real testimonials | The 3 "Review coming soon" placeholders are replaced with real, attributed reviews. Copy-integrity rule applies. |
| Hero media | S | PLANNED | Adrian supplies video/photo | The homepage hero's solid-color placeholder is replaced with the real hero video or a poster image; the `WhyGreenway` media placeholder is filled. |
| Experience "For Planners" detail | S | PLANNED | Adrian supplies production detail | The placeholder paragraph is expanded with real detail (Ableton-driven arrangements, MIDI-synced production, etc). |
| Vocalist Showcase page | M | PLANNED | Adrian supplies content | `src/pages/vocalists.astro` is built and added to nav; `site.ts`'s `Vocalists` flag flips to `true`. |

## Later
- **FAQ AI assistant:** decide whether to build the originally-planned AI assistant shell for the FAQ page, or keep the static accordion as the final v1. No artifact of a prior plan exists in this repo; ask Adrian if it's still wanted.
- **Wire the `published` flag:** optional refactor to drive the header nav from `site.ts`'s `pages[]` and add a 404 guard for unpublished routes, so publishing becomes a one-line toggle instead of editing `Header.astro` by hand.
- **Minor cleanups:** remove dead `LogoInline.astro` / `LogoMonument.astro`; drop the overridden boxed `.book-form__input` rule in `global.css`; replace `#ffffff` button-hover states and the `Logo.astro` off-token gray with palette tokens.
- **Launch:** flip the Cloudflare A record for `greenwayband.com` from Squarespace to Netlify (reversible in minutes). Coordinate with the staging-redirect decision above. Not imminent — see the pause note at the top of this file.

## Not planned
Things considered and rejected, or intentionally out of scope, so they don't get re-litigated.
- A CMS, auth, e-commerce, or an on-site booking calendar. This is a static marketing site; the only conversion action is the Book inquiry form.
- Any Supabase, Stripe, or Twilio code in this repo. Those belong to the separate Command Center CRM.
- Any additional or competing lead-intake mechanism beyond the one Squarespace embed above and the existing `BookForm.astro` → Command Center path. Growth Hour owns lead intake going forward; don't build a third path.
