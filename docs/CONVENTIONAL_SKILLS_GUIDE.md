# The Conventional Skill System

This guide explains the seven general-purpose skills used to run work safely in this project. It is self-contained and can be read without opening the individual skill files.

The project also has two business-production skills, `create-proposal` and `create-gig-sheet`. Those are intentionally separate because they contain Greenway-specific pricing, source checking, deployment, privacy, and client-delivery rules. The seven skills in this guide are the reusable engineering core.

## What a skill is

A Codex skill is a repeatable work procedure stored in its own directory:

```text
.agents/skills/<skill-name>/SKILL.md
```

Every `SKILL.md` begins with YAML front matter:

```md
---
name: example-skill
description: Explain what the skill does and exactly when it should run.
---

# Example Skill

Goal: the outcome this procedure must produce.

## Steps
1. Do the first required action.
2. Verify the result.

## Output
Describe the required final report.
```

Codex first sees each skill's `name` and `description`. It reads the full instructions only when the user explicitly invokes the skill or the request matches the description. This keeps detailed procedures available without loading all of them into every task.

## What the system solves

The skill system turns recurring engineering judgment into visible, repeatable procedures. It ensures that a new session does not depend on remembered chat history and that work follows the same safety gates every time.

The system separates seven different jobs:

| Skill | Its one job | Typical trigger | Writes allowed? |
|---|---|---|---|
| `start-session` | Establish a safe starting point | Starting work, "where are we?", "what's next?" | No |
| `plan-feature` | Turn an idea into an approvable plan | New feature, change idea, difficulty question | No |
| `build-feature` | Implement an approved change | "Build it", "go", approved roadmap item | Yes, within the approved scope |
| `fix-bug` | Find the root cause, then make an authorized fix | Broken behavior, error, failed build or deploy | Diagnosis: no. Authorized fix: yes |
| `verify-work` | Independently check completed work | "Check this", "review it", after a large stage | No |
| `audit-project` | Review the whole project's health | Audit, health check, inherited or unreliable project | No |
| `end-session` | Leave a safe, understandable handoff | Done for the day, long break, last completed task | Only record updates already authorized |

## The normal flow

```text
start-session
      |
      v
new idea? ---- yes ----> plan-feature ---- approved ----> build-feature
      |
      no
      v
bug? --------- yes ----> fix-bug diagnosis ---- fix authorized ----> smallest fix
      |
      no
      v
review needed? --------> verify-work
      |
project-wide uncertainty?> audit-project
      |
      v
end-session
```

`verify-work` may follow any substantial implementation. `audit-project` is not a routine step. It is reserved for broad uncertainty because it is the one skill allowed to read widely across the repository.

## 1. `start-session`

### Purpose

Open a work session with the repository's real state, not with assumptions from an old conversation.

### Required actions

1. Read `docs/CURRENT_STATE.md`.
2. Run `git status` and identify the current branch.
3. Look for uncommitted work, the wrong branch, an interrupted task, or an unknown verification state.
4. Do not run an expensive build unless a danger sign makes it necessary.
5. Recommend exactly one next action.

### Expected result

A short GREEN, YELLOW, or RED status card. GREEN means it is safe to proceed. YELLOW means something needs attention. RED means work should stop until the problem is resolved.

### Why it matters

This project has had diverged branches and deliberately preserved uncommitted work. A fast safety check prevents a new task from overwriting or mixing with earlier work.

## 2. `plan-feature`

### Purpose

Convert a plain-language idea into a small, testable implementation plan before code changes begin.

### Required actions

1. Restate the requested outcome in one sentence.
2. Inspect the relevant code and decisions.
3. Size the work:
   - Small: one focused change in a few files.
   - Medium: one contained feature across several connected files.
   - Large: multiple systems, authentication, database work, or a broad refactor.
   - Too Large: unrelated features or work that cannot be verified as one task.
4. Split Large work into two to four independently verifiable stages.
5. State risks involving security, data, cost, deployment, or loss.
6. List files to modify, files to inspect only, and files that must remain untouched.
7. Define two to six observable acceptance criteria under "Done means."

### Boundaries

Planning is read-only. It does not create code or silently add a roadmap entry. Questions are limited to choices that change what the owner or users will see, pay, or risk. Technical choices are made by the agent.

### Expected result

A `PLAN READY` status card that can be approved with a simple "build it" or "go."

## 3. `build-feature`

### Purpose

Implement an approved plan with the smallest correct change and prove that the result works.

### Required actions

1. Read the approved plan from the conversation or roadmap.
2. Read every file that will be modified.
3. Confirm the three file lists: modify, read only, and off limits.
4. Record `git status` and the current commit before editing.
5. Preserve every pre-existing change.
6. Implement only the approved scope.
7. Check every acceptance criterion.
8. Run the project's real verification commands.
9. Review the final diff for unrelated files, secrets, fabricated content, and debug leftovers.

### Boundaries

Approval to build authorizes only the named file changes. It does not automatically authorize a commit, push, deployment, account change, deletion, or other separately protected action.

If three unexpected problems appear, stop and return to planning or an audit. Do not keep patching forward.

### Expected result

A `COMPLETE`, `WORKING`, `BLOCKED`, or `WARNING` status card that clearly distinguishes:

- written;
- locally verified;
- committed;
- pushed;
- deployed;
- production verified.

These states are not interchangeable.

## 4. `fix-bug`

### Purpose

Find and explain the real cause of a problem before changing code.

### Required actions

1. Reproduce or verify the failure.
2. Trace the involved files and recent changes.
3. State the root cause in one plain sentence.
4. Check the blast radius, meaning what else the same cause could affect.
5. Stop after diagnosis when the user asked only for an explanation.
6. If a fix was authorized, record Git state and make the smallest cause-level fix.
7. Add a regression check when reasonable.
8. Prove the original problem no longer occurs, then run the normal project checks.

### Boundaries

Diagnosis is read-only. Reporting a bug does not automatically authorize a fix. Random edits are forbidden. If the root cause is an architecture problem, the right next step is `plan-feature`, not a cosmetic patch.

### Expected result

A status card naming the cause, the authorized fix if any, its blast radius, and the proof result.

## 5. `verify-work`

### Purpose

Review a finished change skeptically and independently before it counts as done.

### Required actions

1. Read the original acceptance criteria.
2. Inspect the actual diff rather than trusting a summary.
3. Look for out-of-scope changes, weakened safety checks, secrets, debug code, and unfinished notes.
4. Run read-only proof such as tests, lint, type checks, builds in a temporary copy, and relevant browser checks.
5. Check each acceptance criterion against real behavior.
6. Check nearby features for regressions.

### Boundaries

Verification is read-only. It may recommend a fix or record update, but it does not make one without separate authorization.

### Expected result

Either `COMPLETE` or `FAILED VERIFICATION`. Failure is useful evidence, not a softened warning.

## 6. `audit-project`

### Purpose

Produce a broad, evidence-based health review when the whole project may be unreliable or poorly understood.

### Required actions

1. Map the repository, entry points, data flow, authentication, deployment, and major dependencies.
2. Review security, data integrity, error handling, user experience, performance, dead code, and missing verification.
3. Compare documentation with the actual code.
4. Classify every finding as:
   - Confirmed: visible in code or verified behavior.
   - Possible: needs more evidence.
5. Assign Critical, High, Medium, or Low priority.

### Boundaries

An audit is read-only. It does not create an audit file or modify project records unless those file changes are separately approved. It is the only conventional skill permitted to read broadly across the repository.

### Expected result

A prioritized health summary with the top three findings and one recommended next action.

## 7. `end-session`

### Purpose

Close work without losing context or leaving the next session exposed to hidden changes.

### Required actions

1. Run `git status` and account for every uncommitted file.
2. Distinguish completed, unfinished, and pre-existing work.
3. Never commit, stash, or push automatically.
4. Update state, roadmap, changelog, and start-here records only when project-file changes were already authorized.
5. Produce a self-contained bridge prompt for the next session.

### Required bridge prompt content

The prompt must name:

- the exact project folder;
- what was completed;
- the current status;
- protected or unfinished work;
- the single next action;
- the instruction to run `start-session`.

### Expected result

A `COMPLETE` status card plus a ready-to-copy prompt that allows a cold session to resume safely.

## Rules shared by all seven skills

### Read before write

Read every file before editing it. Do not make drive-by refactors, renames, dependency upgrades, or cleanup changes.

### Preserve unknown work

Run `git status` before changes. Existing modifications belong to someone else unless proven otherwise. Never discard, stage, move, or include them accidentally.

### One task at a time

Keep each change focused and independently verifiable. Split unrelated requests instead of combining them into one large change.

### Approval is action-specific

A general "go" applies only to the action just recommended. Commit, push, deploy, delete, credential, account, external message, and production changes remain separate approval gates when project rules require them.

### Verification is part of the work

Writing files is not completion. A change must satisfy its acceptance criteria, pass the project's actual checks, survive a final diff review, and be inspected in the relevant app or browser when behavior or layout changed.

### Status reports are compact

The standard report contains:

```md
**STATUS:** PLAN READY / WORKING / BLOCKED / WARNING / COMPLETE / FAILED VERIFICATION
**What happened:** no more than three short bullets
**What I need from Adrian:** only when an action is required
**Verification:** PASS or FAIL for each relevant check
**Next move:** one recommendation
```

### Unknown facts stay unknown

Do not fabricate business facts, content, data, credentials, test results, or verification claims. Use `UNKNOWN`, `TBD`, or an explicit placeholder when the source does not establish the answer.

## How the conventional skills relate to project files

| File or folder | Responsibility |
|---|---|
| `AGENTS.md` | Permanent rules that apply to every task in this repository |
| `.agents/skills/` | Task-specific repeatable procedures |
| `START_HERE.md` | Human-readable project control panel |
| `docs/CURRENT_STATE.md` | Short current truth, active work, blockers, last verification |
| `docs/PROJECT_BRIEF.md` | Stable product, architecture, audience, and constraints |
| `docs/ROADMAP.md` | Planned and approved work with acceptance criteria |
| `docs/DECISIONS.md` | Important choices that must not be silently reversed |
| `docs/CHANGELOG.md` | Finished historical record |

`AGENTS.md` says what must always be true. A skill says how to perform one recurring job. The state documents say what is true now. Keeping these responsibilities separate reduces conflicting instructions.

## When to create another skill

Create a new skill only when a recognizable workflow repeats and has a distinct trigger, input, procedure, and result. Good signals include:

- the same long prompt is reused;
- the same correction appears in multiple sessions;
- a business deliverable follows a stable recipe;
- missing a step could create material client, security, data, or deployment risk.

Do not add a skill for a one-time request or a rule that should apply to every task. One-time requirements belong in the prompt. Permanent project rules belong in `AGENTS.md`.

## Canonical sources

The live project files under `.agents/skills/` remain authoritative if this overview ever drifts. For Codex's platform behavior and file locations, see the official OpenAI documentation for [building skills](https://learn.chatgpt.com/docs/build-skills) and [custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
