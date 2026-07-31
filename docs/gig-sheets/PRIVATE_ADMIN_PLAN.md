# Private Gig Admin Portal

**Status:** STAGES 1-2 SHIPPED; STAGE 3A COMPLETE 2026-07-30; STAGE 3B APPROVED
**Size:** Large, three stages
**Owner:** Adrian
**Public musician site:** `https://gigs.greenwayband.com/<last-name>/<mm-dd-yy>/`
**Private admin site:** `https://gigadmin.greenwayband.com/`

## Objective

Give Adrian one private home page where he can find every deployed wedding by couple, date, or venue and open the Full Gig Sheet and MC Cue Sheet. Keep the musician-facing Band Sheet and Listening Room separate and easy to share.

## Current truth

- Matey's Band Sheet and Listening Room are live and safe to send.
- Matey's Full and MC pages are protected at `gigadmin.greenwayband.com`.
- The old public Full and MC routes return `404`.
- Public service-worker cache v22 excludes Full and MC and deletes the old
  private cache after a device reconnects.
- Matey is the only wedding on the shared dated-URL system. The read-only
  historical inventory found seven older weddings across nine Netlify sites.
  None has been migrated or changed.
- The permanent public source is `/Users/adrianjoseph/Desktop/greenway-gigs/`.

## Approved architecture

- Build the admin portal as a separate private static app, not inside the public marketing site and not inside the public gig hostname.
- Serve it at `gigadmin.greenwayband.com` behind a server-side Cloudflare Worker login. The Worker must authenticate Adrian before reading any private HTML, registry data, or asset.
- Allow only the username `adrian@greenwayband.com` with one long, random password stored in 1Password and as an encrypted Cloudflare Worker secret. Never store the password in source code, configuration, generated output, or documentation.
- Use a signed, HTTP-only, Secure, SameSite Strict browser cookie for a 12-hour session. Do not use a client-side password overlay.
- Host the private static files on an isolated origin with its public fallback hostname disabled. Cloudflare Workers Static Assets is the recommended first implementation.
- Use a generated wedding registry for version one. Do not add a database until Adrian wants browser-based editing or multiple administrators.
- Keep public musician URLs unchanged. The public landing page continues to expose only Band Sheet and Listening Room.
- Keep the Apple-inspired motif inside the protected admin origin. Public Gig
  Sheet, Band Sheet, and Listening Room pages remain on the locked Greenway
  palette with Bodoni Moda titles and Plus Jakarta Sans operational text.

## Visible product

The private home page uses the Apple-inspired Growth Hour motif: Apple system
fonts, a soft iOS-gray canvas, white rounded cards, and cobalt actions. It
includes:

1. Search by couple, date, or venue.
2. A newest-first list of weddings.
3. One private wedding record with Full and MC buttons.
4. Reference links to the public Band Sheet and Listening Room.
5. A clear sign-out control.

Default access experience: 1Password fills Adrian's username and password once, then a signed 12-hour browser session keeps the portal open until sign-out or expiry.

## Stage 1: protected shell

Build the empty admin app and generated registry structure in a separate project. Configure the Adrian-only Worker login, 1Password credential, password rotation path, custom hostname, and blocked origin fallback. Use sample records with no private wedding information for security testing.

**Gate:** an unauthenticated request cannot fetch the shell, registry, private HTML, or private assets through either the custom hostname or an origin hostname. Adrian can sign in using the `Greenway Gig Admin` login saved in 1Password, sign out immediately, and rotate both the password and all active sessions through his existing Cloudflare account.

Cloudflare DNS, Worker-secret activation, and the first production deployment remain explicit owner-approval actions.

**Stage 1 result, 2026-07-30:** PASS. The sample-only portal was deployed at `gigadmin.greenwayband.com`; HTTPS enforcement, anonymous blocking, the 1Password credential, 12-hour session, sign-out, response headers, unexpected-host rejection, generated search registry, desktop/phone layouts, and sample-only output passed. Worker version: `e06515d2-0c5c-4478-adf7-a1bdaf3818d0`. This gate cleared the separate Stage 2 migration.

## Stage 2: move Matey private pages

After Stage 1 passed:

- Copy Matey's Full and MC pages into the protected portal.
- Remove Full and MC from the public deployment source.
- Remove them from the public service worker's core cache.
- Make the old public Full and MC URLs return `404` or `403`.
- Keep the public landing, Band Sheet, Listening Room, audio, dated path, and old-link transitions working.

**Gate:** private content is available only after authentication, old public URLs fail closed, and the musician link works exactly as before.

**Stage 2 result, 2026-07-30:** PASS. Matey's Full and MC pages are protected
behind the live login; authenticated page refresh and MC cue controls passed.
All old public Full and MC routes return `404`, while Band, Listening, and all
three audio tracks still return `200`. Cache v22 excludes private pages and
retires the old cache after reconnect. The final local build and all 16 tests
passed. Active Worker version:
`fe4dbf64-e44b-4d45-84bd-4ade7e703e7e`; public deploy:
`6a6bec25536cce7c40933fe7`; admin commit: `a123ad3`.

## Stage 3: archive and future workflow

**Size:** Large. Split into three independently verified parts.

**Planning finding:** the current `create-gig-sheet` skill and
`GIG_SHEET_SYSTEM.md` still instruct future builds to place Full and MC files in
the public folder and cache them offline. That documentation is now unsafe and
must be corrected before the next new gig sheet. The public `netlify.toml`
comment is also stale, but its behavior is unchanged and it remains off limits.

### Stage 3A: read-only historical inventory

- Inspect the Netlify account, live routes, and any matching local source
  folders.
- Record each likely gig site once, including its live URL, event date when
  confirmed, page types, local-source location, and migration readiness.
- Keep client contacts, timelines, and other private facts out of the inventory.
- Do not edit, migrate, retire, or redeploy any older site.

**Gate:** every likely historical gig is classified or explicitly marked
uncertain, duplicate sites are grouped, and Adrian can approve migrations from
one clear list without any live change.

**Stage 3A result, 2026-07-30:** PASS. Seven historical weddings were confirmed
across nine live Netlify sites. Velek / Reinders has two full-site deployments;
Hawk / Clayton is split across Full and MC sites. Three weddings have usable
local source, while four need source recovery or reconciliation. Proposal and
unrelated event sites were excluded. No live site, source file, deployment, or
DNS record changed. The private evidence record is
`/Users/adrianjoseph/Desktop/greenway-gig-admin/docs/HISTORICAL_INVENTORY.md`.

### Stage 3B: dual-audience build workflow

- Update the Gig Sheet skill and system guide so public builds contain only the
  Greenway-styled landing, Band Sheet, Listening Room, manifest, service worker,
  and audio.
- Send Full and MC pages only to the protected admin project and add one
  generated archive record.
- Add checks for duplicate wedding IDs and paths, missing public or private
  pages, private files in the public folder, private service-worker entries, and
  removal of an existing wedding from a full-folder deploy.
- Prove the workflow with sample-only test data. Do not deploy the sample.

**Gate:** one sample build appears in local admin search, its public and private
links resolve to the correct local destination, the public output contains no
Full or MC page, and every failure check stops before deployment.

### Stage 3C: approved historical migrations

- Migrate only weddings Adrian approves from the Stage 3A inventory.
- Move one wedding at a time, deploy the protected copy first, then make the
  public copy safe.
- Verify the migrated wedding and every previously migrated wedding after each
  full-folder deployment.
- Retiring an old one-off Netlify site is a separate destructive action and
  always needs Adrian's explicit approval.

**Gate:** each approved wedding is searchable behind the admin login; its public
musician pages keep the Greenway look; its private pages cannot be fetched
anonymously; and no earlier wedding is removed or broken.

## Acceptance criteria

- Anonymous visitors cannot fetch private HTML, registry data, or private assets.
- Adrian can unlock the portal with the login saved in 1Password.
- Password replacement and full-session revocation work through the existing Cloudflare account.
- Search finds weddings by couple, date, and venue.
- Each wedding exposes protected Full and MC pages plus public Band and Listening references.
- New gig generation updates the archive automatically.
- `gigs.greenwayband.com/<last>/<date>/` remains the musician-facing address.
- Public musician pages keep the locked Greenway visual system. The
  Apple-inspired motif never reaches the public Gig Sheet, Band Sheet, or
  Listening Room.
- No Supabase, Stripe, Twilio, CRM, or marketing-site authentication code is introduced.

## Build scope

**Modify in Stage 3A:** one private inventory record plus project status docs.

**Modify in Stage 3B:** `.agents/skills/create-gig-sheet/SKILL.md`,
`docs/gig-sheets/GIG_SHEET_SYSTEM.md`, the example audience instructions, admin
registry/build validation and tests, and sample-only fixtures.

**Modify in Stage 3C:** only the approved wedding's protected admin folder,
archive record, and shared public source folder. Older wedding sites remain
read-only until the inventory is reviewed and each migration is approved.

**Read only:** this plan, `docs/CURRENT_STATE.md`, D17-D20, the current public deployment configuration, and Cloudflare's current Workers secrets and Web Crypto documentation.

**Off limits:** the paused Astro marketing rebuild, `netlify.toml`, Growth Hour, Command Center CRM, proposal sites, older wedding sites before the Stage 3 inventory, and all unrelated working-tree changes.

## Security references

- Cloudflare Workers secrets: `https://developers.cloudflare.com/workers/configuration/secrets/`
- Cloudflare Workers Web Crypto: `https://developers.cloudflare.com/workers/runtime-apis/web-crypto/`
- Cloudflare Workers Static Assets pricing: `https://developers.cloudflare.com/workers/platform/pricing/`
