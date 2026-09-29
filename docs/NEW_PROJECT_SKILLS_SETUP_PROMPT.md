# Prompt: Give a New Project the Greenway Skill Structure

Copy the prompt below into a Codex task opened inside the new project's folder.

```text
Set up this project with the same agent-instruction, conventional-skill, safety, verification, and continuity structure used by the Greenway website project.

The two reference guides are on this computer at:

1. /Users/adrianjoseph/greenway-website/docs/CONVENTIONAL_SKILLS_GUIDE.md
2. /Users/adrianjoseph/greenway-website/docs/PROJECT_SKILLS_SETUP_GUIDE.md

Treat both files as read-only reference material. Do not edit either guide and do not make any other change inside /Users/adrianjoseph/greenway-website.

Before changing this project:

1. Read this project's applicable AGENTS.md files and existing documentation.
2. Run git status, identify the current branch and commit, and preserve every pre-existing change.
3. Read both reference guides completely.
4. Inspect this project's real stack, commands, folder layout, deployment process, risks, and existing conventions.
5. Adapt the structure to this project. Do not copy Greenway-specific names, prices, clients, hostnames, business rules, deployment steps, or technical assumptions.

The intended structure is:

- AGENTS.md for permanent repository rules.
- START_HERE.md for the owner's short control panel.
- docs/CURRENT_STATE.md for current truth.
- docs/PROJECT_BRIEF.md for stable facts.
- docs/ROADMAP.md for planned and approved work.
- docs/DECISIONS.md for durable decisions.
- docs/CHANGELOG.md for verified completed history.
- .agents/skills/<skill-name>/SKILL.md for the seven conventional skills:
  start-session, plan-feature, build-feature, fix-bug, verify-work, audit-project, and end-session.

First produce a PLAN READY status card. The plan must include:

- task size and risks;
- files to create or modify;
- files to inspect only;
- files that are off limits;
- any conflicts with the project's existing instructions;
- two to six checkable "Done means" criteria;
- the real verification commands for this project.

Do not create or modify files until I approve that plan with "go." When approved, make the smallest correct setup, read every existing file before editing it, and keep every statement specific to this project and supported by evidence.

Do not commit, push, deploy, delete, rename, install dependencies, change credentials, change permissions, or modify external systems without separate explicit approval for that exact action.

If the two reference paths are inaccessible from this project's workspace, stop and tell me exactly which files could not be read. Do not guess their contents and do not ask me to run terminal commands.
```
