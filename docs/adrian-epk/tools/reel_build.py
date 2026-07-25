#!/usr/bin/env python3
"""Vocalist reel v7 (~2:21, 720p30). Adrian's final call 2026-07-24: keep
ALL thirteen of his clip windows at full length ("it's too hard for me to
pick which ones are better... if they don't want to scroll through the whole
thing, they don't have to"). Same edit and same windows as v4/v6.
Verticals get a blurred pillarbox; audio is per-clip live sound, loudness-normalized,
0.5s crossfades. Draft only: nothing uploaded.

v7 (2026-07-25) is a re-encode only, no edit change, forced by ChatGPT's final
audit. Two fixes:

  1. WEB COMPATIBILITY. v6 shipped as H.264 "High 4:4:4 Predictive" / yuv444p,
     which is outside the hardware-decode path on iPhone Safari and is not a
     safe choice for a public <video>. Cause: the per-segment filters set
     format=yuv420p, but this final crossfade pass set neither a filter format
     nor -pix_fmt, so libx264 took xfade's preferred yuv444p. Now pinned in
     both places (filter tail + -pix_fmt) with -profile:v high -level 4.1.
     DO NOT remove either pin; one alone is easy to defeat by a filter edit.
  2. End card copy now BOSTON-BASED VOCALIST, matching the page and the email
     card, and its type is sized to stay readable in a 390px-wide player.

Output is 720p at CRF 21, per the audit's preference: the source is mostly upscaled
vertical phone footage, so 1080p buys file size rather than detail (measured: only
3% more edge definition at real viewing width, for a 55% larger file)."""
import os, subprocess, math, json

EPK = os.path.expanduser("~/Desktop/EPK")
OUT = os.path.join(EPK, "renders")
TMP = os.path.join(OUT, "_reel_tmp")  # scratch, lives beside the renders
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

# v6 = v4's windows exactly: every window is Adrian's own timestamp pass
# (2026-07-24), used at the full length he gave. Energy-arc running order.
SEGS = [
    ("big_spring_ranch_wedding_v1 (2160p).mp4",  0.0,  5.0, "h"),
    ("suavemente_v1 (720p).mp4",                 0.0, 13.0, "v"),
    ("My Girl.MOV",                             40.0, 10.0, "v"),
    ("You Make My Dreams.MOV",                  18.0, 14.0, "v"),
    ("Neon_Moon.mp4",                           12.0, 18.0, "v"),
    ("Mr. Brightside Market Street.MOV",        91.0, 14.0, "v"),
    ("uptown-funk-2026a.mp4",                  150.0, 13.0, "h"),
    ("crazy_in_love_v1 (540p).mp4",              0.0, 10.0, "v"),
    ("Locked Out Of Heaven Neal Hamil.MOV",      5.0, 10.0, "v"),
    ("Friends In Low Places Neal Hamil.MOV",    36.0,  8.0, "v"),
    ("play_that_funky_music_v1 (540p).mp4",      1.0,  6.0, "v"),
    ("yeah!_v1 (540p).mp4",                      0.0,  8.0, "v"),
    ("24k Magic San Marcos Wedding.MOV",         2.0, 13.0, "v"),
]
END_T = 5.5
# Final output size, and the size everything is normalised to before xfade so no
# frame is resampled twice. 1080p, matching the cached intermediates, so the clips
# and the end card both pass through unscaled.
#
# 720p, per the audit's preference: the source is mostly upscaled vertical phone
# footage, so 1080p buys file size rather than detail. Measured, not assumed --
# 1080p scored only 3% more edge definition at the width the reel is actually
# viewed, for a 55% larger file. See the end-card note in cards_build.py.
OUT_W, OUT_H = 1280, 720
# Keyframe every second so scrubbing lands where you drop it.
GOP = ["-g", "30", "-keyint_min", "30", "-sc_threshold", "0"]
XF = 0.5

V_FILTER = ("split[a][b];"
            "[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
            "gblur=sigma=36,eq=brightness=-0.12[bg];"
            "[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0")
H_FILTER = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("FFMPEG FAIL:\n" + " ".join(cmd) + "\n" + r.stderr[-1200:])

# 1) normalized intermediates
files = []
for i, (name, ss, t, orient) in enumerate(SEGS):
    dst = os.path.join(TMP, f"seg{i:02d}.mp4")
    files.append(dst)
    if os.path.exists(dst):
        continue
    vf = (V_FILTER if orient == "v" else H_FILTER) + ",fps=30,format=yuv420p,setsar=1"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-ss", str(ss), "-t", str(t), "-i", os.path.join(EPK, name),
         "-filter_complex", vf,
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000",
         "-ac", "2", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-c:a", "aac", "-b:a", "192k", dst])
    print("seg", i, name, t, "s")

# endcard segment, built at OUT_W x OUT_H. cards_build.py authors endcard.png at
# exactly that size (END_W/END_H), so this scale is a no-op and the card reaches
# the encoder unresampled. Keep those two pairs in step.
endseg = os.path.join(TMP, "seg_end.mp4")
if not os.path.exists(endseg):
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-loop", "1", "-t", str(END_T), "-i", os.path.join(OUT, "endcard.png"),
         "-f", "lavfi", "-t", str(END_T), "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
         "-vf", f"scale={OUT_W}:{OUT_H},fps=30,format=yuv420p,setsar=1",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-c:a", "aac", "-b:a", "192k", "-shortest", endseg])
    print("endcard seg done")
files.append(endseg)

# 2) crossfade chain
durs = [s[2] for s in SEGS] + [END_T]
offsets = []
acc = 0.0
for d in durs[:-1]:
    acc += d - XF
    offsets.append(round(acc, 3))

inputs = []
for f in files:
    inputs += ["-i", f]
fc = []
# Normalise every input to the output size BEFORE xfade, so no frame is resampled
# more than once regardless of what OUT_W/OUT_H are set to. At 1080p this is a
# no-op for both the cached clips and the end card, which is the point.
for i in range(len(files)):
    fc.append(f"[{i}:v]scale={OUT_W}:{OUT_H}:flags=lanczos,format=yuv420p,setsar=1[s{i}]")
vprev, aprev = "[s0]", "[0:a]"
for i in range(1, len(files)):
    vout, aout = f"[v{i}]", f"[a{i}]"
    fc.append(f"{vprev}[s{i}]xfade=transition=fade:duration={XF}:offset={offsets[i-1]}{vout}")
    fc.append(f"{aprev}[{i}:a]acrossfade=d={XF}{aout}")
    vprev, aprev = vout, aout

# Format pin. See the v7 note in the docstring: without the explicit format here
# (and -pix_fmt below) this pass silently emits yuv444p.
fc.append(f"{vprev}format=yuv420p[vout]")

final = os.path.join(OUT, "adrian_michael_vocalist_reel_v7_draft.mp4")
run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
     "-filter_complex", ";".join(fc),
     "-map", "[vout]", "-map", aprev,
     "-c:v", "libx264", "-preset", "medium", "-crf", "21", *GOP,
     "-profile:v", "high", "-level", "4.1", "-pix_fmt", "yuv420p",
     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
     "-movflags", "+faststart", final])

p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size",
                    "-of", "json", final], capture_output=True, text=True)
info = json.loads(p.stdout)["format"]
print("REEL:", final)
print("duration:", round(float(info["duration"]), 1), "s  size:", int(info["size"]) // 1_000_000, "MB")

# review contact sheet
sheet = os.path.join(TMP, "reel_review.jpg")
run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", final,
     "-vf", "fps=1/5,scale=320:-2,tile=5x6:padding=4:color=0x333333", "-frames:v", "1", "-q:v", "3", sheet])
print("sheet:", sheet)
