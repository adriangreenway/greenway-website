---
name: create-gig-sheet
description: Build and deploy a per-wedding gig sheet microsite (gig sheet, band sheet, MC cue sheet, and Listening Room) from Gmail, a timeline PDF, and a questionnaire PDF. Use whenever Adrian gives a couple's name and wants a gig sheet ("make a gig sheet for X", "create me a wedding gig sheet", attaches a timeline/questionnaire), or wants an existing one updated (new song, new arrival time, add practice tracks).
---

# Create Gig Sheet

Turn everything Adrian and his vendors know about an upcoming wedding into a live,
offline-capable gig sheet at
`https://gigs.greenwayband.com/<client-last-name>/<mm-dd-yy>/`.

Read first: `docs/gig-sheets/GIG_SHEET_SYSTEM.md` (where things live, Netlify naming,
deploy runbook), `references/final-formula.md` (the controlling content and page
formula), and `docs/gig-sheets/EXAMPLE/` (working page code to adapt, not the
authority for section choice or fact priority). Model: Sol. Adrian uses ChatGPT for
this workflow.

Always read `references/specialty-pages.md` before editing `listen.html` or
`mc.html`; every sheet now includes Listening Room.

## Step 1 — Gather every source, don't guess from one

A gig sheet is only as good as its facts. Pull from all three sources that exist for
this wedding, cross-checking one against another:

1. **Any PDFs Adrian attaches** — a venue/planner final timeline and a 17hats
   questionnaire are typical. Read them in full (`pdftotext -layout` if the Read tool
   can't render them directly). These usually carry the ceremony/reception timeline,
   first dance and parent-dance song choices, attire, and vendor list.
2. **Gmail — read FULL threads, never snippets.** `search_threads` returns
   truncated snippets; **never build a fact from a snippet.** Call `get_thread`
   with `FULL_CONTENT` (the default) on every related thread and read every message
   in it, including quoted reply trails — the real answer is often three replies
   deep in a forwarded chain, not in the top message. Search recipes, in order:
   - `"<couple's first names>" OR "<last name>"` broadly
   - the venue name
   - the wedding planner's or day-of coordinator's domain, once you spot it in one
     thread (planners loop in every vendor on logistics threads you'd otherwise miss)
   - `17hatsmail.com "<name>"` for the intake questionnaire confirmation
   **The newest message wins** — arrival times, sound-package scope, and who's
   handling the reception (Greenway vs an outside DJ/emcee) all get renegotiated
   after the first form. A later email overriding an earlier one is normal, not a
   conflict — just use the latest.
3. **Anything Adrian states directly in chat** (arrival time, soundcheck window,
   "sound package only", attire) — his word in the current conversation is a fact,
   not a guess; use it as given.

If Adrian hasn't provided a timeline or questionnaire and Gmail doesn't have one
either, ask him for it rather than inventing a schedule — this is a copy-integrity
issue, same as fabricating a testimonial. Mark every unresolved fact `UNKNOWN` /
`<!-- PLACEHOLDER: ... -->` in the draft rather than filling the gap.

## Step 2 — Build the fact sheet

Pull out, per wedding:
- Couple's full names, wedding date, venue, city
- Arrival time, load-in, soundcheck window
- What Greenway is providing: full band, sound-package-only, ceremony/cocktail
  sound, or some combination — this changes which pages the site even needs
- Full day timeline: ceremony time, cocktail hour, reception segments, dinner,
  toasts, cake, last dance, send-off
- **Every special song, each tagged LIVE (the band performs it) or TRACK (a
  recording, run by Greenway's PA or by an outside DJ/emcee vendor)**: processional,
  wedding party entrance, bride's entrance, recessional, grand entrance, first
  dance, father/daughter, mother/son, any other named dance, final/last song,
  private last dance. Get this exactly right — it drives both the MC cue sheet
  wording and which songs belong in the Listening Room (LIVE only; never include a
  track a DJ is covering).
- Who's running reception announcements and transitions — Greenway, or an outside
  emcee/DJ (e.g. a family friend's company)? Build `mc.html` for Greenway when
  Greenway announces, or as a clearly labeled reference copy when an outside vendor
  announces.
- Dinner time and location, do-not-play list, couple's open song requests, any
  vendor contacts worth noting (photographer, videographer, planner)
- Anything that reads as a planning conflict between sources — flag it to Adrian,
  don't silently pick one.

Build one music ledger before writing HTML. For every music moment, record the
scheduled time, song, artist, LIVE or TRACK operator, whether the band must learn
it, whether a practice MP3 exists, the announcement wording, and the newest source.
This single ledger feeds Timeline, Specials, MC cues, Songs to Learn, and Listening
Room so those pages cannot contradict one another.

**Two things you never have to look up, because they are standing rules:**

- **Attire.** The attire on a gig sheet is always **the band's**, never the guests'.
  The questionnaire's attire answer ("Black Tie Optional") describes the guests —
  do not put it on the sheet. Weddings are always:
  ```
  Guys - Black suit, black shoes, black tie, white shirt
  Girls - Black dress or jumpsuit
  ```
  On the Full Gig Sheet, place Attire directly beneath Performance Team in the core
  information. Do not repeat it as a later standalone section.
- **Meal count** is always **the number of musicians + 1** for the sound engineer:
  a 10-piece needs 11 meals, a 6-piece needs 7, and an 8-piece needs 9. Keep that
  count in the private fact ledger when it is useful for vendor coordination, but
  never show the count on the gig sheet. Show the meal time and, when known, the
  room.

## Step 3 — Build the site

Use the Freeman/Dass visual and information hierarchy defined in
`references/final-formula.md`, adapting working code from
`docs/gig-sheets/EXAMPLE/`. The MC page is dark. The Gig Sheet landing is cream.
The Listening Room, Full Gig Sheet, and Band Sheet use a cream body with a dark
header. Keep the same CSS variables and `.tag-live` / `.tag-track` pattern.
Build into `~/Desktop/greenway-gigs/<client-last-name>/<mm-dd-yy>/`, then replace
every fact page by page.

**Fix the paths as you copy.** The EXAMPLE folder is from the old one-site-per-wedding
era and uses absolute paths that break in a subfolder: links and the manifest must
become relative (`gig.html`, not `/gig`), the service worker must register as `sw.js`
not `/sw.js`, and inside `sw.js` every `CORE` entry and the offline fallback need the
`/<client-last-name>/<mm-dd-yy>/` prefix. `manifest.json` needs `start_url` and
`scope` set to that complete dated path. Cache cleanup must only delete cache names
for this wedding; Cache Storage is shared across the hostname, so deleting every
other cache would break offline mode for other weddings. Details in
`docs/gig-sheets/GIG_SHEET_SYSTEM.md`.

Netlify rewrites internal `.html` links to extensionless URLs in production.
Cache both versions of every page in `CORE`, such as `band` and `band.html`, so a
clicked production link still opens the correct page offline.

Pages:
- `index.html` — Gig Sheet landing linking only to Band Sheet, then Listening
  Room.
- `gig.html` — Adrian-only comprehensive operational sheet, unlinked from the
  landing page.
- `band.html` — the minimal band-facing version from `final-formula.md`. Never show
  MC detail, DJ identity, money, package terms, configuration, full contacts,
  music direction, private moments, or exact special-dance microtiming. Keep the
  couple's full names and Attire in the top core block, and include a compact,
  title-only `Couple's Song Suggestions` section when sourced favorites exist.
- `mc.html` — Adrian-only time-stamped cue script, unlinked from the landing
  page.
- `listen.html` — always build this page. With no practice files, show a simple
  empty state and no fake player or browser-only upload control. When tracks
  exist, use an audio player with rewind/fast-forward (±10s) and a tap-to-seek
  progress bar, one track card per LIVE song. Convert any WAV to MP3 first
  (`ffmpeg -codec:a libmp3lame -b:a 192k`) — a raw Ableton export is too large for
  a phone to load smoothly at the venue.
- `sw.js` / `manifest.json` — cache every page atomically in `CORE`; cache bundled
  practice tracks separately and best-effort so one failed MP3 never blocks the
  whole offline sheet

Never fabricate a venue, vendor, or song choice not backed by a source from Step 1.

## House style — these sheets are terse, and Adrian will push back if they aren't

The band reads this on a phone, at a venue, mid-gig. Every extra word costs.

- **No bullet separators.** Never `•` between facts. Stack the lines instead:
  ```
  Load In
  Sound - 12:00pm
  Band - 3pm-4pm
  ```
- **Never say who confirmed what, or when.** No "confirmed with Courtney 7/10," no
  "approved by the planner," no "per the questionnaire," no dates of agreement. The
  fact is the fact. If something isn't settled, the value is just `TBD`.
- **No money, ever.** No fees, no add-on prices, no "paid on." The band sees this.
- **Negative scope only when it prevents a gig-day mistake.** A direct line such as
  "Band is not playing ceremony" belongs in Notes when operationally necessary.
  Cut defensive explanations such as "not a must-play list."
- **No explaining why.** "The DJ add-on exists so the energy never drops" is a
  sentence for Adrian, not for the sheet.
- **Unsettled fields are one word.** `TBD`, not "Conflict — questionnaire says no,
  run of show has one at 10:50, planner to confirm." Put the real open questions in
  a short Open Items / Notes block, one line each.
- Timeline rows are a time and a short phrase. Drop parentheticals and durations
  that the next row already implies.
- **Do not rename sections.** Use the exact Full Gig Sheet and Band Sheet labels in
  `references/final-formula.md`. Adrian recognizes his sheets by these headings,
  and a clever new name ("Vibe List") reads as a different document, not a better
  one.

## Step 4 — Deploy

Follow `docs/gig-sheets/GIG_SHEET_SYSTEM.md` exactly.

**All gig sheets share one Netlify site**, so `--prod` replaces everything —
deploying a partial folder silently deletes past weddings' sheets. Always deploy the
whole directory:

```bash
cd ~/Desktop/greenway-gigs && netlify deploy --prod --dir . --site 8205364b-6929-454b-bfe0-51afaeb02636
```

Never trust a site ID copied from documentation. Verify the linked site exists in
the signed-in Netlify account before deploying. Then verify with `curl` that this
wedding's pages return the facts you just wrote **and** that a past wedding still
returns 200, plus a Browser pane check for anything visual (new player controls,
layout).

**A brand-new gig sheet going live for the first time needs Adrian's "go"** — same
rule as a proposal deploy, it's a real public URL even if unlisted. Present a short
status card first: couple, date, venue, what pages you built, the URL it will get,
and anything you marked UNKNOWN. Once it's live, further changes Adrian asks for in
the same conversation (a new song, a time change, a new feature) redeploy directly
without re-asking — that's already the working pattern.

## Revisions

"Add X to the gig sheet" / "change the arrival time" / "add the Listening Room" →
edit the pages in
`~/Desktop/greenway-gigs/<client-last-name>/<mm-dd-yy>/`, redeploy the whole
directory, verify the specific fact changed live. That folder is permanent, so
unlike the old scratch-folder workflow your copy is still there next session. If
this build is now more complete than what's in `docs/gig-sheets/EXAMPLE/` (a new
feature, a page combination not seen before), pull it into that folder so it's the
reference for the next wedding.
