# Scheduling to gig sheets pipeline: plan

**Written:** 2026-11-04. **Status:** Stage 1 BUILT 2026-11-04 (Adrian: "build it"), locally verified, not yet used on a real new sheet. Stages 2-3 not planned.
**Track:** scheduling + gig sheets (independent of the Astro pause and the D13 go-live hold).

## Goal (one line)
A wedding booked and staffed on scheduling.greenwayband.com becomes the starting point of its gig sheet, so nobody retypes the couple, date, venue, or band size, and the sheet link comes back to scheduling on its own.

## What Adrian does by hand today (verified 2026-11-04)
1. **Books the wedding** (17hats contract). Then he or Sersh taps **Add wedding** on scheduling: date, client, venue, brand.
2. **Staffs it** on scheduling: tap-to-pick each of the 11 slots, one MD.
3. **About a week or two out, asks Claude** "make a gig sheet for X" and attaches the planner timeline + 17hats questionnaire.
4. **Claude rebuilds the basics from scratch:** couple names, date, venue, band size ("10-piece Greenway band"), folder name `<last>/<mm-dd-yy>`, and a hand-typed row in the gigs hub list (`~/Desktop/greenway-gigs/index.html`, `GIGS`). Then the real work: Gmail threads, timeline, specials, MC, Listening Room.
5. **Adrian says "go"**, Claude deploys the whole gigs folder.
6. **Claude sets the "Gig sheet" link** back on scheduling (export, write, export, diff).

Steps 4 (the basics) and 6 are pure retyping of facts scheduling already holds. That is where mistakes creep in (hub said one venue spelling, scheduling another) and where the "is this wedding even on scheduling?" check happens.

**Finding that shapes the plan:** gig sheets do NOT list musicians by name today. The Full sheet says "10-piece Greenway band"; the Band Sheet shows no names. Only Hess named players once ("Cocktail hour duo, Rome and Sersh"). So "staffing in" today means band size and brand, not a roster on the sheet.

**Not automatable, on purpose:** the timeline, specials, MC cues, songs. Those come from emails and PDFs and need Claude reading full threads (copy integrity). The pipeline starts the sheet; it never writes the night.

## Stage 1 (automate first): "Kick off gig sheet" tool, Claude-run
**Size:** Medium. One new local script plus skill/runbook edits. No change to the scheduling site, its data, or sign-in. Nothing deploys.

What it does, given a scheduling wedding slug (e.g. `hardaway-10-17-26`):
1. Reads the wedding through the existing admin export (`.env.admin` key, never printed). Refuses if the wedding is missing, removed, or past.
2. Creates `~/Desktop/greenway-gigs/<last>/<mm-dd-yy>/` from `docs/gig-sheets/EXAMPLE/`, filling only what scheduling knows: couple title, date, venue, brand, band size (counted from filled musician slots, sound tech excluded), clock date, folder paths in `sw.js` / `manifest.json`. Every other fact stays an explicit `<!-- PLACEHOLDER: ... -->`, never "TBD" on the page.
3. Adds the hub `GIGS` row with the same client and venue text scheduling has.
4. Refuses to touch a folder that already exists (never overwrites a live wedding).
5. Prints a short checklist of what's still needed (timeline, questionnaire, time zone if not Houston).

Then `create-gig-sheet` Step 1 starts from this folder instead of a blank copy, and Step 4's link-back becomes one command in the same tool (`--link`), still with export before and after.

**Files to create:** `docs/gig-sheets/tools/gig-kickoff.py`
**Files to modify:** `.claude/skills/create-gig-sheet/SKILL.md`, `docs/gig-sheets/GIG_SHEET_SYSTEM.md`, `docs/scheduling/SPEC.md` (pointer), this file.
**Read only:** `~/Desktop/greenway-scheduling/netlify/lib/roster.mjs`, a fresh admin export, `docs/gig-sheets/EXAMPLE/*`, `~/Desktop/greenway-gigs/index.html`.
**Off limits:** scheduling functions, sign-in, env vars, DNS; every existing wedding folder in `~/Desktop/greenway-gigs`; any deploy; this repo's `src/`; the Codex `.agents/` skill copy (sync later, separately).

**Risks:** low. It writes only a new local folder and one hub line, and refuses existing folders. Band size counted from slots can be wrong if a slot is still empty; the tool says "8 of 10 filled" instead of guessing. Venue time zone isn't in scheduling, so it defaults to Houston time and flags it.

**Done means:**
1. Dry run on a copy for Hardaway produces the same couple, date, venue, and "10-piece" as the live sheet and hub row.
2. No "TBD" anywhere; every unknown is a marked placeholder.
3. It refuses a missing, removed, past, or already-built wedding.
4. The live scheduling export is byte-identical before and after a kickoff (nothing written there until `--link`).
5. `--link` changes only that wedding's `sheet` field (export diff).
6. Nothing deployed; existing wedding folders unchanged (`git`/hash check of `~/Desktop/greenway-gigs`).

**Model:** Sonnet 5 can build it (Medium, local, no auth). Opus 5.5 is fine too.

## Later stages (not planned in detail, not approved)
- **Stage 2, "Needs a gig sheet" nudge:** scheduling shows a quiet tag on upcoming weddings within ~3 weeks that have no sheet link. Front end only.
- **Stage 3, lineup changes after the sheet is live:** decide whether a lineup edit should flag the sheet (for example, band size changed). Only if Adrian wants names or size kept in sync.

## Open question for Adrian (one)
Should gig sheets start showing who's playing (names by instrument)? Default: **no**, keep sheets as they are (band size only). Names change late, and a second copy on the sheet goes stale; scheduling stays the one place for the lineup.

## Stage 1 build notes (2026-11-04)
- Tool: `docs/gig-sheets/tools/gig-kickoff.py` (Python, calls `curl` for the web because this Mac's Python has no certificate bundle; the admin key goes to curl on stdin, never on the command line). `--link` writes through Node with the scheduling site's own `roster.mjs` and `@netlify/blobs`.
- Open question settled by "build it" with the recommended default: sheets do NOT list musicians by name; band size only.
- Band size = filled lineup slots except Sound tech. Plan said "8 of 10 filled"; built instead as the plain count, because empty horn slots are normal for a smaller band.
- Kickoff builds `index.html` (Band Sheet + Listening Room only; MC is a per-wedding call), `band.html`, `gig.html`, `listen.html` (empty), `manifest.json`, `sw.js` (CORE = shipped pages only, no PDFs, no audio). Share images and PDFs are left for the build.
- Verified: dry runs for Hardaway, Dass, Hawk, Siegel into scratch; refusals for missing, removed, Kirby, "Wedding" client, no venue, past, already-built; `--check` flags placeholders, TBD, EXAMPLE leftovers, missing cached files, missing share image, and passes the live Hardaway folder; zero EXAMPLE (Blick) text left in any draft; Siegel draft rendered with no console errors; live scheduling export identical before and after a kickoff; `~/Desktop/greenway-gigs` hashes unchanged (2,935 files); `--link` refuses an undeployed sheet and skips an already-linked one; the Node write path authenticates and reads live records (write itself not exercised; first real use is the next new sheet).
- Findings: (1) Hardaway's scheduling lineup has 9 musicians but its sheet and hub say 10-Piece (Dass 9 and Hawk 6 match). Scheduling may be missing a player (Aiden Ross sang the first dance). Not changed. (2) The live Hess Full sheet and MC page print "TBD" for the hora time (past wedding, Adrian-only pages, predates the rule). Not changed.
- Next real candidate: Siegel / Dubel 11/14/26, Le Tesserae, 10-piece, no sheet yet.
