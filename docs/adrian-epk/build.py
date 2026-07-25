#!/usr/bin/env python3
"""Adrian Michael EPK generator (Boston outreach track).

Reads content.json (all copy, links, media wiring) and generates one static
page:

    dist/adrian/index.html

Correction brief v1 (2026-07-24) unified the prior three-page solo/vocalist
lane structure into this single page. Deploy target: proposals.greenwayband.com
(copy dist/adrian/ into ~/Desktop/greenway-proposals/ and run the usual
proposals deploy, only on Adrian's go). Page carries noindex until Adrian
approves indexing.

Modes:
    python3 build.py                         # prod page -> dist/adrian/
    python3 build.py --mode preview --out D  # same page + assets copied alongside

Video hosting (Adrian's call, 2026-07-24): NO Vimeo. Video is a self-hosted
mp4 in /adrian/media/ on the proposals site, exactly like the proposal
template's ../assets/uptown-funk-2026a.mp4 pattern: poster facade, click swaps
in a native <video controls autoplay playsinline>. Nothing loads until click.
"""
import argparse
import html
import json
import os
import shutil
import urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))

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
#reel :focus-visible,#experience :focus-visible{outline-color:var(--black)}

/* top bar (over dark hero) */
.top{position:absolute;top:0;left:0;right:0;z-index:20;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:20px var(--pad);color:var(--cream)}
.top .wordmark{font-family:var(--font-display);font-size:15px;letter-spacing:.28em;text-transform:uppercase;text-decoration:none;white-space:nowrap}
.top nav{display:flex;gap:18px;flex-wrap:wrap;justify-content:flex-end}
.top nav a{font-size:10px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;text-decoration:none;color:var(--muted);display:inline-flex;align-items:center;min-height:44px;padding:0 2px}
.top nav a:hover{color:var(--cream)}
@media(max-width:640px){
  .top{flex-direction:column;align-items:flex-start;gap:2px;padding:12px var(--pad)}
  .top .wordmark{font-size:13px}
  .top nav{gap:8px;justify-content:flex-start}
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
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;background:var(--cream);color:var(--black);font-size:11px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;text-decoration:none;padding:0 34px;border:1px solid var(--cream);border-radius:0;transition:background 200ms ease-out,color 200ms ease-out}
.btn:hover{background:transparent;color:var(--cream)}
.textlink{font-size:11px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--cream);text-decoration:none;border-bottom:1px solid var(--dim);padding-bottom:3px}
.textlink:hover{border-color:var(--cream)}
.explink .textlink{color:var(--black);border-color:var(--muted)}
.explink .textlink:hover{border-color:var(--black)}

/* sections */
section{padding:80px var(--pad)}
.wrap{max-width:var(--max);margin:0 auto}
.label{font-size:11px;font-weight:600;letter-spacing:.35em;text-transform:uppercase;color:var(--faint);margin-bottom:28px}
.lede{font-family:var(--font-display);font-weight:400;font-size:clamp(26px,3.6vw,40px);line-height:1.2;max-width:24ch}
.bodytext{font-size:17px;line-height:1.7;max-width:58ch;margin-top:6px}
.range{font-size:14px;letter-spacing:.02em;color:var(--faint);margin-top:20px}
.explink{margin-top:26px}

/* proof strip */
.proofband{background:var(--charcoal);color:var(--cream);padding:34px var(--pad)}
.proof{list-style:none;display:flex;flex-wrap:wrap;gap:10px 0;max-width:var(--max);margin:0 auto;justify-content:center}
.proof li{font-size:11px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);text-align:center;max-width:100%}
.proof li+li::before{content:"\\2022";margin:0 14px;color:var(--faint)}

/* media */
.media{margin-top:8px}
.media.h{max-width:880px}
.media .frame{position:relative;width:100%;background:var(--charcoal)}
.media.h .frame{aspect-ratio:16/9}
.facade{position:absolute;inset:0;width:100%;height:100%;display:block;border:0;padding:0;cursor:pointer;background:var(--charcoal)}
.facade picture,.facade img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.facade::after{content:"";position:absolute;inset:0;background:rgba(10,10,9,.18);transition:background 200ms ease-out}
.facade:hover::after{background:rgba(10,10,9,.05)}
.play{position:absolute;z-index:5;left:50%;top:50%;transform:translate(-50%,-50%);width:64px;height:64px;border:1px solid var(--cream);border-radius:50%;display:flex;align-items:center;justify-content:center;background:rgba(10,10,9,.35)}
.play svg{width:18px;height:18px;fill:var(--cream);margin-left:3px}
.frame iframe,.frame video{position:absolute;inset:0;width:100%;height:100%;border:0}
.cap{font-size:13px;color:var(--faint);margin-top:14px}
.vstate{position:absolute;left:0;right:0;bottom:0;z-index:8;display:none;align-items:center;justify-content:center;gap:8px 16px;flex-wrap:wrap;text-align:center;padding:12px 16px;font-size:12px;line-height:1.5;color:var(--muted);background:rgba(10,10,9,.82)}
.frame.busy .vstate--loading{display:flex}
.frame.failed .vstate--error{display:flex}
.vstate button,.vstate a{font:inherit;color:var(--cream);background:none;border:0;padding:0;text-decoration:underline;cursor:pointer}
.reelcta{margin-top:28px}

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
footer{background:var(--charcoal);color:var(--muted);padding:28px var(--pad);border-top:1px solid rgba(245,242,237,.08)}
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
document.querySelectorAll('.facade').forEach(function(btn){
  btn.addEventListener('click', function(){
    var frame = btn.parentElement;
    if (frame.classList.contains('busy') || frame.querySelector('video')) return;
    frame.classList.remove('failed');
    frame.classList.add('busy');
    var src = btn.dataset.src;
    var v = document.createElement('video');
    v.controls = true;
    v.autoplay = true;
    v.playsInline = true;
    v.setAttribute('playsinline', '');
    v.setAttribute('aria-label', btn.getAttribute('aria-label'));
    v.style.opacity = '0';
    v.addEventListener('playing', function(){
      frame.classList.remove('busy');
      v.style.opacity = '';
      btn.remove();
    });
    v.addEventListener('error', function(){
      v.remove();
      frame.classList.remove('busy');
      frame.classList.add('failed');
    });
    frame.appendChild(v);
    v.src = src;
  });
});
document.querySelectorAll('.retry').forEach(function(btn){
  btn.addEventListener('click', function(){
    var frame = btn.closest('.frame');
    frame.classList.remove('failed');
    var facade = frame.querySelector('.facade');
    if (facade) facade.click();
  });
});
"""

esc = html.escape


# ---------------------------------------------------------------- fragments

def picture(img_base, alt, sizes="100vw", pos=None, eager=False):
    style = f' style="object-position:{pos}"' if pos else ""
    attrs = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    has_800 = not img_base.endswith(("-720", "-1600"))
    if has_800:
        return (f'<picture><source type="image/webp" srcset="assets/img/{img_base}-800.webp 800w, assets/img/{img_base}-1600.webp 1600w" sizes="{sizes}">'
                f'<img src="assets/img/{img_base}-800.jpg" srcset="assets/img/{img_base}-800.jpg 800w, assets/img/{img_base}-1600.jpg 1600w" sizes="{sizes}" alt="{esc(alt)}"{style} {attrs}></picture>')
    return (f'<picture><source type="image/webp" srcset="assets/img/{img_base}.webp">'
            f'<img src="assets/img/{img_base}.jpg" alt="{esc(alt)}"{style} {attrs}></picture>')


def head(title, desc, og_path, path):
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
<meta property="og:image" content="{SITE_ORIGIN}/adrian/{og_path}">
<meta property="og:url" content="{SITE_ORIGIN}{path}">
<meta property="og:type" content="profile">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<style>{CSS}</style>
<script>if(location.search.indexOf('capture')>-1)document.documentElement.style.setProperty('--hmh','900px')</script>
</head>"""


def topbar():
    return """<header class="top">
  <a class="wordmark" href="#">Adrian Michael</a>
  <nav aria-label="Primary">
    <a href="#reel">Reel</a>
    <a href="#experience">Experience</a>
    <a href="#contact">Contact</a>
  </nav>
</header>"""


def hero(c, mailto):
    h = c["hero"]
    ctas = (f'<div class="ctas"><a class="btn" href="{h["cta_primary"]["href"]}">{esc(h["cta_primary"]["label"])}</a>'
            f'<a class="textlink" href="{mailto}">{esc(h["cta_secondary_label"])}</a></div>')
    return f"""<div class="hero">
  <div class="bg">{picture(h['hero_img'], "Adrian Michael performing", pos=h.get('hero_pos'), eager=True)}</div>
  <div class="inner">
    <p class="eyebrow">{esc(h['eyebrow'])}</p>
    <h1>{esc(h['headline'])}</h1>
    <p>{esc(h['sub'])}</p>
    {ctas}
  </div>
</div>"""


def proofband(c):
    lis = "".join(f"<li>{esc(p)}</li>" for p in c["proof"])
    return f'<div class="proofband"><ul class="proof">{lis}</ul></div>'


def media_block(v):
    orient = "v" if v["orient"] == "v" else "h"
    cap = f'<p class="cap">{esc(v["caption"])}</p>' if v.get("caption") else ""
    src = f"media/{esc(v['media'])}"
    return f"""<div class="media {orient}">
  <div class="frame">
    <button type="button" class="facade" data-src="{src}" aria-label="Play video: {esc(v['title'])}">
      {picture(v['poster'], v['title'])}
      <span class="play">{PLAY_SVG}</span>
    </button>
    <div class="vstate vstate--loading" aria-hidden="true"><span>Loading video&hellip;</span></div>
    <div class="vstate vstate--error">
      <span>Playback failed.</span>
      <button type="button" class="retry">Try again</button>
      <a href="{src}">Open the video directly</a>
    </div>
  </div>
  {cap}
</div>"""


def reel_section(c, mailto):
    r = c["reel"]
    return f"""<section id="reel">
  <div class="wrap">
    <h2 class="label">{esc(r['label'])}</h2>
    {media_block(r['video'])}
    <div class="reelcta"><a class="btn" href="{mailto}">{esc(r['cta_label'])}</a></div>
  </div>
</section>"""


def experience_section(c):
    e = c["experience"]
    link = (f'<p class="explink"><a class="textlink" href="{esc(e["link"]["href"])}" rel="noopener">{esc(e["link"]["label"])}</a></p>'
            if e.get("link") else "")
    return f"""<section id="experience">
  <div class="wrap">
    <h2 class="label">{esc(e['label'])}</h2>
    <p class="bodytext">{esc(e['copy'])}</p>
    <p class="range">{esc(e['range'])}</p>
    {link}
  </div>
</section>"""


def contact_section(c, mailto):
    ct = c["contact"]
    links = "".join(f'<a href="{esc(l["href"])}" rel="noopener">{esc(l["label"])}</a>' for l in ct["links"])
    return f"""<section id="contact" class="contactband">
  <div class="wrap">
    <h2 class="label">{esc(ct['label'])}</h2>
    <p class="lede">{esc(ct['headline'])}</p>
    <div class="contactrow">
      <a class="btn" href="{mailto}">{esc(ct['cta_label'])}</a>
      <a class="phone" href="tel:{ct['phone_tel']}">{esc(ct['phone_display'])}</a>
    </div>
    <div class="outlinks">{links}</div>
  </div>
</section>"""


def footer(c):
    return f"""<footer>
  <div class="wrap">
    <span>{esc(c['footer']['disclosure'])}</span>
    <span>&copy; 2026 Adrian Michael</span>
  </div>
</footer>"""


def page_shell(headx, body, mode):
    return f"""{headx}
<body data-mode="{mode}">
<a class="skip" href="#main">Skip to content</a>
{body}
<script>{FACADE_JS}</script>
</body>
</html>
"""


# ---------------------------------------------------------------- page

def build_page(c, mode):
    m = c["meta"]
    mailto = f"mailto:{c['contact']['email']}?subject={urllib.parse.quote(c['contact']['email_subject'])}"
    body = f"""{topbar()}
<main id="main">
{hero(c, mailto)}
{proofband(c)}
{reel_section(c, mailto)}
{experience_section(c)}
{contact_section(c, mailto)}
</main>
{footer(c)}"""
    return page_shell(head(m["title"], m["description"], "assets/email/card-universal.jpg", "/adrian/"), body, mode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["prod", "preview"], default="prod")
    ap.add_argument("--out", default=os.path.join(BASE, "dist", "adrian"))
    a = ap.parse_args()
    c = json.load(open(os.path.join(BASE, "content.json")))
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "index.html")
    htmlx = build_page(c, a.mode)
    with open(path, "w") as f:
        f.write(htmlx)
    print("wrote", path, f"({len(htmlx)//1024}KB)")
    # preview builds need the assets alongside the page
    dist_assets = os.path.join(BASE, "dist", "adrian", "assets")
    if a.mode == "preview" and os.path.abspath(out) != os.path.join(BASE, "dist", "adrian"):
        shutil.copytree(dist_assets, os.path.join(out, "assets"), dirs_exist_ok=True)
        print("copied assets ->", os.path.join(out, "assets"))


if __name__ == "__main__":
    main()
