#!/usr/bin/env python3
"""Adrian Michael EPK generator (Boston outreach track).

Reads content.json (all copy, links, media wiring) and ../song-list/songs.json
(the 433-song authority) and generates three static pages:

    dist/adrian/index.html            lane chooser / general
    dist/adrian/solo/index.html       solo singer-guitarist lane
    dist/adrian/vocalist/index.html   lead/harmony vocalist lane

Deploy target: proposals.greenwayband.com (copy dist/adrian/ into
~/Desktop/greenway-proposals/ and run the usual proposals deploy, only on
Adrian's go). Pages are noindex until Adrian approves indexing.

Modes:
    python3 build.py                         # prod pages -> dist/adrian/
    python3 build.py --mode preview --out D  # same pages + assets copied next to them

Video hosting (Adrian's call, 2026-07-24): NO Vimeo. Videos are self-hosted
mp4s in /adrian/media/ on the proposals site, exactly like the proposal
template's ../assets/uptown-funk-2026a.mp4 pattern: poster facade, click swaps
in a native <video controls autoplay playsinline>. Nothing loads until click.

Copy integrity: every song title rendered comes from songs.json; nothing is
hand-typed here.
"""
import argparse
import html
import json
import os
import shutil
import re
import urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
SONGS_JSON = os.path.join(BASE, os.pardir, "song-list", "songs.json")

# ---------------------------------------------------------------- tokens/CSS
# Colors and type mirror the locked site tokens in src/styles/global.css
# (docs/DESIGN_SYSTEM.md): cream, never pure white; black/charcoal; muted grays;
# Bodoni Moda display over Plus Jakarta Sans body. No gold, no teal.
CSS = """
:root{
  --black:#0A0A09; --charcoal:#111110; --cream:#F5F2ED;
  --muted:#B8B4AC; --dim:#706D66; --faint:#4A4740;
  --font-display:'Bodoni Moda',serif; --font-body:'Plus Jakarta Sans',sans-serif;
  --pad:24px; --max:1100px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-font-smoothing:antialiased}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
body{font-family:var(--font-body);font-weight:300;background:var(--cream);color:var(--black);line-height:1.7;font-size:16px;overflow-x:hidden}
img{display:block;max-width:100%}
a{color:inherit}
.skip{position:absolute;left:-9999px;top:0;background:var(--cream);color:var(--black);padding:10px 16px;z-index:200}
.skip:focus{left:0}
:focus-visible{outline:2px solid var(--cream);outline-offset:3px}
main :focus-visible,footer :focus-visible{outline-color:var(--black)}

/* top bar (over dark hero) */
.top{position:absolute;top:0;left:0;right:0;z-index:20;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:20px var(--pad);color:var(--cream)}
.top .wordmark{font-family:var(--font-display);font-size:15px;letter-spacing:.28em;text-transform:uppercase;text-decoration:none;white-space:nowrap}
.top nav{display:flex;gap:18px;flex-wrap:wrap;justify-content:flex-end}
.top nav a{font-size:10px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;text-decoration:none;color:var(--muted);padding:4px 0}
.top nav a:hover,.top nav a[aria-current]{color:var(--cream)}
.top nav a[aria-current]{border-bottom:1px solid var(--cream)}
@media(max-width:640px){
  .top{flex-direction:column;align-items:flex-start;gap:10px;padding:16px var(--pad)}
  .top .wordmark{font-size:13px}
  .top nav{gap:14px;justify-content:flex-start}
}

/* hero */
.hero{position:relative;min-height:var(--hmh,88svh);display:flex;align-items:flex-end;background:var(--charcoal);color:var(--cream)}
.hero .bg,.hero .bg img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,9,.42) 0%,rgba(10,10,9,.28) 45%,rgba(10,10,9,.82) 100%)}
.hero .inner{position:relative;z-index:10;width:100%;max-width:var(--max);margin:0 auto;padding:120px var(--pad) 56px}
.eyebrow{font-size:11px;font-weight:600;letter-spacing:.35em;text-transform:uppercase;color:var(--muted)}
.hero h1{font-family:var(--font-display);font-weight:400;font-size:clamp(36px,6.4vw,72px);line-height:1.12;letter-spacing:.01em;margin:18px 0 20px;max-width:17ch}
.hero p{max-width:58ch;font-size:16px;color:var(--cream);opacity:.92}
.ctas{display:flex;gap:22px;align-items:center;flex-wrap:wrap;margin-top:32px}
.btn{display:inline-block;background:var(--cream);color:var(--black);font-size:11px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;text-decoration:none;padding:15px 34px;border:1px solid var(--cream);border-radius:0;transition:background 200ms ease-out,color 200ms ease-out}
.btn:hover{background:transparent;color:var(--cream)}
.btn.dark{background:var(--black);color:var(--cream);border-color:var(--black)}
.btn.dark:hover{background:transparent;color:var(--black)}
.textlink{font-size:11px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--cream);text-decoration:none;border-bottom:1px solid var(--dim);padding-bottom:3px}
.textlink:hover{border-color:var(--cream)}
main .textlink{color:var(--black);border-color:var(--muted)}
main .textlink:hover{border-color:var(--black)}

/* sections */
section{padding:80px var(--pad)}
.wrap{max-width:var(--max);margin:0 auto}
.label{font-size:11px;font-weight:600;letter-spacing:.35em;text-transform:uppercase;color:var(--dim);margin-bottom:28px}
.lede{font-family:var(--font-display);font-weight:400;font-size:clamp(26px,3.6vw,40px);line-height:1.2;max-width:24ch}

/* proof strip */
.proofband{background:var(--charcoal);color:var(--cream);padding:34px var(--pad)}
.proof{list-style:none;display:flex;flex-wrap:wrap;gap:10px 0;max-width:var(--max);margin:0 auto;justify-content:center}
.proof li{font-size:11px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);text-align:center;max-width:100%}
.proof li+li::before{content:"\\2022";margin:0 14px;color:var(--faint)}

/* media */
.media{margin-top:8px}
.media.h{max-width:880px}
.media.v{max-width:390px}
.media .frame{position:relative;width:100%;background:var(--charcoal)}
.media.h .frame{aspect-ratio:16/9}
.media.v .frame{aspect-ratio:9/16}
.facade{position:absolute;inset:0;width:100%;height:100%;display:block;border:0;padding:0;cursor:pointer;background:var(--charcoal)}
.facade picture,.facade img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.facade::after{content:"";position:absolute;inset:0;background:rgba(10,10,9,.18);transition:background 200ms ease-out}
.facade:hover::after{background:rgba(10,10,9,.05)}
.play{position:absolute;z-index:5;left:50%;top:50%;transform:translate(-50%,-50%);width:64px;height:64px;border:1px solid var(--cream);border-radius:50%;display:flex;align-items:center;justify-content:center;background:rgba(10,10,9,.35)}
.play svg{width:18px;height:18px;fill:var(--cream);margin-left:3px}
.frame iframe,.frame video{position:absolute;inset:0;width:100%;height:100%;border:0}
.cap{font-size:13px;color:var(--dim);margin-top:14px}
.mediarow{display:grid;gap:40px;margin-top:36px}
@media(min-width:900px){.mediarow{grid-template-columns:1fr 1fr}}
.note{font-size:14px;color:var(--dim);max-width:64ch;margin-top:18px}

/* role points */
.points{list-style:none;margin-top:30px;max-width:560px}
.points li{font-size:16px;padding:16px 0;border-bottom:1px solid rgba(10,10,9,.12)}
.points li:first-child{border-top:1px solid rgba(10,10,9,.12)}

/* repertoire */
.songgrid{display:grid;gap:40px 56px;margin-top:40px}
@media(min-width:700px){.songgrid{grid-template-columns:1fr 1fr}}
@media(min-width:1024px){.songgrid{grid-template-columns:1fr 1fr 1fr}}
.songcat h3{font-family:var(--font-display);font-weight:400;font-size:21px;margin-bottom:14px}
.songcat ul{list-style:none}
.songcat li{font-size:14px;color:var(--faint);padding:5px 0}
.songcat li span{color:var(--muted);font-size:12px}
.songfoot{margin-top:44px;display:flex;gap:24px;align-items:center;flex-wrap:wrap}
.songfoot .count{font-size:13px;color:var(--dim)}

/* lane cards (root) */
.lanes{display:grid;gap:28px;margin-top:40px}
@media(min-width:820px){.lanes{grid-template-columns:1fr 1fr}}
.lane{position:relative;display:block;text-decoration:none;color:var(--cream);background:var(--charcoal);min-height:420px;overflow:hidden}
.lane img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.72;transition:opacity 200ms ease-out,transform 400ms ease-out}
.lane:hover img{opacity:.6;transform:scale(1.015)}
.lane .laneinner{position:relative;z-index:5;display:flex;flex-direction:column;justify-content:flex-end;gap:10px;min-height:420px;padding:28px;background:linear-gradient(180deg,rgba(10,10,9,0) 40%,rgba(10,10,9,.78) 100%)}
.lane h2{font-family:var(--font-display);font-weight:400;font-size:30px}
.lane p{font-size:14px;color:var(--muted);max-width:44ch}
.lane .go{font-size:11px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;margin-top:8px;border-bottom:1px solid var(--dim);align-self:flex-start;padding-bottom:3px}

/* contact + footer */
.contactband{background:var(--charcoal);color:var(--cream)}
.contactband .lede{color:var(--cream)}
.contactband .label{color:var(--muted)}
.contactrow{display:flex;gap:22px;align-items:center;flex-wrap:wrap;margin-top:34px}
.phone{font-size:15px;letter-spacing:.06em;color:var(--cream);text-decoration:none;border-bottom:1px solid var(--dim);padding-bottom:3px}
.phone:hover{border-color:var(--cream)}
.outlinks{display:flex;gap:26px;flex-wrap:wrap;margin-top:36px}
.outlinks a{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);text-decoration:none}
.outlinks a:hover{color:var(--cream)}
.baseline{margin-top:30px;font-size:13px;color:var(--dim)}
footer{background:var(--charcoal);color:var(--faint);padding:28px var(--pad);border-top:1px solid rgba(245,242,237,.08)}
footer .wrap{display:flex;flex-wrap:wrap;gap:8px 28px;justify-content:space-between;font-size:12px}
@media(min-width:768px){
  :root{--pad:48px}
  section{padding:110px var(--pad)}
  .hero .inner{padding-bottom:72px}
}
"""

PLAY_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3.5v17l14-8.5z"/></svg>'

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
           "%3Ccircle cx='50' cy='50' r='48' fill='%23111110'/%3E"
           "%3Ctext x='50' y='63' font-size='34' text-anchor='middle' fill='%23F5F2ED'"
           " font-family='Georgia,serif' letter-spacing='2'%3EAM%3C/text%3E%3C/svg%3E")

FONTS = ("https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;0,500;1,400"
         "&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap")

SITE_ORIGIN = "https://proposals.greenwayband.com"

FACADE_JS = """
document.querySelectorAll('.facade').forEach(function(b){
  b.addEventListener('click',function(){
    var frame=b.parentElement;
    if(frame.querySelector('video'))return;
    var v=document.createElement('video');
    v.controls=true; v.autoplay=true; v.playsInline=true;
    v.setAttribute('playsinline','');
    v.src=b.dataset.src;
    v.setAttribute('aria-label',b.getAttribute('aria-label'));
    frame.replaceChildren(v);
  });
});
"""

esc = html.escape


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def pick_songs(rep):
    """Curated picks per category. Only titles that exist in songs.json render."""
    data = json.load(open(SONGS_JSON))
    by_genre = {g["name"]: g["songs"] for g in data["genres"]}
    total = data["total"]
    used = set()
    cards = []
    for cat in rep["categories"]:
        pool = []
        for g in cat["genres"]:
            pool += by_genre.get(g, [])
        index = {norm(s["song"]): s for s in pool}
        picks = []
        for want in cat["prefer"]:
            s = index.get(norm(want))
            if s and norm(s["song"]) not in used and len(picks) < 6:
                picks.append(s)
                used.add(norm(s["song"]))
        for s in pool:  # fill to six from the real list if preferences missed
            if len(picks) >= 6:
                break
            if norm(s["song"]) not in used:
                picks.append(s)
                used.add(norm(s["song"]))
        cards.append((cat["name"], picks))
    return cards, total


# ---------------------------------------------------------------- fragments

def picture(img_base, alt, assets, sizes="100vw", pos=None):
    style = f' style="object-position:{pos}"' if pos else ""
    has_800 = not img_base.endswith(("-720", "-1600"))
    if has_800:
        return (f'<picture><source type="image/webp" srcset="{assets}img/{img_base}-800.webp 800w, {assets}img/{img_base}-1600.webp 1600w" sizes="{sizes}">'
                f'<img src="{assets}img/{img_base}-800.jpg" srcset="{assets}img/{img_base}-800.jpg 800w, {assets}img/{img_base}-1600.jpg 1600w" sizes="{sizes}" alt="{esc(alt)}"{style} loading="lazy" decoding="async"></picture>')
    return (f'<picture><source type="image/webp" srcset="{assets}img/{img_base}.webp">'
            f'<img src="{assets}img/{img_base}.jpg" alt="{esc(alt)}"{style} loading="lazy" decoding="async"></picture>')


def head(title, desc, og_img, path):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="noindex, nofollow">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE_ORIGIN}/adrian/assets/img/{og_img}">
<meta property="og:url" content="{SITE_ORIGIN}{path}">
<meta property="og:type" content="profile">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<style>{CSS}</style>
<script>if(location.search.indexOf('capture')>-1)document.documentElement.style.setProperty('--hmh','900px')</script>
</head>"""


def topbar(root, active):
    def cur(k):
        return ' aria-current="page"' if active == k else ""
    return f"""<header class="top">
  <a class="wordmark" href="{root}">Adrian Michael</a>
  <nav aria-label="EPK">
    <a href="{root}solo/"{cur('solo')}>Solo</a>
    <a href="{root}vocalist/"{cur('vocalist')}>Vocalist</a>
    <a href="{root}../song-list/">Song List</a>
    <a href="#contact">Contact</a>
  </nav>
</header>"""


def hero(page, c, assets, ctas_html):
    return f"""<div class="hero">
  <div class="bg">{picture(page['hero_img'], f"Adrian Michael performing", assets, pos=page.get('hero_pos'))}</div>
  <div class="inner">
    <p class="eyebrow">{esc(c['identity']['eyebrow'])}</p>
    <h1>{esc(page['headline'])}</h1>
    <p>{esc(page['sub'])}</p>
    {ctas_html}
  </div>
</div>"""


def proofband(c):
    lis = "".join(f"<li>{esc(p)}</li>" for p in c["proof"])
    return f'<div class="proofband"><ul class="proof">{lis}</ul></div>'


def media_block(v, root, assets, extra=""):
    orient = "v" if v["orient"] == "v" else "h"
    cap = f'<p class="cap">{esc(v["caption"])}</p>' if v.get("caption") else ""
    return f"""<div class="media {orient} {extra}">
  <div class="frame">
    <button type="button" class="facade" data-src="{root}media/{esc(v['media'])}" aria-label="Play video: {esc(v['title'])}">
      {picture(v['poster'], v['title'], assets)}
      <span class="play">{PLAY_SVG}</span>
    </button>
  </div>
  {cap}
</div>"""


def repertoire(c, assets, root):
    cards, total = pick_songs(c["repertoire"])
    cats = ""
    for name, picks in cards:
        lis = "".join(f'<li>{esc(s["song"])} <span>&middot; {esc(s["artist"])}</span></li>' for s in picks)
        cats += f'<div class="songcat"><h3>{esc(name)}</h3><ul>{lis}</ul></div>'
    lede = f'<p class="lede">{esc(c["repertoire"]["intro"])}</p>' if c["repertoire"].get("intro") else ""
    return f"""<section id="songs">
  <div class="wrap">
    <h2 class="label">Repertoire</h2>
    {lede}
    <div class="songgrid">{cats}</div>
    <div class="songfoot">
      <a class="btn dark" href="{root}../song-list/">{esc(c['repertoire']['full_list_label'])}</a>
      <span class="count">{esc(c['repertoire']['footnote'])}</span>
    </div>
  </div>
</section>"""


def greenway_section(c, root, assets):
    return f"""<section id="greenway">
  <div class="wrap">
    <h2 class="label">With The Greenway Band</h2>
    {media_block(c['videos']['film'], root, assets)}
    <p class="note">{esc(c['identity']['disclosure'])}</p>
  </div>
</section>"""


def testimonial_section(c, root, assets):
    return f"""<section id="testimonial">
  <div class="wrap">
    <h2 class="label">Testimonial</h2>
    {media_block(c['videos']['testimonial'], root, assets)}
  </div>
</section>"""


def contact_section(c):
    ct = c["contact"]
    mail = f"mailto:{ct['email']}?subject={urllib.parse.quote(ct['email_subject'])}"
    links = "".join(f'<a href="{esc(l["href"])}" rel="noopener">{esc(l["label"])}</a>' for l in ct["links"])
    return f"""<section id="contact" class="contactband">
  <div class="wrap">
    <h2 class="label">Contact</h2>
    <p class="lede">Check availability.</p>
    <div class="contactrow">
      <a class="btn" href="{mail}">Email Adrian</a>
      <a class="phone" href="tel:{ct['phone_tel']}">{esc(ct['phone_display'])}</a>
    </div>
    <div class="outlinks">{links}</div>
    <p class="baseline">{esc(c['identity']['base_line'])}</p>
  </div>
</section>"""


def footer(c):
    return f"""<footer>
  <div class="wrap">
    <span>{esc(c['identity']['band_line'])}</span>
    <span>&copy; 2026 Adrian Michael</span>
  </div>
</footer>"""


def page_shell(c, headx, body, mode):
    return f"""{headx}
<body data-mode="{mode}">
<a class="skip" href="#main">Skip to content</a>
{body}
<script>{FACADE_JS}</script>
</body>
</html>
"""


# ---------------------------------------------------------------- pages

def build_lane(c, lane, mode):
    p = c[lane]
    assets, root = "../assets/", "../"
    ctas = (f'<div class="ctas"><a class="btn" href="{p["cta_primary"]["href"]}">{esc(p["cta_primary"]["label"])}</a>'
            f'<a class="textlink" href="{p["cta_secondary"]["href"]}">{esc(p["cta_secondary"]["label"])}</a></div>')
    if lane == "solo":
        watch = f"""<section id="watch">
  <div class="wrap">
    <h2 class="label">Watch</h2>
    {media_block(c['videos']['neon'], root, assets)}
  </div>
</section>"""
        mid = ""
    else:
        watch = f"""<section id="watch">
  <div class="wrap">
    <h2 class="label">Watch</h2>
    {media_block(c['videos']['reel'], root, assets)}
  </div>
</section>"""
        pts = "".join(f"<li>{esc(x)}</li>" for x in p["role_points"])
        mid = f"""<section id="role">
  <div class="wrap">
    <h2 class="label">In Your Band</h2>
    <ul class="points">{pts}</ul>
  </div>
</section>
<section id="solo-proof">
  <div class="wrap">
    <h2 class="label">Adrian, Solo</h2>
    {media_block(c['videos']['neon'], root, assets)}
  </div>
</section>"""
    body = f"""{topbar(root, lane)}
{hero(p, c, assets, ctas)}
{proofband(c)}
<main id="main">
{watch}
{mid}
{repertoire(c, assets, root) if lane == 'solo' else ''}
{greenway_section(c, root, assets)}
{'' if lane == 'solo' else repertoire(c, assets, root)}
{testimonial_section(c, root, assets)}
{contact_section(c)}
</main>
{footer(c)}"""
    path = f"/adrian/{lane}/"
    return page_shell(c, head(p["title"], p["description"], f"{p['hero_img']}-1600.jpg", path), body, mode)


def build_root(c, mode):
    p = c["root"]
    assets, root = "assets/", "./"
    lanes = ""
    for lane in p["lanes"]:
        img = lane["card_img"]
        base = f"{img}-800" if not img.endswith("-1600") else img
        lanes += f"""<a class="lane" href="{lane['slug']}/">
  <img src="assets/img/{base}.jpg" alt="" style="object-position:{lane['card_pos']}" loading="lazy" decoding="async">
  <span class="laneinner">
    <h2>{esc(lane['label'])}</h2>
    <p>{esc(lane['line'])}</p>
    <span class="go">{esc(lane['cta'])}</span>
  </span>
</a>"""
    ctas = ('<div class="ctas"><a class="btn" href="solo/">Watch Adrian Solo</a>'
            '<a class="textlink" href="vocalist/">Watch the Live Reel</a></div>')
    body = f"""{topbar(root, None)}
{hero(p, c, assets, ctas)}
{proofband(c)}
<main id="main">
<section id="lanes">
  <div class="wrap">
    <h2 class="label">Two Ways To Book Adrian</h2>
    <div class="lanes">{lanes}</div>
  </div>
</section>
{contact_section(c)}
</main>
{footer(c)}"""
    return page_shell(c, head(p["title"], p["description"], f"{p['hero_img']}-1600.jpg", "/adrian/"), body, mode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["prod", "preview"], default="prod")
    ap.add_argument("--out", default=os.path.join(BASE, "dist", "adrian"))
    a = ap.parse_args()
    c = json.load(open(os.path.join(BASE, "content.json")))
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    pages = {
        os.path.join(out, "index.html"): build_root(c, a.mode),
        os.path.join(out, "solo", "index.html"): build_lane(c, "solo", a.mode),
        os.path.join(out, "vocalist", "index.html"): build_lane(c, "vocalist", a.mode),
    }
    for path, htmlx in pages.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(htmlx)
        print("wrote", path, f"({len(htmlx)//1024}KB)")
    # preview builds need the assets alongside the pages
    dist_assets = os.path.join(BASE, "dist", "adrian", "assets")
    if a.mode == "preview" and os.path.abspath(out) != os.path.join(BASE, "dist", "adrian"):
        shutil.copytree(dist_assets, os.path.join(out, "assets"), dirs_exist_ok=True)
        print("copied assets ->", os.path.join(out, "assets"))


if __name__ == "__main__":
    main()
