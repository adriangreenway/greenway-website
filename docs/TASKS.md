# TASKS

> **Superseded 2026-07-03 by [docs/ROADMAP.md](ROADMAP.md)**, which carries this same list forward
> in the Foreman workflow's format (with statuses) and adds the 2026-07-03 cross-project pause
> note. Kept here for its original evidence trail; update ROADMAP.md going forward, not this file.

Derived from the 2026-06-27 reconciliation (see docs/PROJECT_STATE.md). Owner: Adrian.
Status legend: **Now** (do next) · **Next** · **Later** · **Blocked**.

## Now
1. **Reconcile `dev` vs `main` and the uncommitted April work.**
   - `dev` (deployed) lacks committed Reviews/FAQ; `main` has them committed + published but isn't
     deployed; the working tree of `dev` has them as **uncommitted** files + nav/publish edits.
   - Decide: merge `main`'s Reviews/FAQ into the deploy branch, or commit the working-tree April
     work. Then push. *(Owner approval required to commit/push.)*
2. **Decide the staging self-redirect.** `netlify.toml` 301s `greenway-website.netlify.app/*` →
   `greenwayband.com` (Squarespace). This makes the new site **unviewable at the staging URL**.
   Either remove the redirect until launch (so staging shows the new build) or rely on Netlify
   deploy-preview URLs. *(Owner approval required.)*
3. **Confirm the Netlify deploy branch** in the Netlify dashboard (inferred to be `dev`).

## Next
4. **Reviews content:** replace the 3 "Review coming soon" placeholders with real, attributed
   testimonials (real content only — copy-integrity rule).
5. **Hero media:** add the real hero video or poster image (currently a solid placeholder); fill
   the `WhyGreenway` media placeholder.
6. **Experience "For Planners":** expand the placeholder production paragraph with real detail.
7. **Vocalist Showcase page:** build `src/pages/vocalists.astro` (currently missing) when content
   is ready; add to nav.

## Later
8. **FAQ AI assistant:** decide whether to build the planned UI-only AI assistant shell, or keep
   the static accordion as the final v1.
9. **Wire the `published` flag (optional refactor):** drive the header nav from `site.ts pages[]`
   and add a 404 guard for unpublished routes, so publishing is a one-line toggle. *(Currently the
   flag is dead metadata and nav is hardcoded.)*
10. **Minor cleanups:** remove dead `LogoInline.astro` / `LogoMonument.astro`; drop the overridden
    boxed `.book-form__input` rule in `global.css`; replace `#ffffff` button-hover states and the
    `#8a867e` logo gray with palette tokens.
11. **Launch:** flip the Cloudflare `greenwayband.com` A record from Squarespace to Netlify
    (reversible). Coordinate with removing/adjusting the staging redirect.

## Blocked
- **Real content items (4–6)** are blocked on Adrian providing testimonials, video, and planner copy.
- **Commit/push/deploy/DNS actions** are blocked on explicit owner approval (hard-stop rules).

## Notes
- The "WEB-07" brand-compliance audit referenced in the brief has **no artifact in this repo**
  (see docs/PROJECT_STATE.md). Nothing to resolve in-code; if a checklist exists it's external.
- External historical Greenway docs exist outside this repo (e.g. in Dropbox/Desktop). They were
  **not** imported here. If you want them archived in-repo, copy them into `docs/archive/`.
