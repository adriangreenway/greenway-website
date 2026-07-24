#!/usr/bin/env python3
"""Build responsive image derivatives for the EPK (heroes from approved photos,
posters from approved frames). Sources untouched. Output: docs/adrian-epk/dist/adrian/assets/img/"""
import os, subprocess
from PIL import Image, ImageOps

EPK = os.path.expanduser("~/Desktop/EPK")
SRC = os.path.join(EPK, "renders", "_poster_src")   # scratch, regenerated below
OUT = os.path.expanduser("~/greenway-website/docs/adrian-epk/dist/adrian/assets/img")
os.makedirs(OUT, exist_ok=True)
os.makedirs(SRC, exist_ok=True)

# Poster frames, pulled fresh from the approved sources at native resolution.
# (No 9pc-promo frame: Adrian excluded that video 2026-07-24, it fronts another
# vocalist.) Format: (source video, timestamp, output name)
FRAMES = [
    ("big_spring_ranch_wedding_v1 (2160p).mp4",        "2",  "bigspring_t2_4k.jpg"),
    ("big_spring_ranch_wedding_v1 (2160p).mp4",       "40",  "bigspring_t40_4k.jpg"),
    ("Neon_Moon.mp4",                                 "13",  "neon_t13.jpg"),
    ("november_12,_2022_testimonial_v1 (720p).mp4",    "3",  "testimonial_t3.jpg"),
]
for video, ts, name in FRAMES:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", ts,
                    "-i", os.path.join(EPK, video),
                    "-frames:v", "1", "-q:v", "2", os.path.join(SRC, name)], check=True)

JOBS = [
    # (source path, out base name, widths)
    (os.path.join(EPK, "04_a_strong.JPEG"),                                   "hero-vocalist", [1600, 800]),
    (os.path.join(EPK, "04_captures_band_members_performing_on_stage_2.jpg"), "hero-solo",     [1600, 800]),
    (os.path.join(SRC, "bigspring_t2_4k.jpg"),                                "poster-reel",    [1600, 800]),
    (os.path.join(SRC, "bigspring_t40_4k.jpg"),                               "poster-film",    [1600, 800]),
    (os.path.join(SRC, "neon_t13.jpg"),                                       "poster-neon",    [720]),
    (os.path.join(SRC, "testimonial_t3.jpg"),                                 "poster-testimonial", [720]),
]

manifest = []
for src, base, widths in JOBS:
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    for w in widths:
        if im.width < w:
            w_eff = im.width
        else:
            w_eff = w
        r = im.resize((w_eff, round(im.height * w_eff / im.width)), Image.LANCZOS)
        jp = os.path.join(OUT, f"{base}-{w}.jpg")
        wp = os.path.join(OUT, f"{base}-{w}.webp")
        r.save(jp, "JPEG", quality=85, progressive=True, optimize=True)
        r.save(wp, "WEBP", quality=82, method=6)
        manifest.append((os.path.basename(jp), r.size, os.path.getsize(jp)//1024, os.path.getsize(wp)//1024))

for m in manifest:
    print(f"{m[0]:34} {m[1][0]}x{m[1][1]}  jpg {m[2]}KB / webp {m[3]}KB")
