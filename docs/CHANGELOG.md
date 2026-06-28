# CHANGELOG

Derived from git history of `github.com/adriangreenway/greenway-website` (2026-06-27). Dates are
commit dates. `dev` and `main` diverged after the Experience page commit.

## Unreleased — uncommitted working tree on `dev` (April 2026, not pushed)
- Publish **Reviews** and **FAQ** (`site.ts` flags → true; added to `Header` nav).
- Bring `reviews.astro` + `faq.astro` onto `dev` (byte-identical to `main`'s versions).
- *(Not committed; therefore not deployed.)*

## `main` branch (diverged line, latest 2026-03-27)
- `e17d5a6` Add FAQ page with 12 pre-written answers and accordion
- `8000c01` Add Reviews page with placeholder structure
- `eaae9c8` Update proposal: add Location field to Hope Bostrom details grid
- `2f55682` Add proposal: August 29 Dallas Arboretum (Hope Bostrom)
- `204b8a1` Add proposal: December 12 Meekermark (Ashley Eastin)
- `b162e74` Trigger Netlify rebuild for experience page

## Shared history (both branches)
- `98d5569` Add Experience page with phase sections and real copy *(divergence point)*
- `f5050a2` Fix: Bodoni Moda variable font with optical sizing
- `6697c98` Fix: Replace Google Fonts with Fontsource local packages
- `46f1bef` Week 12R Phase 3: Book page + full site QA
- `3caf99f` Week 12R Phase 2: Homepage sections
- `dd3e408` Week 12R Phase 1: Design system + global layout
- `f5d42d4` Week 12 Phase 5: 404 page, QA fixes, production deploy
- `7a755a2` Week 12 Phase 4: Book page with inquiry form
- `fa6bacd` Week 12 Phase 3: Homepage — hero, social proof, why greenway, CTA
- `96ea88e` Week 12 Phase 2: BaseLayout, Header, Footer, Logo components
- `d15dc70` Week 12 Phase 1: Astro scaffold, design tokens, site config, Netlify
- `07ae1cb` Initial Astro scaffold

## `dev` branch tip (latest 2026-04-13)
- `4198c83` Redirect netlify.app subdomain to production domain *(adds the staging→greenwayband.com 301)*

## 2026-06-27 — Recovery & documentation pass (this change set)
- Added `CLAUDE.md`, `README.md` (replaced Astro starter boilerplate), and `docs/` (this set).
- Hardened `.gitignore` to exclude all `.env*`.
- No application/source code changed; no commits, pushes, or deploys performed.
