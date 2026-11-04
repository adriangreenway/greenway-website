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
