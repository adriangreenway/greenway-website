# Handoff: The Greenway Skill System (for ChatGPT)

Written 2026-08-05. Give the prompt at the bottom of this file to ChatGPT.
The explainer above it is for you (Adrian) and for any agent that wants the
full picture.

---

## What the skill system is

The greenway-website repo carries 9 "skills." Each one is a playbook file at
`.agents/skills/<name>/SKILL.md` inside the repo at
`~/greenway-website`. A skill is not code. It is a written procedure the AI
must follow for one job: how to start a session, how to plan a feature, how
to build a proposal, and so on. Each file starts with a description that says
exactly when to use it, followed by numbered steps and a required output
format.

The point of the system: Adrian is nontechnical. The skills carry the
engineering discipline so no session depends on the AI remembering it. Any
agent (Claude Code or ChatGPT/Codex) working in this repo follows the same
playbooks and produces the same safety behavior.

## The 9 skills

**Session lifecycle**

1. **start-session** — Opens every work session. Reads
   `docs/CURRENT_STATE.md`, runs `git status`, checks for danger signs
   (uncommitted changes it didn't make, wrong branch, interrupted task),
   then recommends exactly one next action. Fast and cheap, no builds.
2. **end-session** — Closes a session safely. Identifies every uncommitted
   change, updates the record docs only if changes were already authorized,
   and writes a paste-ready opening prompt for the next session. Never
   commits or pushes on its own.

**Engineering discipline**

3. **plan-feature** — Turns a plain-English idea into an approvable plan
   before any code. Sizes the task (Small / Medium / Large / Too Large),
   splits Large into stages, lists files to modify / inspect / never touch,
   defines "done means" criteria. Plans only, never implements. Asks at
   most 3 questions, only about what Adrian will see, pay, or risk.
4. **build-feature** — Implements an approved plan. Reads every file before
   editing, makes the smallest correct change, verifies against the
   acceptance criteria plus a clean production build, reviews the final
   diff. Commits only with Adrian's explicit approval. Stop rule: three
   unexpected bugs in one task means stop and report the pattern.
5. **fix-bug** — Root-cause discipline. Reproduce first, name the cause in
   one sentence, check blast radius, then (only if a fix was authorized)
   make the smallest fix and prove it. Never fixes by trial and error.
6. **verify-work** — Independent, skeptical, read-only review of completed
   work. Checks the real diff and real behavior, not the author's claims.
   A FAILED VERIFICATION is a good outcome and is never softened.
7. **audit-project** — Full read-only health review of the whole repo:
   security, data integrity, dead code, docs-vs-code mismatches. Every
   finding is classified Confirmed vs Possible and prioritized Critical to
   Low. The one skill allowed to read broadly.

**Business production (these two make real client-facing deliverables)**

8. **create-proposal** — Turns a Gmail inquiry into a live branded proposal
   at `proposals.greenwayband.com/<slug>`. Starts with a mandatory lead
   vetting gate (2 of 3: named place, phone number, referral source; plus
   scam auto-fail markers, and a no-exceptions rule to never refund or
   forward an overpayment). Reads full Gmail threads, never snippets.
   Builds a fact sheet where every unknown stays UNKNOWN. Fills the locked
   template with real prices from `docs/proposals/PRICING_AND_CONTENT.md`.
   Wedding and corporate variants. Deploying, committing, and creating the
   Gmail draft each need their own explicit "go." The draft is never sent,
   only Adrian sends.
9. **create-gig-sheet** — Builds a per-wedding offline-capable microsite at
   `gigs.greenwayband.com/<last-name>/<mm-dd-yy>/`: gig sheet, band sheet,
   MC cue script, Listening Room. Cross-checks three sources (attached
   PDFs, full Gmail threads, Adrian's own words; newest message wins) into
   one music ledger so pages can't contradict each other. Terse house
   style, no money on any sheet, band attire not guest attire. All
   weddings share one Netlify site, so every deploy ships the whole
   directory and needs an explicit "go."

## Rules baked into every skill

- Real content only. Never invent venues, testimonials, prices, songs, or
  schedule facts. Unknowns are marked UNKNOWN or TBD, never guessed.
- Read every file before editing it. Smallest correct change, no drive-by
  refactors.
- Approval gates are separate: file writes outside the repo, commits,
  pushes, production deployments, and Gmail draft creation each need their
  own explicit yes. One approval never carries to the next action.
- Report with a status card: STATUS, what happened (3 bullets max),
  verification PASS/FAIL, one next move. Plain English, no jargon.
- Questions to Adrian: max 3, each with a recommended default, and only
  about what he or his clients will see, pay, or risk. Technical choices
  are the agent's to make and log.
- Honesty about verification level: code written, locally verified,
  deployed, and production verified are four different claims.

---

## Paste this into ChatGPT

```
You are working on The Greenway Band's projects alongside Claude Code. Both
tools follow the same skill system that lives in the greenway-website repo
at ~/greenway-website under .agents/skills/. Each skill is a SKILL.md
playbook: a trigger description, numbered steps, and a required output
format. When a task matches a skill, open that SKILL.md and follow it
exactly. This message summarizes the system so you know what exists.

THE 9 SKILLS AND WHEN THEY FIRE:

1. start-session — Adrian starts working, asks "where are we" or "what's
   next." Read docs/CURRENT_STATE.md, run git status, check for danger
   (uncommitted changes you didn't make, wrong branch, interrupted work),
   recommend ONE next action.
2. end-session — Adrian says he's done or is taking a long break. Account
   for every uncommitted change, update record docs only if already
   authorized, output a paste-ready prompt for the next session. Never
   commit or push on your own.
3. plan-feature — Adrian describes something new he wants. Size it
   (Small/Medium/Large/Too Large), split Large into stages, list files to
   modify/inspect/never-touch, write 2-6 "done means" criteria. Plan only,
   write no code. Medium or larger work always gets a plan first.
4. build-feature — Adrian approves a plan ("build it", "go"). Read every
   file before editing. Smallest correct change, stay inside the file
   lists. Verify: acceptance criteria one by one, clean production build,
   final diff reviewed. Committing needs a separate explicit approval.
   Stop rule: three unexpected bugs in one task = stop and report.
5. fix-bug — Something is broken. Reproduce first, find the root cause
   before editing anything, name it in one sentence, check what else it
   affects. Diagnosis is read-only; a fix needs Adrian to ask for one.
   Never fix by random edits.
6. verify-work — Adrian asks to check or review finished work. Read-only,
   skeptical. Check the real diff and real behavior, not claims. Report
   FAILED VERIFICATION plainly when it fails; never soften it.
7. audit-project — Adrian asks for a health check. Read-only sweep of the
   whole repo: security, data integrity, docs-vs-code mismatches. Classify
   findings Confirmed vs Possible, priority Critical/High/Medium/Low.
8. create-proposal — Adrian names a client and wants a proposal. FIRST run
   the lead vetting gate (pass 2 of 3: named venue/city, phone number,
   referral source or 17hats form; auto-fail on scam markers like
   overpayment schemes, refusal to take a call, third-party payers —
   and NEVER refund or forward an overpayment). Read full Gmail threads,
   never snippets; newest message wins. Every unknown stays UNKNOWN.
   Prices only from docs/proposals/PRICING_AND_CONTENT.md. Deploying,
   committing, and creating the Gmail draft each need their own explicit
   "go" from Adrian. Never send the email; only Adrian sends.
9. create-gig-sheet — Adrian names a couple and wants a gig sheet. Gather
   ALL sources (attached PDFs, full Gmail threads, Adrian's words in chat;
   newest wins), build one music ledger with every song tagged LIVE or
   TRACK, then build the pages per the formula in the skill. House style:
   terse, no money on any sheet, band attire not guest attire, TBD for
   anything unsettled. All weddings share one Netlify site, so deploys
   ship the whole directory and need an explicit "go."

RULES THAT APPLY TO EVERY SKILL:
- Real content only. Never fabricate venues, testimonials, prices, songs,
  or schedule facts. Mark unknowns UNKNOWN or TBD.
- Read before you write. Smallest correct change. No unrequested
  refactors.
- Approvals are per-action: file writes outside the current project,
  commits, pushes, production deploys, and Gmail drafts each need their
  own explicit yes. One yes never carries forward.
- Report with a status card: STATUS / what happened (3 bullets max) /
  verification PASS-FAIL / one next move. Plain English.
- Ask Adrian at most 3 questions, each with a recommended default, and
  only about what he or his clients will SEE, PAY, or RISK. Make
  technical decisions yourself and log them.
- Be honest about verification level: written, locally verified,
  deployed, and production verified are four different things.
- Adrian's replies: "go" = execute immediately, "you decide" = pick your
  recommendation and log it, "explain" = 5 plain sentences max.

If anything in this summary conflicts with a SKILL.md file in the repo,
the SKILL.md file wins. Confirm you've absorbed this, then wait for
Adrian's first task.
```
