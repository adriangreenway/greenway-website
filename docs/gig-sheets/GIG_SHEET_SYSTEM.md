# Gig Sheet System

Per-wedding, offline-capable microsites with separate band and Adrian views.
This is separate from proposals, the Astro rebuild, and the Squarespace embed.

Last verified: 2026-09-28.

## Where things live

| What | Where |
|---|---|
| Permanent deploy source | `~/Desktop/greenway-gigs/` |
| Wedding folder | `~/Desktop/greenway-gigs/<client-last-name>/<mm-dd-yy>/` |
| Public URL | `https://gigs.greenwayband.com/<client-last-name>/<mm-dd-yy>/` |
| ChatGPT workflow | `.agents/skills/create-gig-sheet/SKILL.md` |
| Controlling page formula | `.agents/skills/create-gig-sheet/references/final-formula.md` |
| Specialty-page rules | `.agents/skills/create-gig-sheet/references/specialty-pages.md` |
| Working page code | `docs/gig-sheets/EXAMPLE/` |
| Source facts | Full Gmail threads, timeline/questionnaire PDFs, and Adrian's chat instructions |

## Hosting facts

- Netlify site: `greenway-gigs`
- Netlify site ID: `8205364b-6929-454b-bfe0-51afaeb02636`
- Account: `Proposal Landing Page`
- Cloudflare record: DNS-only CNAME `gigs.greenwayband.com` to
  `greenway-gigs.netlify.app`
- Privacy: `noindex, nofollow` on every path
- Shared-hostname weddings so far: Matey/Sackschewsky (08-01-26), Shepard/Perugini (08-08-26, deployed 2026-08-05), Blick/Courtois (09-05-26, deployed 2026-08-31), Hess/Cassiday (10-03-26, deployed 2026-09-28; first out-of-town sheet, adds a Travel section).
- Older weddings remain on their original one-off Netlify sites. Do not migrate,
  delete, or redeploy them unless Adrian asks.

## Critical deploy hazard

`netlify deploy --prod` replaces the entire shared site. Deploying one wedding's
folder by itself would remove every other wedding from `gigs.greenwayband.com`.

Always deploy the complete permanent folder:

```bash
cd ~/Desktop/greenway-gigs
netlify deploy --prod --dir . --site 8205364b-6929-454b-bfe0-51afaeb02636
```

Before deploying, confirm every existing wedding folder is still present, then
run a live-vs-local hash diff over every file in every OTHER wedding folder plus
the root `index.html` (`shasum` local vs `curl` live). If live differs, live wins
for weddings this session is not editing: pull the live copy into the local
folder before deploying. This is mandatory — proven 2026-08-31, when six
matey/shepard files were newer on live (another tool's absolute-link pass) and a
presence-check-only deploy would have silently reverted them. After deploying,
confirm the changed wedding and at least one older shared-hostname wedding both
return HTTP 200, and re-hash one previously-drifted file to prove it survived.

## Subfolder path rules

- Internal page-to-page nav links (hub links, Listening Room back link) are
  absolute extensionless: `/<client-last-name>/<mm-dd-yy>/band`. This is the
  live-site convention since a 2026-08 pass across matey/shepard; Blick follows
  it. The manifest link, sw registration, PDF download links, and audio paths
  in pages stay relative: `manifest.json`, `sw.js`, `band-sheet.pdf`.
- Register the service worker as `sw.js`, not `/sw.js`.
- In `sw.js`, every `CORE` entry and the offline fallback use absolute
  `/<client-last-name>/<mm-dd-yy>/...` paths.
- Netlify Pretty URLs rewrites internal `.html` links to extensionless paths in
  production. Cache both versions of every page, such as `band` and `band.html`,
  or a clicked production link will fall back to the hub when the phone is offline.
- `manifest.json` uses the complete dated path for both `start_url` and `scope`.
- Bump the service-worker cache name on every revision.
- Cache pages atomically in `CORE`. Fetch every `CORE` path with
  `{ cache: 'reload' }` before writing the new cache, so the browser's one-hour
  HTML cache cannot seed a new service-worker version with stale pages. Cache
  practice audio separately with `Promise.allSettled` so a failed MP3 cannot
  block the sheet from installing.
- Cache cleanup must only delete this wedding's older cache names. Cache Storage
  is shared across the hostname, so never delete every cache except the current one.

## Build and deploy

1. Check `~/Desktop/greenway-gigs/` before creating anything. If the wedding
   folder exists, revise it in place.
2. Build the controlling formula: `index.html`, `gig.html`, `band.html`,
   `listen.html`, optional `mc.html`, plus `manifest.json` and `sw.js`.
   The Gig Sheet landing page links only to Band Sheet and Listening Room. Full
   Gig Sheet and MC Cue Sheet are labeled Adrian Only and are available only by
   direct URL.
   Listening Room stays present with a clear empty state until tracks are added.
3. Preview the whole shared folder locally at
   `/<client-last-name>/<mm-dd-yy>/`. Serve with `npx serve` (clean URLs), NOT
   `python3 -m http.server` — python 404s the extensionless `CORE` paths so the
   service worker can never install locally. Confirm every link stays inside
   that wedding's folder. The Claude in-app browser pane cannot run service
   workers on localhost at all; the real offline check is step 6, live:
   headless Chrome `--dump-dom` on the live hub must show `Saved for offline use`.
4. For a new wedding, show Adrian the couple, date, venue, pages, public URL, and
   every visible `TBD` or `UNKNOWN`. Wait for his explicit `go`.
5. Deploy the complete folder with the command above.
6. Verify every changed page at the public hostname, the privacy headers, the
   service-worker file list, phone-width layout, and browser console. After the
   service worker installs, confirm an actual rewritten hub link still opens the
   correct page with the network unavailable.

## Practice tracks and lyrics

- Convert every WAV to MP3 first (`ffmpeg -i in.wav -codec:a libmp3lame -b:a 192k
  out.mp3`) into the wedding's `audio/`, kebab-case, matching the `file:` in
  `listen.html`'s `TRACKS`. A card only renders once its MP3 exists, so a registry
  entry for a track that is still coming is harmless. Check each WAV's length with
  `afinfo` before converting: a bad export can be a fraction of a second long
  (Ain't Nobody, 2026-09-28).
- Add each MP3 to `sw.js` `AUDIO`, bump `CACHE`, then the usual live diff and
  whole-folder deploy.
- Lyrics come from Adrian's AbleSet sets (`<Song> - Synced Lyrics for AbleSet.als`,
  GWB Show SSD, `Ableton/_Trax/<Song>/`): every lyric line is a MIDI clip on the
  `Vocals +LYRICS` track, placed in beats. Run
  `docs/gig-sheets/tools/als-lyrics.py <file.als> --bpm <tempo from the
  practice-track filename> --duration <MP3 seconds>` and paste the printed
  `[[seconds, 'line'], ...]` array as that track's `lyrics:`. Always pass the
  song's real tempo: the standalone lyric set's master tempo is a throwaway (Hot
  Stuff's said 200 for a 120 BPM song). The script's duration check must say OK.
  When the practice-track filename has no tempo, the song's main project file
  in the same folder is named `<Key>_<bpm> bpm_<Song>.als` (`Dm_120.45 bpm_Bad
  Girls.als`, `Ebm_104 bpm_Ain't Nobody.als`); use that, and cross-check with
  `docs/gig-sheets/tools/tempo-estimate.py <mp3>` (audio beat analysis, needs
  numpy + ffmpeg; validated on all five Hess tracks).
- Prefer the lyric track inside the SHOW project (`<Key>_<bpm> bpm_<Song>.als`,
  pass `--track "vocals +lyrics"` so the older `LYRICS` track is skipped) over a
  standalone `Synced Lyrics for AbleSet.als`: the standalone can be stale. Ain't
  Nobody's standalone file was a 144-bar layout (90 lines) while the show
  arrangement and every export are 96 bars (67 lines); only the show project's
  track ended at the MP3's end. If the duration check says CHECK BPM and the
  tempo is confirmed, the lyric file is the wrong length, not the tempo.
- Some lyric sets are chord-annotated: the clip names carry ChordPro marks inside
  the words (`[Am]Feeling m[F]y way`) and some clips are chords only (Wake Me Up,
  2026-10-02). The script prints them as-is. Strip `\[[^\]]*\]`, collapse the
  extra spaces, and drop any line that ends up empty before pasting; chords never
  belong in a Listening Room card. The same goes for set-list plugin tags such as
  `[red]` on a clip name (Ain't Nobody, caught live 2026-10-02): strip every
  `[...]` tag, not just chord marks.
- Timed lyrics highlight the current line while the track plays and jump the
  track when a line is tapped; a plain string still works for untimed lyrics.
  First shipped on Hess, 2026-09-28; the code lives in `EXAMPLE/listen.html`.

## MC Slides deck

`mc-cue-slides.pdf` (the landscape one-cue-per-page deck Adrian loads into forScore)
is generated from the finished `mc.html` by `docs/gig-sheets/tools/mc-slides.py
<wedding-folder> "<Couple>" <mm.dd.yy>`. Re-run it whenever a cue changes, re-render
`mc-cue-sheet.pdf` (headless Chrome `--print-to-pdf` of `mc.html` off a local
server), keep both listed in `sw.js` `CORE`, and bump `CACHE`.

## Audience and sharing rules

- Send the landing URL or `band.html` to musicians.
- Keep `gig.html` and `mc.html` for Adrian. They are deliberately unlinked from
  the Gig Sheet landing page.
- The Band Sheet contains the couple's full names, musician call information,
  attire in the top core block, broad performance blocks, live specials, a compact
  title-only list of the couple's sourced song suggestions, do-not-play items, and
  direct team notes.
- Do not show money or package terms on any page. Do not show MC detail, DJ
  identity, music direction, full contacts, or event minutiae on the Band Sheet.
- Label non-performance coverage as `Break`; do not identify the DJ to the band.
- `noindex` and unlinked URLs reduce discovery but are not authentication. Never
  describe these pages as password protected unless real access control exists.

## Naming

Use the couple's lowercase client last-name slug, followed by the wedding date in
`mm-dd-yy` format. Use both last names only to avoid a client-name collision.

Example:

`~/Desktop/greenway-gigs/matey/08-01-26/` becomes
`https://gigs.greenwayband.com/matey/08-01-26/`.

## Auto-refresh for open pages (Hess, 2026-09-29)

Gig sheets are cache-first so they work offline, which used to leave band members on
stale copies. Every page now polls `registration.update()` when the tab regains focus,
when the phone comes back online, and every 5 minutes, and reloads on
`controllerchange`. `sw.js` also navigates open pages on an upgrade (old cache
existed). Always bump `CACHE` on any change; that bump is what triggers all of this.
Nobody should ever be told to refresh or clear cache. A tab sitting in the background
updates the moment it is opened or woken.

## Live clock (Band Sheet + Full Gig Sheet, 2026-10-02)

On the wedding day the Schedule highlights the block happening now and a fixed
bottom bar reads the block, minutes in and left, and what is next. Adrian's phone
(opened once via `band#clock=<key>`) can tap a row's time to mark it "now"; every
phone follows within 30 s through the Netlify Function in
`docs/gig-sheets/functions/`. Plan and spec: `docs/gig-sheets/LIVE_CLOCK_PLAN.md`.

- Markup: the schedule `<section>` carries `data-schedule data-date="YYYY-MM-DD"
  data-tz="America/Chicago"` (Montana: `America/Denver`), and every row with a
  real clock time carries `data-at="HH:MM"` in 24-hour venue time. Rows like
  `After toasts` or `TBD` get no `data-at` and are never highlighted. Times
  before `06:00` mean the morning after. `docs/gig-sheets/EXAMPLE/band.html` and
  `gig.html` carry the CSS, the bar markup, and the script; copy all three parts.
- `Stage` in the bar (or `#stage` on the URL) opens a full-screen display for a mounted
  phone or iPad: block name, mm:ss countdown, next block, behind/ahead, venue clock,
  wake-lock, the whole timeline (past dimmed, current highlighted, projected times),
  `Full screen` where the browser allows it (iPad Safari, not iPhone), and `Unlock
  taps` (a password field for the key, meant for 1Password autofill inside a
  home-screen app, which has its own storage). Key holders get per-block tap
  buttons, a confirm guard on taps more than 90 min from the scheduled time, and a
  permanent `Reset` (top-right of Stage and in the bar). The bar and Stage always
  say which mode is running: `Auto · on schedule` (no stored tap, the default: the
  whole night follows the clock untouched) or `Manual · 12 min behind` (a tap is
  stored; it still follows the clock with that adjustment). Every tap means "this
  block starts right now"; Reset returns everyone to Auto. Sized for iPhone landscape (`max-height:460px` rules) and
  iPad portrait (wrapped timeline grid); checked 2026-10-03.
- Off the wedding day the pages are byte-for-byte the same to look at and to print.
  The bar, projected times, and highlights are all hidden in print.
- State is `localStorage` `gig-clock:<wedding path>` on each phone (per wedding,
  because storage is shared across the hostname) and expires after 24 h; the key
  is `gig-clock-key` (hostname-wide). Nothing is cached by the service worker.
- The pages call `/.netlify/functions/clock?w=<wedding path>`. The function is live
  on the gigs site since 2026-10-02 (`~/Desktop/greenway-gigs/.functions/` plus the
  `[functions]` block in its `netlify.toml`; canonical copy and runbook in
  `docs/gig-sheets/functions/`). It is shared by every wedding, so a new sheet needs
  only the page markup. If it were ever missing, the calls 404 harmlessly and every
  phone simply follows the clock. Adrian's private `#clock=` link is the website
  field of the 1Password item.
- Never put the key in a page, a doc, a commit, or chat. It lives in the Netlify
  env var `GIG_CLOCK_KEY` and 1Password `Greenway Gig Clock Key` only.
