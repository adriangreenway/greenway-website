# LEGACY_PROJECT_RECOVERY — historical reference only

> **HISTORICAL REFERENCE ONLY.** This file preserves the project "brain" carried into the
> 2026-06-27 recovery pass, because the original planning environment could not be read. It is
> **not** authoritative about current code. For verified current state, always use
> [PROJECT_STATE.md](PROJECT_STATE.md) and the code itself. No pre-existing
> `LEGACY_PROJECT_RECOVERY.md` was found in the repo or `~/Downloads`; this was authored from the
> recovery brief.

## Identity
The Greenway Band — a premium Houston live wedding/event band. Sole client contact: Adrian.
Visual standard Fortune 500 ("$400M, not $4M"); north stars Apple / Aman / Aesop.

## Stack (as briefed)
Astro static site on Netlify, DNS on Cloudflare. Repo `adriangreenway/greenway-website`.
Staging `greenway-website.netlify.app`. Production target `greenwayband.com` (Squarespace until
launch; launch = flip the Cloudflare A record to Netlify, reversible). Fonts via Fontsource (not
Google Fonts).

## Separate projects (do not merge/import)
- **Command Center** CRM (`greenway-crm`, command.greenwayband.com).
- **Kai** — a personal app.
Shared only: a Supabase database and the Cloudflare DNS zone. The website has no Supabase/Stripe/
Twilio code; its only backend touchpoint is the Book form → `lead-intake`.

## Pages as briefed (6, each with a published/unpublished flag)
1. Homepage — published.
2. Experience — published (replaces "About"; planner production detail near the bottom).
3. Vocalist Showcase — unpublished shell (content pending).
4. Reviews — published (written reviews v1; video slots placeholders).
5. FAQ — published (was to host the AI assistant shell).
6. Book — published (inquiry form → lead-intake).

> Reconciliation note (2026-06-27): the flag mechanism was never wired in code; FAQ shipped as a
> static accordion (no AI shell); Reviews shipped as placeholders; Vocalist Showcase was never
> built. See PROJECT_STATE.md.

## Design tokens (locked, as briefed)
- Colors: black `#0A0A09`, charcoal `#111110`, cream `#F5F2ED`, muted `#B8B4AC`, dim `#706D66`,
  faint `#4A4740`. Never pure white. No gold/metallic/teal (teal = sister brand).
- Fonts: Bodoni Moda (display 400/500/600), Plus Jakarta Sans (body 300/400/500/600).
- Type scale (desktop/mobile): hero 64/44; section headline 36/28; inner headline 40/32; body 16;
  nav 12; button 11; descriptor 14/13; footer 12.
- Spacing: max width 1200px; section padding 120/80; component gap 48; body line-height 1.7;
  headline 1.2. Breakpoints 375/768/1024/1440.
- Animation: 200ms ease-out; scroll reveal fade-up 600ms, 80px threshold, 100ms stagger; no parallax.
- Components: filled sharp-corner buttons (11px uppercase Jakarta 600, 14px 32px); underline form
  inputs; dark footer with stacked Monument logo; hero overlay 55% dark; editorial reviews layout.
- Logo: inline-SVG wordmark, no browser hairlines. Descriptor: "The sound of a great night."

## Copy integrity (non-negotiable)
Never fabricate venues/testimonials/stats. Real content or explicit HTML placeholder. The rule
exists because an earlier build shipped fabricated venues. The 13 approved venues: River Oaks
Country Club, Houston Country Club, Post Oak Hotel, The Astorian, The Houstonian, The Grand Galvez,
Iron Manor, Ashton Gardens, Lakeside Country Club, The Junior League, The Houston Grand Hotel,
Windemere Farms, La Colombe d'Or.

## Book form mapping (as briefed — matches code)
`partner1_name`*, `partner2_name`, `event_date`* (YYYY-MM-DD), `venue`, `email`*, `phone`,
`guest_count` (range), `referral_source`, hidden `_gotcha` (must be empty). POST to
`https://command.greenwayband.com/.netlify/functions/lead-intake`. (* required)

## DNS facts (read-only; do not change)
Cloudflare zone `bcd1a65100066b5e6f2190afc77fd8e9`, account `fe59812014feb92ff5a43ea304b16e58`,
nameservers carter/coraline. A records → Squarespace; `command` CNAME → CRM Netlify site; MX →
Google Workspace.

## Recorded build state (frozen ~2026-03-16, possibly stale as briefed)
"Week 12R" completed — design system, header, footer, homepage, Book page rebuilt to spec, passing
39 acceptance criteria, Fontsource fonts, zero fabricated copy, deployed to staging. Next planned
("Week 13"): Experience, Reviews, FAQ pages + a UI-only AI assistant shell.

## The WEB-07 hint (as briefed)
The brief suspected the site reached ~5 deployed pages and that a brand-compliance audit "WEB-07"
was queued ~April and paused further page rebuilds.

> Reconciliation verdict (2026-06-27): **no WEB-07 artifact exists in the repo or git history.**
> The "~5 pages" best matches the `main` branch (5 published pages), which is not the deployed
> branch. Further pages stalled because the Reviews/FAQ publish work was left uncommitted on `dev`.
> See PROJECT_STATE.md for the evidence.
