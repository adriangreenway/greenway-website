---
name: fix-bug
description: Diagnose and fix a bug with root-cause discipline instead of trial and error. Use whenever Adrian reports something broken, weird, erroring, or not working, or pastes an error message or screenshot description. Also use when a build or deploy fails.
---

# Fix Bug

Goal: find the real cause, make the smallest fix, prove it's fixed, and make sure it stays fixed.

## Steps
1. Reproduce or verify the bug first. State exactly what you observed. If you can't reproduce it, ask Adrian for one specific thing (exact page, exact action, exact error text), not a list of questions.
2. Find the root cause before editing anything. Read the involved files, trace the data flow, check recent commits (`git log --oneline -10`) for what changed. Name the cause in one plain-English sentence.
3. Check the blast radius: does this cause affect other features? Say so.
4. Git safety point: commit or stash so the pre-fix state is recoverable.
5. Implement the smallest fix that addresses the cause, not the symptom.
6. Add regression protection when reasonable: a test, or a validation check. Skip it for trivial cosmetic fixes.
7. Verification gate: bug no longer reproduces, tests pass, build passes, diff reviewed.
8. Update `docs/CURRENT_STATE.md` (remove from Known issues if listed) and CHANGELOG if notable.

## Hard rules
- Never fix by trying random edits until the error changes. Every edit needs a stated reason.
- Three unexpected new problems while fixing one bug means stop: commit WIP, report the pattern, recommend audit-project.
- If the root cause is a design flaw rather than a code slip, say so and recommend plan-feature instead of patching over it.

## Output
**STATUS:** COMPLETE / BLOCKED / WARNING
**What happened:** the cause in one sentence, the fix in one sentence, blast radius in one sentence
**Verification:** PASS or FAIL per check
**Next move:** one line
