---
name: build-feature
description: Implement an approved feature safely. Use whenever Adrian approves a plan ("build it", "go", "yes do it") or asks to build something that already has an APPROVED entry in docs/ROADMAP.md. If no approved plan exists and the task is Medium or larger, run plan-feature first.
---

# Build Feature

Goal: the smallest correct implementation, verified, committed, and reported in plain English.

## Steps
1. Read the approved plan in `docs/ROADMAP.md`. If the task is Small and obvious, a one-line plan stated to Adrian is enough.
2. Read every file you will modify. Confirm the three lists from the plan (modify, inspect, off limits). If reality differs from the plan, say so before proceeding.
3. Git safety point: confirm clean `git status`, then commit or stash appropriately so current work can be recovered. Note the current commit hash.
4. Implement the smallest correct solution. Stay inside the file lists. No unrelated refactors, renames, or dependency upgrades.
5. If building in stages, complete and verify one stage fully before starting the next. Commit per stage.
6. Verification gate (all of these before COMPLETE):
   - Acceptance criteria checked one by one
   - Relevant tests pass
   - Lint and type checks pass if the project has them
   - Production build passes
   - Final diff reviewed: only expected files changed, no secrets, no debug leftovers
7. Update records: `docs/CURRENT_STATE.md`, mark the ROADMAP entry SHIPPED (or note the stage), archive to CHANGELOG if CURRENT_STATE is over 5 completed items.

## Stop rule
Three unexpected bugs or conflicts in this one task: stop, commit work in progress with a WIP message, report the pattern, recommend returning to plan-feature or audit-project.

## Output
**STATUS:** COMPLETE / WORKING / BLOCKED / WARNING
**What happened:** max 3 bullets, plain English
**Verification:** PASS or FAIL per gate item
**What I need from Adrian:** only if needed (like "open [URL] on your phone and confirm the new button shows")
**Next move:** one line

Be honest about verification level: locally verified is not the same as deployed, deployed is not the same as production verified.
