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

## Updating the repertoire

Adrian never edits the xlsx himself. He just says what changed in chat
("add X by Y", "we don't play Z anymore", "rename this genre to..."), and
Claude does the edit + rebuild + resync every time, then reports back with a
PASS/FAIL. This is the whole convention — everything below is the mechanic
Claude follows, not a tool Adrian needs to touch.

- **The xlsx is one single alphabetical list, genre-tagged, not grouped by
  genre.** Row 5 is the header (`Song | Artist | Genre`), rows 6+ are songs,
  sorted A→Z across the whole catalog regardless of genre. `build.py` then
  regroups by the genre column for display — because the source is already
  alphabetical, each genre bucket comes out alphabetical too, for free, with
  **no sort code**. This only holds if edits go in at the right spot.
- **Adding a song:** insert a new row in correct alphabetical position by
  song title (ignore a leading "The"/"A" if that's the existing convention
  for neighboring rows — check a couple of neighbors before trusting it),
  matching the **exact existing genre string** from another song in that
  genre (e.g. `Reggae / Caribbean`, not `Reggae/Caribbean` — a mismatched
  string silently creates a new, duplicate genre bucket instead of joining
  the real one). Use `openpyxl` (`insert_rows`, not a manual append) so nothing
  else in the sheet shifts wrong. Never hand-edit the generated `index.html`
  or `embed.html` — they're overwritten by every rebuild.
- **Removing or renaming a song:** find the row, edit or delete it in place
  the same way.
- **Then always:** run `python3 build.py`, diff the printed genre counts
  against what you expect, spot-check the new/changed song rendered in the
  right place in `index.html`, then re-copy `index.html` to
  `~/Desktop/greenway-proposals/song-list/index.html` (the staged proposals
  copy is not auto-synced) and re-send `embed.html` to Adrian if the
  Squarespace copy needs updating too — Claude has no Squarespace access, so
  that file only updates live once Adrian re-pastes it in.
- **A new xlsx entirely** (Adrian hands over a whole new file): confirm the
  sheet name is still `SONG LIST` and the columns are still `Song | Artist |
  Genre` in that order, then `python3 build.py path/to/new.xlsx`.
