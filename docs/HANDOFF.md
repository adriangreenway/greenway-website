# HANDOFF — living bridge

> **To resume in a new session:** open this repo in Claude Code and say
> *"Read `CLAUDE.md` and `docs/HANDOFF.md`, then continue."* That replaces the old paste-in
> bridge prompt. Keep this file current — update it at the end of any meaningful work.
> **Last updated: 2026-06-27.**

## ▶ Next action (Phase 1 — agreed with Adrian 2026-06-27)
Goal: get the site to ONE clean, previewable, deployable state, then make it viewable.
1. **Make `dev` canonical.** Commit the uncommitted April work on `dev` (publishes Reviews + FAQ —
   see "Working tree" below); fold in anything on `main` not already present; retire/realign `main`.
2. **Remove the `netlify.toml` self-redirect** so staging stops bouncing to the old Squarespace site,
   and give Adrian a working preview (Netlify deploy preview or local `npm run dev`).
3. **Plan mode first** → show Adrian the plan in plain language → then build. Commit per step.
**Do NOT touch:** real Reviews content (Adrian supplies real testimonials) or DNS (Adrian flips at launch).
After Phase 1: wire the real hero video (`~/Desktop/Greenway/website-content/greenway-hero.webm`) into
the placeholder hero, then QA + an end-to-end Book-form lead test. Full roadmap below + in [TASKS.md](TASKS.md).
Note: Adrian is non-technical — keep all updates brief and jargon-free.

## Workflow model (Code-exclusive)
Adrian works **exclusively in Claude Code** now (no claude.ai chat). Plan in-tool (plan mode),
build in-tool, verify in-tool. The repo + agent memory are the "project knowledge"; there are no
Project-Knowledge file swaps and no paste-in bridge prompts. The quality spine still applies —
see [CODE_WORKFLOW.md](CODE_WORKFLOW.md) and the governing docs
([Zero_Compromise_Code_Protocol.md](Zero_Compromise_Code_Protocol.md),
[Claude_Build_Workflow.md](Claude_Build_Workflow.md)). Full rationale in `CLAUDE.md` §11.

## Repo & branch state
- **`dev`** — the **deployed** branch (Netlify; strong inference). Committed pages: Home, Experience,
  Book, 404. HEAD `4198c83`.
- **`main`** — **not deployed**; has Reviews + FAQ committed & published + proposals. Diverged from
  `dev` after the Experience commit. Reconcile before relying on either.
- **`docs/build-context`** — *(current docs branch)* holds the build/relay context docs:
  the Build Bible, the two governing protocol docs, and this handoff. Pushed to GitHub. Never merge
  docs work into `main` without intent.

## Working tree — uncommitted (do not blow away)
- **April work on `dev`** (still uncommitted): `src/config/site.ts` (publish Reviews+FAQ),
  `src/components/Header.astro` (+Reviews/FAQ nav), and the untracked `src/pages/faq.astro` +
  `reviews.astro` (byte-identical to `main`'s). Someone was publishing Reviews/FAQ on `dev` but
  never committed it. Decide its fate before building on top.
- **Recovery docs** (`CLAUDE.md` + most of `/docs`): created in the recovery pass, present locally,
  **not yet committed** pending Adrian's go-ahead. They auto-load from the working tree regardless.

## What lives where
- **Operating manual / auto-loaded context:** [`CLAUDE.md`](../CLAUDE.md)
- **Verified current state + WEB-07 finding:** [PROJECT_STATE.md](PROJECT_STATE.md)
- **Tasks (Now/Next/Later/Blocked):** [TASKS.md](TASKS.md)
- **Design tokens / content rules / integrations:** [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) ·
  [CONTENT_AND_MESSAGING.md](CONTENT_AND_MESSAGING.md) · [INTEGRATIONS.md](INTEGRATIONS.md)
- **Build-decision capture tool (interactive):** [Greenway_Website_Build_Bible_v2.html](Greenway_Website_Build_Bible_v2.html)

## Current priorities (condensed — full list in TASKS.md)
1. **Reconcile `dev` vs `main`** and decide the fate of the uncommitted April work (publish Reviews/FAQ).
2. **Decide the staging self-redirect** (`netlify.toml` 301s the staging URL to the old Squarespace
   site — see below).
3. Real content: written Reviews (currently placeholders), hero video, "For Planners" detail.
4. Unbuilt: Vocalist Showcase page; FAQ AI assistant (FAQ shipped as a static accordion).

## How to view the site
The staging URL **currently bounces to the old Squarespace site** (the `netlify.toml` redirect 301s
`greenway-website.netlify.app` → `greenwayband.com`, which is still Squarespace). To actually see
the build:
- **Local (works now):** `npm run dev` → `http://localhost:4321` *(verified booting this session)*.
- **Netlify deploy permalink:** dashboard → Deploys → latest → preview (different host, skips the redirect).
- **Unblock staging:** remove/comment the redirect block in `netlify.toml`, redeploy.

## Reconcile-later note
The Build Bible lists a few specs that drifted from the live build — e.g. it says **Google Fonts**,
but the site was rebuilt on **Fontsource** (see [DECISIONS.md](DECISIONS.md) D-002). Treat the repo +
`/docs` as the source of truth over the Bible where they disagree.
