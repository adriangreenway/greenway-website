# CONTENT_AND_MESSAGING

**Last verified: 2026-06-27.**

## Copy-integrity rule (NON-NEGOTIABLE)
**Never fabricate** venue names, testimonials, statistics, or anything implying real experience
the band hasn't had. Use **real content only**, or an explicit HTML placeholder comment
(`<!-- PLACEHOLDER: ... -->`). This rule exists because an earlier build shipped **fabricated
venues**; it must never recur. When in doubt, ship a placeholder, not an invention.

Current code **complies**: the Reviews page uses "Review coming soon" placeholders rather than
invented testimonials, and the Experience "For Planners" block is marked as a placeholder to expand.

## The 13 approved real venues
These are the only venue names approved for use as social proof. Used verbatim in
`SocialProofStrip.astro` (homepage) and `Footer.astro`:

1. River Oaks Country Club
2. Houston Country Club
3. Post Oak Hotel
4. The Astorian
5. The Houstonian
6. The Grand Galvez
7. Iron Manor
8. Ashton Gardens
9. Lakeside Country Club
10. The Junior League
11. The Houston Grand Hotel
12. Windemere Farms
13. La Colombe d'Or

> Do not add, rename, or invent venues. Changes require owner (Adrian) approval.

## Brand voice & identity
- **Name:** The Greenway Band. **Descriptor / tagline:** "The sound of a great night."
- **Standard:** Fortune 500 ("$400M, not $4M"). North stars: Apple, Aman, Aesop.
- **Tone (as written in current copy):** confident, concrete, understated. Short declarative
  sentences. Specific over salesy ("Real horns, real keys, real arrangements — not a playlist
  through a speaker"). Avoids hype, exclamation points, and clichés.
- **Positioning:** a premium Houston live band (10–20 piece, horn section, vocalists, music
  director arranging for live performance) for high-end weddings and events; Adrian handles
  emcee duties and planner coordination.

## Key copy that exists today (verified)
- **Home hero:** "THE / GREENWAY / BAND" + "The sound of a great night."
- **Why Greenway:** "The band that reads the room" + paragraph on horn section / genres / planner
  coordination / emcee.
- **Experience:** three phases — "The opening act" (cocktail hour), "The soundtrack" (dinner),
  "Nobody wants to leave" (dance floor) — plus a "For Planners / How we do it" section mentioning
  Ableton-driven arrangements, MIDI-synced production, stemmed tracks (placeholder to expand).
- **FAQ:** 12 real Q&As (band size, "what does 10-piece mean", stage space, pricing approach,
  travel, song requests, arrival/sound check, sound & lighting, emcee, date changes, planner
  coordination, genres).
- **Book confirmation:** "Thank you — We got your inquiry. Adrian will reach out within 24 hours…"

## Content gaps (need real material)
- **Reviews:** real written testimonials (currently 3 "Review coming soon" placeholders). Any
  testimonial must be real and, ideally, attributed (couple + venue) with permission.
- **Hero video / imagery:** the homepage hero is a solid-color placeholder awaiting real video or
  a poster image; `WhyGreenway` has a media placeholder block.
- **For Planners:** expand the production detail beyond the placeholder paragraph.
- **Vocalist Showcase:** entire page content pending (page not built).
