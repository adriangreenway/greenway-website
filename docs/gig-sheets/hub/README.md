# Gig Sheets hub — gigs.greenwayband.com

The home page for `gigs.greenwayband.com`: one list of every wedding that has a
gig-sheet site, upcoming first, with direct links to each site's pages (Full Gig
Sheet, Band Sheet, MC Cue Sheet, Listening Room).

`gigs.greenwayband.com` is the Netlify site **`greenway-gigs`** (same account as
`greenway-proposals` and the per-wedding gig-sheet sites). This folder is its
deploy source. The individual gig sheets still live on their own sites
(`greenway-<lastname>.netlify.app`) exactly as `docs/gig-sheets/GIG_SHEET_SYSTEM.md`
describes; this page only links to them.

## Files

- `index.html` — the page. The wedding list is the `GIGS` array near the bottom
  of the file; everything else is layout. Same brand tokens as every gig sheet
  (`#0A0A09` / `#F5F2ED` / `#C4A35A`, Plus Jakarta Sans).
- `netlify.toml` — security headers + `noindex`. Never remove the noindex.

## Adding a wedding (do this every time a new gig sheet goes live)

1. Add one entry to `GIGS` in `index.html`:
   ```js
   {
     couple: 'Last / Last',            // as written on the sheet
     type: 'Wedding',
     date: '2026-10-24',               // gig date, YYYY-MM-DD
     venue: 'Venue Name',
     city: 'Houston, TX',              // optional
     url: 'https://greenway-lastname.netlify.app',
     pages: ['gig', 'band', 'mc', 'listen'],   // only the pages that exist
   },
   ```
   Order in the array does not matter — the page sorts by date and splits
   Upcoming / Past on load.
2. Deploy from this folder:
   ```bash
   netlify deploy --prod --dir docs/gig-sheets/hub --site greenway-gigs
   ```
3. Verify: `curl -s https://gigs.greenwayband.com/ | grep -c "Last / Last"`
   should print `1`. Then open it on a phone.

Only list sites that are actually live. Check with
`curl -s -o /dev/null -w "%{http_code}" https://greenway-lastname.netlify.app/`
(expect `200`) before adding a row — a dead link on gig day is worse than no link.
