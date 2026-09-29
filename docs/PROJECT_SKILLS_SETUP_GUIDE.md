# Set Up a New Project with the Same Operating Structure

This is a self-contained blueprint for giving a new Git project the same durable instructions, repeatable skills, safety gates, and continuity records used by the Greenway website project.

The goal is not to copy Greenway-specific business rules. The goal is to reproduce the operating system around the code so a new Codex session can start cold, understand the project, work safely, verify changes, and leave a reliable handoff.

## The four layers

A well-structured project separates four kinds of information:

1. **Permanent rules:** `AGENTS.md` contains instructions that apply to every task.
2. **Repeatable procedures:** `.agents/skills/` contains one skill per recurring job.
3. **Project truth:** `START_HERE.md` and `docs/` explain what the product is, what is true now, what was decided, and what comes next.
4. **Enforcement:** tests, lint, type checks, build commands, hooks, and deployment checks prove rules mechanically where possible.

Do not collapse all four layers into one giant prompt or one giant `AGENTS.md`.

## Recommended repository layout

```text
new-project/
├── AGENTS.md
├── START_HERE.md
├── README.md
├── .agents/
│   └── skills/
│       ├── start-session/
│       │   └── SKILL.md
│       ├── plan-feature/
│       │   └── SKILL.md
│       ├── build-feature/
│       │   └── SKILL.md
│       ├── fix-bug/
│       │   └── SKILL.md
│       ├── verify-work/
│       │   └── SKILL.md
│       ├── audit-project/
│       │   └── SKILL.md
│       └── end-session/
│           └── SKILL.md
├── docs/
│   ├── CURRENT_STATE.md
│   ├── PROJECT_BRIEF.md
│   ├── ROADMAP.md
│   ├── DECISIONS.md
│   ├── CHANGELOG.md
│   ├── ARCHITECTURE.md          # when architecture needs more detail
│   ├── INTEGRATIONS.md          # when external systems exist
│   ├── DESIGN_SYSTEM.md         # for a visual product
│   └── CONTENT_AND_MESSAGING.md # for content-heavy products
├── src/                         # product code, adapt to the stack
└── package.json                 # or the stack's equivalent
```

Use the root `.agents/skills/` folder for workflows that apply everywhere in the repository. In a monorepo, a nested `<service>/.agents/skills/` folder may hold workflows specific to that service.

## What Codex discovers automatically

### `AGENTS.md`

Codex reads applicable `AGENTS.md` files before working. It starts with global guidance, then walks from the repository root toward the current working directory. A closer instruction file takes precedence over a more general one.

Use:

- `~/.codex/AGENTS.md` for personal rules that apply across projects;
- `<repo>/AGENTS.md` for shared repository rules;
- nested `AGENTS.md` or `AGENTS.override.md` files only when one subtree genuinely needs different rules.

Keep the combined guidance concise. Codex's documented default limit is 32 KiB for the combined project-instruction chain.

### Skills

Codex scans `.agents/skills/` from the current working directory up to the repository root. Each immediate skill folder must contain a readable `SKILL.md` with `name` and `description` front matter.

Codex can activate a skill in two ways:

- Explicitly, when the user names or invokes it.
- Implicitly, when the request matches its `description`.

Skill descriptions are therefore routing rules. Write the user phrases that should trigger the skill and state important exclusions.

Codex detects skill changes automatically. Restart Codex if a new or updated skill does not appear.

## Step 1: Establish a clean safety point

Before adding the structure:

1. Confirm the exact project folder and Git repository.
2. Run `git status` and record the branch and current commit.
3. Identify every existing modified or untracked file.
4. Do not overwrite, move, stage, or include unknown work.
5. Decide the exact new files to add before writing.

If the project already has agent instructions, read them first and merge deliberately. Do not create competing files that silently disagree.

## Step 2: Write `AGENTS.md`

`AGENTS.md` is the project's constitution. It should contain rules that must be applied on every task, not a long description of one workflow.

Start with this template and replace every bracketed value:

```md
# [Project Name]: Permanent Rules for Codex

## Role and audience

- Codex acts as [technical role].
- The project owner is [name and decision role].
- Explain work at [novice/intermediate/expert] level.
- Make safe technical choices without asking the owner to choose implementation details.

## Project boundary

- This repository contains [what belongs here].
- It does not contain [systems or responsibilities that belong elsewhere].
- The production system is [current production truth].

## Start of every session

1. Read `docs/CURRENT_STATE.md`.
2. Read `docs/PROJECT_BRIEF.md` when product, architecture, design, or content is involved.
3. Run `git status` and identify the current branch.
4. Preserve every pre-existing change.

## Before editing

- Read every file before changing it.
- State files to modify, files to inspect only, and files that are off limits.
- Make the smallest correct change.
- Do not perform unrelated cleanup, renaming, dependency upgrades, or refactors.

## Approval gates

Do not perform these without the owner's explicit approval for the exact action:

- commit, push, merge, rebase, or branch deletion;
- deploy, publish, DNS, or production configuration changes;
- deleting, overwriting, moving, or renaming user files;
- installing or removing dependencies, plugins, or services;
- changing credentials, permissions, security settings, or account data;
- sending messages, submitting forms, spending money, or accepting agreements.

## Project commands

- Install: `[real install command]`
- Develop: `[real local command]`
- Test: `[real test command, or state that none exists]`
- Lint: `[real lint command, or state that none exists]`
- Type check: `[real type-check command, or state that none exists]`
- Build: `[real production build command]`
- Preview: `[real preview command]`

Never claim to have run a command that the project does not provide.

## Verification gate

A change is not complete until:

1. Every acceptance criterion is checked.
2. Relevant tests, lint, type checks, and the production build pass when configured.
3. User-visible behavior is checked in the relevant app or browser.
4. The final diff contains only expected files.
5. No secrets, fabricated content, debug leftovers, or unrelated changes were introduced.

Distinguish written, locally verified, committed, pushed, deployed, and production verified.

## Record keeping

- Current truth: `docs/CURRENT_STATE.md`
- Stable facts: `docs/PROJECT_BRIEF.md`
- Planned work: `docs/ROADMAP.md`
- Durable decisions: `docs/DECISIONS.md`
- Completed history: `docs/CHANGELOG.md`
- Human control panel: `START_HERE.md`

Only update records when project-file changes are authorized.

## Skill routing

- Start of work: `start-session`
- New feature or meaningful change: `plan-feature`
- Approved implementation: `build-feature`
- Broken behavior or failed checks: `fix-bug`
- Independent review: `verify-work`
- Broad health review: `audit-project`
- End of work or long break: `end-session`

## Communication format

Use:

**STATUS:** PLAN READY / WORKING / BLOCKED / WARNING / COMPLETE / FAILED VERIFICATION
**What happened:** no more than three short bullets
**What I need from [owner]:** only when action is required
**Verification:** PASS or FAIL per relevant check
**Next move:** one recommendation
```

### Keep out of `AGENTS.md`

Do not put these in the root rules file:

- long per-task histories;
- detailed implementation plans;
- temporary blockers that change weekly;
- complete schemas or design specifications;
- a full procedure that belongs in a skill;
- secrets or credential values.

Route those to the appropriate document or skill.

## Step 3: Create the project truth documents

### `START_HERE.md`

This is the owner's short control panel. It should answer: what is this, is it healthy, what is active, and what should happen next?

```md
# START HERE: [Project Name]

## What this project is
[Two or three plain sentences.]

## Health
**STATUS:** GREEN / YELLOW / RED
**Last verified:** [date and exact checks]
**Blockers:** [none or short list]

## Active work
[One short current summary.]

## Next step
[One recommended action.]

## Where things live
| File | Purpose |
|---|---|
| `AGENTS.md` | Permanent agent rules |
| `.agents/skills/` | Repeatable workflows |
| `docs/CURRENT_STATE.md` | Current truth |
| `docs/PROJECT_BRIEF.md` | Stable facts |
| `docs/ROADMAP.md` | Planned work |
| `docs/DECISIONS.md` | Durable decisions |
| `docs/CHANGELOG.md` | Completed history |
```

### `docs/CURRENT_STATE.md`

Keep this short enough to read at every session start. It should contain only current truth.

```md
# CURRENT STATE: [Project Name]

**Last updated:** YYYY-MM-DD
**Last verified:** [PASS/FAIL, date, commands or checks]

## Working version
[Branch, environment, and important uncommitted or unpushed work.]

## Active task
[One task and its exact status.]

## Recently completed
- [Newest verified result]

## Known issues
| Issue | Severity | Evidence or impact |
|---|---|---|

## Blockers
- [None or exact blocker]

## Next recommended action
[One action.]
```

Move old completed items to `CHANGELOG.md` instead of letting this file become a diary.

### `docs/PROJECT_BRIEF.md`

This contains stable facts:

```md
# PROJECT BRIEF: [Project Name]

## Product
- What it is:
- Who uses it:
- Primary user outcome:
- Owner:

## Scope
- Included:
- Excluded:

## Technology
| Layer | Choice |
|---|---|

## Folder map
[Small tree plus important entry points.]

## Environments
- Local:
- Preview:
- Production:

## Business and safety constraints
- [Fact that must remain true]

## Real project commands
- Install:
- Develop:
- Test:
- Lint:
- Type check:
- Build:
- Preview:
```

Do not put changing weekly status here. That belongs in `CURRENT_STATE.md`.

### `docs/ROADMAP.md`

Use a small set of statuses such as `PLANNED`, `APPROVED`, `IN PROGRESS`, `SHIPPED`, `DEFERRED`, and `PAUSED`.

```md
# ROADMAP: [Project Name]

## Now
| Item | Size | Status | Depends on | Done means |
|---|---|---|---|---|

## Next
| Item | Size | Status | Depends on | Done means |
|---|---|---|---|---|

## Later
- [Idea not yet planned]

## Not planned
- [Rejected or explicitly out-of-scope idea, with reason]
```

Acceptance criteria belong in "Done means," not in vague labels such as "improve quality."

### `docs/DECISIONS.md`

Use this for choices future sessions must not silently reverse.

```md
# DECISIONS: [Project Name]

## D001: [Decision title]

- Date: YYYY-MM-DD
- Status: Active / Superseded by D###
- Decision: [What was chosen]
- Reason: [Why]
- Consequences: [What this changes]
- Revisit when: [Objective condition, or never]
```

Never delete a superseded decision. Mark it superseded and link the replacement.

### `docs/CHANGELOG.md`

Use this as the archive for verified finished work:

```md
# CHANGELOG: [Project Name]

## YYYY-MM-DD

- [What changed]
- Verification: [exact proof]
- Commit: [hash or "not committed"]
- Deployment: [environment or "not deployed"]
```

The changelog must not claim a deployment or production verification that did not occur.

## Step 4: Add the seven conventional skills

Each skill lives in an immediate subdirectory:

```text
.agents/skills/start-session/SKILL.md
```

Use this base shape:

```md
---
name: skill-name
description: State the user goal, trigger phrases, and important exclusions.
---

# Skill Name

Goal: one observable outcome.

## Steps
1. Use imperative, ordered instructions.
2. Name required inputs and project files.
3. State when to stop or ask a question.
4. Include proof, cleanup, and final diff review when the skill writes files.

## Hard rules
- State facts the skill must never infer.
- State actions needing separate approval.

## Output
[Exact status and report format.]
```

Create the following seven skills. Keep each focused on one job:

| Skill | Description must trigger on | Essential behavior |
|---|---|---|
| `start-session` | Starting work, "where are we?", "what's next?" | Read current state, inspect Git, identify danger, recommend one action |
| `plan-feature` | New feature, change idea, scope or difficulty question | Read-only plan, size work, identify risks and file boundaries, define done |
| `build-feature` | Approved plan, "build it", "go" | Read before write, preserve Git state, smallest change, verify, no automatic commit |
| `fix-bug` | Broken behavior, error, failed build or deploy | Reproduce, find root cause, diagnose without editing unless a fix was requested |
| `verify-work` | Review or verification request, completed large stage | Skeptical read-only review of diff, behavior, acceptance criteria, and regressions |
| `audit-project` | Audit, health check, inherited or unreliable project | Broad read-only review, evidence classification, severity, docs-versus-code check |
| `end-session` | Done, wrapping up, long break | Account for Git state, update authorized records, produce a cold-start bridge prompt |

### Recommended shared rules inside skills

Add these where they apply:

- The user's explicit request defines the authorized scope.
- Planning, diagnosis, review, and audit are read-only.
- Read every file before editing it.
- Preserve pre-existing changes.
- State modify, read-only, and off-limits file lists.
- Make the smallest correct change.
- Do not commit, push, deploy, delete, install, or change accounts without the exact required approval.
- Stop after three unexpected problems instead of fixing forward blindly.
- Check acceptance criteria and the project's real commands.
- Review the final diff.
- Report written, verified, committed, pushed, deployed, and production verified separately.

### Optional supporting resources

Add these only when they materially improve reliability:

```text
.agents/skills/example/
├── SKILL.md
├── references/  # policies, schemas, examples, deep background
├── assets/      # templates or source files to copy or transform
└── scripts/     # deterministic validation or file-processing helpers
```

The `SKILL.md` must explain exactly when to read each reference, reuse each asset, or run each script. Do not add a script when clear instructions and existing tools are reliable enough.

## Step 5: Add project-specific skills only after the core works

Create a specialized skill when all of these are true:

- the workflow repeats;
- it has recognizable user trigger phrases;
- it has stable inputs and output;
- missing a step creates real risk or repeated rework;
- it does not belong as a permanent rule in `AGENTS.md`.

Examples include creating a client proposal, processing an incident, publishing release notes, or building a recurring client deliverable.

For each specialized skill, document:

1. source-of-truth files;
2. required input collection;
3. conflict-resolution rules;
4. unknown-value handling;
5. separate approval gates;
6. verification and rollback;
7. exact final output.

Do not copy another project's pricing, credentials, client names, hostnames, or deployment procedure into the new project.

## Step 6: Connect documentation to the workflow

Use the following routing rules:

| Information | Correct home |
|---|---|
| Applies to every task | `AGENTS.md` |
| Repeatable method for one job | `.agents/skills/<name>/SKILL.md` |
| True right now | `docs/CURRENT_STATE.md` |
| Stable product or architecture fact | `docs/PROJECT_BRIEF.md` or a focused reference |
| Approved or future work | `docs/ROADMAP.md` |
| Choice that must not be silently reversed | `docs/DECISIONS.md` |
| Completed historical work | `docs/CHANGELOG.md` |
| Owner's short control panel | `START_HERE.md` |
| One-time task instruction | Current conversation or approved plan |

When two files disagree, code and verified behavior establish what exists. The mismatch must be reported and then corrected through an authorized documentation change.

## Step 7: Verify the setup

The setup is ready when every item below passes:

- [ ] `AGENTS.md` names the project boundary, real commands, approval gates, and verification rules.
- [ ] `START_HERE.md` gives one clear next action.
- [ ] `CURRENT_STATE.md` is short, current, and names the last real verification.
- [ ] `PROJECT_BRIEF.md` contains only stable facts.
- [ ] `ROADMAP.md` has checkable "Done means" criteria.
- [ ] `DECISIONS.md` preserves major choices.
- [ ] `CHANGELOG.md` distinguishes local work from deployed work.
- [ ] Every skill is one directory below `.agents/skills/`.
- [ ] Every `SKILL.md` has valid `name` and `description` front matter.
- [ ] Trigger descriptions are specific enough to avoid accidental overlap.
- [ ] Read-only skills do not authorize writes.
- [ ] Implementation skills preserve unknown Git changes.
- [ ] Commit, push, deploy, delete, credentials, spending, and external communication have explicit approval rules.
- [ ] The documented test, lint, type-check, build, and preview commands really exist.
- [ ] A trial session correctly invokes `start-session` and reports the branch, working tree, active task, and one next action.

## Operating loop after setup

Use this sequence for normal work:

```text
Open project
  -> start-session
  -> plan-feature for Medium or larger new work
  -> owner approves visible scope and risk
  -> build-feature
  -> project checks and browser/app inspection
  -> verify-work for substantial or high-risk changes
  -> separate approval for commit, push, or deployment when required
  -> end-session
```

For a bug, replace planning with `fix-bug`: reproduce, diagnose, request or confirm fix authorization, make the smallest fix, and verify.

## Common structural mistakes

### One giant `AGENTS.md`

Problem: current status, old history, detailed procedures, and permanent rules compete for context.

Correction: keep permanent rules in `AGENTS.md`; move current truth to `CURRENT_STATE.md`, history to `CHANGELOG.md`, and repeatable procedures to skills.

### Vague skill descriptions

Problem: Codex does not know when to select the skill, or several skills trigger at once.

Correction: name the user goal, common trigger phrases, and important exclusions in the description.

### Skills that mix unrelated jobs

Problem: a single skill becomes hard to trigger, test, and maintain.

Correction: split workflows when their inputs, approvals, or success criteria differ.

### Documentation treated as proof

Problem: records say a feature works even though code or production disagrees.

Correction: verify behavior first. Record exactly whether it is written, locally verified, committed, pushed, deployed, and production verified.

### Approval carried forward

Problem: permission to write code is treated as permission to publish, delete, spend, or change an account.

Correction: require approval for the exact protected action at the moment it is ready.

### Status files that become archives

Problem: session startup consumes stale history and hides the current task.

Correction: keep `CURRENT_STATE.md` small and move completed history to `CHANGELOG.md`.

## Maintenance rule

Treat this structure as a feedback system:

- A recurring mistake that applies everywhere becomes an `AGENTS.md` rule.
- A recurring multi-step job becomes a skill.
- A changing fact goes into `CURRENT_STATE.md`.
- A durable product choice goes into `DECISIONS.md`.
- A machine-checkable rule becomes a test, lint rule, hook, or validation script.

Review the setup after a real task exposes friction. Do not add complexity in anticipation of every possible edge case.

## Official Codex references

- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex customization overview](https://learn.chatgpt.com/docs/customization/overview)

These references describe the Codex discovery behavior and standard skill structure. The safety gates, state documents, and seven-skill lifecycle in this guide are the project operating pattern to copy.
