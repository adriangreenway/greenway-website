# CLAUDE.md — Operating Manual for The Greenway Band Website

> Concise operating manual for anyone (human or AI) working on this repo.
> Deeper detail lives in [`/docs`](docs/). Update these docs after any meaningful change.
> **Last verified against code: 2026-06-27.**

## 1. Identity & goals
**The Greenway Band** — a premium Houston live wedding/event band. The website is the
band's public storefront. The visual standard is Fortune 500 ("$400M, not $4M"); north
stars are Apple, Aman, Aesop. Sole client contact is **Adrian** (adrian@greenwayband.com).

**Goal of the site:** convert high-end couples and wedding planners into booking inquiries.
The single conversion action is the **Book** form (an inquiry, framed as "Check availability").

**Audiences:** (1) engaged couples planning a premium wedding; (2) wedding planners /
venues who refer the band.

## 2. Stack & the REAL commands
- **Framework:** [Astro](https://astro.build) `^6.0.4`, **static** output (`output: 'static'`).
- **Hosting:** Netlify (site id `57df0a8e-c32d-4954-9507-f9f3b1f90e53`). **DNS:** Cloudflare.
- **Fonts:** Fontsource npm packages (NOT Google Fonts CDN) — Bodoni Moda (display) + Plus Jakarta Sans (body).
- **Node:** `>=22.12.0` (from `package.json` engines). **Package manager:** npm (`package-lock.json`).
- **Repo:** `github.com/adriangreenway/greenway-website`.

Commands (the only scripts that exist in `package.json`):
```sh
npm install        # install dependencies
npm run dev        # local dev server (Astro default http://localhost:4321)
npm run build      # production build → ./dist/
npm run preview    # serve the built ./dist/ locally
npm run astro ...   # Astro CLI (e.g. `npm run astro -- --help`)
```
There is **no** `test` script and **no** configured `astro check` (the `@astrojs/check`
package is not installed). See [docs/CODE_WORKFLOW.md](docs/CODE_WORKFLOW.md).

## 3. Folder map
```
src/
  config/site.ts        # siteConfig (name, contact, url) + pages[] metadata
  layouts/BaseLayout.astro   # <head>, font imports, Header/Footer, scroll-reveal observer
  components/
    Header.astro        # fixed header; nav is a HARDCODED navLinks array (not from site.ts)
    Footer.astro        # dark footer, stacked text logo, 13-venue strip
    VideoHero.astro     # homepage hero (text wordmark; video is a placeholder)
    SocialProofStrip.astro  # 13-venue list
    WhyGreenway.astro, HomeCTA.astro   # homepage sections
    BookForm.astro      # the inquiry form + client validation + POST to lead-intake
    Logo.astro          # inline-SVG wordmark (used on 404 only)
    LogoInline.astro, LogoMonument.astro   # UNUSED (dead components)
  pages/
    index.astro, experience.astro, reviews.astro, faq.astro, book.astro, 404.astro
  styles/global.css     # ALL design tokens + most component CSS
public/
  images/experience/    # 3 real .webp photos used on the Experience page
  proposals/            # per-client proposal microsites (untracked on dev; tangential)
  favicon.*, robots.txt
netlify.toml            # build cmd, security headers, netlify.app→greenwayband.com redirect
astro.config.mjs
```

## 4. Conventions
- **Read before write.** Read and understand a file before editing it. No drive-by refactors.
- Design tokens live in `src/styles/global.css` `:root`. Use the CSS variables; never hardcode hex.
- Page-specific CSS is colocated in each page's `<style is:global>` block.
- Nav links are hardcoded in `Header.astro`. The `pages[]`/`published` array in `site.ts`
  is currently **metadata only — nothing consumes it** (see docs/ARCHITECTURE.md).
- Scroll reveal: add `data-reveal` (and optional `data-reveal-delay="N"` for N×100ms stagger).

## 5. Design tokens (locked)
Full set in [docs/DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md). Summary:
- **Colors:** `--color-black #0A0A09`, `--color-charcoal #111110`, `--color-cream #F5F2ED`,
  `--color-muted #B8B4AC`, `--color-dim #706D66`, `--color-faint #4A4740`.
  **Never pure white. No gold, no metallic, no teal** (teal = sister brand only).
- **Fonts:** Bodoni Moda (display 400/500/600), Plus Jakarta Sans (body 300/400/500/600).
- **Buttons:** filled, sharp corners (`border-radius: 0`), 11px uppercase Plus Jakarta Sans 600, padding `14px 32px`.
- **Form inputs:** underline style (bottom border only).
- Max width 1200px; section padding 120/80px; default transition 200ms ease-out; hero overlay 55% dark.

## 6. Copy integrity (NON-NEGOTIABLE)
**Never fabricate** venue names, testimonials, statistics, or anything implying real
experience. Real content only, or an explicit HTML placeholder comment
(`<!-- PLACEHOLDER: ... -->`). This rule exists because an earlier build shipped fabricated
venues. The **13 approved real venues** (see docs/CONTENT_AND_MESSAGING.md):
River Oaks Country Club, Houston Country Club, Post Oak Hotel, The Astorian, The Houstonian,
The Grand Galvez, Iron Manor, Ashton Gardens, Lakeside Country Club, The Junior League,
The Houston Grand Hotel, Windemere Farms, La Colombe d'Or.

## 7. Separate-projects boundary (DO NOT MERGE OR IMPORT)
This website is **only** the public marketing site. Keep it isolated from:
- **Command Center** — CRM (`greenway-crm`, command.greenwayband.com).
- **Kai** — a personal app.

The website contains **no** Supabase, Stripe, or Twilio code. Its **only** backend touchpoint
is the Book form, which POSTs JSON to `https://command.greenwayband.com/.netlify/functions/lead-intake`.
Shared only: a Supabase database (used by the CRM, not the site) and the Cloudflare DNS zone.

## 8. Current priorities
See [docs/TASKS.md](docs/TASKS.md). Top of mind as of 2026-06-27:
1. Decide what to do with the **uncommitted "April work"** on `dev` (publishing Reviews + FAQ).
2. Resolve the `dev` vs `main` branch split and the **netlify.app → greenwayband.com self-redirect**
   that currently makes the staging URL bounce to the old Squarespace site.
3. Real content: written reviews (Reviews page is placeholder), hero video, "For Planners" detail.
4. Build the unbuilt features: **Vocalist Showcase** page and the **FAQ AI assistant** (never built).

## 9. Definition of done
A change is done when: it builds clean (`npm run build`), respects the design tokens and
copy-integrity rule, introduces no fabricated content, keeps the separate-projects boundary,
and **the relevant docs in `/docs` are updated**.

## 10. Deeper docs
[docs/PROJECT_STATE.md](docs/PROJECT_STATE.md) ·
[docs/PRODUCT_SPEC.md](docs/PRODUCT_SPEC.md) ·
[docs/SITE_MAP.md](docs/SITE_MAP.md) ·
[docs/CONTENT_AND_MESSAGING.md](docs/CONTENT_AND_MESSAGING.md) ·
[docs/DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md) ·
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) ·
[docs/INTEGRATIONS.md](docs/INTEGRATIONS.md) ·
[docs/DECISIONS.md](docs/DECISIONS.md) ·
[docs/TASKS.md](docs/TASKS.md) ·
[docs/CHANGELOG.md](docs/CHANGELOG.md) ·
[docs/CODE_WORKFLOW.md](docs/CODE_WORKFLOW.md) ·
[docs/HANDOFF.md](docs/HANDOFF.md) *(living bridge — read this to resume a session)* ·
[docs/LEGACY_PROJECT_RECOVERY.md](docs/LEGACY_PROJECT_RECOVERY.md) *(historical reference only)*

## 11. Governing standard (the Relay Method, Code-native)
The engineering spine in §4 derives from Adrian's **Relay Method**. Two canonical, **do-not-modify**
reference docs now live in `/docs`:
- [docs/Zero_Compromise_Code_Protocol.md](docs/Zero_Compromise_Code_Protocol.md) — the code-quality
  standard (read-before-write, do-not-modify fence, build gate, per-phase commits, regression prevention).
- [docs/Claude_Build_Workflow.md](docs/Claude_Build_Workflow.md) — the PLAN→PREP→BUILD→DEBRIEF→CLOSE lifecycle.

These were written for a **two-tool era** (Claude Chat plans, Claude Code builds). Adrian now works
**exclusively in Claude Code**. The *principles* still govern every change; the two-tool *mechanics*
(Project-Knowledge file swaps, DO-THIS-NOW / CLEANUP cards for PK, paste-in bridge prompts) are
superseded by this repo + agent memory — plan in-tool, build in-tool. See
[docs/CODE_WORKFLOW.md](docs/CODE_WORKFLOW.md). Build-decision capture tool:
[docs/Greenway_Website_Build_Bible_v2.html](docs/Greenway_Website_Build_Bible_v2.html).
