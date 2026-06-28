# DECISIONS (ADR-style log)

Chronological log of notable decisions. Newest at the bottom. Keep entries short.

---
## D-001 — Astro static site on Netlify, DNS on Cloudflare
**Status:** Adopted. The site is a static Astro build deployed to Netlify, with DNS managed in
Cloudflare. Production domain `greenwayband.com` stays on Squarespace until launch (flip the
Cloudflare A record). **Why:** fast, cheap, low-maintenance static hosting; reversible launch.

## D-002 — Fontsource over Google Fonts CDN
**Status:** Adopted (commits `6697c98`, `f5050a2`). Fonts load via `@fontsource-variable/bodoni-moda`
and `@fontsource/plus-jakarta-sans` instead of the Google Fonts CDN. **Why:** self-hosted fonts
remove a third-party request, improve performance/privacy, and avoid CDN dependency.

## D-003 — No hairline rules in browser-rendered logos
**Status:** Adopted. Header, footer, and hero logos are text-based; the inline-SVG `Logo` (404)
uses text elements only — no `<line>`/`<rect>` hairlines. **Why:** hairlines render inconsistently
across browsers/zoom and cheapen the wordmark.

## D-004 — Copy integrity: real content or explicit placeholders only
**Status:** Adopted (hard rule). Never fabricate venues, testimonials, or stats; use real content
or an explicit `<!-- PLACEHOLDER -->`. **Why:** an earlier build shipped fabricated venues; this
guardrail prevents recurrence. Only the 13 approved venues may be used (see
docs/CONTENT_AND_MESSAGING.md).

## D-005 — Six-page site set
**Status:** Adopted (intent). Home, Experience (replaces About), Vocalist Showcase, Reviews, FAQ,
Book. **Why:** covers storytelling + social proof + conversion for a premium band. Status as of
2026-06-27: Vocalist Showcase not built; Reviews placeholder; FAQ shipped as a static accordion.

## D-006 — Separate-projects boundary
**Status:** Adopted (hard rule). The website stays isolated from the Command Center CRM
(`greenway-crm`) and the personal app "Kai". No Supabase/Stripe/Twilio code in this repo; the only
backend touchpoint is the Book form → CRM `lead-intake`. **Why:** clean separation of concerns and
security surface; the site is a static storefront.

## D-007 — "Week 12R" rebuild to the locked design system
**Status:** Adopted (commits `dd3e408`, `3caf99f`, `46f1bef`). The design system, layout, homepage,
and Book page were rebuilt to the locked token spec. **Why:** establish a single, compliant baseline.

## D-008 — FAQ shipped as a static accordion (AI assistant deferred)
**Status:** De facto (commit `e17d5a6`, on `main`). The planned "AI assistant shell" for the FAQ
was not built; the FAQ ships as a static 12-question accordion. **Why:** unknown from the repo —
likely scope/time. Revisit whether the AI assistant is still desired (see docs/TASKS.md).

---
## Open decisions (not yet made — see docs/TASKS.md)
- **Reconcile `dev` vs `main`** and decide the canonical deploy branch.
- **The staging self-redirect to Squarespace** — keep, or remove until launch so the new build is
  previewable at the staging URL.
- Whether to **wire the `published` flag** to nav + a 404 guard, or keep it as metadata.
- Whether to commit/publish the **uncommitted April work** (Reviews + FAQ on `dev`).
