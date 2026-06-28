# SITE_MAP

**Last verified: 2026-06-27.** Routes are file-based (Astro `src/pages/`).

## Routes
| Route | Source file | In nav? | Published intent | Live on deploy branch (`dev`)? |
|---|---|---|---|---|
| `/` | `src/pages/index.astro` | logo → home | Home: published | Yes |
| `/experience` | `src/pages/experience.astro` | Yes | published | Yes |
| `/reviews` | `src/pages/reviews.astro` | Yes *(uncommitted on dev)* | published | **No** (file uncommitted on `dev`) |
| `/faq` | `src/pages/faq.astro` | Yes *(uncommitted on dev)* | published | **No** (file uncommitted on `dev`) |
| `/book` | `src/pages/book.astro` | Yes | published | Yes |
| `/vocalists` | *(none)* | No | Vocalists: unpublished | No — 404 (no file) |
| `404` | `src/pages/404.astro` | n/a | n/a | Yes |
| `/proposals/<client>` | `public/proposals/<client>/` | No | n/a | Per-client static microsites (tangential to the marketing site) |

> "In nav?" reflects the **working tree** of `dev` (Reviews + FAQ added to nav by the uncommitted
> April work). On the committed `dev` branch the nav is only Experience + Book. On `main` the nav
> already includes Reviews + FAQ. Nav is a hardcoded array in `Header.astro`.

## Navigation
- **Header** (`Header.astro`): fixed top bar. Desktop shows inline text wordmark + nav links;
  mobile shows a compact wordmark + hamburger that opens a full-screen menu. Nav links come from
  a hardcoded `navLinks` array (NOT from `site.ts`). Transparent over dark heroes, solidifies to
  cream on scroll.
- **Footer** (`Footer.astro`): dark, stacked text "monument" logo, descriptor, the 13-venue
  social-proof strip, and copyright.

## Page anatomy
- **Home:** `VideoHero` → `SocialProofStrip` (13 venues) → `WhyGreenway` → `HomeCTA`.
- **Experience:** inner hero → 3 alternating phase sections (Cocktail Hour / Dinner / Dance Floor)
  with real photos → "For Planners" section → dark CTA.
- **Reviews:** inner hero → 3 review slots (placeholders) → dark CTA.
- **FAQ:** inner hero → 12-item accordion → dark CTA.
- **Book:** inner hero → `BookForm` (inquiry).
- **404:** centered inline-SVG logo + "Back to home".

## Cross-page CTA
Every inner page ends with the same dark CTA ("Check availability for your date" → `/book`),
funnelling toward the single conversion action.
