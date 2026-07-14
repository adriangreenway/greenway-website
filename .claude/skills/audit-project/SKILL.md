---
name: audit-project
description: Full health review of the project. Use when Adrian asks for an audit, a review, a health check, "is my app okay", when adopting an old or AI-built project, after repeated bug clusters, or before a major launch. This is the one skill allowed to read broadly across the repo.
---

# Audit Project

Goal: an honest, prioritized picture of what's solid and what's not. Best run on the strongest available model (Fable 5). For very large repos, `/effort ultracode` is worth it here and only here.

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

## Output
Write the full findings to `docs/AUDIT_[date].md` so chat stays short. In chat, give:

**STATUS:** COMPLETE
**What happened:** counts per priority, and the top 3 findings in plain English
**What I need from Adrian:** approval to fix Criticals, one line each on what fixing involves
**Next move:** one recommendation, usually "fix the Criticals first, reply 'go'"

Never pad the audit. If the project is healthy, say so plainly. Update CURRENT_STATE Known issues with Critical and High findings.
