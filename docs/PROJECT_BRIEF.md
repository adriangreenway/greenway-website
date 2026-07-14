# PROJECT BRIEF: The Greenway Band Website

Stable facts only. If something changes weekly, it belongs in CURRENT_STATE.md, not here.
Claude Code: read this when a task touches product, design, content, or architecture.

## Product
- **What it is:** the public marketing website for The Greenway Band, a premium Houston live wedding/event band. It is the band's public storefront, not a CRM or booking system.
- **Who uses it:** (1) engaged couples planning a premium wedding (primary audience), (2) wedding planners and venues who book or refer entertainment (secondary; the Experience page has a "For Planners" section aimed at them).
- **Visual standard:** Fortune 500 ("$400M, not $4M"). North stars: Apple, Aman, Aesop.
- **Sole client contact:** Adrian (adrian@greenwayband.com).
- **Single conversion action:** submitting the Book inquiry form, framed as "Check availability for your date." The form posts to a CRM lead-intake endpoint; Adrian follows up directly.

## Brand voice & identity
- **Name:** The Greenway Band. **Descriptor:** "The sound of a great night."
- **Tone:** confident, concrete, understated. Short declarative sentences. Specific over salesy. No hype, no exclamation points, no clichés.
- **Positioning:** a premium 10-20 piece Houston live band (horn section, vocalists, music director arranging for live performance) for high-end weddings and events; Adrian also handles emcee duties and planner coordination.

## Copy integrity (non-negotiable)
Never fabricate venue names, testimonials, statistics, or anything implying real experience the band hasn't had. Real content only, or an explicit `<!-- PLACEHOLDER: ... -->`. This exists because an earlier build shipped fabricated venues.

**The 13 approved real venues** (the only ones allowed as social proof, used in `SocialProofStrip.astro` and `Footer.astro`): River Oaks Country Club, Houston Country Club, Post Oak Hotel, The Astorian, The Houstonian, The Grand Galvez, Iron Manor, Ashton Gardens, Lakeside Country Club, The Junior League, The Houston Grand Hotel, Windemere Farms, La Colombe d'Or. Do not add, rename, or invent venues; changes require Adrian's approval. Full detail and current content gaps: `docs/CONTENT_AND_MESSAGING.md`.

## Page set (6 intended)
1. **Home** — hero, 13-venue social proof strip, "Why Greenway," CTA. Built.
2. **Experience** — replaces a traditional "About"; walks cocktail hour → dinner → dance floor, ends with a "For Planners" production section (currently a placeholder paragraph). Built, real photos.
3. **Vocalist Showcase** — intended, unpublished. Not built; no page file exists.
4. **Reviews** — three "Review coming soon" placeholders, no real testimonials yet. Committed on `main` only; uncommitted on `dev`'s working tree.
5. **FAQ** — a static 12-question accordion. An AI assistant shell was planned but never built. Same commit status as Reviews.
6. **Book** — the inquiry form, wired to the CRM endpoint. Built.

## Tech stack
| Layer | Technology |
|---|---|
| Framework | Astro `^6.0.4`, static output (`output: 'static'`), no server/database/auth |
| Hosting | Netlify (site id `57df0a8e-c32d-4954-9507-f9f3b1f90e53`) |
| DNS | Cloudflare |
| Fonts | Fontsource npm packages (not Google Fonts CDN): `@fontsource-variable/bodoni-moda` (display), `@fontsource/plus-jakarta-sans` (body) |
| Node | `>=22.12.0` (package.json engines) |
| Package manager | npm (`package-lock.json`) |
| Repo | `github.com/adriangreenway/greenway-website` |

**The only scripts that exist** (`package.json`): `npm install`, `npm run dev` (localhost:4321), `npm run build` (→ `./dist/`), `npm run preview`, `npm run astro -- ...`. There is no test script and no configured `astro check`.

## Folder map
```
src/
  config/site.ts             # siteConfig (name, contact, url) + pages[] metadata (pages[] is not wired to anything — see ARCHITECTURE.md)
  layouts/BaseLayout.astro    # <head>, font imports, Header/Footer, scroll-reveal observer
  components/
    Header.astro              # fixed header; nav is a HARDCODED navLinks array, not from site.ts
    Footer.astro               # dark footer, stacked text logo, 13-venue strip
    VideoHero.astro             # homepage hero (text wordmark; video is a placeholder)
    SocialProofStrip.astro       # 13-venue list
    WhyGreenway.astro, HomeCTA.astro  # homepage sections
    BookForm.astro                # the inquiry form + client validation + POST to lead-intake
    Logo.astro                     # inline-SVG wordmark (used on 404 only)
    LogoInline.astro, LogoMonument.astro  # UNUSED (dead components)
  pages/
    index.astro, experience.astro, reviews.astro, faq.astro, book.astro, 404.astro
  styles/global.css          # ALL design tokens + most component CSS
public/
  images/experience/         # 3 real .webp photos used on the Experience page
  proposals/                  # per-client static proposal microsites (tangential to the marketing site)
  favicon.*, robots.txt
netlify.toml                  # build cmd, security headers, netlify.app→greenwayband.com redirect
astro.config.mjs
```

## Design direction (locked tokens)
Full set in `docs/DESIGN_SYSTEM.md`. Summary:
- **Colors:** `--color-black #0A0A09`, `--color-charcoal #111110`, `--color-cream #F5F2ED`, `--color-muted #B8B4AC`, `--color-dim #706D66`, `--color-faint #4A4740`. Never pure white. No gold, no metallic, no teal (teal is the sister brand's).
- **Fonts:** Bodoni Moda (display, 400/500/600), Plus Jakarta Sans (body, 300/400/500/600).
- **Buttons:** filled, sharp corners (`border-radius: 0`), 11px uppercase Plus Jakarta Sans 600, padding `14px 32px`.
- **Form inputs:** underline style (bottom border only), no boxes.
- Max width 1200px; section padding 80px mobile / 120px desktop; default transition 200ms ease-out; hero overlay 55% dark; breakpoints 375/768/1024/1440.

## Environments
- **Repo:** `github.com/adriangreenway/greenway-website`. Branches: `dev` (deployed — strong inference), `main` (has Reviews/FAQ committed, not deployed), `docs/build-context` (documentation only).
- **Local path:** `~/greenway-website`
- **Production URL:** `greenwayband.com` — still Squarespace today, not this site.
- **Staging URL:** `greenway-website.netlify.app` — currently self-redirects to `greenwayband.com` (see Known issues in `docs/CURRENT_STATE.md`), so it doesn't show the new build. Use `npm run dev` or a Netlify deploy-preview link instead.
- **How to run:** `npm install && npm run dev`. No secrets or setup steps needed; this repo has no environment variables.
- **Credentials:** none used in this repo today (verified: no `import.meta.env` / `process.env` / `PUBLIC_` anywhere in `src/`).

## Business constraints
- Real content only. No fabricated venues, testimonials, or stats, ever (see Copy integrity above).
- Keep this repo isolated from the other Greenway projects: the Command Center CRM (`greenway-crm`, command.greenwayband.com) and the personal app "Kai." No Supabase, Stripe, or Twilio code here.
- The only backend touchpoint is `BookForm.astro`'s POST to `https://command.greenwayband.com/.netlify/functions/lead-intake`. Field mapping and spam-trap detail: `docs/INTEGRATIONS.md`.
- Launching (flipping the Cloudflare A record for `greenwayband.com` from Squarespace to Netlify) is owner-approved only and, per the 2026-07-03 cross-project decision, not imminent — see CLAUDE.md "Current milestone."

## Non-negotiables
- No fabricated content, ever (see Copy integrity).
- No hardcoded hex colors; use the design tokens in `src/styles/global.css`.
- No Supabase/Stripe/Twilio/CRM code in this repo.
- No commit, push, deploy, or DNS change without Adrian's explicit approval.
