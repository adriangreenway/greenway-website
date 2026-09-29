---
name: end-session
description: Close a work session safely so the next session can start cold with zero lost context. Use whenever Adrian says he's done, wrapping up, ending the session, or has been given a COMPLETE on the day's last task. Also use before any long break mid-task.
---

# End Session

Goal: repo state understood, records true when updates were authorized, and the
next session's opening prompt ready.

## Steps
1. Run `git status`. Identify every uncommitted change and whether it is
   finished, unfinished, or pre-existing. Never commit or stash automatically.
   If a commit is recommended, explain the exact files and ask for explicit
   approval.
2. Push only when Adrian explicitly approved pushing the exact repo and branch.
   Commit approval never implies push approval.
3. If this session included authorized project-file changes, update
   `docs/CURRENT_STATE.md`: active task, recently completed, known issues, next
   recommended action, last verified build, last updated date. Enforce the
   60-line cap, archive overflow to CHANGELOG. For a read-only session, inspect
   records but leave them unchanged.
4. Update `docs/ROADMAP.md` statuses only when project-file changes were already
   authorized.
5. Update `START_HERE.md` only when project-file changes were already
   authorized.
6. Write a self-contained handoff prompt for the next session and put it in the
   final message. Name the exact project folder, what was completed, current
   status, protected or unfinished work, the single next action, and the
   matching start-session instruction. Format:

```
Open [exact project folder] and run the start-session skill. Completed:
[completed work]. Current status: [status]. Preserve: [protected or unfinished
work]. Next action: [one action].
```

## Output
**STATUS:** COMPLETE
**What happened:** repo state and any authorized record updates, in 2 bullets
**Next session prompt:** the exact line to paste next time
**Next move:** "You're safe to close this window."

Never end a session leaving the repo in a state that would confuse or endanger the next session.
