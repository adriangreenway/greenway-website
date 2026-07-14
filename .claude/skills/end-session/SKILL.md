---
name: end-session
description: Close a work session safely so the next session can start cold with zero lost context. Use whenever Adrian says he's done, wrapping up, ending the session, or has been given a COMPLETE on the day's last task. Also use before any long break mid-task.
---

# End Session

Goal: repo safe, records true, and the next session's opening prompt ready.

## Steps
1. `git status`. Nothing important may be left uncommitted. Commit finished work with clear messages. Commit unfinished work as WIP with a message saying exactly what's mid-flight.
2. Push only if Adrian already authorized pushing, otherwise ask in one line.
3. Update `docs/CURRENT_STATE.md`: active task, recently completed, known issues, next recommended action, last verified build, last updated date. Enforce the 60-line cap, archive overflow to CHANGELOG.
4. Update `docs/ROADMAP.md` statuses.
5. Update `START_HERE.md`: Health status and the "Your next step" paste-able prompt.
6. Write the handoff prompt for the next session and put it in your final message. Format:

```
Run the start-session skill. Context: [one line on where things stand]. Then [the next action].
```

## Output
**STATUS:** COMPLETE
**What happened:** committed X, records updated, in 2 bullets
**Next session prompt:** the exact line to paste next time
**Next move:** "You're safe to close this window."

Never end a session leaving the repo in a state that would confuse or endanger the next session.
