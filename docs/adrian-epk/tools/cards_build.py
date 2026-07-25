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
  .txt {{ position:absolute; left:56px; right:56px; bottom:44px; color:#F5F2ED; }}
  h1 {{ font-family:'Bodoni Moda',serif; font-weight:400; font-size:52px; letter-spacing:.01em; margin-bottom:14px; }}
  .role {{ font-size:17px; font-weight:600; letter-spacing:.28em; color:#B8B4AC; margin-bottom:22px; }}
  .cta {{ display:inline-block; font-size:14px; font-weight:600; letter-spacing:.22em;
         color:#F5F2ED; border-top:1px solid rgba(245,242,237,.35); padding-top:16px; }}
</style></head><body>
<img class="bg" src="{img}">
<div class="shade"></div>
<div class="txt">
  <h1>ADRIAN MICHAEL</h1>
  <div class="role">BOSTON-BASED VOCALIST</div>
  <div class="cta">PLAY THE REEL</div>
</div>
</body></html>"""

# The end card is authored at the reel's NATIVE output size. Keep END_W/END_H in
# step with OUT_W/OUT_H in reel_build.py so the card is never resampled.
#
# Adrian called this card "grainy" on 2026-07-25. TWO encoding theories were
# tested and BOTH were wrong, so don't retry them:
#   1. "It's the 1920->1280 downscale." Authored it natively at 720p instead:
#      edge energy 23.5 -> 22.3. No visible change. The card was already as
#      sharp as 720p allows.
#   2. "It's the output resolution." Rebuilt at 1080p: edge energy 23.47 ->
#      24.16 measured at the width he actually views it (~1250px). A 3% gain
#      for a 55% bigger file (53MB -> 82MB). Not worth it, and not the cause.
#
# The real cause is TYPE, not pixels. On a Retina display the video sits beside
# page text that renders at 2x device pixels; video text renders at 1x and can
# never match it. Thin, widely letter-spaced, muted-gray glyphs lose that
# contest badly. The fix is legibility: heavier weight, brighter cream instead
# of muted gray, larger, and less letter-spacing on the long contact line.
# Judge changes here by looking at the card at ~1250px and at 390px, not by
# reaching for resolution.
END_W, END_H = 1280, 720

END_TPL = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="{fonts}" rel="stylesheet">
<style>
  * {{ margin:0; box-sizing:border-box; }}
  body {{ width:1280px; height:720px; background:#111110; color:#F5F2ED;
         font-family:'Plus Jakarta Sans',sans-serif; display:flex; align-items:center; justify-content:center; }}
  .in {{ text-align:center; }}
  .rule {{ width:64px; height:2px; background:rgba(245,242,237,.45); margin:0 auto 26px; }}
  .eyebrow {{ font-size:22px; font-weight:600; letter-spacing:.3em; color:#B8B4AC; margin-bottom:20px; }}
  h1 {{ font-family:'Bodoni Moda',serif; font-weight:500; font-size:92px; letter-spacing:.05em; margin-bottom:22px; }}
  .roles {{ font-size:34px; font-weight:600; letter-spacing:.16em; color:#F5F2ED; margin-bottom:38px; }}
  .contact {{ font-size:33px; font-weight:500; letter-spacing:.03em; color:#F5F2ED; }}
</style></head><body>
<div class="in">
  <div class="rule"></div>
  <div class="eyebrow">BOSTON &bull; NEW ENGLAND</div>
  <h1>ADRIAN MICHAEL</h1>
  <div class="roles">BOSTON-BASED VOCALIST</div>
  <div class="contact">ADRIAN@GREENWAYBAND.COM &nbsp;&bull;&nbsp; (281)&nbsp;467-1226</div>
</div>
</body></html>"""

def shoot(html_path, png_path, w, h):
    subprocess.run([CH, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--allow-file-access-from-files",
                    "--force-device-scale-factor=1", f"--window-size={w},{h}",
                    f"--screenshot={png_path}", "--virtual-time-budget=9000",
                    "file://" + html_path], capture_output=True)


# Correction brief v1 (2026-07-24): one universal card replaces the prior
# card-solo/card-vocalist pair. Vocalist hero image, per Adrian's call, so the
# card matches the page's own hero exactly.
name, img, pos = "card-universal", os.path.join(IMG, "hero-vocalist-1600.jpg"), "50% 22%"
html_path = os.path.join(CARDS, f"{name}.html")
open(html_path, "w").write(CARD_TPL.format(fonts=FONTS, img="file://" + img, pos=pos))
shoot(html_path, f"{CARDS}/{name}.png", 1200, 675)
Image.open(f"{CARDS}/{name}.png").convert("RGB").save(
    os.path.join(DIST_EMAIL, f"{name}.jpg"), "JPEG", quality=88, optimize=True)
print("card:", name, os.path.getsize(os.path.join(DIST_EMAIL, name + '.jpg')) // 1024, "KB")

end_html = os.path.join(CARDS, "endcard.html")
open(end_html, "w").write(END_TPL.format(fonts=FONTS))
shoot(end_html, f"{RENDERS}/endcard.png", END_W, END_H)
_ec = Image.open(os.path.join(RENDERS, "endcard.png"))
assert _ec.size == (END_W, END_H), f"endcard rendered {_ec.size}, expected {(END_W, END_H)}"
print("endcard:", f"{_ec.size[0]}x{_ec.size[1]}",
      os.path.getsize(os.path.join(RENDERS, "endcard.png")) // 1024, "KB")
