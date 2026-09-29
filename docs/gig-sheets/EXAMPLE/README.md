# Working Code Example — Courtois / Blick (2026-08-31)

Snapshot of the newest complete shared-host gig sheet build
(`gigs.greenwayband.com/blick/09-05-26/`). Use its HTML, CSS, and specialty-page
controls as working code. The controlling content hierarchy and page formula
live in `.agents/skills/create-gig-sheet/references/final-formula.md`. When this
example and the formula differ on page structure, this example is newer for:
hub links Band Sheet + MC Cue Sheet + Listening Room (D20 v3 made MC
band-visible), a hub Band Sheet PDF download link, per-page PDF download links,
`@media print` CSS on `mc.html` so the cue sheet prints multi-page, absolute
extensionless internal nav links, and a Listening Room empty-state line.
Everywhere else, the formula wins. Per Adrian (2026-08-31): sheets carry no
source citations and no change-history — current facts only.

Files:
- `index.html` — Gig Sheet landing: Band Sheet, MC Cue Sheet, Listening Room,
  plus a Band Sheet PDF download link
- `band.html` — minimal band-facing sheet: calls, performance blocks, live
  specials, attire, do-not-play items, and direct team rules
- `gig.html` — Adrian-only full operational sheet, reached only by its direct URL
- `mc.html` — time-stamped cue script with print CSS; notice bar links its PDF
  and a landscape per-cue Slides PDF (generated from a scratch slides HTML)
- `listen.html` — permanent Listening Room. It shows a clear empty state when no
  files exist; with files, it uses rewind/fast-forward players for practice tracks
  (only include songs the band actually plays live — never recorded-playback songs)
- `sw.js` / `manifest.json` — offline PWA support; `sw.js`'s `CORE` array lists
  every page in both URL forms plus the four PDFs, and audio caches separately

Design tokens live inline in each file's `<style>` block: black `#0A0A09`, cream
`#F5F2ED`, muted `#B8B4AC`, dim `#706D66`, and faint `#4A4740`. Use Bodoni Moda
for editorial titles and Plus Jakarta Sans for operational text. Keep square
controls, hairline grouping, and `.tag-live` / `.tag-track` badges. No gold or
rounded cards. The Gig Sheet landing and Listening Room bodies are cream.

The band-facing pages never show money, package names, MC detail, DJ identity,
music direction, planner or client contacts, or full event minutiae. The
Adrian-only pages may hold operational detail, but never money or package terms.
An unlinked direct URL limits accidental discovery; it is not password protection.
