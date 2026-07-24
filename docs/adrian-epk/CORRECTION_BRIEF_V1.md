# Adrian Michael EPK Claude Correction Brief

Version: 1

Date: July 24, 2026

## Purpose

Rebuild the current three-page Adrian EPK as one short, mobile-first booking page.

This brief supersedes the prior solo-versus-vocalist page architecture. Adrian is not asking visitors to choose between two separate versions of him. The page should present one professional identity, show the best performance proof quickly, and make it easy to contact him.

This is an EPK correction only. Do not change the Boston 75 CRM app, Command Center, Greenway proposals, the main Greenway website, or unrelated routes.

Do not deploy to production. A draft or preview deployment is allowed only after the approved implementation phase.

## Controlling direction

1. One page at the existing Adrian root route.
2. One primary 50- to 60-second live reel.
3. One clear contact action immediately below the reel.
4. No separate solo page.
5. No separate vocalist page.
6. Do not repeatedly label Adrian as an acoustic act.
7. Solo, duo, trio, private-event, hospitality, and established-band work are booking options, not separate brands.
8. Preserve the current premium visual language and the quality of the existing email cards.
9. Reduce the copy sharply. The page should feel written by a working musician, not a marketing department.

## Phase 0: read-only inspection

Before changing anything:

1. Inspect the actual current repository state, git status, route structure, build scripts, media locations, deployment configuration, and any existing redirects.
2. Identify every file that would need to change.
3. Confirm that the Adrian EPK is isolated from unrelated Greenway and Boston 75 application code.
4. Confirm whether the final 50- to 60-second reel exists. If only the current 2:21 reel exists, treat it as a temporary draft asset.
5. Explain how the old `/solo/` and `/vocalist/` paths will safely point to the unified Adrian page.
6. Report any conflict between this brief and the actual repository.

Stop after the Phase 0 report. Do not edit files until Adrian approves Phase 1.

## Phase 1: approved implementation

### Route and information architecture

- Keep one canonical Adrian landing page.
- Remove the solo-versus-vocalist choice from the visitor experience.
- Redirect any existing solo and vocalist child routes to the canonical Adrian page.
- Replace the current mobile navigation with only:
  - Reel
  - Experience
  - Contact
- Keep the page short enough that contact begins within roughly 2,500 to 3,000 CSS pixels on a 390px-wide phone.

### Exact page order

1. Hero
2. Three-point credibility strip
3. Primary live reel
4. Immediate `Email Adrian` CTA
5. Compact experience and musical range
6. Contact
7. Short Houston-band disclosure in the footer

Do not add more sections without Adrian's approval.

## Approved copy

Use this copy as written unless a technical constraint requires a small formatting change.

### Metadata

Title:

`Adrian Michael | Boston Vocalist & Live Performer`

Description:

`Boston-based professional vocalist available for band work, private events, hospitality, and select solo, duo, and trio dates.`

### Hero

Eyebrow:

`ADRIAN MICHAEL • BOSTON`

Headline:

`Professional vocalist and live performer, now based in Boston.`

Support:

`Available for substitute and recurring band work, private events, hospitality, and select solo, duo, or trio dates.`

Primary CTA:

`WATCH THE LIVE REEL`

Secondary CTA:

`EMAIL ADRIAN`

### Credibility strip

- `10 years full-time`
- `Lead and harmony vocals`
- `Owner and lead singer of The Greenway Band`

### Reel

Section label:

`LIVE REEL`

Place a full-width or visually dominant 16:9 reel here. Put an `EMAIL ADRIAN` button immediately below the player. Do not place another video, song list, biography, or proof section between the reel and this button.

### Experience

Section label:

`EXPERIENCE`

Copy:

`Adrian has performed full-time for 10 years and owns and fronts The Greenway Band, a Houston-based private-event band.`

Musical range:

`Top 40 • Motown • country • classic rock • pop`

Optional single link:

`VISIT GREENWAYBAND.COM`

### Contact

Section label:

`CONTACT`

Headline:

`Get in touch.`

Keep Adrian's existing email, phone number, personal Instagram, and Greenway Instagram. Email remains the strongest visual action.

### Footer disclosure

`Full-band footage features Adrian Michael & The Greenway Band, Adrian's Houston-based band.`

## Remove from the first release

- Separate solo and vocalist pages
- The “two ways to book Adrian” section
- The 31-second `Neon Moon` video as a separate section
- The standalone Big Spring Ranch video
- The testimonial video
- The full repertoire grid
- The `400+ songs` claim
- The “View full song list” CTA
- The five-item proof strip
- Long third-person biography copy
- Repeated references to acoustic guitar
- Any language implying Adrian has a Boston full-band lineup

Do not delete source media merely because it is removed from the page. Preserve it outside the rendered buyer journey unless Adrian separately authorizes deletion.

## Reel direction

The primary reel must be 50 to 60 seconds.

It should:

1. Begin immediately with Adrian's strongest clear vocal moment.
2. Show lead vocals, crowd connection, range, and at least one moment that demonstrates he can work inside a band.
3. Use fewer, longer, cleaner moments instead of rapid or awkward cutting.
4. Avoid redundant clips that prove the same thing.
5. End on a strong musical or crowd-response moment.

Do not invent a new cut order in Phase 1. If Adrian has not supplied an approved final reel or exact timestamps, use the existing reel only as a clearly temporary draft asset and list the final reel as an open launch blocker.

Use the final Vimeo reel when Adrian supplies its link. If the draft must temporarily use a local MP4, retain a poster-first experience and do not present that draft asset as production-ready.

## Email card

Replace the two lane-specific email cards with one universal 1200×675 card that links to the canonical Adrian page.

Preserve the premium visual style of the existing cards. Keep the text minimal:

`ADRIAN MICHAEL`

`BOSTON VOCALIST & LIVE PERFORMER`

`WATCH THE LIVE REEL`

Use the strongest live vocalist image, not an image that makes the page look exclusively acoustic.

## Required technical corrections

1. Load the hero image eagerly and use `fetchpriority="high"`.
2. Keep below-the-fold images and posters lazy-loaded.
3. Correct the failed small-text color contrast identified in the audit.
4. Give mobile navigation and buttons comfortable tap targets of at least 44px.
5. Keep the poster visible until video playback can begin.
6. Add a concise loading state, playback error state, retry action, and direct fallback link.
7. Use the universal email card as the Open Graph image.
8. Keep the hero and main proof inside the page's main landmark.
9. Make the build reproducible without relying on a missing external `song-list/songs.json`.
10. Remove stale song-list build dependencies if the unified page no longer uses them.
11. Reconcile the media manifest, reel-building script, README, file names, reel duration, and final asset sizes.
12. Preserve direct email and phone links.

## Design guardrails

- Preserve the existing cream, black, photography, typography, spacing character, and premium restraint.
- Do not redesign the brand.
- Do not add gradients, badges, floating widgets, animations, carousels, accordions, forms, or decorative cards.
- Do not turn the page into a resume.
- Do not introduce generic sales copy.
- Do not add claims that are not supported by Adrian's footage or confirmed history.
- Prioritize a clean first screen, a large reel, and a fast contact path.

## Phase 2: QA and audit package

After Adrian approves and Phase 1 is complete:

1. Build from a clean state and record the exact build command and result.
2. Provide desktop and 390px mobile screenshots of the entire page.
3. Report full mobile page height and the vertical position where the reel and contact section begin.
4. Test the final reel on desktop Chrome, desktop Safari, iPhone Safari, and Android Chrome.
5. Test poster loading, play, pause, seeking, audio, fallback behavior, and a simulated media failure.
6. Run contrast, keyboard, focus, landmark, heading-order, and tap-target checks.
7. Confirm both retired child routes point safely to the canonical page.
8. Provide a sanitized changed-file list and diff summary.
9. Provide the final media manifest and note any temporary assets.
10. Provide a draft deployment URL only.

Stop after the Phase 2 package. Do not deploy to production.

## Acceptance criteria

The correction is ready for independent re-audit only when:

- A visitor sees one identity, not two lanes.
- The offer is clear within the first screen.
- The live reel is the dominant proof.
- `Email Adrian` appears immediately below the reel.
- The first release contains one video only.
- The page contains no unsupported solo repertoire or `400+ songs` implication.
- The page does not overemphasize acoustic guitar.
- The final 50- to 60-second reel is approved or clearly listed as the only remaining launch blocker.
- The page is materially shorter than the audited three-page version.
- The build is reproducible.
- The draft passes the required mobile, playback, accessibility, and route checks.
