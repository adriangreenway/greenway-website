# Working Code Example — Ditta / Johnson (2026-07-11)

Snapshot of a complete working gig sheet, pulled from the live
`greenway-ditta.netlify.app` site. Use its HTML, CSS, and enhanced specialty-page
controls as working code. The controlling content hierarchy and page formula now
live in `.agents/skills/create-gig-sheet/references/final-formula.md`, based on
Adrian's preferred Freeman/Dass build. When this example and the formula differ,
the formula wins.

Files:
- `index.html` — band hub, links only to Band Sheet and Listening Room
- `band.html` — minimal band-facing sheet: calls, performance blocks, live
  specials, attire, do-not-play items, and direct team rules
- `gig.html` — Adrian-only full operational sheet, reached only by its direct URL
- `mc.html` — Adrian-only time-stamped cue script, reached only by its direct URL
- `listen.html` — permanent Listening Room. It shows a clear empty state when no
  files exist; with files, it uses rewind/fast-forward players for practice tracks
  (only include songs the band actually plays live — never tracks a DJ covers)
- `sw.js` / `manifest.json` — offline PWA support; `sw.js`'s `CORE` array must list
  every page in the site or that page won't work offline

Design tokens live inline in each file's `<style>` block: `#0A0A09` background,
`#F5F2ED` text, `#C4A35A` gold accent, Plus Jakarta Sans font, `.tag-live` /
`.tag-track` badges on every song. Keep these exact values — they're what makes a
gig sheet instantly recognizable as a Greenway one.

The band-facing pages never show money, package names, MC detail, DJ identity,
music direction, planner or client contacts, or full event minutiae. The
Adrian-only pages may hold operational detail, but never money or package terms.
An unlinked direct URL limits accidental discovery; it is not password protection.
