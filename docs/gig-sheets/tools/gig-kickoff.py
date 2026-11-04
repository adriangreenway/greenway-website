#!/usr/bin/env python3
"""Kick off a gig sheet from a wedding on scheduling.greenwayband.com.

Claude runs this; Adrian never does. It only starts a sheet: it copies what
scheduling already knows (couple, date, venue, band size) into a new dated
folder built from docs/gig-sheets/EXAMPLE/, and marks every other fact as an
HTML PLACEHOLDER comment. The night itself (timeline, specials, MC, songs)
still comes from the timeline, questionnaire, and full Gmail threads per the
create-gig-sheet skill. Nothing here deploys.

  gig-kickoff.py <slug>                 new folder in ~/Desktop/greenway-gigs + hub row
  gig-kickoff.py <slug> --out DIR       dry run: write into DIR instead (past weddings allowed,
                                        live gigs folder and hub untouched)
  gig-kickoff.py --check <folder>       is this folder ready to deploy? (exit 1 if not)
  gig-kickoff.py --link <slug>          after the sheet is live: set its "Gig sheet" link on
                                        scheduling (export before + after, only that wedding changes)

Options: --export FILE uses a saved admin export instead of fetching a fresh one.
The admin key (~/Desktop/greenway-scheduling/.env.admin) and the Netlify token are
read from disk and never printed. Plan: docs/scheduling/GIG_PIPELINE_PLAN.md.
"""
import argparse, datetime, html, json, re, subprocess, sys
from pathlib import Path
from zoneinfo import ZoneInfo

HOME = Path.home()
REPO = Path(__file__).resolve().parents[3]
EXAMPLE = REPO / 'docs/gig-sheets/EXAMPLE'
GIGS = HOME / 'Desktop/greenway-gigs'
SCHED = HOME / 'Desktop/greenway-scheduling'
SCHED_SITE = '51069c4e-b3ef-435e-a3f8-5c4c95295bc4'
EXPORT_URL = 'https://scheduling.greenwayband.com/api/admin/export'
HOST = 'https://gigs.greenwayband.com'
HOUSTON = ZoneInfo('America/Chicago')
SOUND = 'Sound tech'
P = lambda what: f'<!-- PLACEHOLDER: {what} -->'


def die(msg):
    sys.exit(f'STOP: {msg}')


# ---------- scheduling data ----------

def admin_key():
    for line in (SCHED / '.env.admin').read_text().splitlines():
        if line.startswith('ADMIN_KEY='):
            return line.split('=', 1)[1].strip()
    die('no ADMIN_KEY in .env.admin')


def fetch_export():
    # curl, not urllib: this Mac's python.org Python has no CA bundle. Key goes in on stdin, never argv.
    r = subprocess.run(['curl', '-sS', '--fail', '-m', '30', '-H', '@-', EXPORT_URL],
                       input=f'Authorization: Bearer {admin_key()}\n', capture_output=True, text=True)
    if r.returncode != 0:
        die(f'admin export failed: {r.stderr.strip()[:200]}')
    return json.loads(r.stdout)


def http_status(url):
    r = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '-m', '20', url], capture_output=True, text=True)
    return r.stdout.strip()


def save_export(exp, tag):
    out = SCHED / 'backups' / f'export-{datetime.date.today()}-{tag}.json'
    out.write_text(json.dumps(exp, indent=1))
    return out


def find_wedding(exp, slug):
    hits = [(k, r['data']) for k, r in exp['records'].items() if k.startswith('w:') and r['data'].get('slug') == slug]
    if not hits:
        die(f'no wedding with slug "{slug}" on scheduling. Add it there first (Add wedding), or check the slug.')
    if len(hits) > 1:
        die(f'{len(hits)} weddings share slug "{slug}"')
    key, w = hits[0]
    if w.get('removed'):
        die(f'"{slug}" is a removed wedding on scheduling')
    return key, w


def folder_parts(slug):
    m = re.fullmatch(r'([a-z]+)-(\d\d-\d\d-\d\d)(?:-\d+)?', slug)
    if not m:
        die(f'slug "{slug}" is not <last>-<mm-dd-yy>')
    return m.group(1), m.group(2)


def band_size(lineup):
    musicians = [(p, s['name']) for p, s in lineup.items() if p != SOUND]
    unconfirmed = [n for _, n in musicians if '(unconfirmed)' in n]
    return len(musicians), unconfirmed, SOUND in lineup


# ---------- page building ----------

def long_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f'{d:%A}, {d:%B} {d.day}, {d.year}'


def example_ids():
    """The EXAMPLE wedding's identifying strings, so nothing of theirs survives in a new sheet."""
    man = json.loads((EXAMPLE / 'manifest.json').read_text())
    couple = man['name'].split(' — ')[0]
    base = man['start_url']
    ids = {couple, base, base.strip('/').split('/')[1]}
    ids |= {n.strip() for n in couple.split('/') if n.strip()}
    sec = re.search(r'data-date="(\d{4}-\d\d-\d\d)"', (EXAMPLE / 'band.html').read_text())
    if sec:
        ids |= {sec.group(1), long_date(sec.group(1))}
    return couple, base, ids


def swap_main(page, body):
    new, n = re.subn(r'<main class="body">.*?</main>', lambda _: body, page, count=1, flags=re.S)
    if n != 1:
        die('EXAMPLE page layout changed: no <main class="body"> block')
    return new


def common(page, ctx):
    ex_couple, ex_base = ctx['ex_couple'], ctx['ex_base']
    ex_date = ctx['ex_long_date']
    page = page.replace(ex_base, ctx['base']).replace(ex_couple, ctx['client_html'])
    if ex_date:
        page = page.replace(ex_date, ctx['long_date'])
    page = re.sub(r'(<meta (?:property|name)="(?:og|twitter):description" content=")[^"]*(">)', lambda m: m.group(1) + ctx['long_date'] + ' · ' + ctx['venue_html'] + m.group(2), page)
    # Share images are made per wedding later; drop the EXAMPLE's.
    lines = [l for l in page.split('\n') if not re.search(r'(og|twitter):image', l)]
    page = '\n'.join(lines)
    page = page.replace('<meta property="og:type"', P('share image og-band-hub.png + og:image/twitter:image tags (see a live sheet)') + '\n<meta property="og:type"', 1)
    return page


def section(label, value_html):
    return f'<section class="section"><div class="section-label">{label}</div>{value_html}</section>'


def val(x):
    return f'<div class="value">{x}</div>'


def schedule_open(ctx, label):
    return (f'<section class="section" data-schedule data-date="{ctx["date"]}" data-tz="America/Chicago">'
            f'{P("data-tz is Houston time; change it if the venue is in another zone")}\n'
            f'    <div class="section-label">{label}</div>\n'
            f'    {P("one .row per timeline line; data-at=HH:MM (24h venue time) on every row with a real clock time")}\n'
            f'  </section>')


def band_body(ctx):
    v = ctx['venue_html']
    return f'''<main class="body">
  {P("KICKOFF DRAFT from scheduling.greenwayband.com. Fill every placeholder from the timeline, questionnaire, and full Gmail threads; copy row and special markup from docs/gig-sheets/EXAMPLE/band.html")}
  <div class="two-col">
    <div>
      {section("Couple", val(P("both full names")))}
      {section("Location", val(v) + '<div class="sub">' + P("room, address with maps link") + '</div>')}
      {section("Attire", P("attire for this wedding"))}
    </div>
    <div>
      {section("Sound Load In", val(P("time")))}
      {section("Band Load In", val(P("time")))}
      {section("Soundcheck", val(P("time window")))}
      {section("Meals", val(P("time")) + '<div class="sub">' + P("room") + '</div>')}
    </div>
  </div>

  <div class="divider"></div>
  {schedule_open(ctx, "Schedule")}

  <div class="divider"></div>
  {section("Specials", P("each special: moment, song, LIVE or TRACK tag"))}

  <div class="divider"></div>
  {section("Songs to Learn", P("list, or remove this section"))}

  <div class="divider"></div>
  {section("Do Not Play", P("list, or remove this section"))}

  <div class="divider"></div>
  {section("Notes", P("band-facing notes only, or remove this section"))}
</main>'''


def gig_body(ctx):
    v = ctx['venue_html']
    team = f'{ctx["size"]}-piece band' + (' + sound engineer' if ctx['has_sound'] else '')
    return f'''<main class="body">
  {P("KICKOFF DRAFT from scheduling.greenwayband.com. Fill every placeholder from the timeline, questionnaire, and full Gmail threads; copy markup from docs/gig-sheets/EXAMPLE/gig.html")}
  <div class="two-col">
    <div>
      {section("Location", val(v) + '<div class="sub">' + P("room, address with maps link") + '</div>')}
      {section("Performance Team", val(team) + P("band size counted from the scheduling lineup; confirm against the contract"))}
      {section("Attire", P("attire for this wedding"))}
      {section("Guests", val(P("guest count, or remove")))}
    </div>
    <div>
      {section("Sound Load In", val(P("time")))}
      {section("Band Load In", val(P("time")))}
      {section("Soundcheck", val(P("time window")))}
      {section("Meals", val(P("time")) + '<div class="sub">' + P("room") + '</div>')}
    </div>
  </div>

  <div class="divider"></div>
  {schedule_open(ctx, "Full Timeline")}

  <div class="divider"></div>
  {section("Specials", P("each special: moment, song, cut times, LIVE or TRACK tag"))}

  <div class="divider"></div>
  {section("Songs to Learn", P("list, or remove this section"))}

  <div class="divider"></div>
  <div class="two-col">
    {section("Emcee", P("who emcees, couple introduction wording"))}
    {section("Key Contacts", P("planner, venue, couple, photographer"))}
  </div>

  <div class="divider"></div>
  {section("Operational Notes", P("operational notes"))}
</main>'''


def build(ctx, dest):
    dest.mkdir(parents=True)
    footer_old = re.search(r'<footer class="footer"><span>The Greenway Band</span><span>([^<]*)</span></footer>', (EXAMPLE / 'band.html').read_text())
    for name, body in (('band.html', band_body), ('gig.html', gig_body)):
        page = common((EXAMPLE / name).read_text(), ctx)
        page = swap_main(page, body(ctx))
        if footer_old:
            page = page.replace(f'<span>{footer_old.group(1)}</span></footer>', f'<span>{ctx["client_html"]} {ctx["dots"]}</span></footer>')
        (dest / name).write_text(page)

    hub = common((EXAMPLE / 'index.html').read_text(), ctx)
    names = [html.escape(n.strip()) for n in ctx['client'].split('/')]
    h1 = f'{names[0]} <span>/</span><br>{names[1]}' if len(names) == 2 else html.escape(ctx['client'])
    hub = re.sub(r'<h1>.*?</h1>', lambda _: f'<h1>{h1}</h1>', hub, count=1, flags=re.S)
    hub = re.sub(r'<div class="venue">.*?</div>', lambda _: f'<div class="venue">{ctx["venue_html"]}{P("<br>City, State")}</div>', hub, count=1, flags=re.S)
    nav = (f'<nav class="hub-nav" aria-label="Gig sheet resources">\n'
           f'      <a class="hub-link" href="{ctx["base"]}band"><span class="number">01</span><span class="label">Band Sheet</span><span class="arrow" aria-hidden="true">&rarr;</span></a>\n'
           f'      {P("MC Cue Sheet link here if the band sees it (ask Adrian per wedding, D20); renumber")}\n'
           f'      <a class="hub-link" href="{ctx["base"]}listen"><span class="number">02</span><span class="label">Listening Room</span><span class="arrow" aria-hidden="true">&rarr;</span></a>\n'
           f'    </nav>')
    hub = re.sub(r'<nav class="hub-nav".*?</nav>', lambda _: nav, hub, count=1, flags=re.S)
    hub = re.sub(r'\s*<a class="download"[^\n]*</a>', lambda _: '\n    ' + P('Band Sheet PDF download link once band-sheet.pdf exists'), hub, count=1)
    (dest / 'index.html').write_text(hub)

    listen = common((EXAMPLE / 'listen.html').read_text(), ctx)
    listen, n = re.subn(r'const TRACKS = \[.*?\n\];', 'const TRACKS = [];', listen, count=1, flags=re.S)
    if n != 1:
        die('EXAMPLE listen.html changed: no TRACKS list')
    (dest / 'listen.html').write_text(listen)

    man = json.loads((EXAMPLE / 'manifest.json').read_text())
    man.update(name=f'{ctx["client"]} — Greenway Gig Sheet', start_url=ctx['base'], scope=ctx['base'])
    (dest / 'manifest.json').write_text(json.dumps(man, indent=2, ensure_ascii=False) + '\n')

    sw = (EXAMPLE / 'sw.js').read_text()
    tag = f'gig-{ctx["last"]}-{ctx["mmddyy"]}-'
    sw = re.sub(r"const CACHE = '[^']*';", f"const CACHE = '{tag}v1';", sw)
    sw = re.sub(r"const PREFIX = '[^']*';", f"const PREFIX = '{tag}';", sw)
    sw = re.sub(r"const BASE = '[^']*';", f"const BASE = '{ctx['base']}';", sw)
    core = ',\n'.join(['  BASE'] + [f"  BASE + '{p}'" for p in ('index.html', 'band', 'band.html', 'gig', 'gig.html', 'listen', 'listen.html', 'manifest.json')])
    sw = re.sub(r'const CORE = \[.*?\];', lambda _: f'const CORE = [\n{core}\n];', sw, count=1, flags=re.S)
    sw = re.sub(r'const AUDIO = \[.*?\];', 'const AUDIO = [];', sw, count=1, flags=re.S)
    (dest / 'sw.js').write_text(sw)


def hub_row(ctx):
    q = lambda s: "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"
    return (f"  {{ couple: {q(ctx['client'])}, date: {q(ctx['date'])}, venue: {q(ctx['venue'])}, "
            f"size: {q(str(ctx['size']) + '-Piece')}, url: {q(HOST + ctx['base'])} }},")


def add_hub_row(row):
    hub = GIGS / 'index.html'
    text = hub.read_text()
    if 'const GIGS = [\n' not in text:
        die('gigs hub layout changed: no "const GIGS = [" line')
    hub.write_text(text.replace('const GIGS = [\n', 'const GIGS = [\n' + row + '\n', 1))


# ---------- check ----------

def check(folder):
    folder = Path(folder).expanduser().resolve()
    _, _, ids = example_ids()
    problems = []
    for f in sorted(folder.glob('*.html')) + [folder / 'sw.js', folder / 'manifest.json']:
        if not f.exists():
            continue
        t = f.read_text()
        n = t.count('PLACEHOLDER')
        if n:
            problems.append(f'{f.name}: {n} placeholder(s) left')
        if re.search(r'\bTBD\b', t):
            problems.append(f'{f.name}: prints "TBD" (never allowed on a sheet)')
        for s in ids:
            if s and s in t:
                problems.append(f'{f.name}: still carries the EXAMPLE wedding\'s "{s}"')
    sw = (folder / 'sw.js').read_text() if (folder / 'sw.js').exists() else ''
    base = re.search(r"const BASE = '([^']*)'", sw)
    for p in re.findall(r"BASE \+ '([^']+)'", sw):
        local = folder / p
        if not (local.exists() or local.with_suffix('.html').exists()):
            problems.append(f'sw.js caches {p}, which is not in the folder')
    if base and not (folder / 'og-band-hub.png').exists():
        problems.append('no og-band-hub.png share image')
    if problems:
        print('NOT READY to deploy:')
        for p in problems:
            print('  -', p)
        sys.exit(1)
    print('READY: no placeholders, no TBD, no EXAMPLE leftovers, every cached file exists.')


# ---------- link back ----------

NODE_LINK = r'''
const [, siteID, token, key, sheet, sched] = process.argv; // node -e: no script path in argv
const { getStore } = await import(sched + '/node_modules/@netlify/blobs/dist/main.js');
const { cleanWedding, saveChecked } = await import(sched + '/netlify/lib/roster.mjs');
const store = getStore({ name: 'scheduling', siteID, token });
const cur = await store.getWithMetadata(key, { type: 'json' });
if (!cur) { console.log('MISSING'); process.exit(2); }
const next = cleanWedding({ ...cur.data, sheet }, cur.data);
const res = await saveChecked(store, key, cur, next, 'gig sheet link added by Claude (kickoff)');
console.log(res.ok ? 'SAVED v' + res.version : 'CONFLICT');
process.exit(res.ok ? 0 : 3);
'''


def netlify_token():
    cfg = json.loads((HOME / 'Library/Preferences/netlify/config.json').read_text())
    return cfg['users'][cfg['userId']]['auth']['token']


def link(slug):
    last, mmddyy = folder_parts(slug)
    url = f'{HOST}/{last}/{mmddyy}/'
    code = http_status(url)
    if code != '200':
        die(f'{url} returned {code or "nothing"}. Deploy first, then link.')
    before = fetch_export()
    key, w = find_wedding(before, slug)
    if w.get('sheet') == url:
        print(f'Already linked: {url}')
        return
    b = save_export(before, f'pre-link-{slug}')
    r = subprocess.run(['node', '--input-type=module', '-e', NODE_LINK, SCHED_SITE, netlify_token(), key, url, str(SCHED)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        die(f'link write failed: {r.stdout.strip()} {r.stderr.strip()[:300]}')
    after = fetch_export()
    a = save_export(after, f'post-link-{slug}')
    changed = [k for k in set(before['records']) | set(after['records'])
               if k.startswith(('w:', 'musicians')) and before['records'].get(k, {}).get('data') != after['records'].get(k, {}).get('data')]
    want = dict(w, sheet=url)
    ok = changed == [key] and after['records'][key]['data'] == want
    print(f'{r.stdout.strip()}  {url}')
    print(f'Export diff: changed {changed}; only that wedding\'s sheet field: {"PASS" if ok else "FAIL"}')
    print(f'Backups: {b.name}, {a.name}')
    if not ok:
        sys.exit(1)


# ---------- kickoff ----------

def kickoff(slug, out, export_file):
    exp = json.loads(Path(export_file).read_text()) if export_file else fetch_export()
    key, w = find_wedding(exp, slug)
    last, mmddyy = folder_parts(slug)
    if w['brand'] != 'Greenway':
        die(f'{w["brand"]} gig sheets are not set up; this tool only builds Greenway sheets.')
    today = datetime.datetime.now(HOUSTON).date()
    if not out and datetime.date.fromisoformat(w['date']) < today:
        die(f'{w["date"]} is in the past. Use --out <scratch dir> to dry-run an old wedding.')
    if not out and w.get('sheet'):
        die(f'"{slug}" already has a gig sheet: {w["sheet"]}')
    if not w.get('venue'):
        die('this wedding has no venue on scheduling. Fill it there first.')
    if not w.get('client') or w['client'] == 'Wedding':
        die('this wedding has no client name on scheduling yet (reads "Wedding"). Fill it there first.')
    root = Path(out).expanduser().resolve() if out else GIGS
    dest = root / last / mmddyy
    if dest.exists():
        die(f'{dest} already exists. Never overwrite a wedding folder.')

    size, unconfirmed, has_sound = band_size(w.get('lineup', {}))
    ex_couple, ex_base, _ = example_ids()
    ex_date = re.search(r'data-date="(\d{4}-\d\d-\d\d)"', (EXAMPLE / 'band.html').read_text())
    d = datetime.date.fromisoformat(w['date'])
    ctx = dict(client=w['client'], client_html=html.escape(w['client'], quote=False), venue=w['venue'],
               venue_html=html.escape(w['venue'], quote=False), date=w['date'], long_date=long_date(w['date']),
               dots=f'{d:%m.%d.%y}', last=last, mmddyy=mmddyy, base=f'/{last}/{mmddyy}/', size=size,
               has_sound=has_sound, ex_couple=ex_couple, ex_base=ex_base,
               ex_long_date=long_date(ex_date.group(1)) if ex_date else '')
    build(ctx, dest)
    row = hub_row(ctx)
    if out:
        (root / 'HUB_ROW.txt').write_text(row + '\n')
    else:
        add_hub_row(row)

    print(f'Kicked off {w["client"]}, {ctx["long_date"]}, {w["venue"]}')
    print(f'  folder  {dest}')
    print(f'  hub row {"written to " + str(root / "HUB_ROW.txt") if out else "added to greenway-gigs/index.html"}')
    print(f'  band    {size}-piece from the scheduling lineup' + (' + sound engineer' if has_sound else ', no sound tech booked'))
    if unconfirmed:
        print(f'          unconfirmed: {", ".join(unconfirmed)}')
    print('Still needed (create-gig-sheet skill): timeline PDF, questionnaire, full Gmail threads;'
          ' venue city + address; time zone if not Houston; MC page decision; share image; PDFs.')
    print(f'Before deploy: gig-kickoff.py --check {dest}   After deploy: gig-kickoff.py --link {slug}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('slug', nargs='?')
    ap.add_argument('--out')
    ap.add_argument('--export')
    ap.add_argument('--check', metavar='FOLDER')
    ap.add_argument('--link', metavar='SLUG')
    a = ap.parse_args()
    if a.check:
        check(a.check)
    elif a.link:
        link(a.link)
    elif a.slug:
        kickoff(a.slug, a.out, a.export)
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
