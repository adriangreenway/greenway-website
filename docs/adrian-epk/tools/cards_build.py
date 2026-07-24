#!/usr/bin/env python3
"""Email thumbnail cards (1200x675) + reel end card (1920x1080).
Rendered by headless Chrome straight off the filesystem, so this needs no
preview server and no particular port. Run after assets_build.py."""
import os, subprocess
from PIL import Image

DIST = os.path.expanduser("~/greenway-website/docs/adrian-epk/dist/adrian")
IMG = os.path.join(DIST, "assets", "img")
DIST_EMAIL = os.path.join(DIST, "assets", "email")
RENDERS = os.path.expanduser("~/Desktop/EPK/renders")
CARDS = os.path.join(RENDERS, "_cards")          # scratch for the html + png
CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for d in (DIST_EMAIL, RENDERS, CARDS):
    os.makedirs(d, exist_ok=True)

FONTS = ("https://fonts.googleapis.com/css2?family=Bodoni+Moda:wght@400;500"
         "&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap")

CARD_TPL = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="{fonts}" rel="stylesheet">
<style>
  * {{ margin:0; box-sizing:border-box; }}
  body {{ width:1200px; height:675px; overflow:hidden; background:#111110; position:relative;
         font-family:'Plus Jakarta Sans',sans-serif; }}
  img.bg {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:{pos}; }}
  .shade {{ position:absolute; inset:0;
           background:linear-gradient(180deg,rgba(10,10,9,.18) 0%,rgba(10,10,9,.12) 55%,rgba(10,10,9,.86) 100%); }}
  .play {{ position:absolute; left:50%; top:44%; transform:translate(-50%,-50%);
          width:104px; height:104px; border:2px solid #F5F2ED; border-radius:50%;
          background:rgba(10,10,9,.38); display:flex; align-items:center; justify-content:center; }}
  .play svg {{ width:34px; height:34px; fill:#F5F2ED; margin-left:6px; }}
  .txt {{ position:absolute; left:56px; right:56px; bottom:44px; color:#F5F2ED; }}
  .eyebrow {{ font-size:17px; font-weight:600; letter-spacing:.32em; color:#B8B4AC; margin-bottom:14px; }}
  h1 {{ font-family:'Bodoni Moda',serif; font-weight:400; font-size:52px; letter-spacing:.01em; }}
</style></head><body>
<img class="bg" src="{img}">
<div class="shade"></div>
<div class="play"><svg viewBox="0 0 24 24"><path d="M6 3.5v17l14-8.5z"/></svg></div>
<div class="txt"><div class="eyebrow">ADRIAN MICHAEL &bull; BOSTON</div><h1>{title}</h1></div>
</body></html>"""

END_TPL = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="{fonts}" rel="stylesheet">
<style>
  * {{ margin:0; box-sizing:border-box; }}
  body {{ width:1920px; height:1080px; background:#111110; color:#F5F2ED;
         font-family:'Plus Jakarta Sans',sans-serif; display:flex; align-items:center; justify-content:center; }}
  .in {{ text-align:center; }}
  .rule {{ width:88px; height:1px; background:rgba(245,242,237,.35); margin:0 auto 42px; }}
  .eyebrow {{ font-size:19px; font-weight:600; letter-spacing:.42em; color:#B8B4AC; margin-bottom:30px; }}
  h1 {{ font-family:'Bodoni Moda',serif; font-weight:400; font-size:124px; letter-spacing:.06em; margin-bottom:34px; }}
  .roles {{ font-size:23px; font-weight:500; letter-spacing:.3em; color:#B8B4AC; margin-bottom:66px; }}
  .contact {{ font-size:21px; font-weight:400; letter-spacing:.14em; color:#706D66; }}
</style></head><body>
<div class="in">
  <div class="rule"></div>
  <div class="eyebrow">BOSTON &bull; NEW ENGLAND</div>
  <h1>ADRIAN MICHAEL</h1>
  <div class="roles">LEAD &amp; HARMONY VOCALS &nbsp;&bull;&nbsp; ACOUSTIC GUITAR</div>
  <div class="contact">ADRIAN@GREENWAYBAND.COM &nbsp;&bull;&nbsp; (281)&nbsp;467-1226</div>
</div>
</body></html>"""

def shoot(html_path, png_path, w, h):
    subprocess.run([CH, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--allow-file-access-from-files",
                    "--force-device-scale-factor=1", f"--window-size={w},{h}",
                    f"--screenshot={png_path}", "--virtual-time-budget=9000",
                    "file://" + html_path], capture_output=True)


# Card titles stay honest to the actual media: the reel is 2:21 as of v4, so
# no duration claim goes on the card.
cards = [
    ("card-solo", os.path.join(IMG, "hero-solo-1600.jpg"), "50% 18%", "Solo vocals &amp; acoustic guitar."),
    ("card-vocalist", os.path.join(IMG, "poster-reel-1600.jpg"), "50% 30%", "Watch the live reel."),
]
for name, img, pos, title in cards:
    html_path = os.path.join(CARDS, f"{name}.html")
    open(html_path, "w").write(
        CARD_TPL.format(fonts=FONTS, img="file://" + img, pos=pos, title=title))
    shoot(html_path, f"{CARDS}/{name}.png", 1200, 675)
    Image.open(f"{CARDS}/{name}.png").convert("RGB").save(
        os.path.join(DIST_EMAIL, f"{name}.jpg"), "JPEG", quality=88, optimize=True)
    print("card:", name, os.path.getsize(os.path.join(DIST_EMAIL, name + '.jpg')) // 1024, "KB")

end_html = os.path.join(CARDS, "endcard.html")
open(end_html, "w").write(END_TPL.format(fonts=FONTS))
shoot(end_html, f"{RENDERS}/endcard.png", 1920, 1080)
print("endcard:", os.path.getsize(os.path.join(RENDERS, "endcard.png")) // 1024, "KB")
