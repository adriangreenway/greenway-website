# Live Clock for Gig Sheets (plan)

**Status:** PLAN READY, revised 2026-10-02 after Adrian chose "everyone" over
"just my phone". Awaiting his "build it". Nothing built.
**Track:** Gig sheets (track 4). Independent of the Astro pause and the go-live hold.
**Size:** Large, two stages built back to back and shipped together to the
**next** wedding. Not Hess (2026-10-03).

## What Adrian asked for, in one line

On the gig sheet, press play at the start of the night and have every band
phone show where we are in the schedule, with a way for Adrian to say "we're
running behind" so the rest of the night moves for everyone.

## How it works (plain English)

- **Every phone follows the clock on its own.** On the wedding day, in the
  venue's time zone, the Schedule highlights the block happening right now and a
  slim bar at the bottom of the phone reads something like
  `Dance set one · 23 min in · 67 min left · Next: Break at 9:30`. No tap, no
  signal needed.
- **Adrian's tap moves everyone.** On Adrian's phone only, each schedule row's
  time is a "we're here" button. Tapping it marks that block as started right
  now, shifts every later row by the same gap, and sends that one fact (which
  row, what time) to a tiny shared memory on the gigs site. Every band phone
  checks that memory every 30 seconds while the sheet is open on the wedding day
  and shifts the same way. The bar reads `12 min behind` (or ahead). `Reset`
  clears it for everyone.
- **Only Adrian can tap.** He opens the sheet once from a private link saved on
  his phone; that phone then shows the tap controls on every wedding's sheet. The
  band's phones show the moving bar and nothing to press. No login, no password
  typed on gig day.
- **Printed times never change.** The planner's timeline stays as written.
  Projected times appear as a second, dimmer line only when the night is off
  schedule.
- **It fails safe.** No signal, or the shared memory down: every phone keeps its
  last known shift, and the bar keeps following the clock. The sheets themselves
  are untouched by any of this.
- **It stays out of the way.** On any other day the pages look and print exactly
  as today. Nothing from this feature appears in the PDFs.

## Where it lives

The **Band Sheet** (`band.html`, Schedule) and the **Full Gig Sheet** (`gig.html`,
Full Timeline). Both already use identical row markup, and one script block
serves both. The MC Cue Sheet keeps its manual up/down cue flow; a one-line
readout in its header is an optional follow-on (Stage C).

## Build spec

### Stage A: the pages (Medium)

**Markup convention**
- The schedule `<section>` gains `data-schedule data-date="YYYY-MM-DD"
  data-tz="America/Denver"` (Houston weddings: `America/Chicago`). The MC page's
  "All times ..." notice is the source of truth for the zone.
- Every row with a real clock time gains `data-at="HH:MM"` in 24-hour venue time
  (`6:30 PM` → `data-at="18:30"`). Rows like `After toasts`, `Then`, `TBD`,
  `3 songs in` get no `data-at`; they belong to the previous timed block and are
  never highlighted on their own.
- Times before `06:00` mean the morning after the wedding date. No other
  past-midnight convention.
- A block runs from its `data-at` until the next timed row's `data-at`. The last
  timed row's block ends 60 minutes after it starts.

**Time math (the one trap, pinned)**
Build each row's absolute moment from `data-date` + `data-at` + `data-tz` with
the standard `Intl.DateTimeFormat` offset method: take `Date.UTC(y, m, d, h, min)`
as a guess, read the zone's offset at that instant via `formatToParts` with
`timeZone: tz, hour12: false`, and subtract. No date library. "Today is the
wedding day" is judged in `data-tz`, never in the phone's zone.

**States**
1. **Dormant** (not the wedding day, no saved shift): no bar, no highlight, no
   polling, only a once-a-minute date check. Zero visual change from today.
2. **Live by clock** (wedding day in venue zone): the current block row gets the
   "now" treatment, earlier timed rows dim, the bottom bar shows block name,
   minutes in, minutes left, next block and its time. Ticks every 15 s and on
   `visibilitychange`. Polls the shared memory every 30 s while visible, and on
   `online` and `visibilitychange`.
3. **Shifted** (a saved tap exists, from Adrian's tap or from the shared memory):
   `offset = tapTime − tapped row's scheduled time`. Every row at or after the
   tapped row shows `scheduled + offset` as a dim second line in the time cell.
   The bar adds `N min behind` / `N min ahead` / `On time` and, on Adrian's phone,
   a `Reset` control. A newer tap replaces the older one everywhere.

**Adrian's phone (the key)**
- The private link is the normal sheet URL plus a fragment:
  `/hess/10-03-26/band#clock=<key>`. The page reads the fragment, saves the key
  in `localStorage` under `gig-clock-key` (hostname-wide, so it covers every
  wedding), and removes the fragment from the address bar. Fragments are never
  sent to the server or logged.
- A phone holding the key shows the tap targets (the `.time` cell only, not the
  whole row, so scrolling thumbs do not fire it) and `Reset`. A tap applies
  locally at once, then POSTs to the shared memory; if the POST fails it retries
  on the next tick and on `online`. Band phones without the key get no controls.

**Persistence**
- `localStorage` key `gig-clock:<BASE>` (Hess: `gig-clock:/hess/10-03-26/`),
  value `{ "row": <timed-row index>, "at": <epoch ms>, "set": <epoch ms> }`. Keyed
  by wedding path because `localStorage` is shared across the hostname, like
  Cache Storage. A value older than 24 h is ignored and removed. All
  `localStorage` access is try/catch; private mode must not break the page.
- Survives the service worker's upgrade reload (`controllerchange`): the value is
  on disk, not in memory.

**Design (locked tokens only)**
- "Now" row: `background: var(--black); color: var(--cream)`, padding extended
  edge to edge, mirroring the hub link hover. Past rows `color: var(--dim)`.
  Projected time in the existing `.sub` style.
- Bottom bar: fixed, `var(--black)` on `var(--cream)` page, `border-top: 1px solid
  var(--faint)`, Plus Jakarta Sans, labels in the existing 9 px `.24em` uppercase
  eyebrow style. Body gets matching bottom padding only while the bar is visible.
  Phone: two lines max.
- `Behind` may use restrained `--warning` oxblood as a label color only; `Ahead`
  and `On time` stay `--muted`. No new hex values.
- `@media print`: bar, projected times, tap affordances, and "now" treatment all
  removed, so `band-sheet.pdf` and `gig-sheet.pdf` render exactly as today.

**Verification for Stage A alone:** fake `Date.now`, fake key, and a stubbed
fetch; no backend needed to prove states 1 to 3, the zone math (Mountain and
Central, one past-midnight row), persistence across reload, print output, and
phone width.

### Stage B: the shared memory (Medium, security-sensitive)

- **Where:** a Netlify Function on the existing `greenway-gigs` site, same origin
  as the sheets, so no CORS and no new hostname. Storage: Netlify Blobs, store
  `gig-clock`, one key per wedding path.
- **Routes:** `GET /.netlify/functions/clock?w=/hess/10-03-26/` → the saved value
  or `{}`; `Cache-Control: no-store`. `POST` same path with
  `Authorization: Bearer <key>` and body `{row, at}` or `{reset: true}` → writes
  or deletes; anything else `401`. Wedding path validated against
  `^/[a-z-]+/\d\d-\d\d-\d\d/$`. Body size capped. Nothing else is stored.
- **The key:** generated at build time, never typed in chat or printed. Stored in
  two places only: a new 1Password item `Greenway Gig Clock Key` (created by
  Claude via the `op` CLI, Adrian approves Touch ID) and the Netlify site env var
  `GIG_CLOCK_KEY` (set by piping `op read` into `netlify env:set`, so the value
  never appears in a command or log). Rotating = regenerate both and re-open the
  private link on Adrian's phone. Leaked key worst case: someone with a band URL
  shifts a schedule; rotate and reset.
- **Deploy mechanics (check before trusting):** `~/Desktop/greenway-gigs/` gains
  `netlify/functions/clock.mjs`, a minimal `package.json` with `@netlify/blobs`,
  `node_modules/`, and a `[functions] directory = "netlify/functions"` block in its
  `netlify.toml`. The Netlify CLI's default file filter skips `node_modules` and
  dot-folders on `--dir .` uploads; **prove it with a draft deploy (no `--prod`)
  first** and read the uploaded file count before any production deploy. If the
  CLI cannot carry the function cleanly, the fallback is a Cloudflare Worker + KV
  route with CORS limited to `gigs.greenwayband.com`, reusing the admin portal's
  Worker-secret pattern; that fallback needs its own approval.
- **The existing `Cache-Control: public, max-age=3600` header** applies to static
  files only; the function sets its own `no-store`. The service worker never
  caches the function path (it is not in `CORE`); offline, the fetch rejects and
  the page keeps its last value.
- **Load:** 10 to 11 phones polling every 30 s for a 11-hour day is roughly 13k
  function calls per wedding, well inside Netlify's free allowance, and polling
  only runs on the wedding day while the tab is visible. Confirm the account's
  plan during the build; if it ever matters, lengthen the poll.
- **Verification for Stage B:** `curl` GET empty, POST without key `401`, POST
  with key then GET returns it, reset deletes, bad wedding path `400`, response
  headers include `no-store`; then one real phone end to end on the draft URL.

### Stage C (optional, after A + B are proven at a wedding, Small)

MC Cue Sheet header shows the bar's one-line readout from the same shared value.
No change to its cue flow.

## Stage D (scoped 2026-10-03, not built): a proper home-screen app

Already true today: every wedding's `manifest.json` has `display: standalone`, so
Safari's **Add to Home Screen** on the Band Sheet gives a full-screen app with no
browser bars on iPhone and iPad. A home-screen app has its own storage, so the
`#clock=` link does not carry the key into it; the Stage view's **Unlock taps**
field (1Password autofill) covers that. iPad Safari also has the **Full screen**
button; iPhone Safari cannot go full screen, so the home-screen route is the iPhone
answer.

What a proper app still needs (Small, no special risks):
1. A square icon: `apple-touch-icon` 180x180 plus manifest icons 192/512, the
   wordmark on `--black`, locked palette only (today iOS uses a page screenshot).
2. A Stage start page: either `start_url` pointing at `band#stage` for a dedicated
   "Stage" app, or a tiny `stage.html` that redirects there, so one tap opens the
   countdown. The hub app and the Stage app can coexist as two home-screen icons.
3. `apple-mobile-web-app-status-bar-style: black-translucent` so Stage bleeds to
   the edges, with the safe-area padding already in the CSS.
4. Optional: an "Add to Home Screen" hint line on the hub for the band.

Done means: a home-screen icon opens straight into Stage, the key sticks after
Unlock, offline works inside the app, and the icon is the wordmark.

## Stages

| Stage | What | Size | Model |
|---|---|---|---|
| A | Pages: clock-follow, bar, Adrian-only tap, persistence, polling hooks; EXAMPLE template + system doc + both gig-sheet skills | M | Sonnet |
| B | Netlify Function + Blobs, key in 1Password + Netlify env, draft-deploy proof | M, security-sensitive | Fable |
| C | MC header readout | S | Sonnet |

A and B ship together to the next wedding's folder; neither is deployed to
production alone. Fable runs `verify-work` on the pair.

## Risks

- **Time-zone math.** Pinned to the Intl offset method, judged in the venue zone,
  verified on Mountain and Central with a fake clock.
- **A new online part on the live gigs site.** First function on that site. Draft
  deploy first, file-count check, then the normal whole-folder production deploy
  with the two-way live diff. Fails safe to clock-follow if it is ever down.
- **The key.** One new secret, two homes (1Password, Netlify env), never in a file
  or chat. Worst case is a shifted schedule, fixed by rotate + reset.
- **Wrong tap on gig day** now moves everyone, by design. Mitigations: tap target
  is the time cell only, Reset is one tap, the bar shows when the shift was set.
- No database beyond one Blobs store, no DNS, no money, no fabricated content.

## Files

**Modify:**
- `docs/gig-sheets/EXAMPLE/band.html`, `docs/gig-sheets/EXAMPLE/gig.html`
- `docs/gig-sheets/GIG_SHEET_SYSTEM.md` (new "Live clock" section: convention,
  zone, storage key, the private link, the function, the deploy check)
- `.claude/skills/create-gig-sheet/SKILL.md` and
  `.agents/skills/create-gig-sheet/references/final-formula.md` (every timed
  schedule row carries `data-at`; the section carries date and zone)
- `~/Desktop/greenway-gigs/netlify.toml` (add `[functions]`; owner-approved, it
  is the live site's config), new `~/Desktop/greenway-gigs/netlify/functions/clock.mjs`,
  new `~/Desktop/greenway-gigs/package.json` (+ `node_modules`, never deployed)
- `docs/ROADMAP.md`, `docs/CURRENT_STATE.md`, `docs/CHANGELOG.md`, `docs/DECISIONS.md`
  (new decision: first dynamic piece on the gigs site, key handling)
- The next wedding's `band.html`, `gig.html`, `sw.js` when that sheet is built

**Read only:** `~/Desktop/greenway-gigs/hess/10-03-26/{band.html,gig.html,mc.html,index.html,sw.js}`,
`docs/gig-sheets/EXAMPLE/sw.js`, `docs/DECISIONS.md` D17, D18, D20,
`docs/gig-sheets/PRIVATE_ADMIN_PLAN.md`.

**Off limits:** every live wedding folder's pages (`hess`, `blick`, `shepard`,
`matey`) and the gigs root `index.html`; `mc.html` cue logic and
`docs/gig-sheets/tools/mc-slides.py`; everything under `src/` (Astro, paused);
the `gigadmin.greenwayband.com` Worker; Cloudflare DNS.

## Done means

1. On any day other than the wedding date, both pages look, scroll, and print
   exactly as today: no bar, no highlight, no polling, no console errors.
2. On the wedding day in the venue's zone, every phone highlights the current
   block and the bar shows block name, minutes in, minutes left, and the next
   block, with no tap and with wifi off.
3. From Adrian's phone (opened once via the private link), tapping a row's time
   shifts later rows and the bar on **every** phone within 30 seconds; Reset
   clears it everywhere. A phone without the key shows no controls.
4. The shift survives a reload and a service-worker update, and another
   wedding's sheet on the same phone shows no trace of it.
5. The function rejects requests without the key, validates the wedding path,
   sends `no-store`, and the key appears in no file, command, log, or chat.
6. Draft deploy proves `node_modules` is not uploaded; production deploy follows
   the whole-folder + two-way live diff rules; other weddings return 200.
7. Verified with a fake clock for Mountain and Central including a past-midnight
   row, at phone width, and PDFs re-rendered byte-identical in content.

## Decisions taken while planning (technical, logged here, not asked)

- "Everyone" is the product. Adrian ruled per-phone confusing (2026-10-02).
- Only Adrian taps, via a saved private link rather than a login: no typing on
  gig day, no cross-origin cookie problem with the admin portal, one secret.
- Netlify Function + Blobs on the existing gigs site over a Cloudflare Worker:
  same origin, same deploy, no DNS or proxy change. Worker is the named fallback.
- Band Sheet and Full Gig Sheet first, MC readout later: identical markup, one
  script; the MC page has its own working cue flow.
- Printed times stay fixed and projections are a second line: the planner's
  timeline is the record and the band needs both numbers.
- Later rows shift by the same gap; a second tap at the next block handles
  compression without modeling it.
- Not shipped to Hess: Large, two stages, one new online part, wedding is
  tomorrow and the Hess sheet is verified and frozen.
