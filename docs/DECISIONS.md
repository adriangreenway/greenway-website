# DECISIONS: The Greenway Band Website

Big architecture and product choices that must not be silently reversed.
Claude Code: check this file before proposing a change to anything listed here. Only record decisions that would be expensive or confusing to reverse. Trivial choices don't belong here.

Format:

## D[n]: [Decision in one line]
- **Date:** [date]
- **Why:** [One or two sentences.]
- **Consequences:** [What this locks in.]
- **Reconsider if:** [The condition that would justify reopening it.]

---

## D1: Astro static site on Netlify, DNS on Cloudflare
- **Date:** project start
- **Why:** fast, cheap, low-maintenance static hosting; a reversible launch (flip one DNS record).
- **Consequences:** no server, database, or auth in this repo. Production domain `greenwayband.com` stays on Squarespace until launch.
- **Reconsider if:** the site ever needs server-rendered or dynamic content beyond a static build.

## D2: Fontsource over Google Fonts CDN
- **Date:** commits `6697c98`, `f5050a2`
- **Why:** self-hosted fonts remove a third-party request, improve performance/privacy, and avoid CDN dependency.
- **Consequences:** fonts load via `@fontsource-variable/bodoni-moda` and `@fontsource/plus-jakarta-sans`, not a CDN `<link>`.
- **Reconsider if:** never, unless a font vendor issue forces it.

## D3: No hairline rules in browser-rendered logos
- **Date:** Week 12R rebuild
- **Why:** hairlines render inconsistently across browsers/zoom levels and cheapen the wordmark.
- **Consequences:** header, footer, and hero logos are text-based; the inline-SVG `Logo` (404 only) uses text elements only, no `<line>`/`<rect>` hairlines.
- **Reconsider if:** never, unless the brand mark itself changes.

## D4: Copy integrity — real content or explicit placeholders only
- **Date:** hard rule, origin predates the 2026-06-27 recovery pass
- **Why:** an earlier build shipped fabricated venues. This guardrail prevents recurrence.
- **Consequences:** never fabricate venues, testimonials, or stats; use real content or an explicit `<!-- PLACEHOLDER -->`. Only the 13 approved venues may be used (`docs/CONTENT_AND_MESSAGING.md`).
- **Reconsider if:** never.

## D5: Six-page site set
- **Date:** intent set at project start
- **Why:** covers storytelling + social proof + conversion for a premium band: Home, Experience (replaces "About"), Vocalist Showcase, Reviews, FAQ, Book.
- **Consequences:** as of 2026-07-03, Vocalist Showcase is not built, Reviews is a placeholder, and FAQ shipped as a static accordion instead of the planned AI assistant shell.
- **Reconsider if:** Adrian wants to drop or add a page.

## D6: Separate-projects boundary
- **Date:** hard rule, origin predates the 2026-06-27 recovery pass
- **Why:** clean separation of concerns and security surface; this site is a static storefront, not a system of record.
- **Consequences:** no Supabase/Stripe/Twilio code in this repo. The only backend touchpoint is the Book form → CRM `lead-intake`. Keep isolated from the Command Center CRM (`greenway-crm`) and the personal app "Kai."
- **Reconsider if:** never, unless Adrian explicitly decides to merge projects.

## D7: "Week 12R" rebuild to the locked design system
- **Date:** commits `dd3e408`, `3caf99f`, `46f1bef`
- **Why:** establish a single, compliant baseline after drift from the original spec.
- **Consequences:** the design system, layout, homepage, and Book page were rebuilt to the locked token spec in `docs/DESIGN_SYSTEM.md`.
- **Reconsider if:** the design system itself is revisited by Adrian.

## D8: FAQ shipped as a static accordion; AI assistant deferred
- **Date:** de facto, commit `e17d5a6` on `main`
- **Why:** unknown from the repo history, likely scope or time. No artifact of a formal decision exists.
- **Consequences:** FAQ is a static 12-question accordion today, not the planned AI assistant shell.
- **Reconsider if:** Adrian confirms he still wants the AI assistant (see `docs/ROADMAP.md` Later).

## D9: This site's Astro rebuild is paused for a separate project's lead-intake build
- **Date:** 2026-07-03 (decided in the Growth Hour project, not this repo)
- **Why:** Adrian's biggest near-term priority is lead intake, owned by the separate Growth Hour app. He decided greenwayband.com stays on Squarespace and gets its own lead-capture form (built dark, gated go-live) posting to Growth Hour's new endpoint, rather than accelerating this Astro site's launch.
- **Consequences:** no new Astro features, deploys, or DNS changes on this repo until Adrian lifts the pause. Reconciliation hygiene (branch split, staging redirect) remains available but not urgent. **The Squarespace lead-form embed itself (D11) is explicitly NOT covered by this pause** — it's a separate, small, unblocked task that happens to also live in this repo. Source: `~/greenway-growth-hour/docs/{CURRENT_STATE,ROADMAP,DECISIONS}.md`, `START_HERE.md`, and `WEBSITE_PLAN_2026-07-03.md` (kept at `~/greenway-growth-hour`, referenced by this repo).
- **Reconsider if:** Growth Hour's M3 ships, or Adrian explicitly asks to resume this site's launch track sooner.

## D11: Squarespace lead-form embed built dark, gated by 4 go-live checks
- **Date:** 2026-07-03 (`WEBSITE_PLAN_2026-07-03.md`, Bridge Prompt B)
- **Why:** Adrian's Squarespace site once had a form go live half-working and quietly lost real leads. The 4-gate sequence (renders correctly → endpoint live → one real end-to-end test → Adrian's explicit "go") exists specifically to prevent a repeat.
- **Consequences:** the embed code (`docs/squarespace/lead-form-embed.html`) posts to Growth Hour's `POST /api/lead-intake` (a different app/repo, `~/greenway-growth-hour`), not to this repo's own `BookForm.astro` → Command Center path — the two intake paths are intentionally independent and must not be merged casually. The embed is not part of the Astro build; it's pasted directly into Squarespace's CMS by Adrian. CORS on the Growth Hour endpoint is locked to `greenwayband.com` origins only (verified live 2026-07-03), so the embed only works once actually placed on a real greenwayband.com page. Never skip a gate, especially Gate 3 (going live) — that one is Adrian's call every time, not something to infer from the other gates passing.
- **Reconsider if:** the Growth Hour endpoint's schema or CORS policy changes (the embed would need a matching update), or Adrian decides to fold this into the Astro rebuild instead of Squarespace.

## D10: Adopt the Foreman workflow (CLAUDE.md rules + `.claude/skills/`)
- **Date:** 2026-07-03
- **Why:** match the process already running in the Growth Hour project, so Adrian gets the same brevity, safety, and skill-based workflow across every Greenway repo he works in with Claude Code.
- **Consequences:** `CLAUDE.md` was rewritten around the Foreman rule set; `.claude/skills/` (start-session, plan-feature, build-feature, fix-bug, audit-project, verify-work, end-session) was copied verbatim from `~/greenway-growth-hour`; `START_HERE.md`, `docs/CURRENT_STATE.md`, `docs/PROJECT_BRIEF.md`, `docs/ROADMAP.md`, and this file were added or reshaped to match. The prior recovery-pass docs (`PROJECT_STATE.md`, `ARCHITECTURE.md`, `INTEGRATIONS.md`, etc.) were kept as-is for their deep, evidence-backed detail; the two governing Relay Method docs (`Zero_Compromise_Code_Protocol.md`, `Claude_Build_Workflow.md`) remain do-not-modify reference material.
- **Reconsider if:** never, unless Adrian wants a different workflow.

## D12: Squarespace lead-form Gate 3 — go live via main nav, not a Book-page link (SUPERSEDED same day, see D13)
- **Date:** 2026-07-03
- **Why:** Adrian said "go" on Gate 3 and chose adding the page to the site's main navigation (renamed from "Inquiry test" to a real client-facing title) over linking it from an existing Book/Contact page.
- **Consequences:** never executed. Adrian reconsidered minutes later, before any Squarespace change was made (Claude has no Squarespace access — nothing was actually clicked live). See D13 for the current, controlling decision.
- **Reconsider if:** superseded, see D13.

## D13: Nothing goes live until BOTH the website build and the Growth Hour app are entirely done
- **Date:** 2026-07-03
- **Why:** Adrian was burned before by a form going live too early — submissions weren't landing in the right place and leads were quietly lost. He wants to be "very clinical" this time: no go-live of anything, on either project, until both are fully finished, not just at a milestone like Growth Hour's M3.
- **Consequences:** this is a stricter hold than D9/D11 described. Building, coding, and phone-testing the Squarespace lead-form embed continues normally — only the actual go-live step (Gate 3: publishing the hidden page or linking it into nav) is frozen. Same freeze applies to the Astro rebuild's eventual launch. Do not propose or execute any go-live action (Squarespace publish/nav-link, Cloudflare DNS flip, Astro production deploy) without Adrian explicitly confirming both builds are complete — a "go" on a smaller sub-decision (like which go-live method) is not the same as a go on going live itself.
- **Reconsider if:** Adrian explicitly says both the website and Growth Hour builds are done and he's ready to go live.

---
## Open decisions (not yet made — see `docs/ROADMAP.md`)
- Reconcile `dev` vs `main` and decide the canonical deploy branch.
- The staging self-redirect to Squarespace: keep, or remove until launch so the new build is previewable at the staging URL.
- Whether to wire the `published` flag to nav + a 404 guard, or keep it as metadata.
- Whether to commit/publish the uncommitted April work (Reviews + FAQ on `dev`).
- Whether the FAQ AI assistant is still wanted (D8).
