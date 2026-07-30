# Gig Sheet System

Per-wedding, offline-capable microsites with separate band and Adrian views.
This is separate from proposals, the Astro rebuild, and the Squarespace embed.

Last verified: 2026-07-30.

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
- Matey/Sackschewsky is the first wedding on the shared hostname.
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

Before deploying, confirm every existing wedding folder is still present. After
deploying, confirm the changed wedding and at least one older shared-hostname
wedding both return HTTP 200. Matey is currently the only shared-hostname wedding,
so the older-wedding check becomes applicable after the second wedding is added.

## Subfolder path rules

- Page links and the manifest link are relative: `gig.html`, `band.html`,
  `manifest.json`.
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
   The landing hub links only to Band Sheet and Listening Room. Full Gig Sheet and
   MC Cue Sheet are labeled Adrian Only and are available only by direct URL.
   Listening Room stays present with a clear empty state until tracks are added.
3. Preview the whole shared folder locally at
   `/<client-last-name>/<mm-dd-yy>/`. Confirm every link stays inside that
   wedding's folder and the landing page reports that it was saved for offline use.
4. For a new wedding, show Adrian the couple, date, venue, pages, public URL, and
   every visible `TBD` or `UNKNOWN`. Wait for his explicit `go`.
5. Deploy the complete folder with the command above.
6. Verify every changed page at the public hostname, the privacy headers, the
   service-worker file list, phone-width layout, and browser console. After the
   service worker installs, confirm an actual rewritten hub link still opens the
   correct page with the network unavailable.

## Audience and sharing rules

- Send the landing URL or `band.html` to musicians.
- Keep `gig.html` and `mc.html` for Adrian. They are deliberately unlinked from
  the band hub.
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
