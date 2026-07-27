# START HERE: The Greenway Band Website

This is your control panel. Claude Code keeps it updated. If you're ever lost, read this file and nothing else.

---

## What this project is
The public marketing website for The Greenway Band, your Houston premium live wedding/event band. It's a static site (Astro) that will eventually replace your current Squarespace site at greenwayband.com. Its one job: turn couples and planners visiting the site into booking inquiries through the Book form.

---

## Health

**STATUS:** YELLOW
**Last verified build:** 2026-07-26 (`npm run build` clean, 6 pages; no test suite exists in this repo, so that's the whole check)
**Blockers:** None. Both site tracks are deliberately on hold by your own decision: the Astro rebuild waits for Growth Hour's M3, and the Squarespace form's go-live waits until both builds are entirely done (docs/DECISIONS.md D13).
**Heads up:** your EPK is finished, approved, and sitting on a private preview link. It is deliberately NOT public yet, because you asked to move it off the proposals address first and publishing it now would give you a link that changes next week. One correction worth knowing before next session: your domain's DNS is run by Cloudflare, not Squarespace, so the new address gets set up there instead. The site still lives on two branches that disagree (`dev` and `main`). Uncommitted leftovers are the April page files (kept safe on purpose), a stale `public/proposals/` folder, and the Codex files (`AGENTS.md`, `.agents/`). Both repos have commits on this Mac not yet backed up to GitHub, waiting on your word. Nothing is broken.

GREEN means everything works and it's safe to build. YELLOW means something needs attention first. RED means stop and run a fix-bug or audit session before anything else.

---

## Being worked on right now
Four separate things going, plus the song list which just wrapped. Only the Astro rebuild is paused.

**The Astro rebuild: paused, on purpose.** You decided 2026-07-03, in a session about your Growth Hour app, that greenwayband.com stays on Squarespace for now. This Astro rebuild is about 70% done and resumes after Growth Hour's M3 milestone ships.

**The Squarespace lead-form embed: built, tested, and holding before the last step.** The form is live and dark at `greenwayband.com/inquiry-test` and your phone test landed correctly in Growth Hour. The only remaining step is making it public (Gate 3), and you decided that waits until BOTH this website and the Growth Hour app are entirely finished (docs/DECISIONS.md D13). Nobody should raise it until you do.

**Client proposals: the third track, never paused.** Kate Campbell's proposal shipped 2026-07-23. Marli Hinojosa's proposal was redesigned and updated live today (2026-07-24) at `proposals.greenwayband.com/hinojosa`: original package layout restored, 10-piece band now always the recommended, first-shown option, both packages sit side by side on a desktop screen, and the video section is simpler. The 10-piece-first default now applies to every new proposal going forward.

**Your song list: started and finished today, its own small track.** Your full song list, all 434 songs including the Bob Marley add, now lives at `proposals.greenwayband.com/song-list` — same look as your proposals, a genre row across the top with dividers like your homepage's venue line, search built in. A first pass came back green and got rejected on the spot ("our color scheme isn't green"); the rebuild matches your proposal design exactly instead. You tried it on Squarespace too, hit two real snags there (one was your site's own pre-existing footer-color bug, now fixed; the other was Squarespace mangling apostrophes on paste, also fixed at the source) and then decided to drop the Squarespace copy entirely and keep only the proposals page. Every new proposal now links to it, right under the video.

**What happened last session (2026-07-23, proposal redesign, 3 sessions in one day):** you asked for a bigger upgrade to how proposals look and feel: real photos of the band, a real video people can watch, and a button to book a call, right on the page. Built it, stress-tested it, you reviewed and refined it (lighter background, self-hosted video, venue-strip trust line dropped, an optical text-weight fix, a softer photo transition). That version (v4) is committed. Session 3: you took a draft PDF to ChatGPT for a fresh look and brought back two briefs. First made the photo layout and PDF export genuinely better (whole-frame photos, a proper multi-page PDF instead of one sliced mid-sentence). The second, a bigger correction pass, you did not like once you saw it: **"I'm not liking these changes."** That work is built but deliberately not committed, and production was never touched. **Then today (2026-07-24):** three rounds, all done. Round one restored the original package layout and put Schedule a Call back as the main closing button. Round two: the 10-Piece is now always the Recommended, always-first option, both packages sit side by side on a desktop screen (stacked on phone), and the video section is just the label, player, and one caption. Round three: a "50% deposit secures your date" line was tried and then cut, the one thing you actually wanted gone, everything else you liked stayed exactly as it was. Names stay 6-Piece Band and 10-Piece Band. All of it is committed, pushed to GitHub, and **live now** at `proposals.greenwayband.com/hinojosa` — you asked for the update and it's done.

**Your Boston EPK: the fourth track, now on its second build, never paused.** Your own press kit for Boston work, separate from the band's site. You took the first build to ChatGPT for a second opinion and it made a good point: one page presenting you as one performer reads better than making visitors pick between "solo you" and "band you." So that's what it is now, one page: your reel front and center, an Email button right below it, then a short line about your experience and range, then contact. It will live at `proposals.greenwayband.com/adrian`, hidden from Google, only seen by people you send the link to. Built and checked on this Mac, nothing published yet. Same calls as before still stand: no Vimeo, videos play right inside the page like your proposals do; the 9-piece promo video is out everywhere because that's your other singer up front, not you. **The reel is settled, your call: the full 2 minutes 21 seconds.** You tried a 55-second cut, watched it, and decided you'd rather keep every clip in — anyone who doesn't want the whole thing can just stop watching. The full-length version is back on the page, with one quiet improvement kept from the short-cut experiment: the closing title card inside the video now says "Boston Vocalist & Live Performer" instead of the old wording that leaned on acoustic guitar. Nothing about it is live, so everything is still easy to change.

**Reconciliation debt, whenever you want it tackled (not urgent, part of the Astro track only):**
- Two branches disagree about which pages exist: `dev` (the one that's live) is missing the Reviews and FAQ pages that `main` already has.
- There's unfinished, uncommitted work sitting in this project from April that was bringing the two branches together, but was never finished.
- The test/staging web address currently bounces visitors to your old Squarespace site instead of showing the new build.

None of these affect your live site today, because your live site is still Squarespace either way.

---

## Your next step
**Give your EPK its own web address, then put it live.** The page itself is done and you already approved it. The only
open question is where it lives. Right now it would sit under your proposals address, and you said that address was
only ever meant for actual client proposals. So the last step is a new address of its own.

One thing I got wrong side up until now and you should know: **your domain is run through Cloudflare, not Squarespace.**
The DNS panel in Squarespace isn't the one your domain actually listens to. That's not a problem, it just means the new
address gets created in a different place than you expected. I'll walk you through it the same way we did the proposals
address.

Start a session on **Sonnet 5** and paste:

**Run the start-session skill. Context: the EPK is approved and draft-deployed but not public. I want to move it to its own web address instead of living under proposals.greenwayband.com, then take it live. Walk me through the address setup the way we did for proposals.**

Expect one question early on: what you want the address to be. Have a preference in mind if you have one.

**Small housekeeping:** say **push** whenever you want today's commits backed up to GitHub (the song-list fix, the proposal-template link, plus the earlier EPK ones). Nothing depends on it. Whenever you want it: a reusable "next steps" reply email (deposit, contract, invoice, payment options).

Everyone with a live proposal today (Garrett, Giulia, Marli, Kate) still has their original links working no matter what you decide, nothing is live-broken. Two small offers stay open, either starts with one word: the fix that stops proposal pages showing you hour-old copies after a revision, and moving the GitHub access key on this Mac into the keychain.

**Separately, whenever:** the Astro rebuild waits for Growth Hour's M3. When that ships, start a session here on **Sonnet 5** and say:

**Run the start-session skill. Context: resuming the Astro site after the Growth Hour pause.**

If you want the branch/reconciliation cleanup done sooner, just say so in a session and it'll run as its own small task, no need to wait for the pause to lift.

Claude runs all commands itself, including your browser when needed. You never open Terminal. Squarespace's own dashboard is the one thing only you can click through, since Claude has no login there — but you've decided to keep the song list off Squarespace entirely, so that's not on the table right now anyway.

---

## Where things live
| File | What it is |
|---|---|
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
