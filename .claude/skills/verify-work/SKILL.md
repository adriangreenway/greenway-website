---
name: verify-work
description: Independently review a completed implementation before it counts as done. Use when Adrian asks to check, review, or verify work, when a stronger model reviews a weaker model's build (Fable reviewing Sonnet), or after any Large stage. Approach the code as a skeptical reviewer, not the author.
---

# Verify Work

Goal: catch problems before Adrian or his users do. Assume nothing the implementation claimed. Check it.

## Steps
1. Read the acceptance criteria (ROADMAP entry or the stated plan).
2. Inspect the actual diff: `git diff [safety-point-commit]..HEAD` or the latest commits. Look for:
   - Changes outside the declared file list
   - Removed safety checks, weakened auth, exposed secrets
   - Debug leftovers, commented-out code, TODO landmines
3. Run the proof: tests, lint, type check, production build. Do not trust prior PASS claims, re-run.
4. Check each acceptance criterion against real behavior, not against the code's intent.
5. Where relevant: check mobile layout, keyboard and screen-reader basics, empty and error states, and that database changes match what migrations actually applied.
6. Check for regressions in the features nearest to the change.

## Output
**STATUS:** COMPLETE (pass) or FAILED VERIFICATION
**Verification:** PASS or FAIL per criterion and per proof step
**What happened:** on fail, each problem in one plain sentence with severity
**Next move:** on pass, "safe to consider done." On fail, the single best fix path.

A FAILED VERIFICATION is a good outcome, it means the system worked. Never soften a fail to be polite. Record the result in `docs/CURRENT_STATE.md`.
