# CLAUDE BUILD WORKFLOW

## The Greenway Band — How Every Build Gets Done

**Version:** 1.0
**Created:** March 8, 2026
**Purpose:** This document governs the full lifecycle of every Claude-assisted build project. It lives in project knowledge permanently. Every build chat references it. If you follow the stages in order, nothing gets missed.

**Relationship to other documents:**
- **Zero Compromise Code Protocol** governs what happens *inside* Claude Code sessions (prompt structure, build gates, regression checks, commit protocol)
- **This document** governs the full cycle *around* those sessions (planning, handoff, post-build, checkpoint)
- **Build Manifest** is the product spec Bible
- **Master Status** is the decision record

---

## THE FIVE STAGES

Every build — whether it's a new feature week, a bug fix session, or an infrastructure task — follows five stages in order. No skipping.

```
PLAN → PREP → BUILD → DEBRIEF → CLOSE
 Chat    You    Code    Chat     Chat
```

### Stage 1: PLAN (Claude Chat)

This is where spec writing, manifest cross-referencing, and verification happen. You and Claude Chat work through the scope, nail down every detail, and produce the build materials.

**What Claude Chat delivers at the end of this stage:**

1. **Spec file** (if needed) — the technical specification
2. **Verification Receipt** (if needed) — proof that spec matches manifest
3. **Claude Code Prompts file** — the actual prompts you'll paste
4. **DO THIS NOW card** — your single action sheet (see format below)

**The only file you need to read is the DO THIS NOW card.** The spec, receipt, and prompts file exist for Claude's verification process. You never need to open them yourself. You trust the process, you follow the card.

---

### Stage 2: PREP (You, Solo)

You follow the DO THIS NOW card. It tells you exactly what to do before opening Claude Code. This stage takes 2 to 5 minutes.

Typical prep actions:
- Delete old files from project knowledge
- Upload new files to project knowledge
- Run a Supabase migration (copy/paste SQL into the SQL editor)
- Set an environment variable in Netlify
- Open Claude Code

**You do not improvise during prep.** If the card says upload 3 files, you upload 3 files. If it says run SQL, you run the SQL. If something isn't on the card, you don't do it.

---

### Stage 3: BUILD (Claude Code)

You paste prompts from the Claude Code Prompts file, one phase at a time. Wait for the Glass sound after each phase. Two phases per session maximum (per Zero Compromise Protocol).

**Rules during Build:**
- Paste Phase 1 prompt. Attach any files the card specifies. Wait for Glass.
- Paste Phase 2 prompt. Wait for Glass.
- If more than 2 phases: commit, close Claude Code, open a fresh session, paste the bridge prompt from the card, then continue.
- If context compaction occurs: stop immediately, follow the recovery protocol in Zero Compromise Code Protocol Section 1.5.
- If 3+ bugs appear in one phase: stop, commit WIP, close Claude Code. Come back to Chat.

**When Build is done:** Claude Code will list each acceptance criterion as PASS or FAIL. Copy the full completion summary. Come back to Claude Chat.

---

### Stage 4: DEBRIEF (Claude Chat)

You return to the Chat that produced the DO THIS NOW card (or start a new one with the bridge prompt if the original chat hit its exchange limit).

**What you say:** "Build complete. Here's the output:" then paste Claude Code's completion summary.

**What Claude Chat does:**
- Reviews the PASS/FAIL results
- Identifies anything that needs a fix pass
- If all PASS: moves to Close
- If any FAIL: diagnoses the issue and either (a) delivers a fix prompt for one more Claude Code session, or (b) revises the spec

---

### Stage 5: CLOSE (Claude Chat)

**What Claude Chat delivers:**
1. Updated Master Status (version bumped, decisions recorded)
2. Updated Build Manifest (if features were added)
3. Bridge prompt for the next chat (pre-filled, copy verbatim)
4. **CLEANUP card** — tells you which PK files to delete/upload for the next session

**You follow the CLEANUP card, then you're done.**

---

## THE DO THIS NOW CARD

This is the single most important deliverable in the system. Every time Claude Chat hands off to you for action, it delivers one of these. The format is locked.

```
═══════════════════════════════════════════
  DO THIS NOW
  [Build Name] — [Stage Description]
═══════════════════════════════════════════

  PK FILES — DELETE THESE:
  ☐ [filename] (reason it's being removed)
  ☐ [filename]

  PK FILES — UPLOAD THESE:
  ☐ [filename] (just delivered above)
  ☐ [filename]

  PK FILES — NO CHANGES:
  • [filename] (stays as is)
  • [filename]

  ─────────────────────────────────────────

  PRE-FLIGHT (do these before opening Claude Code):

  1. [Exact action with exact location]
     Example: "Open Supabase SQL Editor → paste this:"
     ```sql
     ALTER TABLE leads ADD COLUMN IF NOT EXISTS lead_score integer DEFAULT 0;
     ```

  2. [Next action]

  ─────────────────────────────────────────

  CLAUDE CODE SESSION:

  1. Open Claude Code
  2. Attach these files: [list]
  3. Paste the OPENING PROMPT from [prompts filename], Section "[section name]"
  4. Wait for Glass sound ding
  5. Paste the PHASE 2 PROMPT from [prompts filename], Section "[section name]"
  6. Wait for Glass sound ding
  7. Copy the completion summary (the PASS/FAIL list)
  8. Close Claude Code

  ─────────────────────────────────────────

  WHEN YOU'RE DONE:

  Come back to this chat and say:
  "Build complete. Here's the output:"
  Then paste the completion summary.

═══════════════════════════════════════════
```

### Card Rules

- Every action is numbered
- Every file reference uses the exact filename
- Every paste target says exactly where to find the text ("from [file], Section [name]")
- SQL, env vars, and other copy/paste content is included inline on the card (not "see the prompts file")
- The card never says "see [other document] for details." Everything you need is on the card
- If a build has more than 2 phases (requiring multiple Claude Code sessions), the card includes a SESSION BREAK section with commit instructions and a bridge prompt

---

## THE CLEANUP CARD

Delivered at Close (Stage 5). Same format, simpler content.

```
═══════════════════════════════════════════
  CLEANUP — [Build Name] Complete
═══════════════════════════════════════════

  PK FILES — DELETE THESE:
  ☐ [old spec file]
  ☐ [old verification receipt]
  ☐ [old prompts file]

  PK FILES — UPLOAD THESE:
  ☐ MASTER_STATUS.md (v[X] — just delivered)
  ☐ BUILD_MANIFEST.md (v[X] — just delivered)
  ☐ [any new permanent file]

  PK FILES — NO CHANGES:
  • Zero_Compromise_Code_Protocol.md
  • Claude_Build_Workflow.md
  • [other permanent files]

  ─────────────────────────────────────────

  NEXT CHAT:

  Name: "[suggested chat name]"
  Bridge prompt: [already at the bottom of MASTER_STATUS.md]

═══════════════════════════════════════════
```

---

## WHEN THINGS DON'T FIT NEATLY

### Infrastructure tasks (no spec or receipt needed)

Some builds are simple utilities (staging environment, export scripts, one-off fixes). These skip the spec and verification receipt but still follow the five stages. The PLAN stage is shorter. The DO THIS NOW card still gets delivered.

### Bug fix sessions

If Debrief reveals failures, Claude Chat delivers a mini DO THIS NOW card for a fix pass. Same format, just shorter. It references the same prompts file with a new FIX section added.

### Multi-session builds (5+ phases)

For large builds spanning 3+ Claude Code sessions, the DO THIS NOW card includes numbered SESSION sections:

```
  SESSION 1 (Phases 1 and 2):
  1. Open Claude Code
  2. Attach: [files]
  3. Paste OPENING PROMPT
  ...
  7. Copy completion summary
  8. Close Claude Code

  SESSION 2 (Phases 3 and 4):
  1. Open Claude Code
  2. Paste SESSION 2 BRIDGE PROMPT from [file], Section "[name]"
  ...
```

### Builds that don't need Claude Code

Some work (copy writing, spec revisions, email templates) happens entirely in Claude Chat. These don't need a DO THIS NOW card. The Chat delivers final files directly and moves to Close.

---

## CLAUDE'S OBLIGATIONS

This section governs Claude Chat's behavior in every build chat.

1. **Always deliver a DO THIS NOW card when handing off to Adrian.** No exceptions. No "here are the files, you know what to do." The card is mandatory.

2. **Never bury action items in prose.** If Adrian needs to do something, it goes on a card. Not in a paragraph. Not in a footnote in the spec.

3. **Include pre-flight content inline.** SQL migrations, env var values, any copy/paste content goes directly on the DO THIS NOW card. Adrian should never need to open the prompts file to find setup steps.

4. **PK file management is explicit every time.** Every card includes the DELETE / UPLOAD / NO CHANGES sections. Even if nothing changes, say "NO CHANGES — all files stay as is."

5. **One card per handoff.** Don't deliver a card at exchange 3 and then amend it at exchange 5. If the plan changes, deliver a fresh card that replaces the old one.

6. **The card is the contract.** If it's not on the card, Adrian doesn't do it. If Claude forgot to include something, that's Claude's problem to fix in the next exchange, not Adrian's problem to discover in Claude Code.

7. **Every code reference in a prompt must be verified against the actual codebase before the prompt ships.** Component names, file paths, import paths, Supabase column names, prop names, function names — all must match what actually exists, not what Claude thinks exists. If Claude is unsure, the prompt must include a Read Before Write audit that catches it. "Probably called Pipeline.jsx" is not acceptable. "Verified: src/components/PipelineView.jsx" is the standard.

8. **Zero Compromise Protocol rules must be embedded in every prompt, not referenced.** Claude Code cannot read project knowledge files. A line that says "follow the Zero Compromise Code Protocol" is invisible to Claude Code. The critical rules (Read Before Write, Do Not Modify fence, build gate, no silent refactors, sidebar smoke test, phase-level commits) must appear as literal instructions in every phase prompt. The reference line at the top of the prompts file is for Adrian's awareness only.

9. **The Glass sound line must appear at the end of every phase prompt.** Not just the opening prompt. Not just mentioned once. The literal line `afplay /System/Library/Sounds/Glass.aiff` must be the last instruction in every single prompt block. Claude Code loses instructions across phases. Repetition is the only fix.

---

## PROMPT INTEGRITY STANDARD

This section exists because Claude Code only knows what it's told in each prompt. It cannot read project knowledge, it cannot remember previous sessions, and it drops instructions that aren't repeated. Every prompt must be self-contained.

### The Embedded Protocol Rule

The Zero Compromise Code Protocol lives in project knowledge for Claude Chat's reference. But Claude Code never sees it. That means every Claude Code prompt must physically contain these instructions (not reference them):

**In every OPENING PROMPT:**
```
Before writing any code, read every file you will modify. List the files 
you read and summarize what each one currently does. Do not proceed until 
this audit is complete.
```

**In every phase prompt (including Phase 2, 3, etc.):**
```
DO NOT MODIFY these files unless this prompt explicitly says to:
[explicit file list]

Do not refactor, rename, or reorganize any code outside the scope of 
this phase. If you see code that could be improved but is not part of 
this phase's spec, leave it alone.
```

**At the end of every phase prompt, always these three blocks in this order:**
```
Run npm run build. If there are any errors, fix them before confirming 
this phase is complete. Do not move to the next phase with build errors.

Navigate to each sidebar page (Dashboard, Pipeline, Band Ops, Content, 
Clients, Financials, Settings) and confirm each renders without console errors.

Confirm completion by listing each acceptance criterion and its PASS/FAIL status.

afplay /System/Library/Sounds/Glass.aiff
```

### The Glass Sound Rule

`afplay /System/Library/Sounds/Glass.aiff` is Adrian's signal that a phase is complete. It must be the absolute last line of every prompt block. Not "play a sound when done." Not "alert me." The exact command. Every time.

Why it stops working: Claude Code treats each prompt as a fresh instruction set. If the sound command is only in the opening prompt, Claude Code forgets about it by Phase 2. The fix is pure repetition — include it in every prompt, every time, no exceptions.

### The Code Precision Rule

Every reference to existing code in a Claude Code prompt must be verified against the actual codebase. This is Claude Chat's responsibility before delivering the prompts file. Specific requirements:

- **File paths:** Use the exact path. `src/components/PipelineView.jsx` not `Pipeline.jsx` or `the pipeline component.`
- **Component names:** Use the exact export name. `PipelineView` not `Pipeline`.
- **Supabase columns:** Use the actual column name from the schema. `partner1_first` not `partner_1_first`. `price` not `total_price`. `config` not `piece_count`.
- **Function names:** Use the exact name. `callClaude` not `callClaudeAPI` (or vice versa — whatever the actual name is).
- **Import paths:** Verify the actual relative path. `../../utils/claudeApi` not `../utils/claude-api`.
- **Design tokens:** Use the exact token object paths. `COLORS.warmCream` not `COLORS.cream` or a raw hex value.

If Claude Chat is writing prompts for a codebase it hasn't seen recently, the prompts file must include Read Before Write instructions that force Claude Code to verify names before using them. The opening prompt already includes this audit, but if later phases reference specific files by name, those names must be correct.

**The test:** Could Adrian take any file path or function name from the prompt, search for it in the codebase, and find an exact match? If not, the prompt has a precision error.

---

## FILE NAMING CONVENTIONS

Build deliverables follow this naming pattern:

| File | Naming Pattern | Example |
|------|---------------|---------|
| Spec | `[Project]_[Scope]_Build_Spec.md` | `Greenway_CC_v3_Week6_Build_Spec.md` |
| Verification Receipt | `[Project]_[Scope]_Verification_Receipt.md` | `Greenway_CC_v3_Week6_Verification_Receipt.md` |
| Claude Code Prompts | `[Project]_[Scope]_Claude_Code_Prompts.md` | `Greenway_CC_v3_Week6_Claude_Code_Prompts.md` |

Permanent files use fixed names (no version numbers in filename):
- `MASTER_STATUS.md`
- `BUILD_MANIFEST.md`
- `CHANGELOG.md`
- `Zero_Compromise_Code_Protocol.md`
- `Claude_Build_Workflow.md`

Build-scoped files (spec, receipt, prompts) get deleted from PK after the build ships. They've served their purpose. The manifest and master status carry forward everything that matters.

---

## THE FULL CYCLE, STEP BY STEP

Here's the entire flow as one linear sequence. This is what a build looks like from start to finish.

**1. Start a new Claude Chat.** Paste the bridge prompt from Master Status (or start fresh with your topic).

**2. Claude Chat reads Master Status.** Declares topic. Pulls relevant project files.

**3. You and Claude Chat plan the build.** Scope, architecture, edge cases. Claude Chat writes the spec.

**4. Claude Chat cross-references the Build Manifest.** Produces Verification Receipt. Fixes any mismatches.

**5. Claude Chat writes Claude Code Prompts.** Structured per Zero Compromise Protocol.

**6. Claude Chat delivers the DO THIS NOW card.** This is the handoff. All files are delivered above the card.

**7. You follow the card.** Delete PK files. Upload PK files. Run pre-flight. Open Claude Code. Paste prompts. Wait for Glass. Copy summary.

**8. You come back to Claude Chat.** Paste completion summary.

**9. Claude Chat debriefs.** Reviews results. If clean, moves to Close. If issues, delivers fix card.

**10. Claude Chat closes.** Delivers updated Master Status, updated Manifest, bridge prompt, and CLEANUP card.

**11. You follow the CLEANUP card.** Swap PK files. Done.

**12. Next build starts at step 1.**

---

**END OF DOCUMENT**
