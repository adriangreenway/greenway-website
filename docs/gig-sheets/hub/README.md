# Gig Sheets hub — gigs.greenwayband.com

The home page for `gigs.greenwayband.com`: one list of every wedding that has a
gig-sheet site, upcoming first. Each row is the couple's name and the gig date;
tapping it opens that wedding's site.

`gigs.greenwayband.com` is the Netlify site **`greenway-gigs`** (same account as
`greenway-proposals` and the per-wedding gig-sheet sites). That site is SHARED:
newer weddings live on it as subfolders (`/<lastname>/<mm-dd-yy>/`), deployed
whole-folder from `~/Desktop/greenway-gigs/` per `docs/gig-sheets/GIG_SHEET_SYSTEM.md`.
This folder is the source of truth for the root `index.html` only. Older weddings
still live on their own one-off sites (`greenway-<lastname>.netlify.app`); this
page only links to them.

## Files

- `index.html` — the page. The wedding list is the `GIGS` array near the bottom
  of the file; everything else is layout. Same design and tokens as the current
  gig sheets (`docs/gig-sheets/EXAMPLE/index.html`): cream `#F5F2ED` ground,
  Bodoni Moda + Plus Jakarta Sans.
- `netlify.toml` — reference copy of the shared site's headers. Never remove the noindex.

## Adding a wedding (do this every time a new gig sheet goes live)

1. Add one entry to `GIGS` in `index.html`:
   ```js
   { couple: 'Last / Last', date: '2026-10-24', url: 'https://gigs.greenwayband.com/last/10-24-26/' },
   ```
   `couple` as written on the sheet, `date` as YYYY-MM-DD, `url` the wedding's
   site root (shared-site subfolder with trailing slash, or an older one-off
   `greenway-<lastname>.netlify.app`).
   Order in the array does not matter — the page sorts by date and splits
   Upcoming / Past on load.
2. Copy `index.html` into `~/Desktop/greenway-gigs/index.html`, then deploy the
   WHOLE shared folder (never this folder alone: `--prod` replaces the entire
   site and would wipe every wedding subfolder):
   ```bash
   cp docs/gig-sheets/hub/index.html ~/Desktop/greenway-gigs/index.html
   cd ~/Desktop/greenway-gigs && netlify deploy --prod --dir . --site greenway-gigs
   ```
   Run the live-vs-local hash diff from `GIG_SHEET_SYSTEM.md` first. The shared
   folder's own `netlify.toml` stays; the one here is a reference copy.
3. Verify: `curl -s https://gigs.greenwayband.com/ | grep -c "Last / Last"`
   should print `1`. Then open it on a phone.

Only list sites that are actually live. Check with
`curl -s -o /dev/null -w "%{http_code}" https://greenway-lastname.netlify.app/`
(expect `200`) before adding a row — a dead link on gig day is worse than no link.
