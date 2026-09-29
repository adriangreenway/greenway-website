---
name: audit-project
description: Read-only full health review of the project. Use when Adrian asks for an audit, a review, a health check, "is my app okay", when adopting an old or AI-built project, after repeated bug clusters, or before a major launch. This is the one skill allowed to read broadly across the repo.
---

# Audit Project

Goal: an honest, prioritized picture of what's solid and what's not. Use Sol.
An audit is read-only unless Adrian separately authorizes a named file change.

## Steps
1. Map the repo: structure, entry points, routes or pages, database schema, auth flow, deployment config.
2. Review for:
   - Broken or dead logic, features that look done but aren't reliable
   - Security: exposed keys, missing auth checks, unvalidated input, permissive database policies
   - Data integrity: missing constraints, risky writes, no backups story
   - Error handling: silent failures, missing user feedback
   - UX: confusing flows, broken mobile behavior
   - Performance: obvious heavy queries or renders
   - Dead code and unused dependencies
3. Verify docs against code: does PROJECT_BRIEF match the real stack? Does CURRENT_STATE match reality? Flag every mismatch.
4. Classify every finding:
   - **Confirmed** (you saw it in the code) vs **Possible** (needs testing to confirm)
   - Priority: **Critical** (data loss, security, revenue), **High** (broken feature), **Medium** (degraded quality), **Low** (cleanup)

Do not run a check that writes project files, triggers a deployment, changes
cloud data, or modifies credentials during an audit. Prefer read-only checks or
a temporary copy. If stronger proof requires a write, explain it and ask first.

## Output
Report findings in chat by default. Do not create `docs/AUDIT_[date].md` or
update project records unless Adrian explicitly approves those exact file
changes after reviewing the findings. Give:

**STATUS:** COMPLETE
**What happened:** counts per priority, and the top 3 findings in plain English
**What I need from Adrian:** approval to fix Criticals, one line each on what fixing involves
**Next move:** one recommendation, usually "fix the Criticals first, reply 'go'"

Never pad the audit. If the project is healthy, say so plainly. Recommend any
CURRENT_STATE updates, but do not make them during a read-only audit.
