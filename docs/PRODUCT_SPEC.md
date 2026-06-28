# PRODUCT_SPEC

**Last verified: 2026-06-27.** Sourced from the project brief + verified code.

## Product
The public marketing website for **The Greenway Band**, a premium Houston live wedding/event
band. The site's job is to make the band feel unmistakably high-end (Fortune 500 standard;
north stars Apple / Aman / Aesop) and to convert qualified couples and planners into inquiries.

## Primary user goal & conversion
- **Single conversion action:** submit the **Book** inquiry form (presented as "Check availability
  for your date").
- The form posts to the CRM's `lead-intake` endpoint; the band follows up directly.

## Audiences
1. **Engaged couples** planning a premium wedding (primary).
2. **Wedding planners / venues** who book or refer entertainment (secondary; the Experience page
   has a "For Planners" production section aimed at them).

## Page set (6 intended)
Each page has a published/unpublished intent recorded in `src/config/site.ts`.
(Implementation note: that flag is currently metadata only — see docs/ARCHITECTURE.md.)

1. **Home** — published. Hero + social proof + value prop + CTA.
2. **Experience** — published. Replaces a traditional "About"; walks the arc of a night
   (cocktail hour → dinner → dance floor) and ends with planner-facing production detail.
3. **Vocalist Showcase** — intended unpublished shell; **not yet built** (no page file).
4. **Reviews** — published; **placeholder content** (written reviews are the v1 plan; video slots
   were planned as placeholders).
5. **FAQ** — published. Planned to host an AI assistant shell; **shipped as a static accordion**.
6. **Book** — published. Inquiry form → `lead-intake`.

## Functional requirements (verified in code)
- **Responsive** across breakpoints 375 / 768 / 1024 / 1440.
- **Scroll-reveal** animation (fade-up) via an IntersectionObserver in `BaseLayout.astro`;
  opt-in per element with `data-reveal` / `data-reveal-delay`.
- **Mobile nav** (hamburger → full-screen menu) in `Header.astro`.
- **Book form**: client-side validation (required: name, email, event date), honeypot spam
  trap (`_gotcha`), graceful success/error states, JSON POST to the CRM endpoint.
- **SEO basics**: per-page `<title>`/description, canonical URL, Open Graph tags, `noindex`
  support (used on 404). `robots.txt` present.
- **Security headers** via `netlify.toml` (`X-Frame-Options: DENY`, `X-Content-Type-Options:
  nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`).

## Non-goals / out of scope
- No CMS, no auth, no e-commerce, no booking calendar on the site itself.
- No Supabase/Stripe/Twilio code in this repo (those belong to the separate CRM).
- This is a **recovery + documentation** baseline; not a redesign. Do not add features or change
  the design without owner direction.

## Open product decisions
- Whether to publish Reviews/FAQ on the deploy branch (the April work that's uncommitted on `dev`).
- Whether the FAQ AI assistant is still wanted, or the static accordion is the final v1.
- Launch timing: flipping `greenwayband.com` from Squarespace to Netlify.
