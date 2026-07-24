#!/usr/bin/env python3
"""Regenerate the Greenway song list page from the client xlsx.

Usage:
    python3 build.py [path/to/Greenway_Client_Song_List_vN.xlsx]

Reads the xlsx (default: the copy in this folder), writes:
    index.html   the client-facing page (white + green, Greenway design system)
    songs.json   machine-readable list for other tools (proposals, Growth Hour)

Content policy: every song, artist, genre, and line of copy on the page comes
from the xlsx. Nothing is invented here. The total count is computed from the
actual rows so the number on the page can never drift from the list.
"""
import json
import re
import sys
import unicodedata
import zipfile
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
XLSX = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "Greenway_Client_Song_List_v4.xlsx"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
T = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"


def read_rows(path):
    z = zipfile.ZipFile(path)
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rid = wb.find("m:sheets", NS)[0].get(
        "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    )
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = next(r.get("Target") for r in rels if r.get("Id") == rid).lstrip("/")
    if not target.startswith("xl/"):
        target = "xl/" + target
    shared = []
    try:
        sst = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in sst.findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter(T)))
    except KeyError:
        pass

    def val(c):
        t, v = c.get("t"), c.find("m:v", NS)
        if t == "inlineStr":
            return "".join(x.text or "" for x in c.iter(T))
        if v is None:
            return ""
        return shared[int(v.text)] if t == "s" else v.text

    rows = []
    sheet = ET.fromstring(z.read(target))
    for row in sheet.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row"):
        cells = {}
        for c in row.findall("m:c", NS):
            col = re.match(r"[A-Z]+", c.get("r", "")or "?").group(0)
            cells[col] = (val(c) or "").strip()
        if any(cells.values()):
            rows.append(cells)
    return rows


def display(s):
    """Typography only: curly apostrophes, collapsed whitespace. No rewording."""
    return re.sub(r"\s+", " ", s.replace("'", "’")).strip()


def search_key(*parts):
    s = " ".join(parts).lower().replace("’", "'")
    s = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in s if not unicodedata.combining(ch))


def slug(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


rows = read_rows(XLSX)
doc_title = rows[0].get("A", "")
doc_subtitle = rows[1].get("A", "")
doc_note = rows[2].get("A", "")

songs, skipped = [], []
for r in rows[4:]:
    a, b, c = r.get("A", ""), r.get("B", ""), r.get("C", "")
    if a and b:
        songs.append({"song": a, "artist": b, "genre": c})
    elif a or b:
        skipped.append(r)

no_genre = [s for s in songs if not s["genre"]]
for s in no_genre:
    s["genre"] = "More Favorites"

order, buckets = [], {}
for s in songs:
    if s["genre"] not in buckets:
        buckets[s["genre"]] = []
        order.append(s["genre"])
    buckets[s["genre"]].append(s)

# Largest genres first; Holiday always last (seasonal).
order.sort(key=lambda g: (g == "Holiday", -len(buckets[g]), g))

total = len(songs)
# The number on the page is always the computed total, never a typed claim.
subtitle = re.sub(r"^\d+", str(total), doc_subtitle) if re.match(r"^\d+", doc_subtitle) else doc_subtitle

nav_html = "\n".join(
    f'      <a class="chip" href="#{slug(g)}">{escape(display(g))}'
    f'<span class="chip-n">{len(buckets[g])}</span></a>'
    for g in order
)

sections = []
for g in order:
    items = "\n".join(
        f'        <li class="song" data-q="{escape(search_key(s["song"], s["artist"]))}">'
        f'<span class="t">{escape(display(s["song"]))}</span>'
        f'<span class="a">{escape(display(s["artist"]))}</span></li>'
        for s in buckets[g]
    )
    sections.append(
        f'    <section class="genre" id="{slug(g)}">\n'
        f'      <div class="genre-head">\n'
        f'        <h2>{escape(display(g))}</h2>\n'
        f'        <span class="genre-n">{len(buckets[g])} songs</span>\n'
        f'      </div>\n'
        f'      <ol class="songs">\n{items}\n      </ol>\n'
        f'    </section>'
    )
sections_html = "\n\n".join(sections)

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Song List &middot; The Greenway Band</title>
<meta name="description" content="@@SUBTITLE_PLAIN@@ Live wedding and event band.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='48' fill='%231D392B'/%3E%3Ctext x='50' y='66' font-size='46' text-anchor='middle' fill='%23F5F2ED' font-family='Georgia,serif'%3EG%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;0,500;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  :root {
    --paper: #FBFAF8;
    --mist: #F1F4EF;
    --hairline: #E3E8E0;
    --green-deep: #1D392B;
    --green-deeper: #162D21;
    --green: #27503A;
    --green-dim: #57705F;
    --ink: #161B17;
    --dim: #5E6962;
    --cream: #F5F2ED;
    --cream-dim: #C7D2C4;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html { scroll-behavior: smooth; -webkit-font-smoothing: antialiased; }
  body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 300;
    background: var(--paper);
    color: var(--ink);
  }

  /* ---------- Hero ---------- */
  .hero {
    background: linear-gradient(180deg, var(--green-deep) 0%, var(--green-deeper) 100%);
    color: var(--cream);
    text-align: center;
    padding: 76px 24px 68px;
  }
  .logo-rule { width: 72px; height: 1px; background: rgba(245,242,237,.28); margin: 0 auto; }
  .logo-the  { font-size: 10px; letter-spacing: 5px; padding-left: 5px; color: var(--cream-dim); margin: 18px 0 6px; }
  .logo-name { font-family: 'Bodoni Moda', serif; font-size: 30px; font-weight: 400; letter-spacing: 10px; padding-left: 10px; }
  .logo-band { font-size: 11px; letter-spacing: 11px; padding-left: 11px; color: var(--cream-dim); margin: 6px 0 18px; }
  .hero h1 {
    font-family: 'Bodoni Moda', serif;
    font-weight: 400;
    font-size: clamp(42px, 6.5vw, 60px);
    line-height: 1.15;
    letter-spacing: 1px;
    margin-top: 40px;
  }
  .hero .subtitle {
    font-family: 'Bodoni Moda', serif;
    font-style: italic;
    font-size: 15px;
    letter-spacing: 1.2px;
    color: var(--cream-dim);
    margin-top: 16px;
  }
  .hero .note {
    font-size: 12px;
    font-weight: 400;
    letter-spacing: .4px;
    color: rgba(245,242,237,.62);
    margin-top: 26px;
  }

  /* ---------- Sticky genre bar ---------- */
  .bar {
    position: sticky; top: 0; z-index: 50;
    background: rgba(251,250,248,.94);
    -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--hairline);
  }
  .bar-inner {
    max-width: 1080px; margin: 0 auto;
    padding: 12px 24px;
    display: flex; align-items: center; gap: 14px;
  }
  .chips {
    display: flex; gap: 8px; flex: 1;
    overflow-x: auto; scrollbar-width: none;
  }
  .chips::-webkit-scrollbar { display: none; }
  .chip {
    flex: 0 0 auto;
    font-size: 10px; font-weight: 500;
    letter-spacing: 1.6px; text-transform: uppercase;
    color: var(--green); text-decoration: none;
    border: 1px solid var(--hairline);
    border-radius: 999px;
    padding: 7px 13px;
    transition: background .18s ease, border-color .18s ease;
    white-space: nowrap;
  }
  .chip:hover { background: var(--mist); border-color: var(--cream-dim); }
  .chip-n { color: var(--green-dim); margin-left: 6px; font-weight: 400; }
  .search {
    flex: 0 0 210px;
    font-family: inherit; font-size: 13px; font-weight: 400;
    color: var(--ink);
    background: var(--paper);
    border: 1px solid var(--hairline);
    border-radius: 999px;
    padding: 8px 16px;
    outline: none;
    transition: border-color .18s ease;
  }
  .search::placeholder { color: var(--dim); }
  .search:focus { border-color: var(--green); }

  /* ---------- Sections ---------- */
  main { max-width: 1080px; margin: 0 auto; padding: 20px 24px 40px; }
  .genre { padding-top: 44px; scroll-margin-top: 74px; }
  .genre-head {
    display: flex; align-items: baseline; justify-content: space-between;
    border-bottom: 1px solid var(--hairline);
    padding-bottom: 12px;
  }
  .genre-head h2 {
    font-family: 'Bodoni Moda', serif;
    font-weight: 400; font-size: 24px; letter-spacing: .5px;
  }
  .genre-n { font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: var(--green-dim); }
  .songs { list-style: none; margin-top: 4px; }
  @media (min-width: 760px) { .songs { columns: 2; column-gap: 64px; } }
  .song {
    display: flex; flex-direction: column;
    padding: 9px 2px;
    border-bottom: 1px solid var(--hairline);
    break-inside: avoid;
  }
  .song .t { font-size: 14.5px; font-weight: 500; letter-spacing: .1px; }
  .song .a { font-size: 12.5px; font-weight: 400; color: var(--dim); margin-top: 1px; }
  .no-results {
    display: none;
    text-align: center; color: var(--dim);
    font-size: 14px; padding: 72px 0 40px;
  }
  .no-results em { font-family: 'Bodoni Moda', serif; font-size: 17px; color: var(--green); font-style: italic; }

  /* ---------- Footer ---------- */
  footer {
    text-align: center;
    border-top: 1px solid var(--hairline);
    margin-top: 64px;
    padding: 48px 24px 64px;
  }
  footer .tail-note {
    font-family: 'Bodoni Moda', serif; font-style: italic;
    font-size: 15px; color: var(--green);
    letter-spacing: .5px;
  }
  footer .contact { margin-top: 18px; font-size: 12px; letter-spacing: .6px; }
  footer .contact a {
    color: var(--green-dim); text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color .18s ease, color .18s ease;
  }
  footer .contact a:hover { color: var(--green); border-bottom-color: var(--cream-dim); }
  footer .dot { color: var(--cream-dim); margin: 0 8px; }

  /* ---------- Mobile ---------- */
  @media (max-width: 640px) {
    .hero { padding: 56px 20px 48px; }
    .bar-inner { flex-wrap: wrap; gap: 10px; padding: 10px 16px; }
    .search { flex: 1 1 100%; order: -1; }
    main { padding: 12px 20px 32px; }
  }

  /* ---------- Print ---------- */
  @media print {
    .bar, .no-results { display: none; }
    .hero { background: none; color: var(--green-deep); padding: 0 0 24px; }
    .hero .subtitle, .hero .note { color: var(--green); }
    .logo-rule { background: var(--green-deep); }
    .logo-the, .logo-band { color: var(--green); }
    .hero h1 { margin-top: 16px; font-size: 34px; }
    .genre { padding-top: 24px; }
    .songs { columns: 2; column-gap: 40px; }
    .song { padding: 4px 0; border-bottom: none; }
    footer { margin-top: 24px; padding: 16px 0 0; border-top: 1px solid var(--green-deep); }
  }
</style>
</head>
<body>

<header class="hero">
  <div class="logo-rule"></div>
  <div class="logo-the">THE</div>
  <div class="logo-name">GREENWAY</div>
  <div class="logo-band">BAND</div>
  <div class="logo-rule"></div>
  <h1>Song List</h1>
  <p class="subtitle">@@SUBTITLE@@</p>
  <p class="note">@@NOTE@@</p>
</header>

<nav class="bar" aria-label="Genres">
  <div class="bar-inner">
    <div class="chips">
@@NAV@@
    </div>
    <input class="search" id="q" type="search" placeholder="Search songs or artists" aria-label="Search songs or artists">
  </div>
</nav>

<main>
@@SECTIONS@@
  <div class="no-results" id="none">
    <em>No matches.</em><br><br>@@NOTE@@
  </div>
</main>

<footer>
  <div class="tail-note">@@NOTE@@</div>
  <p class="contact">
    <a href="https://greenwayband.com">greenwayband.com</a><span class="dot">&middot;</span><a href="mailto:adrian@greenwayband.com">adrian@greenwayband.com</a>
  </p>
</footer>

<script>
  (function () {
    var q = document.getElementById('q');
    var none = document.getElementById('none');
    var songs = [].slice.call(document.querySelectorAll('.song'));
    var sections = [].slice.call(document.querySelectorAll('.genre'));
    function fold(s) {
      return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').replace(/\\u2019/g, "'");
    }
    q.addEventListener('input', function () {
      var needle = fold(q.value.trim());
      var any = false;
      songs.forEach(function (li) {
        var hit = !needle || li.getAttribute('data-q').indexOf(needle) !== -1;
        li.style.display = hit ? '' : 'none';
        if (hit) any = true;
      });
      sections.forEach(function (sec) {
        var visible = sec.querySelectorAll('.song:not([style*="none"])').length > 0;
        sec.style.display = visible ? '' : 'none';
      });
      none.style.display = any ? 'none' : 'block';
    });
  })();
</script>

</body>
</html>
"""

page = (
    TEMPLATE
    .replace("@@SUBTITLE_PLAIN@@", escape(display(subtitle)) + ".")
    .replace("@@SUBTITLE@@", escape(display(subtitle)))
    .replace("@@NOTE@@", escape(display(doc_note)))
    .replace("@@NAV@@", nav_html)
    .replace("@@SECTIONS@@", sections_html)
)

(HERE / "index.html").write_text(page, encoding="utf-8")
(HERE / "songs.json").write_text(
    json.dumps(
        {
            "title": doc_title,
            "subtitle": subtitle,
            "note": doc_note,
            "total": total,
            "source": XLSX.name,
            "genres": [
                {"name": g, "count": len(buckets[g]),
                 "songs": [{"song": s["song"], "artist": s["artist"]} for s in buckets[g]]}
                for g in order
            ],
        },
        indent=1,
        ensure_ascii=False,
    ) + "\n",
    encoding="utf-8",
)

print(f"source:   {XLSX}")
print(f"total:    {total} songs (doc subtitle said: {doc_subtitle!r})")
print(f"genres:   " + ", ".join(f"{g} {len(buckets[g])}" for g in order))
if no_genre:
    print(f"WARNING:  {len(no_genre)} songs had no genre, filed under 'More Favorites'")
if skipped:
    print(f"WARNING:  {len(skipped)} partial rows skipped: {skipped}")
print("wrote:    index.html, songs.json")
