# Clemans / Walsh handoff to Claude

Updated 2026-11-05. Adrian explicitly handed this task to Claude because it was taking too long. Codex has stopped task work. Do not rebuild or deploy again merely to resume.

## First action

Run the project's start-session skill, read this file, then verify the ALREADY PUBLISHED wedding. The production command finished successfully before Adrian's interruption. This is a verification handoff, not a request to repeat deployment.

## Deployment and authorization

- Project: `/Users/adrianjoseph/greenway-website`, branch `docs/build-context`.
- Permanent source: `/Users/adrianjoseph/Desktop/greenway-gigs/clemans/11-14-26/`.
- Shared source: `/Users/adrianjoseph/Desktop/greenway-gigs/` (not a Git repo).
- Wedding URL: https://gigs.greenwayband.com/clemans/11-14-26/
- Signed-in Netlify site was verified: `greenway-gigs`, `8205364b-6929-454b-bfe0-51afaeb02636`.
- Completed production deployment: `6aece93f0e57d081860a88a6`.
- Deployment receipt: `tmp/gig-intake-2026-11-14/production-deployment.json`.
- Deployment URL: https://6aece93f0e57d081860a88a6--greenway-gigs.netlify.app
- Approved rollback: `6ad382461408242713bcf20c` (October 17 release).
- Adrian explicitly approved the local save, then answered **Approve publishing and rollback if needed**. These actions do not need approval again. A subsequent corrective publication needs its own approval. No commit, push, scheduling write, email, or message was authorized or performed.
- The completed command deployed the ENTIRE shared folder with `netlify deploy --prod --no-build --dir . --site 8205364b-6929-454b-bfe0-51afaeb02636`, preserving the shared functions. The command is finished; no deployment remains running.

## What is done

Twelve wedding files are saved and deployed: five HTML pages, four PDFs, manifest, service worker v4, and the correct wedding thumbnail. The homepage has one new Clemans / Walsh row. Full and MC pages are marked Adrian Only and unlinked, but are not password protected. The hub links Band Sheet then Listening Room. No practice audio was supplied; Listening Room deliberately has an empty state.

Local checks passed: phone layouts for all five pages, MC next/back/keyboard/tap controls, factual/placeholder scans, shared Full/Band clock timing adjustment, PDF visual review (Band 2 pages, Full 3, MC 3, slides 16). `gig-kickoff.py --check` returned READY for the permanent folder. `npm run build` passed November 5, six Astro pages, with the existing dependency-only unused-import warning. No test/typecheck script exists.

All 132 older-wedding files matched live copies immediately before publishing. All 134 publicly served files matched Netlify's inventory; the prior homepage matched the saved backup. No live-only wedding files were found. The only intended content changes were 12 new wedding files and the one homepage row. Source `netlify.toml` and other weddings were not edited. Netlify's generated config artifact had a different hash from the prior published generated file; it is not publicly served (404). Generated headers and bundler settings matched source. Do not overwrite source configuration with a generated artifact.

Homepage backup: `tmp/gig-intake-2026-11-14/shared-homepage-before-local-save-2026-11-05.html`.

## Required remaining verification

1. Confirm Netlify's current published deployment is `6aece93f0e57d081860a88a6`; do not assume a stale receipt is current if another tool has acted.
2. Check the new hub, Band, Full, MC, Listening Room, all PDFs, thumbnail, privacy headers and service-worker cache list on the public hostname. Compare deployed bytes with the approved hashes in `release-review.json`.
3. Verify older wedding files remain intact against `live-file-inventory.json` and `live-local-comparison-curl.json`, plus the shared clock endpoint without a write or credential.
4. Verify actual new-wedding offline navigation, including a clicked rewritten hub link. New-wedding localhost service-worker installation stalled, so offline readiness has NOT been claimed. A separate Chrome control on the already-live Hardaway wedding succeeded with `Saved for offline use`, showing the live check can run. In-app localhost preview cannot prove offline operation. Use an isolated browser profile under this project's temp folder; no security bypasses.
5. If material checks fail, Adrian approved restoring the exact rollback above. Otherwise update status notes and give Adrian the working wedding link. Avoid further research or redesign.

Do not blindly rerun `render-check.cjs` as a production test: it points at the old local draft server and regenerates PDFs. Adapt verification only if needed.

## Settled wedding facts

- Abigail (Abby) Clemans and Jacob (Jake) Walsh, Saturday November 14, 2026, Le Tesserae, Houston. Use Sara's Gulf Coast packet. The old Siegel / Dubel scheduling label was incorrect; another task's project notes say it has been corrected. Codex did not edit scheduling.
- Sound crew noon, per Adrian. Band call 3:10 PM and soundcheck 4:10–5:10 PM are derived from Adrian's explicitly requested backward formula and the planner's 5:10 hard stop. Keep the earlier noon sound call as buffer.
- Standard formula is saved in `.agents/skills/create-gig-sheet/SKILL.md`: work backward from band meal/cocktail or earlier soundcheck hard stop; one hour soundcheck, one hour band load-in/setup, three hours sound setup. Preserve explicit event-specific commitments. His 5 PM cocktail example was illustrative, not this wedding's times.
- Meals start 4 PM and 5:10 PM in the Wine Room. Adrian explicitly requested starts only. Do not ask for finish times again or suppress these confirmed starts. Counts and unknown role assignments stay private.
- Cocktail trio 5:15 PM; Set One 6:15; entrance/dances 6:30; blessing 6:40; breaks 7 and 8:30; Set Two 7:30; Set Three 9; last guest song cue 10; guests exit 10:05; private dance 10:10; performance ends/departure 10:15; load out 10:20 through 12:15 AM next day.
- Entrance TRACK She's a Rainbow, Rolling Stones, chorus. First dance LIVE Everything, Michael Buble. Father/daughter LIVE You Got It, Roy Orbison. Mother/son LIVE Shimmer, Shawn Mullins. Bouquet TRACK Fearless, Taylor Swift, explicitly selected by Adrian. Private last dance LIVE Starting Over, Chris Stapleton. Do not label Starting Over as the final guest song.
- Full/MC retain sourced dance cut guidance; Band excludes cut durations, private moments, MC detail and contacts. Band has sourced title-only favorites and do-not-play list, and standing band attire.
- Shared clock indices originally differed between Full/Band timelines. This wedding alone now marks matching band-call anchors with `data-clock`; a simulated Set Two ten-minute delay produced the same event/delay on both pages. Shared templates/backend were not changed.

## Private source and verification files

Everything is in `tmp/gig-intake-2026-11-14/`. Never commit this folder: it includes raw planner and contract PDFs, client/vendor details and isolated browser profiles.

- `fact-ledger.json`: source/music ledger and remaining questions. Its scheduling-mismatch note is historical; project notes were updated separately afterward.
- `planner-timeline.pdf`, `venue-diagram.pdf`, `signed-scope.pdf`: originals already read fully.
- `build_draft.py`: generator; creates the temporary preview, not the permanent source.
- `release-review.json`: approved 12-file SHA-256 inventory and local checks.
- `local-save-verification.json`: save receipt and backup path.
- `hosting-preflight.json`: verified site and previous deployment.
- `live-file-inventory.json`, `live-local-comparison-curl.json`: successful pre-publication comparison. The earlier `live-local-comparison.json` used a Python trust store that failed TLS; use the later curl result. No certificate checks were disabled.
- `publishing-review.json`: prepared before approval, so its awaiting-approval status is now superseded by this handoff and the deployment receipt.
- `verification.json`, `pdf-review/`: local checks and visual review.
- `saved-hub-review.png`: screenshot of the saved local wedding hub.

Sources already reconciled: Gmail thread `1a0a0f274d2fe0a4`, October 26 timeline message `1a178c32130872f9`, October 28 sent approval `1a18351b9091199f`, opening clarification `1a1836f9b252081c`, signed-scope thread `19bd80c866ed96fc`. Do not repeat intake research unless a specific inconsistency appears.

Unresolved but omitted from performer pages: final guest-song title, playback operators and special-dance singer/arrangement details, parent names/pronunciations, loading access/case storage, final meal role/count coordination, and stage platform identification. Practice audio absent. No invented replacements or TBD labels appear on sheets/PDFs.

## Protected work and ownership

Codex changed the gig skill and its meal reference at Adrian's request, plus scoped `docs/CURRENT_STATE.md` and `START_HERE.md` records. These are uncommitted. This handoff is also uncommitted. Preserve the new permanent wedding and homepage row.

Pre-existing changes from other work: `.claude/launch.json`, `docs/ROADMAP.md`, and untracked `docs/scheduling/BOOKED_TRUTH_PLAN.md`. Do not stage, overwrite or include them in this work. Astro rebuild and Squarespace go-live remain on hold. No commit or push was done.

Adrian has now handed this wedding to Claude. One tool owns it at a time; Codex will not continue editing or publishing.

## Copyable resume prompt

```text
Open /Users/adrianjoseph/greenway-website and run the start-session skill. Read docs/gig-sheets/CLEMANS_WALSH_2026-11-14_HANDOFF.md. The Clemans / Walsh gig sheet and formula update are complete, and production deployment 6aece93f0e57d081860a88a6 already finished. Live/offline verification is outstanding. Preserve the saved wedding, skill edits, private temp intake and unrelated scheduling/launch-settings changes. Do not redeploy or repeat intake. Next action: verify that existing deployment end to end, using the handoff's already-approved rollback only if checks fail, then send Adrian the wedding link.
```
