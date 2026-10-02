#!/usr/bin/env python3
"""Build the per-cue MC Slides PDF (forScore deck) from a wedding's mc.html.

Usage:
  python3 docs/gig-sheets/tools/mc-slides.py <wedding-folder> "<Couple Label>" <mm.dd.yy>
  e.g. python3 docs/gig-sheets/tools/mc-slides.py ~/Desktop/greenway-gigs/hess/10-03-26 "Hess / Cassiday" 10.03.26

Reads <folder>/mc.html, writes <folder>/mc-cue-slides.pdf (960 x 600 pt, one cue per
page, Greenway black/cream tokens) via headless Chrome. The intermediate HTML goes to
the OS temp dir. Then add 'mc-cue-slides.pdf' to sw.js CORE, link it from mc.html's
notice bar ("Slides PDF"), bump CACHE, live-diff, whole-folder deploy.
"""
import html, os, re, subprocess, sys, tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def part(cue, cls):
    m = re.search(r'<div class="%s[^"]*">(.*?)</div>' % cls, cue, re.S)
    return m.group(1) if m else ''

def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    folder, couple, date = sys.argv[1:4]
    src = open(os.path.join(folder, 'mc.html')).read()
    cues = re.findall(r'<section class="cue[^"]*" data-index="\d+">(.*?)</section>', src, re.S)
    if not cues:
        sys.exit('no .cue sections found in mc.html')
    n = len(cues); slides = []
    for i, c in enumerate(cues, 1):
        t, l, say, note, song = (part(c, k) for k in ('time', 'label', 'say', 'note', 'song'))
        tbd = ' tbd' if 'song tbd' in c else ''
        slides.append(f'''<section class="slide">
<div class="top"><span>{html.escape(couple)} · MC Cues · {html.escape(date)}</span><span>{i} / {n}</span></div>
<div class="time">{t}</div><div class="label">{l}</div>
<div class="say">{say}</div>
{f'<div class="note">{note}</div>' if note else ''}
{f'<div class="song{tbd}">{song}</div>' if song else ''}
<div class="brand">The Greenway Band</div>
</section>''')
    doc = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{html.escape(couple)} MC Cue Slides</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
@page{{size:1280px 800px;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#0A0A09;color:#F5F2ED;font-family:'Plus Jakarta Sans',-apple-system,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.slide{{position:relative;width:1280px;height:800px;padding:64px 88px;page-break-after:always;break-after:page;background:#0A0A09}}
.slide:last-child{{page-break-after:auto;break-after:auto}}
.top{{display:flex;justify-content:space-between;color:#706D66;font-size:14px;font-weight:700;letter-spacing:.22em;text-transform:uppercase}}
.time{{margin-top:60px;color:#B8B4AC;font-size:24px;font-weight:700;letter-spacing:.1em}}
.label{{margin-top:12px;color:#706D66;font-size:15px;font-weight:700;letter-spacing:.24em;text-transform:uppercase}}
.say{{max-width:1060px;margin-top:28px;font-size:46px;font-weight:600;line-height:1.25}}
.name-highlight{{border-bottom:3px solid #F5F2ED}}
.note{{max-width:1020px;margin-top:22px;color:#B8B4AC;font-size:20px;line-height:1.5}}
.song{{position:absolute;left:88px;bottom:64px;padding:12px 16px;border:1px solid #4A4740;color:#B8B4AC;font-size:15px;font-weight:600;letter-spacing:.1em;text-transform:uppercase}}
.song.tbd{{color:#F5F2ED;border-color:#8D2E2A}}
.brand{{position:absolute;right:88px;bottom:64px;color:#4A4740;font-size:12px;font-weight:600;letter-spacing:.3em;text-transform:uppercase}}
</style></head><body>
{''.join(slides)}
</body></html>'''
    tmp = os.path.join(tempfile.mkdtemp(prefix='mc-slides-'), 'mc-cue-slides.html')
    open(tmp, 'w').write(doc)
    out = os.path.join(os.path.abspath(folder), 'mc-cue-slides.pdf')
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                    '--virtual-time-budget=8000', f'--print-to-pdf={out}', f'file://{tmp}'],
                   check=True, stderr=subprocess.DEVNULL)
    print(f'{n} slides -> {out}')

if __name__ == '__main__':
    main()
