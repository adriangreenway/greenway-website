# Squarespace lead-form embed (dark build)

Built per `WEBSITE_PLAN_2026-07-03.md` (Bridge Prompt B), read from `~/greenway-growth-hour`.
This is separate from the Astro rebuild pause — the Astro site itself is untouched by this work.

**Status: dark.** Not linked from any navigation. Not linked from the real Book page. Stops before
Gate 3 (going live) for Adrian's explicit go-ahead. See D9/D10 in `docs/DECISIONS.md`... actually
see `WEBSITE_PLAN_2026-07-03.md` for the authoritative gate list; the summary is repeated below.

## What this is
`lead-form-embed.html` is a single self-contained block (form + scoped stylesheet + script) meant
to be pasted into a Squarespace **Code Block**. **v3 (2026-07-03)** ports the premium dark design
from the Chat 1.3 "CSS Branded Forms" session (export in Adrian's iCloud Drive) and the original
`~/Desktop/Project Knowledge/greenway-inquiry-form.html`: Bodoni Moda headline, charcoal boxed
fields with inset shadows on Rich Black, glow focus rings, inverted cream submit button, phone
auto-format, staggered fade-in. The wrapper carries its own `#0A0A09` background, so the
Squarespace section background setting no longer matters (earlier invisible-text bug can't recur).
**2026-07-03 update:** the old form's extra fields (Event Type, Cocktail Hour, Budget Range,
Planner Name, free notes) are now included — Growth Hour's `/api/lead-intake` schema was extended
to accept them (deployed and live-verified the same day) and this embed was updated to match.
It is NOT part of this repo's Astro build — Squarespace
has its own separate CMS and doesn't read anything from `src/`. This file exists here only so the
code has a home and a paper trail; the live copy of it will live inside Squarespace's page editor.

It posts to Growth Hour's public intake endpoint: `POST https://app-production-a334.up.railway.app/api/lead-intake`
— a different app, in the separate `~/greenway-growth-hour` repo, already deployed. This repo's own
Book form (`BookForm.astro`) is untouched and still posts to the old Command Center endpoint; the
two forms are intentionally independent.

**Why this will actually work from Squarespace:** the endpoint's CORS is locked to
`https://greenwayband.com` and `https://www.greenwayband.com` only. A Squarespace page is served on
that exact domain, so once the code is pasted into a real (even unlinked) page there, the browser's
origin will match. Verified live 2026-07-03 with a manual CORS preflight check against the deployed
endpoint (204, correct `access-control-allow-origin` header).

## Setup steps (Adrian, in the Squarespace dashboard)
1. **Pages panel → add a new page.** Give it any title (e.g. "Inquiry test", doesn't matter, it's not
   going live yet). When Squarespace asks where to add it, choose **"Not Linked"** (Squarespace's own
   section for pages that exist but aren't in any navigation menu) rather than adding it to the main nav.
2. Open the new page's content editor, add a **Code Block** (Insert Block → More → Code), and paste
   the entire contents of `lead-form-embed.html` into it.
3. Save and **publish the page** (it needs to be published to be reachable by URL — "Not Linked" just
   keeps it out of navigation, it doesn't keep it unpublished).
4. Open the page's real URL directly (Squarespace will show it, something like
   `greenwayband.com/inquiry-test`) — that confirms Gate 0.
5. Submit one real test inquiry from your own phone on that page — that's Gate 1 + Gate 2 together
   (the Growth Hour endpoint auto-approves a clean submission immediately into Queue).
6. Tell Claude what happened (rendered fine? submission went through? anything look wrong?) so Gate
   0-2 can be marked done in `docs/CURRENT_STATE.md`.
7. **Do not** add this page to navigation or link it from the real Book page yet. That's Gate 3 —
   it happens only when Adrian says "go."

## The 4 gates (from WEBSITE_PLAN_2026-07-03.md)
- **Gate 0:** the embed code renders correctly on the hidden page.
- **Gate 1:** the Growth Hour endpoint is deployed and a manual test submission lands correctly (confirmed live 2026-07-03 by Claude via a direct CORS check; still needs a real submission through the actual page to fully close).
- **Gate 2:** a real end-to-end test from the hidden page, on Adrian's own phone, works start to finish — and if anything fails, the failure message shows Adrian's real contact info as a fallback (built into the embed's error state).
- **Gate 3:** Adrian deliberately says "go" to publish the page live or link it from the real Book page. Canary check same day, and again a week later.

Never skip a gate. A form once went live half-working and real leads were missed silently — that's
exactly what this sequence protects against.

## Field mapping (must match the Growth Hour endpoint's schema exactly)
| Form field | JSON key | Required |
|---|---|---|
| Your name | `partner1_name` | yes |
| Partner's name | `partner2_name` | |
| Email | `email` | yes |
| Phone | `phone` | |
| Event date | `event_date` | yes (`YYYY-MM-DD`, via `type="date"`) |
| Venue (if known) | `venue` | |
| Estimated guest count | `guest_count` | |
| Event type | `event_type` | |
| Cocktail hour interest | `cocktail_hour_interest` | |
| Budget range | `budget_range` | |
| How did you hear about us? | `referral_source` | |
| Planner/coordinator name | `planner_name` | |
| Anything else? | `message` | |
| *(hidden honeypot)* | `_gotcha` | must stay empty |

Source of truth for this schema: `~/greenway-growth-hour/src/app/api/lead-intake/route.ts`. If that
endpoint's schema ever changes, this embed needs to change with it — they are not automatically kept
in sync (two separate repos).
