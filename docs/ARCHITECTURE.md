# ARCHITECTURE

**Last verified: 2026-06-27.**

## Overview
A static Astro site. No runtime server, no database, no auth. Pages are `.astro` files compiled
to static HTML at build time; a little vanilla `<script>` adds interactivity (scroll reveal,
mobile menu, FAQ accordion, Book form submit). Styling is one global stylesheet plus colocated
per-page `<style is:global>` blocks.

## Rendering & build
- `astro.config.mjs`: `output: 'static'`, `site: 'https://greenway-website.netlify.app'`,
  `build.inlineStylesheets: 'auto'`, `vite.build.cssMinify: true`.
- `npm run build` → `./dist/` (static HTML/CSS/JS). Netlify publishes `dist`.

## Directory structure
```
src/
  config/site.ts            # siteConfig + pages[] metadata (see "Config" below)
  layouts/BaseLayout.astro  # the one layout: <head>, fonts, Header, <slot/>, Footer, reveal observer
  components/               # presentational .astro components (no framework runtime)
  pages/                    # file-based routes
  styles/global.css         # design tokens (:root) + shared/component CSS
public/                     # static passthrough (images, favicons, robots.txt, proposals/)
```

## Layout & composition
- Every page wraps content in `BaseLayout` with `title`, `description`, optional `darkHero`,
  `noIndex`, `ogImage` props.
- `BaseLayout` imports `global.css` and the Fontsource font CSS, renders `Header` + `Footer`,
  and registers the scroll-reveal IntersectionObserver.
- The homepage composes `VideoHero`, `SocialProofStrip`, `WhyGreenway`, `HomeCTA`.

## Config (`src/config/site.ts`)
Exports two things:
- `siteConfig` — `{ name, descriptor, url, email, phone, location, ogImage }`. **Consumed** by
  `BaseLayout.astro` (titles, canonical/OG URLs) and `Footer.astro` (copyright).
- `pages[]` — an array of `{ title, slug, published, description }`. **Not consumed by any code.**
  It is currently documentation/metadata only.

### Important: the "published" flag is not wired
- The header/mobile nav is a **hardcoded `navLinks` array inside `Header.astro`**, independent of
  `pages[]`.
- Nothing reads `published` to hide nav links or to force a 404. A page is reachable iff a file
  exists in `src/pages/`. `/vocalists` 404s simply because there is no `vocalists.astro`.
- Consequence: to truly publish/unpublish a page you must edit `Header.astro` (nav) and add/remove
  the page file — not just toggle `site.ts`. (A future improvement could drive nav + a 404 guard
  from `pages[]`; see docs/TASKS.md.)

## Client-side behavior (no framework)
- **Scroll reveal:** IntersectionObserver in `BaseLayout.astro` adds `.visible` to `[data-reveal]`.
- **Header:** scroll listener toggles `header--scrolled`; hamburger toggles the mobile menu.
- **FAQ:** accordion toggle script (single-open) in `faq.astro`.
- **Book form:** validation + honeypot + `fetch` POST in `BookForm.astro` (see docs/INTEGRATIONS.md).

## Assets
- `public/images/experience/` holds the 3 real `.webp` photos used by the Experience page.
- `public/proposals/` holds per-client static proposal microsites (e.g. `ally-byrne`). These are
  tangential to the marketing site and are deployed as static passthrough if present in the build.

## What this site deliberately is NOT
- No Supabase / Stripe / Twilio / auth / CMS in this repo.
- The only outbound integration is the Book form → CRM `lead-intake` endpoint.
