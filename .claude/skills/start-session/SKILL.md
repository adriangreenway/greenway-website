---
name: start-session
description: Open every work session with this skill. Use it whenever Adrian starts a session, says "start session", "where are we", "what's next", pastes a session-opening prompt, or begins working after any break. It checks project health, Git safety, and unfinished work, then recommends one next action.
---

# Start Session

Goal: in under a minute of Adrian's attention, confirm the project is safe to work on and tell him the one next move.

## Steps
1. Read `docs/CURRENT_STATE.md`.
2. Run `git status` and `git branch --show-current`.
3. Check for danger signs:
   - Uncommitted changes you did not create this session
   - Being on the production branch when a working branch exists
   - CURRENT_STATE says a task is mid-build
   - Last verified build is FAIL or unknown
4. If the project has a quick health check (like `npm run build` finishing recently, or tests), do NOT run it now unless something looks wrong. Session start should be fast and cheap.
5. Decide the next action. Priority order: finish an interrupted task, fix a blocker, then the top item in ROADMAP "Now".

## Output
One status card only:

**STATUS:** GREEN, YELLOW, or RED (as a WARNING/BLOCKED card if not green)
**What happened:** repo state, branch, active task, in 3 bullets max
**What I need from Adrian:** only if something is unsafe. Exact recovery steps.
**Next move:** one recommendation, phrased so Adrian can reply "go" to start it.

Do not summarize the whole project. Do not list the roadmap. One next move.
