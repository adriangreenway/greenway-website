---
name: create-proposal
description: Create and deploy a branded client proposal at proposals.greenwayband.com from a Gmail inquiry. Use whenever Adrian gives a client name and wants a proposal ("make a proposal for X", "she filled out the form", "send the Smiths a proposal"), or wants an existing proposal revised.
---

# Create Proposal

Turn a client inquiry in Adrian's Gmail into a live branded proposal at
`https://proposals.greenwayband.com/<slug>`.

Read first: `docs/proposals/PROPOSAL_SYSTEM.md` (where things live, deploy runbook),
`docs/proposals/PRICING_AND_CONTENT.md` (real prices, locked lineups, testimonial
pool, copy rules), `docs/proposals/TEMPLATE.html` (the page to fill in).
Model: Sonnet 5 is fine for this workflow.

## Steps

1. **Find the inquiry in Gmail.** Load the Gmail tools via ToolSearch (query
   "gmail search threads" → `search_threads`, `get_thread`). If the Gmail connector
   isn't connected, stop and tell Adrian to connect Gmail in the Claude app's
   connector settings — never guess inquiry content.
   Search recipes, in order:
   - `from:17hatsmail.com "<client name>"` — the 17hats lead form is the primary
     inquiry source. Fields: Name, Email, Phone, Date of the event, Venue, Band size,
     Type of Event, How did you hear about us, Anything else.
   - `"<last name>"` broadly, and the venue name — clients and planners often send
     richer follow-ups (e.g. a fiancé's requirements email, a planner negotiating).
   Read every related thread. **The newest message wins** — requirements evolve
   (band size, add-ons, budget) after the first form.

2. **Build a fact sheet** from the emails only: couple/client full names, date,
   venue + city, event type, planner/coordinator, referral, band size requested,
   add-ons mentioned (cocktail hour, DJ, ceremony), timeline hints, budget signals,
   special notes. Mark every unknown as UNKNOWN — never fill a gap by invention.

3. **Draft the offer.** Default: the size they asked for as the Recommended card,
   plus one sensible alternative (the other size they mentioned, else the 6-piece).
   Prices from PRICING_AND_CONTENT.md (Houston baseline; outside Houston expect
   higher and flag travel). Add-ons only if they asked or Adrian says so.

4. **Ask Adrian at most 3 questions** — see/pay/risk only, each with a recommended
   default. Typically: (a) packages + prices, (b) add-ons, (c) anything odd in the
   thread. Skip anything the inquiry already answers. Technical choices are yours.

5. **Build the page.** Copy `docs/proposals/TEMPLATE.html` to
   `~/Desktop/greenway-proposals/<slug>/index.html` (slug rules in
   PROPOSAL_SYSTEM.md). Fill every `{{TOKEN}}`; NO intro section — the Template 4.1
   email carries the greeting (Adrian, 2026-07-14; see PRICING_AND_CONTENT.md);
   timeline section only if the schedule is known — else delete it; lineups exactly
   per PRICING_AND_CONTENT.md. Corporate event → base on the live `the-united-way`
   page instead of the wedding template.

6. **Verify locally.**
   - `grep -c '{{' index.html` must output 0
   - names, date, venue, prices correct against the fact sheet; totals = sum of rows
   - open the file in a browser and eyeball cover, packages, closing

7. **Present the draft and WAIT.** Status card: client, date, venue, packages with
   prices and totals, add-ons, the URL it will get, plus anything else in the deploy
   folder that will ride along. Deploying is production — needs Adrian's explicit
   "go" (CLAUDE.md destructive-actions rule).

8. **Deploy + verify** exactly per the PROPOSAL_SYSTEM.md runbook (pre-deploy live
   diff, deploy from the folder, "CDN requesting N files" sanity check, curl the new
   URL + spot-check two existing ones). Report the live URL.

9. **After.** Commit in `~/Desktop/greenway-proposals` ("Add proposal: <slug>").
   Then ALWAYS create the Gmail **draft** to the client automatically (Adrian,
   2026-07-14) — never send; sending is his. Follow Template 4.1 in
   `docs/proposals/EMAIL_TEMPLATES.md` exactly: the proposal link embedded on the
   word "proposal" (`https://proposals.greenwayband.com/<slug>/`, trailing slash),
   the 17hats scheduling link on the word "here", raw URLs only in hrefs, no other
   links. The draft sitting in Gmail is the source of truth for what gets sent.
   Report that it's in Drafts and tell Adrian to click-test both links before
   sending (see the Google "Redirect Notice" gotcha noted there).

## Revisions

"Update X's proposal" → overwrite the same `<slug>/index.html` (URL stays valid for
the client), same verify + approval + deploy flow, commit message
"Update proposal: <slug>". Note the prior deploy ID as the rollback point.
