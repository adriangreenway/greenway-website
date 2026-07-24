# START HERE: The Greenway Band Website

This is your control panel. Claude Code keeps it updated. If you're ever lost, read this file and nothing else.

---

## What this project is
The public marketing website for The Greenway Band, your Houston premium live wedding/event band. It's a static site (Astro) that will eventually replace your current Squarespace site at greenwayband.com. Its one job: turn couples and planners visiting the site into booking inquiries through the Book form.

---

## Health

**STATUS:** YELLOW
**Last verified build:** 2026-07-03 (`npm run build` clean, 6 pages; no test suite exists in this repo, so that's the whole check)
**Blockers:** None. Both site tracks are deliberately on hold by your own decision: the Astro rebuild waits for Growth Hour's M3, and the Squarespace form's go-live waits until both builds are entirely done (docs/DECISIONS.md D13).
**Heads up:** the site lives on two branches that disagree with each other (`dev` and `main`). The docs and workflow files are now committed and pushed (2026-07-14); the only uncommitted things left are the April page files that belong to that branch cleanup (kept safe on purpose), one stale leftover folder (`public/proposals/`), and a small local dev-server config tweak. The proposal template work (v5–v8) is committed as of 2026-07-24. Nothing is broken, but don't commit or push here without reading `docs/CURRENT_STATE.md` first.

GREEN means everything works and it's safe to build. YELLOW means something needs attention first. RED means stop and run a fix-bug or audit session before anything else.

---

## Being worked on right now
Two separate things. Only one is paused.

**The Astro rebuild: paused, on purpose.** You decided 2026-07-03, in a session about your Growth Hour app, that greenwayband.com stays on Squarespace for now. This Astro rebuild is about 70% done and resumes after Growth Hour's M3 milestone ships.

**The Squarespace lead-form embed: built, tested, and holding before the last step.** The form is live and dark at `greenwayband.com/inquiry-test` and your phone test landed correctly in Growth Hour. The only remaining step is making it public (Gate 3), and you decided that waits until BOTH this website and the Growth Hour app are entirely finished (docs/DECISIONS.md D13). Nobody should raise it until you do.

**Client proposals: the third track, never paused.** Kate Campbell's proposal shipped 2026-07-23, live at `proposals.greenwayband.com/campbell` (10-piece $14,375 recommended, 6-piece $10,350, cocktail hour cards), and her reply email went out the same day, links verified clean. Two defaults changed on this build: the 10-piece now leads Recommended by default on every new proposal (previously it depended on what the client asked for), and the cocktail hour option cards now show by default on every wedding proposal (previously only when you asked for them).

**What happened last session (2026-07-23, proposal redesign, 3 sessions in one day):** you asked for a bigger upgrade to how proposals look and feel: real photos of the band, a real video people can watch, and a button to book a call, right on the page. Built it, stress-tested it, you reviewed and refined it (lighter background, self-hosted video, venue-strip trust line dropped, an optical text-weight fix, a softer photo transition). That version (v4) is committed. Session 3: you took a draft PDF to ChatGPT for a fresh look and brought back two briefs. First made the photo layout and PDF export genuinely better (whole-frame photos, a proper multi-page PDF instead of one sliced mid-sentence). The second, a bigger correction pass, you did not like once you saw it: **"I'm not liking these changes."** That work is built but deliberately not committed, and production was never touched. **Then today (2026-07-24):** two rounds, both done. Round one restored the original package layout and put Schedule a Call back as the main closing button, per your correction spec. Round two, on your feedback: the 10-Piece is now always the Recommended option and always shown first (the price walking down makes the 6-Piece feel like the saving), on a desktop screen the two packages sit side by side so both prices are visible at once, on a phone they stack, and the video section is just the small label, the player, and one caption now. Names stay 6-Piece Band and 10-Piece Band. You approved the draft ("this is great") and the work is committed. Marli's live page stays untouched until you say otherwise.

**Reconciliation debt, whenever you want it tackled (not urgent, part of the Astro track only):**
- Two branches disagree about which pages exist: `dev` (the one that's live) is missing the Reviews and FAQ pages that `main` already has.
- There's unfinished, uncommitted work sitting in this project from April that was bringing the two branches together, but was never finished.
- The test/staging web address currently bounces visitors to your old Squarespace site instead of showing the new build.

None of these affect your live site today, because your live site is still Squarespace either way.

---

## Your next step
**Right now:** the proposal template is settled and committed. Final copy ruling: the deposit line is the only thing removed (payment details live in your 17hats contract and invoice flow, never on the page), everything else stays exactly as you approved, "Two Ways to Fill the Room" included. Say **push** to back the last commit up to GitHub. Separate call: whether Marli's live page gets the new version (her July 21 original stays up until you say so). The "next steps" reply email is parked until you ask for it.

Everyone with a live proposal today (Garrett, Giulia, Marli, Kate) still has their original links working no matter what you decide, nothing is live-broken. Two small offers stay open, either starts with one word: the fix that stops proposal pages showing you hour-old copies after a revision, and moving the GitHub access key on this Mac into the keychain.

**Separately, whenever:** the Astro rebuild waits for Growth Hour's M3. When that ships, start a session here on **Sonnet 5** and say:

**Run the start-session skill. Context: resuming the Astro site after the Growth Hour pause.**

If you want the branch/reconciliation cleanup done sooner, just say so in a session and it'll run as its own small task, no need to wait for the pause to lift.

Claude runs all commands itself. You never open Terminal. Squarespace's own dashboard is the one exception right now — Claude doesn't have a connected browser this session, so that one paste-in step is yours.

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
