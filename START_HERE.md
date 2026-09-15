# START HERE: The Greenway Band Website

This is your control panel. Claude Code keeps it updated. If you're ever lost, read this file and nothing else.

---

## What this project is
The public marketing website for The Greenway Band, your Houston premium live wedding/event band. It's a static site (Astro) that will eventually replace your current Squarespace site at greenwayband.com. Its one job: turn couples and planners visiting the site into booking inquiries through the Book form.

---

## Health

**STATUS:** YELLOW
**Last verified build:** 2026-07-30 (`npm run build` clean, 6 pages; no test suite exists in this repo, so that's the whole check)
**Blockers:** None. Both site tracks are deliberately on hold by your own decision: the Astro rebuild waits for Growth Hour's M3, and the Squarespace form's go-live waits until both builds are entirely done (docs/DECISIONS.md D13).
**Heads up (2026-09-15):** Becca and Henry are mid-way through Song Selections (40 songs ranked, not yet sent) and emailed that the page stopped saving. Their work is safe. Two fixes are now DEPLOYED and production-checked (commits `94d3fad` and `f7ae2c9`, latest deploy `6aa96523000db6fbffacc788`); the second closed four ways two phones on one link could still lose a song or get stuck at Send, each proven in a browser before and after. What's left is yours: send Becca the drafted reply (reload the same link, nothing is lost) and add your Bailamos answer. The fix counts as confirmed only once they tell you Send worked. Portal: `selections.greenwayband.com/portal`, login in 1Password `Greenway Song Selections Portal`. Older: the premium Matey Band Sheet and Listening Room are live, production-checked, and safe to send at `gigs.greenwayband.com/matey/08-01-26/`. Full and MC are now protected at `gigadmin.greenwayband.com`; the old public routes return `404`, and cache v22 removes the old private cache after a device reconnects. The site still has the known branch split and preserved April changes; both repos have local commits not yet pushed. **New on 2026-08-05:** the Jones proposal is live and its intro email is sent; the same deploy repaired the proposals site after a stale drag-and-drop deploy the night before had silently broken photos, video, the song list, and two proposals. If anyone deploys to proposals.greenwayband.com outside the Claude runbook again, the same breakage can recur.

GREEN means everything works and it's safe to build. YELLOW means something needs attention first. RED means stop and run a fix-bug or audit session before anything else.

---

## Being worked on right now
Four separate things going, plus the song list which just wrapped. Only the Astro rebuild is paused.

**The Astro rebuild: paused, on purpose.** You decided 2026-07-03, in a session about your Growth Hour app, that greenwayband.com stays on Squarespace for now. This Astro rebuild is about 70% done and resumes after Growth Hour's M3 milestone ships.

**The Squarespace lead-form embed: built, tested, and holding before the last step.** The form is live and dark at `greenwayband.com/inquiry-test` and your phone test landed correctly in Growth Hour. The only remaining step is making it public (Gate 3), and you decided that waits until BOTH this website and the Growth Hour app are entirely finished (docs/DECISIONS.md D13). Nobody should raise it until you do.

**Client proposals: the third track, never paused.** Newest: Randy Jones (father of the bride, Nora, June 11, 2027, The Woodlands CC Palmer Course) passed the D19 vetting gate 3 for 3 and was independently verified as a real Houston business owner referred by the venue's real events director. His proposal is live at `proposals.greenwayband.com/jones/` and the intro email was sent 2026-08-05. Still waiting on Brooks Kendall's answers before revising `/mckinney-juneteenth/` again. The D19 gate qualifies every lead before any pricing goes out.

**Gig sheets: Matey is live, premium, stable, and split by audience.** Band and Listening stay public in the Greenway look. Full and MC live behind the `Greenway Gig Admin` password saved in 1Password. The Apple-inspired motif stays inside the private admin origin. Stage 3A is complete: seven historical weddings were found across nine Netlify sites without changing any of them. Three have usable local source; four need recovery or reconciliation. Stage 3B builds the tested dual-audience workflow next.

**Your song list: started and finished today, its own small track.** Your full song list, all 434 songs including the Bob Marley add, now lives at `proposals.greenwayband.com/song-list` — same look as your proposals, a genre row across the top with dividers like your homepage's venue line, search built in. A first pass came back green and got rejected on the spot ("our color scheme isn't green"); the rebuild matches your proposal design exactly instead. You tried it on Squarespace too, hit two real snags there (one was your site's own pre-existing footer-color bug, now fixed; the other was Squarespace mangling apostrophes on paste, also fixed at the source) and then decided to drop the Squarespace copy entirely and keep only the proposals page. Every new proposal now links to it, right under the video.

**What happened last session (2026-07-23, proposal redesign, 3 sessions in one day):** you asked for a bigger upgrade to how proposals look and feel: real photos of the band, a real video people can watch, and a button to book a call, right on the page. Built it, stress-tested it, you reviewed and refined it (lighter background, self-hosted video, venue-strip trust line dropped, an optical text-weight fix, a softer photo transition). That version (v4) is committed. Session 3: you took a draft PDF to ChatGPT for a fresh look and brought back two briefs. First made the photo layout and PDF export genuinely better (whole-frame photos, a proper multi-page PDF instead of one sliced mid-sentence). The second, a bigger correction pass, you did not like once you saw it: **"I'm not liking these changes."** That work is built but deliberately not committed, and production was never touched. **Then today (2026-07-24):** three rounds, all done. Round one restored the original package layout and put Schedule a Call back as the main closing button. Round two: the 10-Piece is now always the Recommended, always-first option, both packages sit side by side on a desktop screen (stacked on phone), and the video section is just the label, player, and one caption. Round three: a "50% deposit secures your date" line was tried and then cut, the one thing you actually wanted gone, everything else you liked stayed exactly as it was. Names stay 6-Piece Band and 10-Piece Band. All of it is committed, pushed to GitHub, and **live now** at `proposals.greenwayband.com/hinojosa` — you asked for the update and it's done.

**Your Boston EPK: live and complete.** It now has its own address at `epk.greenwayband.com`, separate from client proposals. The page, email card, and reel were production-verified. It remains hidden from search engines with `noindex` until you decide otherwise.

**Reconciliation debt, whenever you want it tackled (not urgent, part of the Astro track only):**
- Two branches disagree about which pages exist: `dev` (the one that's live) is missing the Reviews and FAQ pages that `main` already has.
- There's unfinished, uncommitted work sitting in this project from April that was bringing the two branches together, but was never finished.
- The test/staging web address currently bounces visitors to your old Squarespace site instead of showing the new build.

None of these affect your live site today, because your live site is still Squarespace either way.

---

## Your next step

Run the start-session skill. Context: both Song Selections fixes (94d3fad stale-tab merge, f7ae2c9 two-phone merge paths) were deployed and verified 2026-09-15; I replied to Becca and Henry. Tell me whether they've confirmed Send worked (check Gmail thread "Music selections" and the portal at selections.greenwayband.com/portal, read only). If yes, close that item and start Stage 3B of docs/gig-sheets/PRIVATE_ADMIN_PLAN.md via build-feature. If they report a new error, run fix-bug on ~/greenway-music-priorities.

<!-- previous next-step kept below for history -->

**Build Stage 3B of the protected gig admin portal.**

Start the next session on Sol and paste:

**Run the start-session skill. Context: Gig Admin Stages 1 and 2 are live and Stage 3A's read-only inventory is complete. Read `docs/gig-sheets/PRIVATE_ADMIN_PLAN.md` and run build-feature for Stage 3B only: correct the stale Gig Sheet workflow, split public Greenway pages from private admin pages, add duplicate, missing-file, privacy, and full-folder safety checks, then prove it with sample-only data. Do not migrate an older wedding or deploy anything.**

Separately, the Astro rebuild still waits for Growth Hour's M3. The EPK is live; lifting `noindex` is optional whenever you want it searchable.

---

## Where things live
| File | What it is |
|---|---|
| `AGENTS.md` | Codex's permanent project rules. |
| `.agents/skills/` | Repo-scoped Codex workflows, including `$create-proposal`. |
| `CLAUDE.md` | Claude's permanent rules. You never need to touch it. |
| `docs/CURRENT_STATE.md` | The current truth. What works, what's active, what's blocked. |
| `docs/PROJECT_BRIEF.md` | Stable facts. Product, stack, hosting, design direction, the 13 approved venues. |
| `docs/ROADMAP.md` | The plan. Now, Next, Later, Not planned. |
| `docs/DECISIONS.md` | Big choices that must not be silently reversed. |
| `docs/CHANGELOG.md` | The archive. Finished history lives here. |
| `docs/HANDOFF.md` | Deep per-session engineering history from the 2026-06-27 recovery pass. Claude reads it for detail. |
| `docs/PROJECT_STATE.md`, `ARCHITECTURE.md`, `INTEGRATIONS.md`, `DESIGN_SYSTEM.md`, `CONTENT_AND_MESSAGING.md` | Deep, evidence-backed reference docs from the recovery pass. Still authoritative for their topics. |
| `docs/squarespace/` | The dark Squarespace lead-form embed: the code to paste in, plus setup steps and the gate checklist. Not part of the Astro build. |
| `docs/adrian-epk/` | Your Boston press kit: the copy, the page generator, the media scripts, and the notes on every video clip used. Not part of the Astro build. |
| `docs/song-list/` | Your song list: the source spreadsheet, the page generator, and how to add or remove a song. Deploys to your proposals site, not part of the Astro build. |
