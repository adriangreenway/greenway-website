#!/usr/bin/env python3
"""Estimate a practice track's tempo from the audio (cross-check for als-lyrics.py).

    python3 tempo-estimate.py audio/bad-girls.mp3 [more files]

Prints the top tempo candidates (BPM, score) per file. Needs ffmpeg and numpy.
Validated 2026-09-28 on the Hess tracks: Hot Stuff 120.2 (real 120), Miles On It
130.0 (130), Like a Prayer 112.3 (111.93), How Will I Know 118.1 (118), Bad Girls
120.2 (120.45). Use it when a filename gives no tempo; the real source of truth is
still the song's main Ableton project, named `<Key>_<bpm> bpm_<Song>.als` on the
GWB Show SSD. Half/double-time candidates can appear; prefer the one that makes
the last lyric clip end near the MP3's end.
"""
import subprocess, sys
import numpy as np


def tempo(path, lo=95, hi=140):
    sr = 22050
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'],
                         capture_output=True).stdout
    x = np.frombuffer(pcm, dtype=np.float32)
    n, hop = 1024, 256
    frames = (len(x) - n) // hop
    idx = np.arange(n)[None, :] + hop * np.arange(frames)[:, None]
    S = np.abs(np.fft.rfft(x[idx] * np.hanning(n), axis=1))
    L = np.log1p(1000 * S)
    flux = np.maximum(L[1:] - L[:-1], 0).sum(axis=1)
    flux = flux - np.convolve(flux, np.ones(43) / 43, 'same')
    fps = sr / hop
    ac = np.correlate(flux, flux, 'full')[len(flux) - 1:]
    ac /= ac[0]
    out = []
    for bpm10 in range(lo * 10, hi * 10 + 1):
        bpm = bpm10 / 10
        lag = 60 * fps / bpm
        score = 0
        for k, w in ((1, 1.0), (2, 0.75), (4, 0.5)):
            l = lag * k
            i = int(l); fr = l - i
            score += w * ((1 - fr) * ac[i] + fr * ac[i + 1])
        out.append((score, bpm))
    out.sort(reverse=True)
    best = []
    for score, bpm in out:
        if all(abs(bpm - b) > 2 for _, b in best):
            best.append((score, bpm))
        if len(best) == 4:
            break
    return best


for p in sys.argv[1:]:
    print(p.split('/')[-1], [(round(b, 1), round(float(s), 3)) for s, b in tempo(p)])
