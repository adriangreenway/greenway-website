# Reference Example — Ditta / Johnson (2026-07-11)

Snapshot of the most feature-complete gig sheet built so far, pulled from the live
`greenway-ditta.netlify.app` site. Use this as the structural starting point for a
new gig sheet: copy the folder, then replace every wedding-specific fact page by
page. Do not treat it as a fill-in-the-blank template with tokens — the sections
that apply (Listening Room, MC cue sheet, sound-package-only vs full band, PRP/DJ
handoff) vary per wedding, so read each file and keep only what applies.

Files:
- `index.html` — landing hub, links to the other pages, registers the service worker
- `gig.html` — full gig sheet (sound package, ceremony music, timeline, specials)
- `band.html` — band-facing sheet (timeline, specials, requests, do-not-play, emcee)
- `mc.html` — time-stamped emcee/DJ cue script (only needed if a separate MC/DJ runs
  the reception, e.g. PRP Entertainment; omit if Greenway MCs)
- `listen.html` — Listening Room, audio player with rewind/fast-forward for practice
  tracks (only include songs the band actually plays live — never tracks a DJ covers)
- `sw.js` / `manifest.json` — offline PWA support; `sw.js`'s `CORE` array must list
  every page in the site or that page won't work offline

Design tokens live inline in each file's `<style>` block: `#0A0A09` background,
`#F5F2ED` text, `#C4A35A` gold accent, Plus Jakarta Sans font, `.tag-live` /
`.tag-track` badges on every song. Keep these exact values — they're what makes a
gig sheet instantly recognizable as a Greenway one.
