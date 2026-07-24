# Client Song List page

Client-facing song list for proposals and emails. White + deep green, same
Bodoni Moda / Plus Jakarta Sans system as the proposal template.

- **Source of truth:** `Greenway_Client_Song_List_v4.xlsx` (Adrian edits this,
  came from `~/Desktop`). Every song, artist, genre, and line of page copy comes
  from it. Nothing on the page is typed by hand, so nothing can be invented.
- **Build:** `python3 build.py [newer.xlsx]` regenerates `index.html` and
  `songs.json`. The 433 count in the subtitle is computed from the rows, so it
  can never drift from the real list.
- **songs.json:** machine-readable copy for future use by the create-proposal
  skill or the Growth Hour app.
- **Deploy target:** copy `index.html` to
  `~/Desktop/greenway-proposals/song-list/` and run the usual proposals deploy
  (`netlify deploy --prod --site c6041c94-…` from a neutral cwd). Lands at
  `proposals.greenwayband.com/song-list`. Deploy only on Adrian's go.
- **greenwayband.com/song-list:** later, via Squarespace. Link to the hosted
  page or embed it as an iframe. Do not paste the raw HTML into a Squarespace
  code block, it is a standalone page, not a scoped widget.

Green palette (new accent, introduced 2026-07-24 for this piece, see
DECISIONS.md D15): deep `#1D392B`, mid `#27503A`, paper `#FBFAF8`. Hue ~150,
deliberately far from teal, which is reserved for the sister brand.
