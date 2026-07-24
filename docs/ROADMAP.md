# ROADMAP: The Greenway Band Website

The plan, split by when. Claude Code: update statuses when items ship. New ideas from Adrian go into Later unless he says otherwise.

Statuses: PLANNED, APPROVED (plan exists), IN PROGRESS, SHIPPED, DEFERRED, PAUSED

**Note on sequencing:** the Astro rebuild items below are PAUSED at the project level per the 2026-07-03 cross-project decision (see `CURRENT_STATE.md` "Active task"). Nothing there is urgent until Adrian lifts the pause. The **Squarespace lead-form embed** (below) is the one exception — it's a separate, unblocked track per `WEBSITE_PLAN_2026-07-03.md` and moves independently of the pause.

## In progress (unblocked — not part of the Astro pause)
| Item | Size | Status | Depends on | Done means |
|---|---|---|---|---|
| Squarespace lead-form embed (Gates 0-3) | S | Gates 0-2 SHIPPED 2026-07-03; Gate 3 PLANNED | Adrian's explicit "go" | Gates 0-2 done: v3 premium-dark embed live and dark at `greenwayband.com/inquiry-test`, real phone test confirmed landing correctly in Growth Hour Contacts. Gate 3 (actually going live — publish or link from the real Book page) needs Adrian's explicit "go," plus a same-day and one-week-later canary check. |

## Proposals track (independent of all holds)
| Item | Size | Status | Depends on | Done means |
|---|---|---|---|---|
| Proposal template upgrade: photos + embedded video + CTA | M | SHIPPED 2026-07-23 | — | Built, locally verified (see spec below + CURRENT_STATE.md). Applies to every new proposal build automatically; hinojosa was redeployed live 2026-07-24 with the full v5-v9 upgrade. |
| Template v2: hybrid palette + self-hosted video | S/M | SHIPPED 2026-07-23 | — | Built + locally verified same day as v1. Palette locked "C" (hybrid) after a 3-judge panel voted unanimously, strong confidence. Video is now self-hosted, no Vimeo, no watermark. Venue strip built then removed at Adrian's call. See CURRENT_STATE.md for the verified summary. |
| Template v4: whole-frame photos | S | SHIPPED 2026-07-23 | — | Committed `a7884bd`. Photo bands show the whole frame on wide screens, immersive crop kept on phones. All 3 items from the v3 Hinojosa review closed. |
| Template v5: dedicated print/PDF layout | M | SHIPPED 2026-07-24 (committed with v6-v8) | Adrian's ChatGPT brief | Paginated `@media print` layout (8 Letter pages after v6's cocktail page), crowd photo capped at every width, a phone-specificity CSS bug fixed. See D14 v5 in DECISIONS.md. |
| Template v6: ChatGPT correction pass | M | Partially kept; superseded by v7/v8 | — | 14-item brief executed verbatim; Adrian rejected the package/closing changes ("I'm not liking these changes"). v7 rolled those back; the approved improvements (video click-to-play, clickable contacts, contrast floors, cocktail print page) survive. See D14 v6/v7. |
| Template v7+v8+v9: strict-spec rollback, 10pc-first comparison grid, copy settled | M | SHIPPED + LIVE 2026-07-24 | — | v7: original per-package itemization + Schedule-a-Call-primary closing restored, subtitles → one benefit sentence. v8: 10-Piece always leads Recommended, desktop side-by-side comparison cards, video section trimmed to label + player + caption. v9: no payment/terms copy on the page (the only cut Adrian wanted), established helper lines and "Two Ways to Fill the Room" kept verbatim. Committed + pushed (website repo); hinojosa production-deployed and verified live at `proposals.greenwayband.com/hinojosa` (proposals repo `59716b4`, rollback `6a569f09a251fd14726df077`). See D14 v7-v9. |
| Template v10: third photo band (sparkler exit) before closing | S | BUILT, pending Adrian's review | Adrian's own photos | A real gig photo (his, confirmed) as a new default photo-band-3 right before the closing, screen-only (PDF untouched). Devil's-advocate review kept it to exactly one photo, not the color duplicate or the greenhouse shot. See D14 v10. |
| Template v11: crowd photo paired with the greenhouse walk-in | S | BUILT, pending Adrian's review | Adrian's pairing idea | The greenhouse photo returns, side by side with the existing crowd photo (Adrian's own idea), screen-only — print keeps the original single crowd band via a hidden twin. See D14 v11. |

**v2, as shipped (2026-07-23, second Fable session):**
- **Palette (Adrian's "C", hybrid):** cover + closing keep the exact dark palette (byte-identical to every proposal shipped before today — the cover is the first-impression unit during the ~30-day old/new coexistence window). Document body (everything between) uses the website design system's own tokens: bg `#F5F2ED`, ink `#0A0A09`, secondary `#706D66` / `#4A4740`. Implementation: `:root` holds the cream values, `.cover, .closing` scope-override back to the original dark values.
- **All 8 judge-panel tweaks shipped:** solid-fill closing CTA (not outline); cream hairlines strengthened to ink at 12/16/26% alpha; hard-edge photo/cream seams (only band-1's top blends into the dark cover); video frame + play button hardcoded dark-plate colors regardless of section; crowd photo + video plate are the only two dark elements inside the cream body.
- **Self-hosted video (no Vimeo):** Adrian's own line — "if we're going to be premium, let's be premium," plus Vimeo Plus can't remove its logo from embeds. Source `~/Desktop/uptown_funk_v1 (1080p).mp4` (1080p, 259.8s, 177MB), encoded with ffmpeg to 720p H.264 ~2.1Mbps + AAC 128k + faststart → `~/Desktop/greenway-proposals/assets/uptown-funk-2026a.mp4` (73MB). Template's video block is a native `<video>` swapped in on click (verified `readyState: 4`, plays, correct src, no console errors). Vimeo master stays up unlisted, Adrian's own reference only.
- **Venue strip: built, then removed same day.** Adrian: "maybe we just skip the venues, I don't think it adds much value." Not re-added; see D14 v2 note in DECISIONS.md if this comes up again.

**Spec (locked 2026-07-23 after mockup + 15-agent stress test; mockup at the session scratchpad `mockup/index.html`, stress-test findings in that session's transcript):**
- **Adrian's inputs, all received:** video = Vimeo `https://vimeo.com/1129682149` ("Uptown Funk", 4:20, 720p, his account, embeddable — verified via oEmbed); photo/video reuse rights confirmed by Adrian 2026-07-23 (band's client contract grants reuse of gig media — see D14); venue strip + hours line approved.
- **Modify:** `docs/proposals/TEMPLATE.html`, `docs/proposals/PRICING_AND_CONTENT.md`, `.claude/skills/create-proposal/SKILL.md`, plus new shared `~/Desktop/greenway-proposals/assets/` (versioned filenames, one copy shared by all proposals). **Read only:** `docs/CONTENT_AND_MESSAGING.md`, `docs/proposals/EMAIL_TEMPLATES.md` (email is unchanged — it already carries the scheduler link). **Off limits:** this repo's `netlify.toml`, `src/`, all existing live proposal folders.
- **Template additions (port additively — keep every existing CSS rule, unlike the mockup which dropped a few):**
  1. Photo band after cover: `assets/band-stage-2026a.webp` (from `public/images/experience/20230311Preview0069.webp`), `loading="eager"`, `object-position: 50% 62%`, height capped ~640px on desktop.
  2. Video section after event details, before packages: self-hosted poster `assets/uptown-funk-poster-2026a.jpg` (the Vimeo thumbnail — shows the full band on stage), click-to-load swap to `https://player.vimeo.com/video/1129682149?autoplay=1` iframe (no third-party JS). Play button: ~60px, 0.5px ring, no backdrop blur. Copy: desc "Photos only say so much. Here's a full song, live." / caption "Uptown Funk · Recorded live" (caption must stay honest to the asset — it is one song, never claim a full set). The old bride close-up poster idea is RETIRED (brand finding: band invisible, play button on her face); `IMG_0668.webp` stays in the pool, unplaced.
  3. Crowd photo band (`assets/crowd-2026a.webp` from `_JHZ1145.webp`) before testimonials, `object-position: 50% 30%` (hides the videographer rig at the bottom), plus a section-divider between photo and testimonials (avoids implying the pictured guests wrote the quotes).
  4. Venue strip: micro-caps label "Where we've played" + middot-separated names from the 13-approved list ONLY. Default six (assumption, Adrian may swap): River Oaks Country Club · Houston Country Club · Post Oak Hotel · The Houstonian · The Astorian · The Grand Galvez.
  5. Hours line appended to the package note: "Three hours of live music across a four hour reception." (contract standard already documented in PRICING_AND_CONTENT.md).
  6. CTAs: quiet inline link after the cocktail block ("Want to talk through your options? Schedule a call." — `white-space: nowrap` on the anchor) + closing bordered button "Schedule a Call", both to the 17hats scheduler URL; one plain line above the button: "On the call we'll walk through the options and how to hold your date." Phone number becomes `tel:+12814671226`.
- **Docs:** PRICING_AND_CONTENT.md gains an "Approved media pool" section (the 3 photos + the Vimeo URL + poster file, usage rights note, video-honesty rule) and the two new approved copy lines. SKILL.md: media + CTA become defaults on every wedding proposal; build gate adds "video URL is real and returns 200 via oEmbed" and "all referenced /assets/ files exist in the deploy folder" alongside the existing `grep '{{'` check.
- **Verify:** grep tokens = 0, all links checked, desktop + phone-width render pass. 2026-07-24: hinojosa redeployed live and verified on the real domain (HTTP 200, correct content); every other existing proposal page untouched.

## Now (Astro reconciliation hygiene — paused, optional, do only if Adrian asks)
| Item | Size | Status | Depends on | Done means |
|---|---|---|---|---|
| Reconcile `dev` vs `main` and the uncommitted April work | S | PLANNED | Owner approval to commit/push | Either `main`'s Reviews/FAQ are merged into the deploy branch, or the working-tree April work on `dev` is committed and pushed. One canonical branch going forward. |
| Decide the staging self-redirect | S | PLANNED | Owner approval | `netlify.toml`'s netlify.app→greenwayband.com redirect is either removed (so staging shows the new build) or explicitly kept, with the tradeoff stated to Adrian. |
| Confirm the Netlify deploy branch in the dashboard | S | PLANNED | none | Netlify UI confirms which branch actually deploys (inferred to be `dev`, unverified). |

## Next (real content — blocked on Adrian)
| Item | Size | Status | Depends on | Done means |
|---|---|---|---|---|
| Reviews content | S | PLANNED | Adrian supplies real testimonials | The 3 "Review coming soon" placeholders are replaced with real, attributed reviews. Copy-integrity rule applies. |
| Hero media | S | PLANNED | Adrian supplies video/photo | The homepage hero's solid-color placeholder is replaced with the real hero video or a poster image; the `WhyGreenway` media placeholder is filled. |
| Experience "For Planners" detail | S | PLANNED | Adrian supplies production detail | The placeholder paragraph is expanded with real detail (Ableton-driven arrangements, MIDI-synced production, etc). |
| Vocalist Showcase page | M | PLANNED | Adrian supplies content | `src/pages/vocalists.astro` is built and added to nav; `site.ts`'s `Vocalists` flag flips to `true`. |

## Later
- **FAQ AI assistant:** decide whether to build the originally-planned AI assistant shell for the FAQ page, or keep the static accordion as the final v1. No artifact of a prior plan exists in this repo; ask Adrian if it's still wanted.
- **Wire the `published` flag:** optional refactor to drive the header nav from `site.ts`'s `pages[]` and add a 404 guard for unpublished routes, so publishing becomes a one-line toggle instead of editing `Header.astro` by hand.
- **Minor cleanups:** remove dead `LogoInline.astro` / `LogoMonument.astro`; drop the overridden boxed `.book-form__input` rule in `global.css`; replace `#ffffff` button-hover states and the `Logo.astro` off-token gray with palette tokens.
- **Launch:** flip the Cloudflare A record for `greenwayband.com` from Squarespace to Netlify (reversible in minutes). Coordinate with the staging-redirect decision above. Not imminent — see the pause note at the top of this file.

## Not planned
Things considered and rejected, or intentionally out of scope, so they don't get re-litigated.
- A CMS, auth, e-commerce, or an on-site booking calendar. This is a static marketing site; the only conversion action is the Book inquiry form.
- Any Supabase, Stripe, or Twilio code in this repo. Those belong to the separate Command Center CRM.
- Any additional or competing lead-intake mechanism beyond the one Squarespace embed above and the existing `BookForm.astro` → Command Center path. Growth Hour owns lead intake going forward; don't build a third path.
