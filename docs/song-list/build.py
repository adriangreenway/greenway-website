#!/usr/bin/env python3
"""Regenerate the Greenway song list page from the client xlsx.

Usage:
    python3 build.py [path/to/Greenway_Client_Song_List_vN.xlsx]

Reads the xlsx (default: the copy in this folder) and fills two shells with
the same song data:
    template.html       -> index.html    standalone hosted page
    embed_template.html -> embed.html    Squarespace Code Block embed
    songs.json                           machine-readable list for other tools

Content policy: every song, artist, and genre comes from the xlsx. Page copy
beyond that (wordmark, "Song List", search placeholder, footer links) is
fixed in the templates, not generated, and nothing else is added here.
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

DOT = '      <span class="dot">&middot;</span>'
nav_html = f"\n{DOT}\n".join(
    f'      <a class="chip" href="#{slug(g)}">{escape(display(g))}</a>'
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
        f'      </div>\n'
        f'      <ol class="songs">\n{items}\n      </ol>\n'
        f'    </section>'
    )
sections_html = "\n\n".join(sections)

TEMPLATE = (HERE / "template.html").read_text(encoding="utf-8")

page = (
    TEMPLATE
    .replace("@@NAV@@", nav_html)
    .replace("@@SECTIONS@@", sections_html)
)

(HERE / "index.html").write_text(page, encoding="utf-8")

# --- Squarespace embed: same content, prefixed markup, no <html>/<head>/<body> ---
DOT_EMBED = '      <span class="gw-dot">&middot;</span>'
nav_html_embed = f"\n{DOT_EMBED}\n".join(
    f'      <a class="gw-chip" href="#gw-{slug(g)}">{escape(display(g))}</a>'
    for g in order
)

sections_embed = []
for g in order:
    items = "\n".join(
        f'        <li class="gw-song" data-q="{escape(search_key(s["song"], s["artist"]))}">'
        f'<span class="gw-title">{escape(display(s["song"]))}</span>'
        f'<span class="gw-artist">{escape(display(s["artist"]))}</span></li>'
        for s in buckets[g]
    )
    sections_embed.append(
        f'    <div class="gw-genre" id="gw-{slug(g)}">\n'
        f'      <div class="gw-genre-head">\n'
        f'        <h2>{escape(display(g))}</h2>\n'
        f'      </div>\n'
        f'      <ol class="gw-songs">\n{items}\n      </ol>\n'
        f'    </div>'
    )
sections_html_embed = "\n\n".join(sections_embed)

EMBED_TEMPLATE = (HERE / "embed_template.html").read_text(encoding="utf-8")
embed = (
    EMBED_TEMPLATE
    .replace("@@NAV@@", nav_html_embed)
    .replace("@@SECTIONS@@", sections_html_embed)
)
# Squarespace's Code Block re-encoded our UTF-8 bytes as MacRoman on paste
# (2026-07-24: every curly apostrophe rendered as "Can,Aot"). The embed has no
# <head> of its own, so it cannot declare a charset and is at the mercy of
# whatever the host CMS does. Emitting pure ASCII with numeric entities makes
# the file immune to that. index.html is unaffected — it declares UTF-8 itself.
embed = embed.encode("ascii", "xmlcharrefreplace").decode("ascii")
(HERE / "embed.html").write_text(embed, encoding="ascii")

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
print("wrote:    index.html, embed.html, songs.json")
