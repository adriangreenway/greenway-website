# Client Song List page

Client-facing song list for proposals and emails, built strictly on the
proposal template's design system: charcoal cover with the wordmark, cream
body, Bodoni Moda / Plus Jakarta Sans, hairline rules. No other colors, no
copy beyond the wordmark, "Song List", genres, songs, search, and footer
links (D15 v2 — a green v1 was rejected; never reintroduce it).

- **Source of truth:** `Greenway_Client_Song_List_v4.xlsx` (Adrian edits this,
  came from `~/Desktop`). Every song, artist, genre, and line of page copy comes
  from it. Nothing on the page is typed by hand, so nothing can be invented.
- **Build:** `python3 build.py [newer.xlsx]` fills `template.html` (the page
  shell; `@@NAV@@`/`@@SECTIONS@@` slots) and regenerates `index.html` and
  `songs.json`. Edit design in `template.html`, content in the xlsx, wiring in
  `build.py`.
- **songs.json:** machine-readable copy for future use by the create-proposal
  skill or the Growth Hour app.
- **Deploy target:** copy `index.html` to
  `~/Desktop/greenway-proposals/song-list/` and run the usual proposals deploy
  (`netlify deploy --prod --site c6041c94-…` from a neutral cwd). Lands at
  `proposals.greenwayband.com/song-list`. Deploy only on Adrian's go.
- **greenwayband.com/song-list:** later, via Squarespace. Link to the hosted
  page or embed it as an iframe. Do not paste the raw HTML into a Squarespace
  code block, it is a standalone page, not a scoped widget.

Palette: proposal tokens only — cover `#0A0A09`, body cream `#F5F2ED`, inks
`#111110`/`#2A2A27`, dims `#706D66`/`#8A867E`/`#4A4740`, hairlines
`rgba(10,10,9,.12/.16/.26)` and `rgba(245,242,237,…)` on the cover.
