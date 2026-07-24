# Proposal Pricing + Approved Content

Everything here is **observed from real shipped proposals and Adrian's real emails**,
with its source. It is a reference, NOT a rate card: location, travel, date, and
negotiation move prices. **Adrian confirms every price before a proposal deploys** —
price is a "pay" decision and is always his. Never invent a number, a lineup, or a
claim. Last compiled 2026-07-13 from the 9 proposals then live.

## Observed band pricing

| Configuration | Price | Seen in (venue, city) |
|---|---|---|
| 10-Piece | $14,375 | garcia (Hotel ZaZa, Houston), harris (Sandlewood Manor, Tomball), hergenrether (Sandlewood Manor), the-united-way (713 Music Hall, Houston) — **Houston-area baseline** |
| 10-Piece | $15,000 | ashley-eastin (The Meekermark) |
| 10-Piece | $17,250 | bielitz (Texas Discovery Gardens, **Dallas**) |
| 10-Piece (Atlanta) | $32,500 | ally-byrne (Grand Hyatt Buckhead, **Atlanta** — major travel) |
| 8-Piece | $14,500 | garcia negotiation email, Jul 2026 (single observation) |
| 7-Piece (sax) | $11,600 | garcia (Houston) |
| 6-Piece | $10,350 | garcia, harris (Houston-area baseline) |
| 6-Piece | $10,800 | ashley-eastin |
| 6-Piece | $11,900 | bielitz (**Dallas**) |
| Unlabeled pair | $20,403 / $14,186 | thompson (Arts District Mansion, **Dallas**) — configs not marked in page, likely 10/6-piece with travel |

Pattern: Houston ≈ baseline; Dallas runs ~$1,500–$3,000 higher; far travel (Atlanta)
is bespoke. Non-Houston → flag travel and ask Adrian.

## Observed add-ons

| Add-on | Price | Seen in |
|---|---|---|
| Cocktail Hour Solo / Piano | $1,250 | garcia, bielitz |
| Cocktail Hour Duo | $1,875 | garcia v1, bielitz |
| Cocktail Hour Trio | $2,500 | garcia v1, bielitz |
| DJ Set (1 hr, end of night) | $1,250 | garcia |
| Additional hour of live music | $2,900 | garcia negotiation email, Jul 2026 (single observation) |
| Cocktail hour (negotiated concession) | $500 | garcia negotiation email — do NOT treat as a default |

Contract standard seen in email: **3 hours of live music across a 4-hour reception**.
Longer receptions price the extra hour.

Presentation (2026-07-13, updated 2026-07-23): client **chose** an add-on → single
priced row inside each package's investment total (garcia). Otherwise the "Cocktail
Hour" addon-section is the **DEFAULT on every wedding proposal** (Adrian, 2026-07-23,
campbell build — no longer opt-in): three bordered cards (Solo, Duo, Trio), excluded
from all totals, style locked from Adrian's Blick/Courtois reference doc
(giulia-costantini; block + CSS in TEMPLATE.html). Approved desc line:
*Live music during cocktails sets the tone before the reception begins. We offer
acoustic arrangements tailored to the mood you want.*
Package with **no add-ons** → one single "Investment" line with the price. Never a
band-only itemized row plus a "Total Investment" row (Adrian, 2026-07-13; matches
hergenrether/bielitz).
Package note (standard): *Additional instrumentation available upon request. Travel
fee may apply for events over 50 miles from Houston.*

## Locked lineups (never invent an instrumentation)

| Config | Rows exactly as shipped |
|---|---|
| 10-Piece | Male Vocals 1 · Female Vocals 2 · Keys 1 · Guitar 1 · Bass 1 · Drums 1 · Horns 3 |
| 7-Piece | Male Vocals 1 · Female Vocals 1 · Keys 1 · Guitar 1 · Bass 1 · Drums 1 · Saxophone 1 |
| 6-Piece | Male Vocals 1 · Female Vocals 1 · Keys 1 · Guitar 1 · Bass 1 · Drums 1 |

Included services (all wedding configs, verbatim — an "Included Services" column
inside EACH package card, restored 2026-07-24 by Adrian's correction spec; the
2026-07-23 shared-section rewording is retired): Sound Equipment and Engineer ·
Lighting Equipment and Engineer · Emcee Services · Personalized First Dances ·
Song Requests.
Corporate variant (the-united-way) can show `Production: Provided by Venue`.

Package benefit sentences (2026-07-24, Adrian's correction spec; `{{PKG1_DESC}}`/
`{{PKG2_DESC}}`, exactly one short, visually-secondary sentence directly under
each package title — the uppercase subtitle line is retired — verbatim for the
standard configs, adapt only if the lineup differs, never claim instruments a
config doesn't have):
- 10-Piece: *Three featured vocalists and a full horn section for a bigger sound
  and more dynamic stage presence.*
- 6-Piece: *Two featured vocalists and a versatile rhythm section for a polished,
  high-energy reception.*

## Approved testimonial pool — the ONLY three, verbatim

1. "From start to finish, the songs, the sound, and the look of the band were all just
   amazing. You left our guests wanting more." — **Allison · WeddingWire**
2. "Every guest was on their feet by the second song. We still have people texting us
   about the band three months later." — **Sarah & James H. · WeddingWire**
3. "Our wedding guests danced the night away like I've never seen before." —
   **Emma B. · WeddingWire**

All 9 shipped proposals use exactly these. Reordering is fine. Editing or adding is
not — a new testimonial requires Adrian supplying the real review.

## Standard approved copy (keep verbatim)

- Descriptor: *The sound of a great night.*
- Closing phrase: *Your guests won't stop talking about it.*
- Validity: *This proposal is valid through {{VALID_THROUGH_DATE}}.* (exact date =
  send date + 30 days; the old "30 days from date of receipt" wording retired
  2026-07-23, still live on pre-v5 pages)
- Duration line (2026-07-23, body copy directly above Cocktail Hour, never fine
  print): *Each reception package includes three hours of live performance across
  a four-hour reception.*
- Travel note, CONDITIONAL (only when the venue is 50+ miles from Houston):
  *Travel fee may apply for events over 50 miles from Houston.*
- Closing CTA (2026-07-24, Adrian's correction spec — Schedule a Call is primary
  again): note *On the call we'll walk through the options and how to hold your
  date.* → primary solid button **Schedule a Call** (static 17hats scheduler URL)
  → quiet secondary line *Ready now? Move forward by email.*
  ({{MOVE_FORWARD_MAILTO}}, prefilled email, no preselected package).
- Contact block: Adrian Michael · adrian@greenwayband.com · (281) 467-1226 ·
  greenwayband.com
- **NO-INTRO IS THE STANDARD (Adrian, 2026-07-14, locked on the turner build):** the
  Template 4.1 email (EMAIL_TEMPLATES.md) carries greeting/thanks/congrats; the page
  repeats none of it and runs cover → details → options → testimonials → closing.
  TEMPLATE.html has the section removed. Adrian may later refine page copy via a
  ChatGPT-interview spec; until he says so, build proposals with no intro. The
  intro-wording entries below are history only.
- Wedding intro paragraph 1 (reworked 2026-07-14, Adrian-approved, turner build):
  *Thank you for reaching out to us. We would love to be a part of your big day.*
  The 2026-07-13 "thousand decisions / drive home" opener is RETIRED (Adrian: corny).
- Wedding intro closing paragraph (2026-07-14): *Below are some options. If you have
  any questions, just reach out.* Replaces the retired "We'd love to be part of your
  night." — that sentiment now lives in paragraph 1.
- Intro tone (Adrian, 2026-07-14): plain sentences, ONE warm sentence max, nothing
  corny, no metaphors ("the drive home" is the banned example). Optional middle
  paragraph only for a real, plain fact about their event; most proposals skip it.
- Greeting format (2026-07-14): "Congratulations,&lt;br&gt;&lt;first name(s)&gt;!" — ends
  with an exclamation point, never a period. The old "&lt;names&gt;, congratulations."
  style is retired.
- Package subtitles RETIRED (2026-07-24, Adrian's correction spec): no uppercase
  subtitle under package names; the single benefit sentence above replaces it.
  (Historical style on pre-2026-07-24 shipped pages: "Full horn section +
  reception entertainment + MC", garcia.)
- The 10-Piece ALWAYS leads with the Recommended badge — no per-client
  exceptions (Adrian 2026-07-13, made exceptionless 2026-07-24 on the hinojosa
  redo). Premium-first: the price descends, the 6-Piece reads as the saving.
  On desktop (≥900px) the two packages sit side by side (`.packages-grid`,
  10-Piece left); on mobile they stack, 10-Piece first.

## Approved media pool (D14, 2026-07-23, v2 same day)

Default on every wedding proposal since the 2026-07-23 template upgrade (mockup +
15-agent stress test, then a 3-judge palette panel, see `docs/DECISIONS.md` D14).
All files live once in `~/Desktop/greenway-proposals/assets/` (shared across
every proposal folder, not duplicated per client) and are referenced by relative
path `../assets/<file>`.

| Asset | File | Source | Notes |
|---|---|---|---|
| Photo band 1 (after cover) | `assets/band-stage-2026a.webp` | website repo `public/images/experience/20230311Preview0069.webp`, re-encoded 1600px/q80 | Couple dancing, band + lighting rig behind them |
| Photo band 2 (before testimonials) | `assets/crowd-2026a.webp` | `.../_JHZ1145.webp`, re-encoded 1600px/q80 | Packed dance floor; `object-position: 50% 30%` keeps a videographer's camera rig out of the mobile crop |
| Video poster | `assets/uptown-funk-poster-2026a.jpg` | Vimeo thumbnail for the video below | Full band visible on stage, 16:9 native |
| Video | `assets/uptown-funk-2026a.mp4` (self-hosted, ~73MB, 720p H.264/AAC) | Encoded 2026-07-23 from `~/Desktop/uptown_funk_v1 (1080p).mp4`, Adrian's "Uptown Funk" clip | Click-to-load, self-hosted — **no third-party player, no watermark** (Adrian: "if we're going to be premium, let's be premium"; Vimeo Plus can't remove its logo from embeds). Master copy stays on Vimeo (`vimeo.com/1129682149`), unlisted, for Adrian's own reference only — the page never links to it. If Adrian ever supplies a proper highlight reel, re-encode and swap this file, same filename convention (bump the year-suffix, e.g. `-2026b`). |
| Third photo (unplaced) | `public/images/experience/IMG_0668.webp` | — | Not used in the template pool: reviewed poster candidate, but the square 1:1 crop hid the band behind a bride close-up. Available for a future placement if Adrian wants it, no current use. |

**Usage rights:** Adrian confirmed 2026-07-23 that the band's standard client
contract grants reuse of photo and video from gigs, which covers the pictured
couples and the photographer's work. This is the standing basis for using any
gig photo/video as proposal media — no separate release needed per photo.

**Video honesty rule:** captions and copy must stay true to whatever asset is
actually linked. The current video is one song — never "full performance" or
"full set" unless the linked video actually is one.

**Video section structure (2026-07-24):** the small "Watch the band" label,
the player, and one caption (*Uptown Funk, recorded live · tap to play*) —
nothing else. The serif title and the "Photos only say so much" desc line were
cut (Adrian: the stacked copy read cluttered; let the video speak).

**Venue strip: REMOVED (Adrian, 2026-07-23, same day it was built).** A "Where
we've played" trust line was built, then Adrian pulled it: "I don't think it
adds much value." He was also unsure whether the 13-approved list undersold the
band's real experience versus overselling into invented territory, and decided
the tradeoff wasn't worth it. Do not re-add without Adrian raising it again.

**CTA:** two "Schedule a Call" links per proposal (inline after pricing, solid
cream button in the closing — judge-panel fix: it's the page's only conversion
action, an outline read too weak against the dark closing), both to the static
17hats scheduler URL already used in the Template 4.1 email. Phone number in the
closing is a `tel:` link.

## Palette (v2, D14 amendment, 2026-07-23 — "hybrid," Adrian's own word: "C")

Adrian's reaction to the all-dark template: dark is "sexy," but he wanted to see
a lighter option against the site's real brand guide before committing. A
3-judge panel (art director, buyer-simulation, brand-system consultant) compared
three built variants — full dark, full cream, and a hybrid — and voted the
hybrid unanimously, strong confidence on all three.

**The hybrid:** cover and closing keep the original dark palette exactly
(near-black bg, cream ink) — the cover stays byte-identical to every proposal
shipped before this date, so the first-impression unit doesn't change during the
~30-day window where old dark proposals and new hybrid ones coexist. Everything
between (event details, video, packages, cocktail hour, testimonials) uses the
website's own locked design-system tokens (`docs/DESIGN_SYSTEM.md`): `#F5F2ED`
cream background ("never pure white"), near-black ink, secondary/faint text
mapped directly from the site's `--color-dim` / `--color-faint`. Implementation:
CSS custom properties are re-declared at `:root` for the cream body, then
scoped-overridden back to the original dark values on `.cover, .closing` only.

Judge-panel fixes folded into the build: solid-fill closing CTA (not outline);
hairline borders on cream strengthened to ink at 12%/16%/26% alpha (was reading
"wireframe-y" at the old low-alpha cream values); every photo-to-cream seam is a
hard edge with a hairline, no gradient scrim (only the top of photo band 1 blends
into the dark cover above it); the video frame and its play button stay
hardcoded dark-plate colors regardless of section palette, since they always sit
over a dark photo/video; the crowd photo and video plate are the *only* two dark
elements allowed inside the cream body — never add a third, or the bookend
structure degrades into stripes.

## Copy-integrity rules for proposals (same spirit as CLAUDE.md, applied here)

1. Every fact on the page traces to the inquiry email, a prior shipped proposal, or
   Adrian's explicit word.
2. **No venue-experience claims** ("we've played here before", "our pianist knows the
   room") unless Adrian confirms it. The ZaZa pianist line in garcia was
   Adrian-approved for that venue only — do not recycle it elsewhere.
3. Unknown detail → ask Adrian (if it's see/pay/risk) or leave the cell/section out.
   Placeholders and `{{TOKENS}}` never deploy.
4. Prices, lineups, and totals must match this file or Adrian's instruction; totals
   must equal the sum of their rows.
5. Never mention another client, couple, or their wedding by name anywhere in a
   proposal, including grid cells and intro copy (Adrian, 2026-07-13). Referral
   history informs the offer, never the page.
