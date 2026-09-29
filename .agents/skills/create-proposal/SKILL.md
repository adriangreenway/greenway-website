---
name: create-proposal
description: Vet inbound booking leads, then create and deploy a branded client proposal at proposals.greenwayband.com from a Gmail inquiry, wedding or corporate. Use whenever Adrian asks whether a lead is qualified or suspicious, gives a client name and wants a proposal ("make a proposal for X", "she filled out the form", "send the Smiths a proposal", "quote this corporate gig"), or wants an existing proposal revised. Corporate events follow the Corporate proposals section.
---

# Create Proposal

Turn a client inquiry in Adrian's Gmail into a live branded proposal at
`https://proposals.greenwayband.com/<slug>`.

Read first: `docs/LEAD_VETTING_GATE.md` (mandatory qualification gate),
`docs/proposals/PROPOSAL_SYSTEM.md` (where things live, deploy runbook),
`docs/proposals/PRICING_AND_CONTENT.md` (real prices, locked lineups, testimonial
pool, copy rules), `docs/proposals/TEMPLATE.html` (the page to fill in).
Model: Use Sol for research, building, verification, and deployment.

## Lead vetting gate (D19, 2026-07-29)

No proposal, pricing sheet, or package list goes to a lead until it passes
**2 of 3**:

1. **Place:** a named venue, or at least a named city. A state or region alone
   does not count.
2. **Phone:** a phone number for the couple or their planner.
3. **Source:** a stated referral source, or arrival through the 17hats capture
   form. Form arrival satisfies this check by itself.

**Auto-fail regardless of score** when any of these appear:

- Overseas, international-travel, or email-only framing used to refuse a call.
- Hearing-impaired or deaf framing used to refuse phone contact.
- An unverified third party, coordinator, agent, or relative handling payment.
- Any overpayment, check-plus-refund, or request to forward the difference.
- Instant agreement to book without questions about music, the band, or
  availability.
- Pressure to move fast, or a date that keeps changing.

For a score of 0 or 1, or any auto-fail marker, stop before drafting pricing.
Report the score and markers to Adrian with one recommended action: a short
vetting reply asking for venue, phone, and a call, or ignore the inquiry. Never
guess in the lead's favor.

Blind requests for a standard package or pricing sheet also fail when they have
no venue, no date detail beyond a month, and no personal detail.

**Money rule with no exceptions:** never refund or forward an overpayment. Treat
the transaction as void, return the original instrument uncashed, or let the bank
reverse it. Never send a partial refund or forward money to another party.

Any future lead-intake or proposal automation must hard-stop failed leads, queue
the score and markers for Adrian, and never auto-send pricing. Full policy and
precedent: `docs/LEAD_VETTING_GATE.md`.

## Steps

1. **Find the inquiry in Gmail.** Load the connected Gmail search and full-thread
   reading tools with tool search. If the Gmail connector isn't connected, stop and
   tell Adrian to connect Gmail in the Codex app's connector settings — never guess
   inquiry content.
   Search recipes, in order:
   - `from:17hatsmail.com "<client name>"` — the 17hats lead form is the primary
     inquiry source. Fields: Name, Email, Phone, Date of the event, Venue, Band size,
     Type of Event, How did you hear about us, Anything else.
   - `"<last name>"` broadly, and the venue name — clients and planners often send
     richer follow-ups (e.g. a fiancé's requirements email, a planner negotiating).
   Read every related thread IN FULL. `search_threads` returns truncated
   snippets — NEVER build facts from a snippet. Call `get_thread`
   (FULL_CONTENT, the default) on every related thread and read every message
   in it, including quoted reply trails, before writing the fact sheet.
   **The newest message wins** — requirements evolve (band size, add-ons,
   budget) after the first form.

2. **Build a fact sheet and score the lead** from the emails only: couple/client full names, date,
   venue + city, event type, planner/coordinator, referral, band size requested,
   add-ons mentioned (cocktail hour, DJ, ceremony), timeline hints, budget signals,
   special notes, gate score, markers, and PASS/FAIL. Mark every unknown as
   UNKNOWN — never fill a gap by invention.

3. **Only after PASS, draft the offer.** Default: the 10-Piece leads with the Recommended badge
   regardless of the size they asked for (Adrian, 2026-07-23, campbell build);
   the size they requested rides as the second card (else the 6-piece).
   Prices from PRICING_AND_CONTENT.md (Houston baseline; outside Houston expect
   higher and flag travel). The Cocktail Hour options block (Solo/Duo/Trio cards,
   no totals) is included by DEFAULT on every wedding proposal (Adrian,
   2026-07-23); if the client already chose a cocktail add-on, show it as a
   priced row inside each package instead. Other add-ons (DJ, extra hour) only
   if they asked or Adrian says so.

4. **Ask Adrian at most 3 questions** — see/pay/risk only, each with a recommended
   default. Typically: (a) packages + prices, (b) add-ons, (c) anything odd in the
   thread. Skip anything the inquiry already answers. Technical choices are yours.

5. **Build the page.** Copy `docs/proposals/TEMPLATE.html` to
   `~/Desktop/greenway-proposals/<slug>/index.html` (slug rules in
   PROPOSAL_SYSTEM.md). Before creating or overwriting anything outside the
   active project, tell Adrian the exact target folder, what will change, the
   overwrite risk, and how it can be undone, then wait for explicit approval to
   modify that folder. This file approval does not authorize deployment,
   commit, or Gmail changes. Fill every `{{TOKEN}}`; NO intro section — the Template 4.1
   email carries the greeting (Adrian, 2026-07-14; see PRICING_AND_CONTENT.md);
   timeline section only if the schedule is known — else delete it; lineups exactly
   per PRICING_AND_CONTENT.md. Corporate event → follow **Corporate proposals**
   below instead of the wedding template.
   **Media + CTA are on by default (D14, 2026-07-23 + v2 same day, see
   PRICING_AND_CONTENT.md "Approved media pool" + "Palette (v2)"):** the two
   photo bands, the click-to-load self-hosted video, the hours line, and both
   Schedule-a-Call CTAs all come with the template unchanged — nothing to fill
   in, they reference the shared `~/Desktop/greenway-proposals/assets/` files
   by fixed relative path. Confirm that folder exists in the deploy directory
   before building (it should already be there from the 2026-07-23 build; if
   missing, stop and tell Adrian rather than recreating it from guesswork).
   Never change the video file without Adrian supplying a new source. **No
   venue strip** — it was built then removed same day (Adrian: "doesn't add
   much value"); don't re-add it without him asking. **Palette is the hybrid**
   (dark cover + dark closing, cream document body) — never flatten it back to
   all-dark or all-cream without Adrian raising it again.

6. **Verify locally.**
   - `grep -c '{{' index.html` must output 0
   - names, date, venue, prices correct against the fact sheet; totals = sum of rows
   - open the file in a browser and eyeball cover, packages, closing
   - `assets/band-stage-2026a.webp`, `assets/crowd-2026a.webp`,
     `assets/uptown-funk-poster-2026a.jpg`, and `assets/uptown-funk-2026a.mp4`
     all exist in the deploy folder (shared, sit one level up from `<slug>/`,
     not per-client — don't recreate them)

7. **Present the draft and WAIT.** Status card: client, date, venue, packages with
   prices and totals, add-ons, the URL it will get, plus anything else in the deploy
   folder that will ride along. Deploying is production — needs Adrian's explicit
   "go" (AGENTS.md destructive-actions rule).

8. **Deploy + verify** exactly per the PROPOSAL_SYSTEM.md runbook (pre-deploy live
   diff, deploy from the folder, "CDN requesting N files" sanity check, curl the new
   URL + spot-check two existing ones). Report the live URL.

9. **After.** Ask for Adrian's explicit approval before committing in
   `~/Desktop/greenway-proposals` ("Add proposal: <slug>"). Creating or updating
   a Gmail draft changes connected cloud data and needs its own explicit
   approval. After that approval, create the Gmail **draft** to the client after
   live verification, but never send it; sending is Adrian's. Follow Template 4.1 in
   `docs/proposals/EMAIL_TEMPLATES.md` exactly: the proposal link embedded on the
   word "proposal" (`https://proposals.greenwayband.com/<slug>/`, trailing slash),
   the 17hats scheduling link on the word "here", raw URLs only in hrefs, no other
   links. The draft sitting in Gmail is the source of truth for what gets sent.
   Report that it's in Drafts and tell Adrian to click-test both links before
   sending (see the Google "Redirect Notice" gotcha noted there).

## Corporate proposals (Adrian, 2026-07-27, Ken-Ran build)

Same pipeline as the steps above — Gmail fact sheet, verify, present, wait for
the file-write approval, then separate deployment and Gmail-draft approvals.
Where this section is silent, wedding rules apply.

- **Base page:** copy `~/Desktop/greenway-proposals/the-united-way/index.html`
  (the approved corporate layout), NOT the wedding TEMPLATE.html. `opengroup` is
  a second shipped corporate reference. **Delete the intro section** ("A note
  for you" / greeting / body / signature) when you copy it — corporate follows
  the same no-intro standard as weddings (Adrian, 2026-07-28); the page runs
  cover straight into the package. Any personal note belongs in the email only.
- **Cover "Prepared for" = the client or company name, never the event name**
  (Adrian, 2026-07-28). If the inquiry only names a talent-buying agency
  (e.g. Ken-Ran Productions) and no separate host org, the agency's name still
  goes there — not the event title. The event name/date/venue belong in the
  Event Details grid as their own row, not the cover.
- **Slug:** hyphenated org name per PROPOSAL_SYSTEM.md (`the-united-way`). If an
  agency inquires on behalf of an end client, ask Adrian which name the slug
  should carry (agencies shop proposals to their client).
- **Tone:** no "Congratulations" greeting, no wedding words (reception, first
  dance, big day). It's "your event", "your program", "your guests".
- **One package by default** — the configuration that fits the event (10-Piece
  unless the inquiry says otherwise). A second config card only if Adrian asks.
  No Cocktail Hour block — that default is wedding-only.
- **Production lines mirror the inquiry.** If production/staging is provided by
  the purchaser or venue, the page says so (`Production: Provided by Purchaser`)
  and Sound/Lighting Equipment come OUT of the included-services list. Backline,
  stage specs, and set times come from the inquiry, never invented.
- **Travel pricing:** use the corporate travel formula in
  PRICING_AND_CONTENT.md. Show Adrian the math (miles, rate, headcount) in the
  pre-build questions; fold the result into a single Investment figure on the
  page. Miles and the final price are pay decisions — his confirm required.
- **Testimonials:** same approved pool of 3, nothing new.
- **Email draft:** adapt Template 4.1 — strip congratulations and wedding lines,
  keep the proposal-link-on-"proposal" and scheduler-link mechanics exactly.
- **Agencies are repeat buyers.** Search Gmail for prior threads from the same
  domain (e.g. kenran.com goes back to 2022). Prior quotes and negotiation
  history inform Adrian's pricing but NEVER appear on the page.

## Revisions

"Update X's proposal" → first explain the exact external file that will be
overwritten and wait for explicit file-write approval. The URL stays valid for
the client. Verify locally, then obtain separate deployment, commit, and Gmail
draft approvals as applicable. Note the prior deploy ID as the rollback point.
