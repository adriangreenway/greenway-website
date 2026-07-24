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

## D14: Proposals get real media + embedded video + on-page CTA; gig-contract reuse covers the imagery
- **Date:** 2026-07-23
- **Why:** the proposal pages were beautifully typeset pricing documents with zero proof of the product. A mockup plus a 15-agent adversarial review confirmed the upgrade (photos, video before pricing, Schedule-a-Call CTA) with every reviewer voting "ship with fixes." Adrian confirmed the band's client contract grants reuse of photos and video from gigs, which clears the pictured couples and photographer-permission question raised in review.
- **Consequences:** every new wedding proposal includes by default: two performance-photo bands, an on-page video, the three-hours contract-standard line, and two Schedule-a-Call CTAs on the static 17hats URL. Only assets in the "Approved media pool" (PRICING_AND_CONTENT.md) may appear; video captions must stay honest to the actual asset (one song is "one song," never "full performance"). Photos of unnamed prior clients are allowed on proposals per the contract-reuse clause; naming any prior client remains banned. **Superseded same day by the v2 amendment below** on palette and video hosting — the venue strip mentioned in the original consequence was built, then removed (see v2).
- **Reconsider if:** a pictured couple or a photographer objects (pull the asset immediately, contract or not), or Adrian supplies a proper highlight reel to replace the single-song video.

### D14 v2 amendment: hybrid palette; self-hosted video, no Vimeo; venue strip dropped
- **Date:** 2026-07-23 (same day, second session — Adrian on Fable 5 reviewing the v1 build)
- **Why:** Adrian liked the direction but wanted to see it against the site's real brand guide before committing to all-dark. A 3-judge panel (art director, buyer-simulation, brand-system consultant) compared three built variants — full dark, full cream, hybrid — and voted the hybrid unanimously at strong confidence: it keeps the dark cover's drama as the first-impression unit while making the mid-page pricing/details legible black-on-cream instead of gray-on-near-black, which was the actual complaint (a paying parent squinting at the total). Adrian also said "if we're going to be premium, let's be premium" about the Vimeo embed — a fair point, since his Plus plan can't remove the Vimeo logo from embeds — so the video moved to self-hosted. He separately looked at the venue-strip trust line the same day and pulled it: "I don't think it adds much value."
- **Consequences:** proposal palette is the hybrid — dark cover + dark closing (byte-identical to every proposal shipped before 2026-07-23), cream document body using the website's own locked design tokens (`docs/DESIGN_SYSTEM.md`). The video is a self-hosted mp4 (`assets/uptown-funk-2026a.mp4`, 720p, ~73MB) with no third-party player or watermark; the Vimeo copy stays up unlisted as Adrian's own reference only, never linked from the page. There is no venue strip — do not re-add without Adrian raising it again. Full technical detail (color tokens, judge-panel fixes, encode settings) is in `docs/proposals/PRICING_AND_CONTENT.md`.
- **Reconsider if:** Adrian wants the venue strip back, wants a different video, or wants to revisit the palette once more real (non-sample) proposals have shipped under it.

### D14 v3 amendment: text-weight compensation + gradient photo seam restored (overrides the judge panel)
- **Date:** 2026-07-23 (same day, third pass — Adrian reviewed a live preview built on Marli Hinojosa's real content)
- **Why:** seeing the hybrid palette on real content, Adrian felt the cream-body text looked visibly thinner than the dark-zone text ("could just be in my mind, but..."). It's a genuine optical effect, not a font or weight change (dark ink on a light page reads thinner than the same weight in light ink on a dark page), but he wanted it to look like before regardless: "let's fix this to look like it did before, even if an optical illusion." He also felt the hard-edge cut from the first photo into "Your Evening" was too abrupt and asked to try the gradient again, overriding the judge panel's explicit "no gradient scrim, hard edges only" recommendation from the v1 stress test.
- **Consequences:** `body` now carries `-webkit-text-stroke: 0.35px var(--cream)` (a hairline stroke that visually thickens cream-body text to match the dark zones), cancelled back to 0 inside `.cover`/`.closing` since those don't need compensation. The photo-band-1 seam (`.photo-band::after`) is a gradient again — dark at the top blending into the cover, cream at the bottom blending into the body — replacing the v2 hard-edge treatment. The crowd photo band (`.photo-band--short`) keeps its hard-edge treatment; Adrian's feedback was specifically about the first seam.
- **Reconsider if:** the text-stroke reads as heavier than intended on a real device (it was verified only via headless-Chrome screenshot, not Adrian's own eyes yet), or Adrian wants the second (crowd) photo seam softened to match.

### D14 v4 amendment: photo bands show the whole frame on wide screens, keep the crop on phones
- **Date:** 2026-07-23 (fourth pass — closed the last open item from the v3 review; Adrian replied "you decide" to Claude's recommended mix)
- **Why:** Adrian flagged in the v3 review that the fixed-height strip crops the photos and he wanted to see the whole frame. A side-by-side built from the real Hinojosa preview showed the strip crop was literally cutting the musicians out of the first photo — the band is the product, so the crop was deleting the proof. But the same whole-frame treatment on a phone renders the 3:2 photo only ~250px tall and the gradient scrim swallows its bottom third, while the current crop fills most of a phone screen. The tradeoff flips by device, so the layout does too.
- **Consequences:** `.photo-band img` is now `height: auto` (full 3:2 frame, no crop) by default; a `@media (max-width: 560px)` block restores the previous immersive crop (68vh / 52vh with `object-fit: cover`) on phones. Applies to both photo bands in `docs/proposals/TEMPLATE.html`. Verified via headless-Chrome captures at 1280px and 390px.
- **Reconsider if:** Adrian sees it on his own phone and wants the whole frame there too (one-line change: delete the media-query block), or a future photo's key subject sits outside the phone crop's center framing.

### D14 v5 amendment: dedicated print/PDF layer; crowd photo capped everywhere; two flags left open
- **Date:** 2026-07-23 (fifth pass — Adrian took the draft PDF to ChatGPT for fresh eyes and brought back a print-layout brief; he approved trying it in full)
- **Why:** the first PDF export sliced the continuous-scroll page at arbitrary Letter boundaries (half-height cover, orphaned 10-piece heading, 10MB file). The fix is a dedicated `@media print` layout, not screen changes. Along the way: (a) Adrian saw the whole-frame crowd photo on the draft and called it too dominant, so it is height-capped (52vh/max 480px) at every width while the first band photo keeps the v4 whole-frame treatment; (b) that cap exposed a real CSS bug — `.photo-band--short` is a single class, so the phone media rule was silently overriding the cap on phones (equal specificity, later source order); fixed by re-asserting the cap inside the media block, and the draft Adrian phone-checked before the fix showed the crowd photo taller than intended.
- **Consequences:** template and hinojosa page now carry: a 7-page Letter print layout (cover / photo+details / video, vertically centered / package 1 / package 2+cocktail / crowd+testimonials / closing; full-bleed `@page margin 0`); print-only video links (poster + caption link to the proposal's live URL; on screen the poster now plays the video inline); `greenwayband.com` in the closing is a real link; a reduced-motion guard; and shared `-print.jpg` photo copies + export runbook in `PROPOSAL_SYSTEM.md` (~1.4MB, was 10.6). New tokens: `{{SLUG}}`, `{{VALID_THROUGH_DATE}}` (send date + 30 days — hinojosa computed as August 20, 2026 from its 2026-07-21 send). **Two business flags Adrian has not decided:** (1) Marli's page still shows 6-Piece as Recommended and listed first, which predates the 2026-07-23 "10-Piece always leads" default — left as sent deliberately; (2) no reservation/retainer policy language exists anywhere, so none was added.
- **Reconsider if:** Adrian rules on either flag, a proposal needs a different page plan (e.g. with a timeline section the print pagination needs re-checking), or a photo asset changes (regenerate its `-print.jpg` twin).

### D14 v6 amendment: ChatGPT correction pass executed verbatim (14-item brief)
- **Date:** 2026-07-23 (sixth pass — Adrian rejected the "Greenway Six/Ten" rename experiment and pasted a strict correction brief; executed as scoped, no extras)
- **Why:** fresh-eyes review. The brief reverted the rename, differentiated the packages in copy instead of names, consolidated the duplicated services lists, promoted the reception-duration sentence out of the fine print, dropped the travel disclaimer for this Houston venue, fixed the video poster's navigation risk, added a direct "Move Forward" conversion path ahead of scheduling, finished the cover contact links, and raised the floor on low-contrast/tiny utility text.
- **Consequences:** names stay "6-Piece Band"/"10-Piece Band" (badge stays on the 6-Piece, still flagged open from v5). One shared "Included With Every Reception Package" section with reworded items ("Personalized First-Dance Performance", "Advance Song Requests"). Duration line is body copy above Cocktail Hour ("...four-hour reception.", hyphenated). Travel note is now conditional copy (template keeps it with a 50+ mile rule; hinojosa drops it). Video: whole-frame click plays inline, no screen link anywhere, print-only overlay carries the PDF link; video column widened to a ~700px frame on desktop. Closing: primary Move Forward mailto (prefilled, no preselected package) + secondary Schedule-a-call line. Cover footer site/email are links. Contrast/type floors: scroll hint, cover footer, closing note, validity now ≥10px and brighter vars; section labels and badge ≥10px on phones. PDF is 8 intentional pages (~1.4MB): the cocktail block became its own vertically centered print page. New template tokens {{PKG1_DESC}}/{{PKG2_DESC}}/{{MOVE_FORWARD_MAILTO}}; copy synced to PRICING_AND_CONTENT.md. Other live proposals untouched.
- **Reconsider if:** Adrian wants package names revisited properly (options presented, not invented mid-build), the Move Forward email wording needs tuning after real replies arrive, or a non-Houston proposal needs the travel line back (it is conditional, not deleted).

### D14 v7 amendment: package composition + closing hierarchy rolled back to original (Adrian's strict correction spec)
- **Date:** 2026-07-24 (fresh session; Adrian sent a structured correction spec naming the original-composition draft deploy `6a62bd98…` as the visual reference — verified it is indeed the original layout before restoring)
- **Why:** Adrian judged the v6 package redesign visually weaker than the original: the detached shared-services section left each package feeling incomplete, and the Move-Forward-primary closing demoted the call that actually converts. The spec is a targeted rollback of those two areas, explicitly not another redesign.
- **Consequences:** each package card again carries the original two-column itemization (Musicians left, Included Services right, investment beneath both) with the original five labels — "Personalized First Dances" and "Song Requests" return; the v6 rewordings and the "Included With Every Reception Package" section are retired. Uppercase package subtitles are retired; exactly one visually-secondary benefit sentence sits under each package name (new approved copy in PRICING_AND_CONTENT.md; {{PKG1_SUBTITLE}}/{{PKG2_SUBTITLE}} tokens removed). Closing hierarchy: primary solid **Schedule a Call** button (17hats) + quiet *Move forward by email* secondary ({{MOVE_FORWARD_MAILTO}} is now the secondary's href). Marli's page keeps 6-Piece first with the Recommended badge as sent, per the spec — closes v5 open flag (1) for her page; the template default stays 10-Piece-leads. All v5/v6 approved improvements preserved: names, print/PDF layout and page breaks, inline video playback, larger video frame, clickable cover/closing contacts, no Houston travel line, exact August 20 2026 validity, dance-floor crop, reduced motion, mobile text floors. Applied to TEMPLATE.html + the hinojosa draft only; every other proposal and prod untouched. v5 open flag (2), reservation-policy language, remains open.
- **Reconsider if:** Adrian revisits package presentation or naming again (present real options first, per his standing instruction), or real client replies show the closing hierarchy needs tuning.

### D14 v8 amendment: 10-Piece always Recommended and first; desktop side-by-side comparison; video copy stripped
- **Date:** 2026-07-24 (same day as v7 — Adrian reviewed the v7 draft: "this actually looks really good… we're almost there," then asked for two changes plus a stress-test of package order)
- **Why:** Adrian's instinct ("always recommend the 10-piece") matches convention: lead with the premium option so the price descends — the 6-Piece then reads as the saving instead of the 10-Piece reading as a jump — and the badge on the larger band gives buyers permission to choose it. Side-by-side on desktop removes scroll order from the anchoring question entirely (both prices visible at once); mobile keeps the stacked order, 10-Piece first. He floated renaming the tiers (Signature/Greenway) and backed off in the same breath; names stay descriptive per v6 — size is the fact that sells the upgrade. The video section's three stacked copy lines ("Watch the band" / "See the Band Live" / "Photos only say so much…") read cluttered to him; the player itself was fine.
- **Consequences:** the 10-Piece leads with the Recommended badge on EVERY wedding proposal, no per-client exceptions — the hinojosa redo is realigned (v5 open flag 1 closes as "always 10-Piece"; her as-sent live page still shows the old order until Adrian chooses to update prod). New screen-only `@media screen and (min-width: 900px)` layout in TEMPLATE.html + hinojosa: `.packages-grid` two-column comparison, bordered cards, badge overlapping the card's top border, lists stacked inside each card, totals pinned so both prices sit on one line, card-divider hidden; packages section content widens to 1080px. Mobile/tablet stacked layout and the print pagination are untouched (screen-scoped query; Letter is 816px wide). Video section is now label + player + caption only ("Uptown Funk, recorded live · tap to play"); serif title, desc line, and their CSS removed. Verified at 1280px and 375px, console clean.
- **Reconsider if:** real client behavior suggests premium-first intimidates instead of anchors, or Adrian supplies reservation-policy language — the one buyer question the page still can't answer (v5 flag 2, still open).

### D14 v9 amendment: no payment/terms copy on the page; broader filler sweep vetoed; "Two Ways to Fill the Room" locked
- **Date:** 2026-07-24 (two same-day reversals around the reservation line; this is Adrian's final ruling)
- **Why:** Adrian supplied the real reservation policy (50% deposit; contract → invoice via 17hats; Zelle/check/card+4%) and a deposit line went on the draft — he cut it within the hour: "superfluous… too much noise… less is more with this copy. That screams AI, and I'm trying to put my own spin on this." A follow-up sweep also cut the closing note and both lead-in questions; on review he restored them: "I like the 'Want to talk through your options? Schedule a call' thing. That one was fine. The only thing I wanted you to take out was the 50% deposit thing."
- **Consequences:** the page is exactly the approved v8 state with NO deposit/reservation copy anywhere (v5 open flag 2 closes as "deliberately none on the page"; the full policy lives in PRICING_AND_CONTENT "Reservation + payment flow" for contract/invoice/email use only — Zelle, CBJ Productions check address, 4% card fee never appear on a proposal URL). Kept verbatim at his word: inline CTA *Want to talk through your options? Schedule a call.*, closing note *On the call we'll walk through the options and how to hold your date.*, secondary *Ready now? Move forward by email.*, and the packages heading **"Two Ways to Fill the Room"** — "i love that one" (locked; never touch). Standing rule in TEMPLATE.html header: no payment/terms copy ever; don't invent NEW filler beyond the established lines. The "next steps" reply email is deferred at his word ("we can build that in later").
- **Reconsider if:** Adrian later wants a terms line in his own words, or real client replies argue for changing the closing.

---
## Open decisions (not yet made — see `docs/ROADMAP.md`)
- Reconcile `dev` vs `main` and decide the canonical deploy branch.
- The staging self-redirect to Squarespace: keep, or remove until launch so the new build is previewable at the staging URL.
- Whether to wire the `published` flag to nav + a 404 guard, or keep it as metadata.
- Whether to commit/publish the uncommitted April work (Reviews + FAQ on `dev`).
- Whether the FAQ AI assistant is still wanted (D8).
