#!/usr/bin/env python3
"""Draft vocalist reel v1 (~51s, 1080p30). EDL v2 as approved in Phase 0.
Verticals get a blurred pillarbox; audio is per-clip live sound, loudness-normalized,
0.5s crossfades. Draft only: nothing uploaded."""
import os, subprocess, math, json

EPK = os.path.expanduser("~/Desktop/EPK")
OUT = os.path.join(EPK, "renders")
TMP = os.path.join(OUT, "_reel_tmp")  # scratch, lives beside the renders
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

# v4: every window is Adrian's own timestamp pass (2026-07-24), used at the
# full length he gave. Running order is an energy arc; his windows untouched.
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

# endcard segment
endseg = os.path.join(TMP, "seg_end.mp4")
if not os.path.exists(endseg):
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-loop", "1", "-t", str(END_T), "-i", os.path.join(OUT, "endcard.png"),
         "-f", "lavfi", "-t", str(END_T), "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
         "-vf", "scale=1920:1080,fps=30,format=yuv420p,setsar=1",
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
vprev, aprev = "[0:v]", "[0:a]"
for i in range(1, len(files)):
    vout, aout = f"[v{i}]", f"[a{i}]"
    fc.append(f"{vprev}[{i}:v]xfade=transition=fade:duration={XF}:offset={offsets[i-1]}{vout}")
    fc.append(f"{aprev}[{i}:a]acrossfade=d={XF}{aout}")
    vprev, aprev = vout, aout

final = os.path.join(OUT, "adrian_michael_vocalist_reel_v4_draft.mp4")
run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
     "-filter_complex", ";".join(fc),
     "-map", vprev, "-map", aprev,
     "-c:v", "libx264", "-preset", "medium", "-crf", "19", *GOP,
     "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final])

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
