# Client Song List page

Client-facing song list for proposals and emails, built strictly on the
proposal template's design system: charcoal cover with the wordmark, cream
body, Bodoni Moda / Plus Jakarta Sans, hairline rules. No other colors, no
copy beyond the wordmark, "Song List", genres, songs, search, and footer
links (D15 v2 — a green v1 was rejected; never reintroduce it).

- **Source of truth:** `Greenway_Client_Song_List_v4.xlsx` (Adrian edits this,
  came from `~/Desktop`). Every song, artist, genre, and line of page copy comes
  from it. Nothing on the page is typed by hand, so nothing can be invented.
- **Build:** `python3 build.py [newer.xlsx]` fills two shells with the same
  song data and writes three files:
  - `template.html` → `index.html` — standalone hosted page (own `<head>`,
    fonts, full charcoal-cover design). Deploy to
    `~/Desktop/greenway-proposals/song-list/` → proposals.greenwayband.com,
    same flow as any other proposal, on Adrian's go.
  - `embed_template.html` → `embed.html` — **the file to paste into
    Squarespace.** One `<div id="greenway-songlist">` wrapper, every
    selector/id/class scoped or prefixed `gw-`, literal hex colors (no CSS
    custom properties), fonts via `@import`. Same convention already proven
    live in `docs/squarespace/lead-form-embed.html`. Verified isolated in
    both directions with an adversarial test harness (colliding tag/class
    names like bare `main`, `.search`, `.song`, `.a` outside the wrapper) —
    nothing leaks in, nothing leaks out.
  - `songs.json` — machine-readable copy for future use by the
    create-proposal skill or the Growth Hour app.
  Edit design in `template.html` / `embed_template.html` (kept in sync by
  hand, see the maintenance note at the top of `embed_template.html`),
  content in the xlsx, wiring in `build.py`.
- **Squarespace setup (Adrian):** Insert Block → Code on whichever page you
  want it on, paste the whole contents of `embed.html`. No fonts/header
  injection step needed, it's all in the one block. If the site's own header
  is sticky and overlaps our sticky genre bar, or the charcoal cover feels
  redundant right under the site's own logo, say so and it's a quick tweak.
- **proposals.greenwayband.com/song-list:** the standalone `index.html`,
  useful for proposal emails/links specifically. Independent of the
  Squarespace embed; both can exist at once.

Palette: proposal tokens only — cover `#0A0A09`, body cream `#F5F2ED`, inks
`#111110`/`#2A2A27`, dims `#706D66`/`#8A867E`/`#4A4740`, hairlines
`rgba(10,10,9,.12/.16/.26)` and `rgba(245,242,237,…)` on the cover.
