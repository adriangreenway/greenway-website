---
name: create-proposal
description: Vet inbound booking leads, then create or revise branded wedding and corporate proposals at proposals.greenwayband.com from Gmail inquiries. Use for lead qualification, proposal creation, proposal revisions, pricing offers, or suspicious booking inquiries.
---

# Create Proposal

Turn a qualified inquiry into a verified proposal without fabricating content, re-reading evidence, or expanding the user's requested external actions. Use Sol throughout.

**Brand reference (v4, approved 2026-11-05).** For any logo, thumbnail, favicon,
avatar, color, or type choice, follow `~/Desktop/Greenway_Brand_Guide_v4.html`
(sections 02 to 05 and the Digital Marks page). Thumbnail or avatar = the nameplate
(Greenway: rich black `#0A0A09` lettering on a warm cream `#F5F2ED` circle). Favicon =
the editorial pair, GB, both letters on one line. Staggered initials, single-letter
icons and outlined avatar badges are retired. No gold, metallic, pure white, or
invented colors; teal belongs to Kirby only. The page template still controls layout.
Never read anything in an `_ARCHIVE_OLD_VERSIONS_DO_NOT_USE` folder.

## Operating rules

- One agent owns the proposal through closeout. A read-only delegate may handle one
  bounded check, but must not repeat full research or edit the proposal source.
- Treat an explicit **NO EMAIL** instruction as sticky. Do not read the email
  template, draft, send, or ask for email approval unless Adrian later changes it.
  Proposal creation never implies permission to draft or send email.
- Keep separate approvals for: business choices plus exact external file write;
  publishing plus exact credential read; post-verification commit. Push, email,
  and unrelated repairs each need their own authorization.
- Never re-ask for an approved action or same-scope retry, even after a process
  ends, unless Adrian limited or revoked it. Never transfer approval across phases.

## Read references only when needed

Do not load every proposal document at the start.

1. Before scoring a lead, read `docs/LEAD_VETTING_GATE.md` once in full.
2. After a PASS, read only the relevant sections of
   `docs/proposals/PRICING_AND_CONTENT.md`: requested configurations, add-ons,
   locked lineups, approved copy/testimonials, and copy-integrity rules. Read its
   corporate/travel section only for a corporate event or out-of-town pricing.
3. For a wedding build, use `docs/proposals/TEMPLATE.html` as an immutable source.
   Inspect its token list and editable body sections with focused searches and
   line ranges; do not dump the 1,974-line CSS and JavaScript into context.
4. Read `docs/proposals/PROPOSAL_SYSTEM.md` slug and canonical-location sections
   when choosing the path. Read its deploy runbook only when the local draft is
   review-ready and publishing is in scope. Do not read the PDF section unless
   Adrian asks for a PDF.
5. Read `docs/proposals/EMAIL_TEMPLATES.md` only after explicit authorization for
   an email draft and only when NO EMAIL is not active.

## Phase 1: inquiry and gate

Use the Gmail connector. If it is unavailable, stop rather than guessing.

- For the newest 17hats inquiry, query `17hatsmail.com`; add a name only if already
  known. Batch justified related queries when the connector allows.
- Search results are metadata, not facts. Filter them for the same people, date,
  planner, or event before fetching content. Do not read a venue's unrelated
  inquiry history merely because the venue name matches.
- Deduplicate thread IDs, then read every truly related thread once in FULL,
  including every message and quoted reply trail. Never build from snippets.
  The newest message controls changing requirements.
- Build one fact sheet: names, email, phone, date, venue/city, event type, planner,
  referral, band size, add-ons, timing, budget, notes, score, markers, PASS/FAIL.
  Mark unknowns UNKNOWN.
- Apply the full gate policy. A failed score or any auto-fail marker stops all
  pricing and proposal work. Report the evidence and one recommended response.

## Phase 2: offer and file approval

Only a PASS reaches pricing. Never invent a price, lineup, claim, venue history,
schedule, or relationship.

- Wedding default: 10-Piece first with the Recommended badge. Put a requested size
  other than 10-Piece second; otherwise use 6-Piece. If that size lacks an approved price or locked
  lineup, obtain both before building; never infer either.
- Cocktail Hour Solo/Duo/Trio cards are the wedding default and stay outside
  totals. If the lead already chose one option, make it a priced row in each
  package instead. Add DJ or extra hours only when requested or approved.
- Houston uses the observed baseline as the recommendation. Outside Houston,
  flag travel and obtain Adrian's confirmation. Exact supplied prices override
  the need to review irrelevant historical price examples.
- Ask at most three see/pay/risk questions. In one approval request, present the
  recommended packages, prices, add-ons, and the exact canonical target
  `~/Desktop/greenway-proposals/<slug>/index.html`. State whether it is new or
  will be overwritten, what changes, the risk, and how to undo it. This approval
  authorizes only that local file write.

## Phase 3: build and local verification

Canonical deploy folder: `~/Desktop/greenway-proposals/`. Never use
`~/greenway-proposals/` or this repo's `public/proposals/`.

- Before writing, inspect destination/repo status and compare local HEAD/origin
  with remote main once, read-only. Never auto-pull or merge; stop on newer work.
  Preserve unrelated work. Create new pages exclusively; read a revision's full destination before overwriting it.
- Copy and fill the wedding template programmatically. Change tokens and the
  required editable markup only; keep CSS, JavaScript, media, scheduler links,
  song-list link, hybrid palette, and CTA structure unchanged. Strip instructional
  HTML comments. No intro, venue strip, payment terms, or invented filler.
- Include a timeline only when it is known. Omit unknown cells or replace them
  with known facts. Use the locked lineup and approved testimonial text exactly.
- Confirm all template tokens are gone; names, date, venue, descriptions, prices,
  totals, lineups, slug links, and validity date match the fact sheet; and all six
  shared image/video assets exist. Review the final changed-file list.
- Run one focused browser pass covering desktop and mobile layout, cover, details,
  packages, media playback, both call links, song list, email CTA when present,
  and closing. Repeat checks only after a new change or a failure.

Present the client, date, venue, packages, totals, add-ons, intended URL, and
deploy-folder ride-alongs for review. Do not publish yet.

## Phase 4: publish once approved

Publishing changes production. After local review, ask separately and name the
site, full-folder risk, rollback, and credential `Greenway Dev/Netlify Personal
Access Token`. Approval covers that task, normally one read; same-scope retries
retain approval unless Adrian explicitly limited or revoked it.

Use `~/Desktop/greenway-proposals/` and site ID
`c6041c94-c26c-4ab8-ae5f-96c43addb081`; run preflight, API comparison, deploy, and authenticated checks inside one continuous exec process:

- Call `op read` once. Let the same process wait for Touch ID. Do not launch a
  duplicate command while it waits, and do not run auth probes such as
  `op whoami`. If a successful read is empty, retry once unless Adrian explicitly
  authorized only one read. For any other authorization failure, stop.
- Keep the token only in process memory and a child process environment. Never
  print it, write it to a file, put it in command arguments, enable `set -x`, or
  expose it through debug output. API code must construct auth headers internally
  from the environment.
- Compare live/local manifests and hashes for every publishable file in both
  directions; the delta must exactly match the approved scope. Record the current
  deploy ID as rollback. Normalize known Netlify path case or generated-config
  serialization only after proving equivalent redirects/headers. Generated config
  may count as one additional requested file only after that proof. Never blanket-
  ignore differences. Stop on an unexpected real difference; its repair and republish are changed
  scope and need separate approval before modifying anything.
- Deploy the entire canonical folder and check that the reported requested-file
  count matches the intended changes.

Public postchecks require no token: verify the new URL and two existing proposals
return 200, title/media are correct, and both `/CLAUDE.md` and `/claude.md` return
404. Report the live URL and rollback ID.

## Phase 5: closeout

After production verification, show the exact changed files and ask separately
before a local commit. Use `Add proposal: <slug>` for a proposal-only commit;
name any additional approved repair explicitly and keep it separately traceable.
A commit does not authorize a push.

If email is explicitly authorized and NO EMAIL is not active, read the email
template then create a Gmail draft only after live verification. Never send it;
sending is Adrian's action unless separately and explicitly authorized.

## Conditional corporate and revision rules

For corporate work, follow the same phases but use approved layout
`~/Desktop/greenway-proposals/the-united-way/index.html`, never the wedding template.
Remove its intro. “Prepared for” names the buyer/company; event facts stay in details.
Use a hyphenated organization slug; if an agency represents an
end client, ask which visible name and slug Adrian wants. Use corporate language,
one package by default (10-Piece unless requested otherwise), no Cocktail Hour, and production lines that
mirror the inquiry. Remove Sound/Lighting when the purchaser provides them.
Confirm travel miles and final price with Adrian. For agencies, search related
buyer-domain threads; correspondence informs price but does not prove a booking.

For revisions, read the existing page, name the exact overwrite and rollback point,
preserve the URL, and obtain the same separate approvals that apply to the scope.
