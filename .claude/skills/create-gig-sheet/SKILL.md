---
name: create-gig-sheet
description: Build and deploy a per-wedding gig sheet microsite (gig sheet, band sheet, MC cue sheet, optional Listening Room) from Gmail, a timeline PDF, and a questionnaire PDF. Use whenever Adrian gives a couple's name and wants a gig sheet ("make a gig sheet for X", "create me a wedding gig sheet", attaches a timeline/questionnaire), or wants an existing one updated (new song, new arrival time, add the Listening Room).
---

# Create Gig Sheet

Turn everything Adrian and his vendors know about an upcoming wedding into a live,
offline-capable gig sheet site at `https://greenway-<lastname>.netlify.app`.

Read first: `docs/gig-sheets/GIG_SHEET_SYSTEM.md` (where things live, Netlify naming,
deploy runbook) and `docs/gig-sheets/EXAMPLE/` (the most recent full build — copy its
structure, don't reinvent the page layout or CSS). Model: Sonnet 5 is fine for this
workflow (this is building, not planning).

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
  emcee/DJ (e.g. a family friend's company)? If it's not Greenway, the `mc.html`
  page is a reference copy for that vendor, not Greenway's own script.
- Meals (count, dietary notes), attire, do-not-play list, couple's open song
  requests, any vendor contacts worth noting (photographer, videographer, planner)
- Anything that reads as a planning conflict between sources — flag it to Adrian,
  don't silently pick one.

## Step 3 — Build the site

Copy the structure of `docs/gig-sheets/EXAMPLE/` — same dark theme, same CSS
variables, same `.tag-live` / `.tag-track` pattern — into a scratch folder, then
replace every fact page by page:
- `index.html` — landing hub linking to whichever pages apply, in this order:
  Full Gig Sheet, Band Sheet, MC Cue Sheet (only if there's an outside emcee/DJ to
  reference), Listening Room (only if there's at least one LIVE song with a
  practice track — put it **last**, after MC, unless Adrian says otherwise)
- `gig.html` — the comprehensive sheet: sound package, ceremony music, full
  timeline, all specials
- `band.html` — the same facts reorganized for the band: timeline, specials,
  couple's requests, do-not-play, who's emceeing
- `mc.html` — only if a separate emcee/DJ runs the reception; a time-stamped cue
  script mirroring the timeline
- `listen.html` — only if there's at least one practice track; audio player with
  rewind/fast-forward (±10s) and a tap-to-seek progress bar, one track card per
  LIVE song. Convert any WAV to MP3 first (`ffmpeg -codec:a libmp3lame -b:a 192k`)
  — a raw Ableton export is too large for a phone to load smoothly at the venue.
- `sw.js` / `manifest.json` — update `sw.js`'s `CORE` array to list every page
  you're actually shipping

Never fabricate a venue, vendor, or song choice not backed by a source from Step 1.

## Step 4 — Deploy

Follow `docs/gig-sheets/GIG_SHEET_SYSTEM.md` exactly: check whether a site already
exists for this couple (`netlify sites:list | grep -i <lastname>`) before creating
a new one, deploy with `netlify deploy --prod --dir <scratch-folder> --site
greenway-<lastname>` (or the existing site ID for a revision), then verify every
page live with `curl` plus a Browser pane check for anything visual (new player
controls, layout).

**A brand-new gig sheet going live for the first time needs Adrian's "go"** — same
rule as a proposal deploy, it's a real public site even if unlisted. Present a short
status card first: couple, date, venue, what pages you built, the URL it will get,
and anything you marked UNKNOWN. Once the site exists, further changes Adrian asks
for in the same conversation (a new song, a time change, a new feature) redeploy
directly without re-asking — that's already the working pattern.

## Revisions

"Add X to the gig sheet" / "change the arrival time" / "add the Listening Room" →
edit the existing pages (re-pull them live first if your scratch copy is gone —
scratch folders don't persist between sessions), redeploy to the existing site ID,
verify the specific fact changed. If this build is now more complete than what's in
`docs/gig-sheets/EXAMPLE/` (a new feature, a page combination not seen before), pull
it down into that folder so it's the reference for the next wedding.
