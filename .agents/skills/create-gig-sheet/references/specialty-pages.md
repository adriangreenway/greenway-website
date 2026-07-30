# MC Cue Sheet and Listening Room

Read this reference whenever a gig sheet includes `mc.html` or `listen.html`.
Start from the complete working pages in `docs/gig-sheets/EXAMPLE/`; replace facts
and fix every path for the wedding's dated subfolder.

## Shared design

- Use the locked Greenway band-facing tokens: black `#0A0A09`, cream
  `#F5F2ED`, muted `#B8B4AC`, dim `#706D66`, and faint `#4A4740`.
  The MC page is dark. The Listening Room uses a cream body with a dark header.
  No gold, teal, blue utility links, translucent cards, gradients, pills, or
  rounded rectangles.
- Use Bodoni Moda for event names and editorial page titles. Keep Plus Jakarta
  Sans for operational text and controls. Navigation rows, track rows, badges,
  and buttons are square; all audio controls remain at least 44px.
- Use relative page, manifest, service-worker, and audio links.
- Cache every specialty page in `CORE`. Cache bundled audio in a separate `AUDIO`
  list with `Promise.allSettled`, so one missing MP3 cannot block the core offline
  sheet. Never delete another wedding's cache.

## MC Cue Sheet

Build `mc.html` whenever Greenway runs reception announcements. If a separate
emcee or DJ runs them, build it when a reference/backup is useful and name that
vendor in a banner. Do not show a vendor banner when Greenway is the emcee. Label
the page `ADRIAN ONLY` and never link it from the Gig Sheet landing page.

Keep the interaction from `EXAMPLE/mc.html`:

- Full-screen layout. The page stays fixed while only the cue list scrolls.
- One active cue at a time. Past cues dim, the active cue has the accent border
  and larger text, and upcoming cues remain partially dimmed.
- Fixed header with page name, couple, date, and live progress count.
- Fixed Back and Next controls. Arrow keys and tapping a cue also navigate.
- Scroll the selected cue into view and keep the final spacer so the last cue can
  reach the active position.

Each `.cue` stays in this order:

1. `.cue-time`: sourced scheduled time.
2. `.cue-label`: moment plus who announces it.
3. `.cue-say`: exact spoken line or action. Highlight names with
   `.name-highlight`.
4. `.cue-song.live` or `.cue-song.track`: one badge per song.
5. `.cue-note`: short logistics that should not crowd the spoken line.

Cover the reception in chronological order. Include only sourced names, times,
songs, speakers, and logistics. Keep LIVE and TRACK labels identical to the fact
sheet. Use `UNKNOWN` for a missing fact. Never invent a cue.

## Listening Room

Build `listen.html` for every wedding. When no practice files exist, keep the page
and show `No practice tracks have been added yet.` Do not show a fake player or a
browser-only upload control. Adrian adds permanent tracks to the source folder and
the site is redeployed. Never include a TRACK song handled by a DJ or emcee.

Start from `EXAMPLE/listen.html` and keep:

- One card per LIVE song, ordered by when it happens.
- Song title, artist, and moment label.
- Play or pause, 10-second back and forward controls, tap-to-seek progress bar,
  elapsed time, total time, and a visible missing-file error.
- Only one playing track at a time.
- Phone-safe controls with no horizontal overflow.

Put supplied audio in the wedding's `audio/` folder. Convert WAV files to 192 kbps
MP3 before deployment. Use relative audio paths in the page and dated absolute
paths in the service worker. Cache each MP3 best-effort so a failed audio download
never rejects the core page install.

## Landing page and verification

On `index.html`, link only to Band Sheet, then Listening Room. Full Gig Sheet and
MC Cue Sheet remain available only through their direct Adrian-only URLs.
Verify cue navigation by buttons, keyboard, and direct tap. Verify every player
control, seeking, one-track-at-a-time behavior, error state, phone layout, and
offline playback when tracks exist. With no tracks, verify the empty state and
confirm the core pages still save offline.
