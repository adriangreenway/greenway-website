# CODE_WORKFLOW

How to work in this repo. Code-first model — no mandatory chat planning, no forced ceremony.
Keep the engineering spine below.

## Engineering spine (always)
1. **Read before write.** Read and understand any file before editing it. No drive-by refactors,
   renames, or reorganizing of working code.
2. **Small, scoped changes.** One concern at a time.
3. **No fabricated content.** Real copy or an explicit `<!-- PLACEHOLDER -->` (copy-integrity rule).
4. **Respect the design tokens** in `src/styles/global.css`; don't hardcode colors/sizes.
5. **Hold the boundary.** No Supabase/Stripe/Twilio/CRM code here; the only backend touchpoint is
   the Book form → `lead-intake`.
6. **Update the docs** in `/docs` after any meaningful change (definition of done).

## The real commands
```sh
npm install        # deps (Node >=22.12.0, npm)
npm run dev        # local dev (Astro, default http://localhost:4321)
npm run build      # static build → ./dist/
npm run preview    # serve ./dist/ locally
npm run astro -- --help
```
- **No test script** exists. "Verification" = `npm run build` succeeds + manual check in `dev`.
- **`astro check`** is not configured (`@astrojs/check` isn't installed). If you want type
  checking, install it first (`npm i -D @astrojs/check typescript`) — owner approval to add deps.

## Typical change loop
1. `npm run dev`, open the page you're changing.
2. Edit the page (`src/pages/*.astro`) or component (`src/components/*.astro`). Page-specific CSS
   lives in that file's `<style is:global>`; global tokens/shared CSS live in `global.css`.
3. For animation, add `data-reveal` (+ optional `data-reveal-delay="N"`).
4. `npm run build` to confirm it compiles clean.
5. Update the relevant `/docs` file(s).

## Adding or publishing a page (important)
Because the `published` flag in `site.ts` is **not wired to anything** (see docs/ARCHITECTURE.md),
publishing a page is a two-step manual change:
1. Create/keep the page file in `src/pages/`.
2. Add its link to the **hardcoded `navLinks` array in `Header.astro`** (and update `site.ts` for
   documentation consistency).
To unpublish, remove it from `navLinks` and remove/guard the page file.

## Branches & git
- Branches: `dev` (deployed — strong inference) and `main` (has committed Reviews/FAQ; not deployed).
  They have **diverged**; reconcile before relying on either (see docs/ROADMAP.md).
- The working tree currently carries **uncommitted April work** on `dev` — don't blow it away;
  decide what to do with it first.
- **Updated 2026-07-03:** the authoritative git-safety rules now live in `CLAUDE.md` (Foreman
  workflow, matching `~/greenway-growth-hour`). Summary: commits are a normal part of finishing a
  stage and don't each need a separate yes; **`git push`, deploys, Cloudflare DNS changes, force
  push, history rewrites, and branch deletion still require Adrian's explicit approval.** Don't
  modify the live site beyond read-only checks.

## Deploy (context, not a self-serve action)
- Netlify builds `npm run build` and publishes `dist`. Deploy branch ≈ `dev` (confirm in UI).
- Launch = flip the Cloudflare A record for `greenwayband.com` to Netlify (reversible). Owner only.
