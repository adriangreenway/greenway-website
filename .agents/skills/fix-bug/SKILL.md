---
name: fix-bug
description: Diagnose a bug with root-cause discipline, and fix it only when Adrian asks for a fix. Use whenever Adrian reports something broken, weird, erroring, or not working, or pastes an error message or screenshot description. Also use when a build or deploy fails.
---

# Fix Bug

Goal: find the real cause. If Adrian authorized a fix, make the smallest one,
prove it is fixed, and make sure it stays fixed.

## Steps
1. Reproduce or verify the bug first. State exactly what you observed. If you can't reproduce it, ask Adrian for one specific thing (exact page, exact action, exact error text), not a list of questions.
2. Find the root cause before editing anything. Read the involved files, trace the data flow, check recent commits (`git log --oneline -10`) for what changed. Name the cause in one plain-English sentence.
3. Check the blast radius: does this cause affect other features? Say so.
4. If Adrian asked only for diagnosis, stop here and report the cause. Diagnosis
   is read-only and does not authorize a fix.
5. Before an authorized fix, run `git status`, note the current commit hash, and
   preserve every pre-existing change. Never commit or stash as a safety point
   without Adrian's separate explicit approval.
6. Implement the smallest fix that addresses the cause, not the symptom.
7. Add regression protection when reasonable: a test, or a validation check. Skip it for trivial cosmetic fixes.
8. Verification gate: bug no longer reproduces, tests pass, build passes, diff reviewed.
9. After an authorized fix, update `docs/CURRENT_STATE.md` (remove from Known issues if listed) and CHANGELOG if notable.

## Hard rules
- Never fix by trying random edits until the error changes. Every edit needs a stated reason.
- Three unexpected new problems while fixing one bug means stop, preserve the
  working tree, report the pattern, and recommend audit-project. Do not commit
  or stash WIP without separate explicit approval.
- If the root cause is a design flaw rather than a code slip, say so and recommend plan-feature instead of patching over it.

## Output
**STATUS:** COMPLETE / BLOCKED / WARNING
**What happened:** the cause in one sentence, the fix in one sentence, blast radius in one sentence
**Verification:** PASS or FAIL per check
**Next move:** one line
