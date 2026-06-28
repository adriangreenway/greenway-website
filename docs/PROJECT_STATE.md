# PROJECT_STATE — Verified Snapshot

**Last verified against code: 2026-06-27** (by reconciliation pass over the canonical repo).
This file records what is *actually* true in the code and git history, with evidence. Where a
fact could not be verified, it is marked **UNKNOWN / to verify**.

## Canonical repo
- **Path:** `/Users/adrianjoseph/greenway-website`
- **Remote:** `origin → https://github.com/adriangreenway/greenway-website.git`
- **Checked-out branch:** `dev` @ `4198c83` ("Redirect netlify.app subdomain to production domain", 2026-04-13)
- A second clone exists in Dropbox (`~/Library/CloudStorage/Dropbox/Claude Code/greenway-website`,
  on `main` @ `e17d5a6`, 2026-03-27). It is the **same GitHub repo**, just a second clone on a
  different branch — not a divergent source of truth. The working directory above is canonical.

## Branch picture (one repo, two branches)
Both `dev` and `main` are fully in sync with their `origin` counterparts (0 ahead / 0 behind).
They diverged after `98d5569` ("Add Experience page"):

| Branch | HEAD | Date | Committed pages | Publishes | Has netlify.app redirect? |
|---|---|---|---|---|---|
| `dev` (deployed) | `4198c83` | 2026-04-13 | index, experience, book, 404 | Home, Experience, Book | **Yes** |
| `main` | `e17d5a6` | 2026-03-27 | index, experience, **reviews, faq**, book, 404 + proposals | Home, Experience, Reviews, FAQ, Book | No |

Note: `main` is the only branch where Reviews/FAQ are **committed and published**. `main` is
**not** the deploy branch.

## What is live / deployed
- **Staging `greenway-website.netlify.app`:** deployed and served by Netlify, but every path
  **301-redirects to `greenwayband.com`** (rule from `netlify.toml`, present only on `dev`).
  Verified 2026-06-27 via `curl` (HTTP 301 → `https://greenwayband.com/...`, `server: Netlify`).
- **Inference:** because the live redirect exists **only on `dev`**, Netlify's deploy branch is
  **`dev`** (strong inference; confirm in Netlify UI). The deployed `dev` build therefore = Home,
  Experience, Book, 404 only — Reviews/FAQ are *not* committed to `dev` and are *not* live.
- **Production `greenwayband.com`:** still **Squarespace** (Cloudflare in front; Squarespace
  `crumb` cookie; 301 → `www`). Verified 2026-06-27 via `curl`.
- **Net effect:** the new Astro site is deployed to Netlify but **not publicly viewable at the
  staging URL** — it self-redirects to the old Squarespace site. To preview the new build you'd
  use a Netlify deploy-preview URL or temporarily remove the redirect.

## Pages — what exists, what's built, what's partial
| Page | File | Published flag (`site.ts`) | State |
|---|---|---|---|
| Home | `index.astro` | true | **Built.** Hero (video is a placeholder — solid bg + comment), 13-venue strip, "Why Greenway", CTA. |
| Experience | `experience.astro` | true | **Built**, real copy, 3 real photos. "For Planners" section has a `<!-- PLACEHOLDER -->` to expand. |
| Vocalist Showcase | *(no file)* | `Vocalists` = false | **Missing.** No `vocalists.astro` exists; `/vocalists` falls through to the branded 404. |
| Reviews | `reviews.astro` | true | **Shell only.** Three "Review coming soon" placeholders (no real reviews, no video slots). Copy integrity respected. |
| FAQ | `faq.astro` | true | **Built as a static 12-question accordion.** The AI assistant shell was **NOT** built. |
| Book | `book.astro` + `BookForm.astro` | true | **Built & wired.** Posts to lead-intake (see below). |
| 404 | `404.astro` | n/a | **Built**, branded, uses inline-SVG `Logo`, `noIndex`. |

## Uncommitted "April work" on `dev` (do NOT assume finished)
`git status` on the canonical repo is **dirty**. Treat these as possible unfinished April work:

Modified (tracked):
- `src/config/site.ts` — flips **Reviews** and **FAQ** `published: false → true`.
- `src/components/Header.astro` — adds **Reviews** and **FAQ** to the nav.
- `.claude/launch.json` — local editor/Claude config (+7 lines; not site code).

Untracked:
- `src/pages/faq.astro`, `src/pages/reviews.astro` — **byte-identical** to `main`'s committed
  versions (verified by matching git blob hashes). I.e. the April work copied the two pages from
  `main` onto `dev` and was wiring them up to publish, but **never committed**.
- `public/proposals/` (`ally-byrne` microsite), `.claude/worktrees/`.

**Interpretation:** someone was bringing `dev` up to `main`'s feature set (publish Reviews + FAQ)
but stopped before committing/pushing — so it never deployed. A local build on 2026-04-13 (the
`dist/` folder) *did* include faq + reviews, so the work builds cleanly.

> No snapshot tag was created during this recovery pass because the working tree is dirty
> (per the recovery brief, tagging is reserved for a clean tree). Decide on the uncommitted
> changes first; a safety tag can then be created at HEAD.

## The WEB-07 question — VERDICT
The brief flagged a possible "WEB-07" brand-compliance audit queued around April that may have
paused page rebuilds. **Finding: no artifact of "WEB-07" exists in this repo.**
- No match for `WEB-07`, `brand compliance`, or `audit` in any source file, doc, or commit
  message (searched `src/`, markdown, and full `git log --all`).
- The git history shows a clean line: Week 12 → **Week 12R** (rebuild) → Fontsource/Bodoni fixes
  → Experience page → (on `main`) Reviews + FAQ → (on `dev`) netlify redirect. No audit-related
  commits or paused-work markers.

**Verdict:** WEB-07 left **no trace in the code or history**. If it existed, it lived only in the
external planning environment (now lost). The real reason further pages stalled is visible in git:
work split across `dev`/`main` and the Reviews/FAQ publish work was left **uncommitted on `dev`**.
The brief's "≈5 deployed pages" hint best matches the **`main`** branch (5 published pages), which
is not the deployed branch.

## Known issues / discrepancies vs the brief
1. **Staging self-redirects to Squarespace** (see above) — new site not viewable at staging URL.
2. **FAQ AI assistant shell never built** — FAQ is a static accordion instead.
3. **Reviews has no real content** — three "Review coming soon" placeholders (brief said "written reviews v1").
4. **`published` flag is dead metadata** — nothing imports `pages[]` from `site.ts`; the nav is a
   hardcoded array in `Header.astro`. So "unpublished ⇒ removed from nav + branded 404" is **not
   implemented** as a mechanism. `/vocalists` 404s only because the file is absent.
5. **Book form input style:** `global.css .book-form__input` defines a **boxed** border, but
   `BookForm.astro`'s own `<style is:global>` overrides it to the spec'd **underline** style. The
   global.css version is effectively dead CSS (minor cleanup).
6. **Minor token deviations:** `#ffffff` used in a few button `:hover` states ("never pure white");
   `Logo.astro` uses an off-token gray `#8a867e` for sub-labels (404 only).
7. **Dead components:** `LogoInline.astro` and `LogoMonument.astro` are not referenced anywhere.

## Local vs remote
- `dev` and `main` are both 0/0 vs `origin` — local matches GitHub for the committed history.
- The **working tree differs from `origin/dev`** by the uncommitted April work above.
- Last `git fetch`: 2026-05-18.
- `dist/` (local build, 2026-04-13) reflects the *working tree at that time* (includes faq/reviews),
  not necessarily what Netlify currently serves from `dev`.

## Toolchain (verified)
- Astro `^6.0.4`, static output. Node engines `>=22.12.0` (machine has v25.8.0). npm 11.x.
- Fonts via Fontsource (`@fontsource-variable/bodoni-moda`, `@fontsource/plus-jakarta-sans`).
- No env vars referenced anywhere in `src`/config (so no `.env.example` is needed).
