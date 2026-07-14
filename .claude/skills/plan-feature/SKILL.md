---
name: plan-feature
description: Turn a plain-English idea into a safe implementation plan before any code is written. Use whenever Adrian describes something new he wants ("add a client portal", "I want the app to..."), asks how hard something would be, or asks to plan a feature. Never skip this for Medium or larger work. This skill plans only, it never implements.
---

# Plan Feature

Goal: a plan Adrian can approve with one word, with risks and cost already thought through. Write NO implementation code in this skill.

## Steps
1. Restate the feature in one sentence. If your restatement might be wrong, ask.
2. Inspect the relevant existing code. Read the files this feature would touch. Check `docs/DECISIONS.md` for conflicts.
3. Size the task:
   - **Small:** one focused change, few files, no database or architecture change
   - **Medium:** one contained feature, several connected files, moderate testing
   - **Large:** multiple systems, database or auth changes, or broad refactor
   - **Too Large:** several unrelated features, unclear architecture, or can't be verified as one task
   Large gets split into 2 to 4 stages, each independently verifiable. Too Large gets split into separate features planned one at a time.
4. Identify risks: database, auth, security, deployment, data loss. Say "no special risks" when true.
5. List: files to modify, files to inspect, files that must not be touched.
6. Define acceptance criteria: 2 to 6 checkable statements. "Done means..."
7. Recommend the model for the build:
   - **Sonnet:** executing this plan if it's Small or Medium with no tricky logic
   - **Fable 5 (or the strongest available model):** Large stages, database or auth work, security-sensitive code, or anything ambiguous
8. Ask questions ONLY if the answer changes cost, architecture, security, or the user experience. Max 3, each with a recommended default.

## Output
**STATUS:** PLAN READY
**The plan:** feature in one line, size, stages if split
**Risks:** plain English, or "none special"
**Done means:** the acceptance criteria
**Model:** Sonnet or Fable 5, one line why
**Next move:** "Reply 'build it' and I'll run build-feature," or the questions if any

Store the approved plan as the feature's entry in `docs/ROADMAP.md` with status APPROVED, so the build session can read it without Adrian re-pasting anything.
