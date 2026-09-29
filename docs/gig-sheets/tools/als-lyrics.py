#!/usr/bin/env python3
"""Pull AbleSet lyric clips out of an Ableton Live Set (.als) as timed lines.

AbleSet stores each lyric line as a MIDI clip whose NAME is the line, placed on
the arrangement timeline in beats. This prints them as a JavaScript array of
[seconds, 'line'] pairs, ready to paste into a Listening Room TRACKS entry:

    python3 als-lyrics.py "Song - Synced Lyrics for AbleSet.als" --bpm 120 > lyrics.js

--bpm is REQUIRED because the standalone lyrics set often carries a throwaway
master tempo (Hot Stuff's file said 200 while the song runs at 120). Use the
tempo from the practice-track filename. Pass --duration <seconds> (the MP3's
length) and the script warns if the last lyric ends past the end of the track,
which is the quickest sanity check that the BPM is right.

The .als is gzip-compressed XML; the script handles both compressed and
already-unzipped files. Only the summary goes to stderr; the lyric lines go to
stdout, so redirect stdout to a file.
"""
import argparse, gzip, json, sys
import xml.etree.ElementTree as ET


def load(path):
    with open(path, 'rb') as fh:
        raw = fh.read()
    if raw[:2] == b'\x1f\x8b':
        raw = gzip.decompress(raw)
    return ET.fromstring(raw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('als')
    ap.add_argument('--bpm', type=float, required=True, help='song tempo used to convert beats to seconds')
    ap.add_argument('--duration', type=float, help='MP3 length in seconds, for a sanity check')
    ap.add_argument('--track', default='lyric', help='substring of the MIDI track name holding the lyric clips (case-insensitive)')
    args = ap.parse_args()

    root = load(args.als)
    live_set = root.find('LiveSet')
    master_tempo = live_set.find('MasterTrack/DeviceChain/Mixer/Tempo/Manual')
    master_tempo = master_tempo.get('Value') if master_tempo is not None else '?'

    tracks = [t for t in live_set.find('Tracks') if t.tag == 'MidiTrack']
    def track_name(t):
        el = t.find('Name/EffectiveName')
        return el.get('Value', '') if el is not None else ''

    named = [t for t in tracks if args.track.lower() in track_name(t).lower()]
    use = named or tracks
    lines = []
    for t in use:
        for clip in t.iter('MidiClip'):
            name_el = clip.find('Name')
            name = (name_el.get('Value', '') if name_el is not None else '').strip()
            if not name:
                continue
            start = float(clip.find('CurrentStart').get('Value'))
            end = float(clip.find('CurrentEnd').get('Value'))
            lines.append((start, end, name))
    lines.sort()
    if not lines:
        sys.exit('no named MIDI clips found')

    spb = 60.0 / args.bpm
    out = [[round(s * spb, 2), n] for s, e, n in lines]
    last_end = lines[-1][1] * spb

    print('const LYRICS = ' + json.dumps(out, ensure_ascii=False, indent=2) + ';')

    err = sys.stderr
    print(f'track(s): {[track_name(t) for t in use]}', file=err)
    print(f'lines: {len(out)}   master tempo in file: {master_tempo}   used bpm: {args.bpm:g}', file=err)
    print(f'first line at {out[0][0]:.2f}s   last line at {out[-1][0]:.2f}s   last clip ends {last_end:.2f}s', file=err)
    if args.duration is not None:
        gap = args.duration - last_end
        flag = 'OK' if -1.0 <= gap <= 30.0 else 'CHECK BPM'
        print(f'track length {args.duration:.2f}s -> last clip ends {gap:+.2f}s from the end: {flag}', file=err)


if __name__ == '__main__':
    main()
