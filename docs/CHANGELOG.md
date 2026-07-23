# CHANGELOG: The Greenway Band Website

The archive. Claude Code does not read this during normal sessions. Read it only when Adrian asks about history or an audit needs it.

Rule: when "Recently completed" in `CURRENT_STATE.md` holds more than 5 items, the oldest move here, one line each, newest first.

Derived from `git log` on `github.com/adriangreenway/greenway-website` plus the 2026-06-27 recovery pass. `dev` and `main` diverged after the Experience page commit (`98d5569`).

| Date | What shipped |
|---|---|
| 2026-07-03 | Foreman workflow installed: `CLAUDE.md` rewritten around the Foreman rule set (model guidance, git safety, verification gate, communication rules); `.claude/skills/` copied verbatim from `~/greenway-growth-hour`; `START_HERE.md`, `docs/CURRENT_STATE.md`, `docs/PROJECT_BRIEF.md`, `docs/ROADMAP.md` added; `docs/DECISIONS.md` reformatted (D9, D10 added). See D10. |
| 2026-07-03 | Squarespace lead-form embed: Gates 0-2 CLOSED. Built dark (D11), redesigned to v3's premium look (Bodoni Moda, charcoal shadowed fields, phone auto-format) per Adrian's Chat 1.3 reference; Adrian's real phone test confirmed landing correctly in Growth Hour Contacts. Gate 3 (going live) still needs Adrian's explicit "go." Separate from, and not blocked by, the Astro rebuild pause (D9). |
| 2026-06-27 | Recovery & documentation pass: added `CLAUDE.md`, replaced the Astro starter `README.md`, added the full `/docs` verified-state set (`PROJECT_STATE.md`, `ARCHITECTURE.md`, `INTEGRATIONS.md`, `DESIGN_SYSTEM.md`, `CONTENT_AND_MESSAGING.md`, `PRODUCT_SPEC.md`, `SITE_MAP.md`, `TASKS.md`, `DECISIONS.md`, `CODE_WORKFLOW.md`, `CHANGELOG.md`). Hardened `.gitignore` to exclude all `.env*`. No application/source code changed; no commits, pushes, or deploys performed. |
| 2026-04-13 | `dev` branch tip (`4198c83`): redirect `netlify.app` subdomain to `greenwayband.com` (currently makes staging bounce to the old Squarespace site — see Known issues in `CURRENT_STATE.md`). |
| 2026-03-27 (unpushed to `dev`) | `main` branch: `8000c01` Reviews page (placeholder structure); `e17d5a6` FAQ page (12 pre-written Q&As, accordion); plus proposal-microsite commits (`eaae9c8`, `2f55682`, `204b8a1`) and `b162e74` (Netlify rebuild trigger for Experience). `main` is not the deployed branch. |
| 2026-03 | Shared history before the branch split: `98d5569` Experience page with phase sections and real copy (divergence point); `f5050a2` Bodoni Moda variable font fix; `6697c98` replaced Google Fonts CDN with Fontsource (D2); `46f1bef`/`3caf99f`/`dd3e408` "Week 12R" rebuild — Book page, homepage sections, design system + global layout (D7); `f5d42d4`/`7a755a2`/`fa6bacd`/`96ea88e`/`d15dc70`/`07ae1cb` "Week 12" original build — 404 page + production deploy, Book page, homepage, BaseLayout/Header/Footer/Logo, Astro scaffold + design tokens + site config + Netlify, initial scaffold. |

## Unreleased — uncommitted working tree on `dev` (since April 2026, still not pushed)
- Publish Reviews and FAQ (`site.ts` flags → `true`; added to `Header` nav).
- Bring `reviews.astro` + `faq.astro` onto `dev` (byte-identical to `main`'s versions).
- Not committed, therefore not deployed. See `PROJECT_STATE.md` for the full evidence trail.
