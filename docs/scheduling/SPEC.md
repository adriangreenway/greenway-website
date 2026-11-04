# scheduling.greenwayband.com — Spec v1 (DRAFT, not approved)

**Written:** 2026-11-04. **Status:** PLAN READY. Sign-in decided (Google). Waiting on "build it".
**Track:** independent (like gig sheets / planner). Not the Astro rebuild, not under the D13 go-live hold (that hold covers greenwayband.com itself, not new private subdomains).

## What it is
A private two-person web page that replaces the "January 9, 2027 — Staffing Roster for Sersh" Google Sheet. It looks exactly like mockup v4 (artifact `https://claude.ai/artifact/Xradda8cFt7VRtCVuN3muY`). Adrian and Sersh sign in and edit the lineups for the two Jan 9, 2027 weddings.

Why not the Sheet: Google Sheets could not reproduce the mockup's look (fonts, rules, MD tags, brand toggle).

## Scope v1 (Adrian, 2026-11-04)
- **One date only:** Jan 9, 2027. Two weddings: Shelton / The Forest Club (Greenway) and Hinson / Houston Country Club (Kirby Collective).
- **Two users only:** Adrian and Sersh (sergiogarzaluna@hotmail.com).
- **No email notifications.**
- Both users can edit everything on the page.

## Screens
1. **Sign-in page.** Greenway styled. One "Sign in with Google" button (see Sign-in below).
2. **Lineups tab** (mockup layout): Greenway / Kirby Collective toggle. Each card shows Client, Venue, then 11 positions (Singer 1-3, Keys, Bass, Drums, Guitar, Trombone, Trumpet, Saxophone, Sound tech) with a musician name and an optional MD tag.
3. **Musicians tab** (mockup layout): the pool of names, grouped by instrument.
4. **Edit mode:** tap a name to change it; pick from that instrument's pool or type a new name; toggle MD. A plain Save. Shows "Saved" or "Someone else changed this, reloaded."

## Data (seeded from the mockup, real names only)
Exactly what mockup v4 shows today. No invented musicians, times, money, or statuses. Empty slots stay empty (never "TBD").

## How it's built (Claude's decision, logged here)
- Its own small project folder and its own Netlify site, same proven pattern as planner.greenwayband.com: one page, a server-side login gate, and a Netlify Blobs store for the roster.
- Login is checked on the server before any roster data is sent. Signed, HTTP-only session cookie, 30 days, so Sersh rarely re-signs in on his phone.
- Save uses a version check, so two people saving at once can't silently overwrite each other.
- Automatic daily backup copy of the roster, so any bad edit can be rolled back.
- Brand tokens from the mockup (cream #F5F2ED, ink, Kirby teal #2A6B6B on COLLECTIVE only). Bodoni Moda + Plus Jakarta Sans.
- No Supabase, Stripe, Twilio, or Growth Hour code. Nothing from this repo's `src/` is touched.
- `noindex`, never linked from greenwayband.com.

## Stages
| Stage | What | Gate (done means) | Model | Sessions |
|---|---|---|---|---|
| 1. Look (BUILT 2026-11-04, locally verified) | The page, read-only, real data, previewed locally | Adrian says it matches the mockup on desktop and phone | Sonnet 5 | 1 |
| 2. Login + saving (CODE BUILT 2026-11-04, locally verified; real Google sign-in not yet tested) | Sign in with Google (2-address allowlist), edit mode, saving, version check, backups | Signed-out visitor sees no roster data; both accounts can sign in, edit, save; a second device sees the change after reload | Fable 5 | 1 |
| 3. Launch (LIVE 2026-11-04) | Netlify site, scheduling.greenwayband.com DNS (Adrian approves the Cloudflare record), phone test, Sersh gets his login | Live at the address, Adrian and Sersh both sign in on their phones | Sonnet 5 | 1 (short) |

**Estimate: 3 sessions.** Add 1 if the look needs more than one round of tweaks.

## Risks
- **Login / privacy (medium):** the page holds names only, but a weak gate would let anyone edit. Mitigation: server-side check, rate limit on sign-in, Stage 2 gate test.
- **Lost edits (low):** version check plus daily backups.
- **DNS (low):** one new Cloudflare record, Adrian approves before it's added.
- **Sersh's Google address (note):** must be the exact Gmail he signs in with, or he's locked out.

## Sign-in (DECIDED 2026-11-04, Adrian: "Sign in with Google")
- Sign in with Google only. An allowlist of exactly two Google addresses; any other Google account is refused.
- Adrian: adrian@greenwayband.com. Sersh: **sershkeys@gmail.com** (assumption: the Gmail Adrian used for the Montana note; confirm with Adrian before Stage 2).
- Needs its own Google OAuth client. The planner's Google project is "Internal" (greenwayband.com accounts only), so it would block Sersh's Gmail. New client uses an External consent screen with only basic sign-in scopes (name + email), which needs no Google review.
- Server-side code flow: the Netlify function swaps Google's code for the verified email, checks the allowlist, then sets the session cookie. Client secret lives only in Netlify env vars and a 1Password item named `Greenway Scheduling Google OAuth` (created in Stage 2, never printed).
- Adrian may need to click once in Google Cloud Console to create the client; Claude can't approve Google consent screens for him.

## Out of scope v1 (later, if wanted)
Other dates, more users (Joe), email alerts, change history, availability statuses, money.

## Stage 1 notes (2026-11-04)
- Files: `public/index.html` (mockup CSS kept as-is, rendered from data), `public/roster.json` (seed, exactly mockup v4's names), `public/robots.txt`. Preview: launch.json `scheduling`, port 8813.
- Cut from the mockup: the working title "Staffing sheet, branded" above the toggles (mockup label, not page copy). The bottom tab strip is kept and now clickable.
- Centered (Adrian 2026-11-04, "weird all that space on the right"): content column 520px (Musicians 640px), brand mark, title, and toggles centered.
- Checked: Greenway and Kirby views, Musicians tab, 375px phone width with no sideways scroll, no console errors.

## Stage 2 notes (2026-11-04, built on Opus 5.5; Adrian no longer has Fable)
- Google sign-in uses Google's "redirect" button and checks Google's signed ID token on the server (`netlify/functions/auth-google.mjs`, `jose`). No Google client secret exists or is needed; the client ID is public.
- Env vars (Netlify, never in git): `GOOGLE_CLIENT_ID`, `SESSION_SECRET` (random, generated by Claude, never printed), `ALLOWED_EMAILS` (`adrian@greenwayband.com,sershkeys@gmail.com`). Local `.env` is gitignored and holds a throwaway secret.
- Roster lives in Netlify Blobs store `scheduling`, key `jan-9-2027`; daily backup `backup:jan-9-2027:<date>`. Seed moved to `netlify/lib/seed.json`, no longer public.
- Local lock tests (netlify dev + forged cookies): no cookie, stranger, tampered, expired all 401; Adrian/Sersh 200; stale save 409; wrong content type 415; overlong text 400; page HTML holds no names; noindex header. All PASS. Edit, Save, Cancel, Sign out checked in the browser at desktop and 375px (one sideways-scroll bug found and fixed).
- Sign-in rate limit from the risk list dropped: no passwords exist to guess.
- Still needed (Stage 3): a Google Cloud project with an External consent screen and a web client ID whose origin and redirect are `https://scheduling.greenwayband.com` and `/api/auth/google`. Real Google sign-in is tested only after that.

## Stage 3 + portal (2026-11-04)
- LIVE at https://scheduling.greenwayband.com (Netlify site `greenway-scheduling`, id 51069c4e-b3ef-435e-a3f8-5c4c95295bc4, team adrian-xyeekr0). Cloudflare CNAME `scheduling` -> greenway-scheduling.netlify.app, DNS-only (Adrian approved).
- Google Cloud project `greenway-scheduling` (org greenwayband.com), Google Auth Platform: External, Testing mode, test users = adrian@greenwayband.com + sershkeys@gmail.com (Google itself refuses anyone else). Web client ID 924882843974-ngr7ntd0tqvpjr1vt40h684ee91fpb29 (public); origin `https://scheduling.greenwayband.com`, redirect `/api/auth/google`. The client secret Google displayed was NOT saved anywhere; the site doesn't use it. Adrian agreed to Google's API User Data Policy in chat.
- Adrian confirmed a real Google sign-in reached the roster.
- Adrian's redesign (same day): home is a portal listing every wedding (date, client, venue, brand); click opens that wedding; Musicians link at the bottom. No big headers anywhere ("January 9, 2027 Staffing" removed, sign-in page = wordmark + Google button only). "Staffing" renamed "Scheduling" (page title "Greenway Scheduling"). MD shown as "Sersh (MD)" in the same font. Brand toggle and fake spreadsheet tab strip removed; each wedding shows its own brand mark. Links: `#/shelton-01-09-27`, `#/hinson-01-09-27`, `#/musicians`.
- Adding a future wedding = add it to `netlify/lib/seed.json` (id, slug, date, brand, client, venue) and deploy.

## Tweaks round (2026-11-04, LIVE)
Adrian: dotted lines and per-row MD boxes made no sense; Musicians ran out of slots; sign-in was "a random cream square." Shipped: every page uses the gigs.greenwayband.com shell (masthead wordmark, rules, gig-hub rows); one grey field style for lineups and Musicians; one MD dropdown per wedding (server keeps only one MD); each instrument always has an empty "Add name" field (cap 60). Scheduling commits `760dadf` + footer fix; prod `6aeb86353efe3e5755e43d34`, rollback `6aeb5d74ffa53e33c78bc105`. Live page hash matches local; signed-out visitors see no names; Google button renders live.

## v2 plan: living scheduling site (APPROVED 2026-11-04 "build it"; Stage 1 LIVE, Stage 2 next)
**Goal:** Adrian and Sersh keep adding weddings as they book, without Claude, and old ones drop to a Past list.
**Size:** Large (changes how saved data is stored). Two stages, each verified on its own.
- **Stage 1, storage:** one saved record per wedding plus one for the Musicians list, instead of one record fixed to Jan 9. Existing Jan 9 data copied over exactly (diffed before/after; the old record kept as a backup). Saves are checked per wedding, so Adrian editing Shelton never collides with Sersh editing Hinson. Portal splits into Upcoming and Past by date, like the gig hub. Fixes the trap where adding a wedding to `seed.json` would have broken the page.
- **Stage 2, add/remove:** "Add wedding" (date, client, venue, brand: Greenway or Kirby Collective) creates an empty lineup. "Remove wedding" asks to confirm, then hides it; nothing is truly deleted, Claude can restore it.
**Risks:** moving live data (mitigated by backup + exact diff before switching); one more write path on a signed-in-only API (same allowlist and size checks). Sign-in itself unchanged.
**Done means:** (1) Jan 9 lineups and Musicians identical after the move; (2) a new wedding added from a phone appears for the other person after reload; (3) removing one asks first and is restorable; (4) a wedding after its date shows under Past; (5) signed-out visitors still get no data; (6) two people saving different weddings at once both succeed.
**Files:** modify `~/Desktop/greenway-scheduling/{public/index.html, netlify/functions/roster.mjs, netlify/lib/roster.mjs, netlify/lib/seed.json}`, maybe one new function; read `netlify/lib/session.mjs`; off limits: `auth-google.mjs`, `session.mjs`, Netlify env vars, Google Cloud settings, DNS, this repo's `src/`.
**Model:** strongest available (Opus 5.5) for Stage 1 data move; Sonnet fine for Stage 2.
**Out of scope:** email alerts, more users, availability/money, change history.

## v2 Stage 1 (LIVE 2026-11-04)
- Scheduling commit `3dfcdd6`, prod `6aeb873d705474c32047c1cb` (rollback `6aeb86353efe3e5755e43d34`).
- Before deploy the live store was EMPTY: nobody had ever saved on the live site (the "test" singer in Adrian's screenshot was typed in edit mode, never saved). So the move is seed -> new records, no real edits at stake.
- Records: `w:gw`, `w:kc`, `musicians`; daily `backup:<key>:<date>`. The first signed-in page load creates them (copies v1 `jan-9-2027` if it exists, else seed). API: GET `/api/roster`, PUT `/api/wedding/:id`, PUT `/api/musicians`.
- Local tests PASS: lock (no cookie, tampered), migration of an old v1 record exact, two people saving different weddings at once, stale save 409, one MD, date/brand fixed, 404/415/400/405, musicians save/stale. Page: lineup + musicians save, Upcoming shows, Past hidden when empty, day-after cutoff (Houston time).
- Live: page hash matches local; all API routes 401 signed out. Migration on live confirmed only after Adrian's next sign-in.
- `seed.json` now only seeds a brand-new store; adding a wedding = Stage 2's Add button (not seed + deploy).
- Adrian signed in after deploy and saw both weddings under Upcoming. v2 lists only weddings that exist as saved `w:` records, so this confirms the move ran on live.
- **Open issue for Stage 2:** Claude's Netlify CLI and the blobs API both show the `scheduling` store as EMPTY even though the live function reads and writes it (same for v1). So Claude cannot read live data or backups directly today. Stage 2 must add a signed-in way to read or restore it (for example an export of every record plus backups), or "Claude can restore a removed wedding" is not true.
- Tabs fix (Adrian: the Musicians row "looks like a client name"): the row is gone; the toolbar now has `Weddings | Musicians` tabs (open tab underlined), Edit / Sign out right-aligned on one line on phones; repeated "Musicians" label removed. Commit `adfc6ad`, prod `6aeb88612a665f631207140c`, live hash matches.

## v2 Stage 2 (LIVE 2026-11-04)
- Scheduling commit `63a64d3` (+ `.gitignore` for `backups/`); prod `6aeb8ce55b802324d6b20152`.
- **Add wedding** (home toolbar) opens a form: date, client, venue, brand. Slug = last name + mm-dd-yy, made unique (`-2`, `-3`; removed weddings keep their slug). **Remove wedding** sits at the bottom of a wedding in Edit mode, asks to confirm, hides it (record kept, `removed: true`).
- **Claude's maintenance door:** `GET /api/admin/export` (every record incl. removed + daily backups), `POST /api/admin/restore {id}`. Key `ADMIN_KEY` = Netlify secret env + gitignored `~/Desktop/greenway-scheduling/.env.admin` (mode 600). Never printed. Unset key = 404. Export copies land in gitignored `backups/export-<date>.json`.
- **Data finding (resolved):** before Stage 2 the live store held NO records, even after Adrian's sign-in, so his load had not saved anything (cause not determined). A live write test showed the store works and the CLI sees it. Running the move step on live created `w:gw`, `w:kc`, `musicians`; after a further redeploy all three were still there and matched seed exactly. Use the admin export after any change to confirm, never assume.
- Local tests: 19 Stage 2 checks + 14 Stage 1 checks PASS (add validation, slug collisions, remove + stale remove, removed hidden and not editable, export locked to the key, restore). Page: add form and remove clicked through; signed-out POSTs 401; live page hash matches.
- Not yet tested: Adrian or Sersh adding a wedding from a phone and the other seeing it.

## Phone test + "Added" message (2026-11-04, LIVE)
- First phone add never reached the site (likely the black Add wedding button was not tapped; the keyboard's Done key does not submit). Server path re-proven live; local phone-size add works.
- Second try PASS: Adrian added Cade, 2026-11-20, Houstonian, Greenway from his phone; admin export shows `w:f26cd1c125` saved by adrian@greenwayband.com.
- Adrian asked for a confirmation: after adding, the wedding page shows "Added" in the toolbar for 4 seconds; "Removed" fades the same way. Scheduling commit `782bf29`, prod `6aeba28c2e20c7ff85197105`; live page carries the change, live data unchanged.
- Still open: Sersh has not been sent the link.

## Planning Center import (2026-11-04, LIVE data)
- Source: Planning Center roster export xlsx (see `ROSTER_IMPORT_PLAN.md`). Adrian: all musicians, 2026 gigs only.
- Musicians tab: 56 names (every person with an instrument; existing names Dishon, Primo, Joe, Sersh kept; full name only where a first name is shared). Skipped, no instrument on file: Amanda Funes, Amanda Garza (Cam/Social), Chino (Percussion, no group), Ramiro Cortez, Tim Del Toro, Vincent Powell.
- Added 4 gigs with Planning Center's confirmed players: 11/14 Le Tesserae (Gulf Coast Ent. wedding), 12/9 Greenwood King Holiday Party, 12/11 Holiday Party at The Rustic Post Oak, 12/18 House Party. Unconfirmed players would read "(unconfirmed)"; declined left empty. No MD marked.
- Written directly to the blob store with the site's own checks (`cleanWedding`/`cleanMusicians`/`saveChecked`), saved by "imported by Claude (Planning Center)". Backups: `backups/export-2026-11-04-pre-roster-import.json` and `-post-`. Old Musicians list also kept as `backup:musicians:2026-11-04`.
- 2027 weddings researched but NOT added (Adrian: 2026 only for now): 2/13 Victoria & Will (Zaza), 3/6 Huang (River Oaks CC), 4/3 Cheak/Clark (Bell Tower on 34th), 4/10 Dodson (Houstonian), 5/29 Giulia Costantini (Houstonian), 6/5 Jennifer Estes (Briscoe Museum, San Antonio), 6/18 Jessica Freeman (Boxwood Manor), 10/23 Garrett Turner (Le Tesserae). 1/30 Astorian is Andrews Kurth (corporate).
- Not checked in a signed-in browser (Claude can't sign in as Adrian). Jan 9 conflicts untouched, waiting on Adrian.
- **Jan 9 conflicts resolved 2026-11-04 (Adrian): keep the site's lineups.** The site is the truth for Shelton and Hinson; Planning Center differences ignored. No data changed.
- **Past 2026 weddings added 2026-11-04** (Adrian: "should have more than four this year"): 17 from Planning Center's 2026 wedding plans. Couple names and venues come from the gigs.greenwayband.com hub for the 12 with gig sheets (Hawk 3/14 through Hardaway 10/17). Cranfield 1/17 comes from Gmail ("1/17/26 Cranfield", GCE). Four have no confirmed couple name, so the client reads "Wedding": 1/3 Junior League, 1/10 Hotel Zaza, 2/14 Woodlands CC, 2/21 Brenners. Leads seen but not proof: Riley McLean (2/14), Morgan Smit is a planner (2/21). Lineups = Planning Center confirmed players. Live: 24 weddings, 22 in 2026. Backups `export-2026-11-04-pre-past-2026.json` / `-post-`. Non-wedding 2026 gigs (duo/trio, Astros, gala, canceled) not added. 2027 still held.
- Cade 11/20/26 phone-test wedding hidden 2026-11-04 (Adrian). Record kept with removed: true; restorable via /api/admin/restore. 23 weddings shown.
- Centered sign-in page LIVE 2026-11-04 (Adrian: 'centered like a traditional login page'): signed out = wordmark + Scheduling + Google button, centered both ways, no rules or footer. Scheduling commit `81c1b62`; live page hash matches local; screenshot-checked live at desktop and locally at 375px. Signed-in views unchanged.
- Sign-in redone as a classic login card LIVE 2026-11-04 (Adrian: centered layout still didn't read as a login page): cream card, rounded, shadow, on the black page; wordmark + Scheduling, rule, 'Sign in' heading, 300px Google button. Scheduling commit `495827d`; live hash matches; live desktop screenshot + local 375px check (no sideways scroll). Known: about 1 s of the plain cream page shows while the site checks sign-in.
- **Client names rule (Adrian 2026-11-04): the wedding/gig title is ALWAYS the client's name; only exception a holiday party may read '<Company> Holiday Party'.** Fixed from Gmail/17hats contracts: 11/14 Siegel / Dubel (GCE subject '11/14/26 Siegel/ Dubel Reception'), 12/11 MetroNational Holiday Party (The Rustic's lead note), 12/18 Christine Perusquia (17hats contract '12.18.26'; she plans it for a River Oaks host), 2/14 Lally McLean (contract '2.14.26 McLean'), 2/21 Lauren Archer (Brenner's contract, same 17hats contact as the 2/21/26 lead). Slugs changed to match. Still 'Wedding': 1/3 Junior League and 1/10 Hotel Zaza (no contract or GCE thread found). 2027 note: 2/13 contract client is Victoria Garcia (signer Will Rosell). Backup `export-2026-11-04-pre-client-names.json`.
- Titles follow the gig hub's 'Last / Last' couple format (Adrian 2026-11-04, pointing at gigs.greenwayband.com). 2/21 → Archer / Solcher (planner thread 'Archer/Solcher Wedding 2/21/2026'). Still need partner names from Adrian: 1/17 Cranfield, 2/14 McLean (couple Riley + Lynden), and both names for 1/3 and 1/10.
- 2026-11-04, from Adrian's pasted ChatGPT research handoff: CONFIRMED and applied: 1/17 Cranfield / Porter (Ryan Cranfield & Bryan Porter; GCE final vendor timeline PDF), 2/14 McLean / Powers (Riley McLean & Lynden Powers; 17hats questionnaire 10137980). NOT applied, unconfirmed: 1/3 possibly King / Gehm (wedding website matches date and Junior League, no booking link), 1/10 possibly McNamara / Hansen (only a ZaZa hotel block). Claude's Gmail search found neither name. Both still read 'Wedding' until Adrian confirms.
