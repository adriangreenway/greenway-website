# Canonical Gig Sheet Formula

Use this reference for every wedding. Freeman/Dass is the approved model for page
architecture, visual hierarchy, operational filtering, and repetition across
roles. Preserve that formula, not its wedding facts, old root paths, or any stale
times from the old live site.

## Contents

- Source priority and fact ledger
- Music ledger
- Visual system and landing order
- Full Gig Sheet
- Band Sheet
- MC Cue Sheet
- Listening Room
- Modern safety upgrades
- Definition of done

## Source priority and fact ledger

Build a private fact ledger before editing HTML. Record each value, its newest
source, its source date, and whether it is settled.

Use this priority:

1. Adrian's direct instruction in the current chat.
2. The newest final planner timeline or explicit operational update.
3. Newer full email-thread facts and attached files.
4. The questionnaire and signed scope.
5. Older messages only when nothing newer addresses the field.

The newest final timeline controls scheduled times unless a later direct message
changes one. After writing the pages, compare every displayed time, song, and
operator back to the ledger. Never let an older questionnaire time survive because
it was already in copied HTML.

## Music ledger

For every music moment record:

- Moment and scheduled time.
- Song and artist.
- `LIVE` when Greenway performs it, or `TRACK` when a recording plays.
- Who starts the music and who announces.
- Whether the band must learn it.
- Whether a practice MP3 exists.
- Pronunciation and logistics notes when sourced.

Use that one ledger everywhere. Timeline, Specials, MC cues, Songs to Learn, and
Listening Room must agree.

Keep the client's sourced favorites available to the band as a compact,
title-only `Couple's Song Suggestions` list. It is a taste guide, not a must-play
list. Keep detailed music direction in the Full Gig Sheet only. A song gets a
player in Listening Room only when Greenway performs it and a practice file exists.

## Visual system and landing order

- Band-facing pages use the locked Greenway palette only: black `#0A0A09`,
  charcoal `#111110`, cream `#F5F2ED`, muted `#B8B4AC`, dim `#706D66`, and
  faint `#4A4740`. No gold, metallic, teal, blue utility links, translucent
  cards, gradients, or decorative status colors.
- `index.html`: cream background with black type and gray support text.
  `listen.html` and `band.html`: cream body with a black header.
- Use Bodoni Moda for event names and editorial page titles. Keep Plus Jakarta
  Sans for every operational fact, label, schedule row, and control.
- Navigation rows, cards, badges, and buttons have square corners. Use hairline
  rules and spacing for grouping instead of rounded containers. Audio controls
  remain at least 44px in both dimensions.
- A sourced warning that prevents a gig-day mistake may use the restrained
  oxblood token `#8D2E2A` as a label or rule. Do not use it as general decoration.
- Keep the compact Freeman/Dass information hierarchy, two-column desktop grids,
  single-column phone layout, small uppercase section labels, and
  LIVE/TRACK/BREAK badges.
- The landing page is labeled `Gig Sheet`. Link only to Band Sheet, then Listening Room.
  Full Gig Sheet and MC Cue Sheet remain unlinked and available only by direct URL.

## Full Gig Sheet

Keep this section order:

1. Core two-column information: Location with map link, Performance Team when
   operationally useful, Attire directly beneath it, Guests, Sound Load In, Band Load In,
   Soundcheck plus quiet time, Meals with time and room. Attire always means the
   band's standing wedding attire, never the guests':
   `Guys: black suit, black shoes, black tie, white shirt` and
   `Girls: black dress or jumpsuit`. Never show the meal count.
2. `Timeline`: the full operational day, including ceremony, cocktail hour,
   reception events, band sets, breaks, and exit.
3. `Specials`: every named music moment with song and LIVE/TRACK badge.
4. `Songs to Learn`: only new or specifically prepared LIVE material.
5. `Emcee`: exact couple introduction and essential pronunciation.
6. `Key Contacts`: only useful day-of roles with tap-to-call/email links.
7. `Notes`: terse logistics that prevent mistakes, including critical scope,
   room changes, toss/send-off mechanics, or setup facts.

The Full Gig Sheet is Adrian's operational view. It may carry guest count,
contacts, MC detail, DJ information, music direction, and event minutiae that the
band-facing sheet does not need. Its header and footer say `ADRIAN ONLY`, and it
is never linked from the Gig Sheet landing page. Never show money or package terms.

## Band Sheet

Keep this section order:

1. Core call information: Couple's full names, Location, Attire, Sound Load In,
   Band Load In, Soundcheck/quiet time, and Meals with time and room, never a
   count. Keep Attire in this top block rather than repeating it later.
2. `Schedule`: broad performance blocks, musician calls, breaks, and only
   transitions that require band action.
3. `Live Specials`: only songs Greenway performs live.
4. `Songs to Learn`: same preparation list as Listening Room.
5. `Couple's Song Suggestions`: a concise, title-only list of sourced favorites.
6. `Do Not Play`.
7. `Notes`: only direct team rules or logistics that prevent a mistake.

Keep this page shorter than the Full Gig Sheet. Its footer shows the couple and
short date. Never show MC information, DJ identity, money, package terms,
configuration, guest count, planner or client contacts, music direction, private
moments, or exact special-dance microtiming. Label outside coverage only as
`Break`.

## MC Cue Sheet

Build it whenever Greenway is responsible for announcements. If an outside
emcee/DJ owns announcements, build it only when a reference/backup is useful and
name that vendor in a banner. Label the page `ADRIAN ONLY` and never link it from
the Gig Sheet landing page. Include every actionable reception transition in
time order, exact spoken wording, LIVE/TRACK badges, pronunciations, and concise
logistics. Use the interaction rules in `specialty-pages.md`.

## Listening Room

Build it for every wedding. When no practice MP3s exist, show a terse empty state:
`No practice tracks have been added yet.` Do not render fake players or a
browser-only upload control. When tracks exist, put special-moment songs first,
followed by dance-set additions, and state the real preparation priority in one
short line. Use the player and offline rules in `specialty-pages.md`.

## Modern safety upgrades

Apply the approved shared-host changes even though Freeman/Dass predates them:

- Dated URL and folder: `<client-last-name>/<mm-dd-yy>/`.
- Relative page, manifest, service-worker, and audio links.
- Dated manifest scope and wedding-scoped cache prefix.
- Netlify rewrites internal `.html` links to extensionless URLs in production.
  Cache both forms of every page so clicked links work offline.
- `CORE` pages, including `listen.html`, cache atomically and every revision fetches them with
  `{ cache: 'reload' }`, so a new cache version cannot repackage hour-old HTML.
  Audio caches separately with `Promise.allSettled`.
- Cache cleanup deletes only older caches for this wedding.
- Privacy headers stay `noindex, nofollow`.
- Unlinked pages and `noindex` are limited distribution, not authentication.
  Never claim password protection unless real access control exists.

## Definition of done

Every fact traces to a source. All pages agree with the ledger. Phone layout,
MC navigation, player controls, missing-audio behavior, offline pages, best-effort
offline audio, privacy headers, and at least one older wedding all pass.
