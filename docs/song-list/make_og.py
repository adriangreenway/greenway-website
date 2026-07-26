#!/usr/bin/env python3
"""Render og_card.html to og-song-list.png, the song list's link preview image.

Usage:
    python3 make_og.py

Kept out of build.py on purpose: the card has no song data in it, so it does
not need re-rendering when the repertoire changes. Only re-run this if
og_card.html changes.

Uses headless Chrome so the card renders with the real brand fonts and the
exact CSS of the page's own cover. Both fonts are also installed locally
(~/Library/Fonts), so this works with or without a network connection.
"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CARD = HERE / "og_card.html"
OUT = HERE / "og-song-list.png"

# The card is laid out at 1200x630 (the Open Graph aspect every app expects) and
# shot at 2x, so it stays sharp on retina phones and on the desktop cards that
# upscale. 2400x1260 is inside every platform's limit (Facebook 8MB, Twitter
# 5MB / 4096px). The og:image:width/height tags in template.html state the real
# pixel size, so they must be updated together with SCALE.
W, H = 1200, 630
SCALE = 2

CHROME = next(
    (p for p in (
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ) if Path(p).exists()),
    shutil.which("google-chrome") or shutil.which("chromium"),
)
if not CHROME:
    sys.exit("FAIL: no Chrome or Chromium found to render the card.")

for flag in ("--headless=new", "--headless"):
    proc = subprocess.run(
        [
            CHROME, flag, "--disable-gpu", "--hide-scrollbars",
            f"--window-size={W},{H}",
            f"--force-device-scale-factor={SCALE}",
            "--default-background-color=0A0A09FF",
            "--virtual-time-budget=4000",  # let the webfonts settle before the shot
            f"--screenshot={OUT}",
            CARD.as_uri(),
        ],
        capture_output=True, text=True,
    )
    if OUT.exists():
        break
else:
    sys.exit(f"FAIL: Chrome wrote no file.\n{proc.stderr[-2000:]}")

# Verify what we actually produced, rather than trusting the exit code.
from PIL import Image  # noqa: E402

with Image.open(OUT) as im:
    size, mode = im.size, im.mode
    corner = im.convert("RGB").getpixel((4, 4))

ok = size == (W * SCALE, H * SCALE) and corner == (10, 10, 9)
print(f"wrote:    {OUT.name}  {size[0]}x{size[1]}  {mode}  {OUT.stat().st_size / 1024:.0f} KB")
print(f"expected: {W * SCALE}x{H * SCALE} (a {W}x{H} card shot at {SCALE}x)")
print(f"corner:   {corner} (expected the cover charcoal (10, 10, 9))")
print("PASS" if ok else "FAIL: wrong size or the card did not paint")
sys.exit(0 if ok else 1)
