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
**Heads up:** the current Matey Band Hub and all three practice tracks are live and production-checked at `gigs.greenwayband.com/matey/08-01-26/`, but Adrian wants one final planning pass before sending it. The site still has the known branch split and preserved April changes; both repos have local commits not yet pushed.

GREEN means everything works and it's safe to build. YELLOW means something needs attention first. RED means stop and run a fix-bug or audit session before anything else.

---

## Being worked on right now
Four separate things going, plus the song list which just wrapped. Only the Astro rebuild is paused.

**The Astro rebuild: paused, on purpose.** You decided 2026-07-03, in a session about your Growth Hour app, that greenwayband.com stays on Squarespace for now. This Astro rebuild is about 70% done and resumes after Growth Hour's M3 milestone ships.

**The Squarespace lead-form embed: built, tested, and holding before the last step.** The form is live and dark at `greenwayband.com/inquiry-test` and your phone test landed correctly in Growth Hour. The only remaining step is making it public (Gate 3), and you decided that waits until BOTH this website and the Growth Hour app are entirely finished (docs/DECISIONS.md D13). Nobody should raise it until you do.

**Client proposals: the third track, never paused.** Brooks Kendall's Juneteenth proposal is live at `proposals.greenwayband.com/mckinney-juneteenth/`. Brooks corrected the production responsibility and gave a $10,000–$15,000 budget, so Adrian asked two follow-up questions before another revision. The new D19 gate now qualifies every lead before any pricing or proposal is prepared. In Codex, invoke that workflow with `$create-proposal`.

**Gig sheets: Matey is live and stable, but the Band Sheet is not final.** The next pass keeps pre-dinner calls and logistics at the top, then makes the reception schedule reflect the planner timeline from dinner set onward, with song selections shown where they occur. The Full and MC pages remain unlinked and Adrian-only.

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
**Plan the final Matey Band Sheet timeline before sending it to the musicians.**

Start the next session on Sol and paste:

**Run the start-session skill. Context: the current Matey Band Sheet is live and stable at `gigs.greenwayband.com/matey/08-01-26/`, but it is not final. Then plan the next revision: keep pre-dinner calls and logistics in the top block, make the reception schedule reflect the planner timeline from dinner set onward, and place every selected song at the moment it occurs. Keep it informative and easy to read while preserving the band-versus-Adrian audience split.**

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
