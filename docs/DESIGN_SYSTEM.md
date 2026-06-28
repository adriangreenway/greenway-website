# DESIGN_SYSTEM

**Last verified: 2026-06-27.** Tokens extracted from `src/styles/global.css` `:root` and media
queries. These match the locked spec in the project brief (deviations noted at the bottom).

## Colors (locked)
| Token | Value | Notes |
|---|---|---|
| `--color-black` | `#0A0A09` | default text; near-black |
| `--color-charcoal` | `#111110` | dark surfaces, button hover |
| `--color-cream` | `#F5F2ED` | page background; "never pure white" |
| `--color-muted` | `#B8B4AC` | muted accents |
| `--color-dim` | `#706D66` | secondary text, labels |
| `--color-faint` | `#4A4740` | faintest text, hairline borders |

**Prohibited:** pure white, gold, any metallic, teal (teal belongs to the sister brand only).

## Typography
- `--font-display`: `'Bodoni Moda Variable', serif` — weights 400/500/600; `font-optical-sizing: auto`.
- `--font-body`: `'Plus Jakarta Sans', sans-serif` — weights 300/400/500/600.
- Loaded via Fontsource (see `BaseLayout.astro`), not Google Fonts.

### Type scale (CSS variables; mobile-first with breakpoint overrides)
| Variable | Mobile (<768) | Tablet (≥768) | Desktop (≥1024) |
|---|---|---|---|
| `--text-hero-wordmark` | 44px | 54px | 64px |
| `--text-section-headline` | 28px | 32px | 36px |
| `--text-page-headline` | 32px | 36px | 40px |
| `--text-body` | 16px | 16px | 16px |
| `--text-nav` | 12px | 12px | 12px |
| `--text-button` | 11px | 11px | 11px |
| `--text-descriptor` | 13px | 14px | 14px |
| `--text-venue` | 11px | 12px | 12px |
| `--text-footer` | 12px | 12px | 12px |

- Body weight 300; headings (`h1–h4`) use display font, weight 400, `line-height 1.2`,
  `letter-spacing 0.02em`.
- `--line-height-body: 1.7`, `--line-height-headline: 1.2`.

## Spacing & layout
- `--max-width: 1200px`; container padding 24px (`.container`).
- `--section-padding`: 80px mobile / 120px (≥768).
- `--content-padding`: 24px → 48px (≥768) → 64px (≥1024).
- `--component-gap: 48px`.
- Spacing scale: `--space-xs 4` · `sm 8` · `md 16` · `lg 24` · `xl 32` · `2xl 48` · `3xl 64`
  · `4xl 96` · `5xl 128` (px).
- Breakpoints: **375 / 768 / 1024 / 1440**.

## Animation
- `--transition-default: 200ms ease-out`; `--transition-slow: 400ms ease-out`.
- Scroll reveal: `--reveal-duration 600ms`, `--reveal-offset 80px` (fade-up), `--stagger-delay 100ms`.
  Implemented in `BaseLayout.astro` via IntersectionObserver (`threshold: 0.15`); `data-reveal-delay="N"`
  multiplies by 100ms. No parallax.
- Z-index layers: `--z-header 100`, `--z-mobile-menu 90`, `--z-video-overlay 10`.

## Components
- **Primary button** (`.home-cta__button`, `.book-form__submit`, page CTAs): filled, **sharp
  corners** (`border-radius: 0`), 11px uppercase Plus Jakarta Sans 600, padding `14px 32px`.
  Black-on-cream or cream-on-dark depending on background.
- **Form inputs** (`BookForm.astro`): **underline style** — `border: none; border-bottom: 1px
  solid var(--color-dim)`, transparent background; focus darkens the underline; error state uses
  a red underline. Selects use a custom SVG chevron.
- **Header:** fixed; transparent over dark heroes, solidifies to cream with a faint bottom border
  on scroll. Logo is **inline text** (not SVG) in the header/footer/hero.
- **Footer:** dark (`--color-black`), centered, stacked text "monument" logo, descriptor, 13-venue
  strip, copyright.
- **Hero:** full-viewport; background is a video slot (`hero__bg`, currently solid black + a
  `<!-- VIDEO: ... -->` placeholder) under a **55% dark overlay** (`rgba(10,10,9,0.55)`).
- **Reviews:** editorial layout — one review per centered block, separated by short rules.

## Logo
- Browser-rendered logos (header, footer, hero) are **text-based** with **no hairline rules**.
- `Logo.astro` is an inline-SVG wordmark (text elements only, no rules/lines) used on the **404**.
- Descriptor: "The sound of a great night."

## Known deviations (minor; not yet reconciled)
- `#ffffff` (pure white) appears in a few button `:hover` states (`reviews.astro`, `faq.astro`,
  `experience.astro`) — technically against "never pure white".
- `Logo.astro` uses an off-token gray `#8a867e` for the THE/BAND sub-labels.
- `global.css` still contains an older **boxed** `.book-form__input` rule that is overridden by
  `BookForm.astro`'s underline rule (dead CSS).
- `LogoInline.astro` and `LogoMonument.astro` are unused.
