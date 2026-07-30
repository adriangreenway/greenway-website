# Private Gig Admin Portal

**Status:** APPROVED 2026-07-30
**Size:** Large, three stages
**Owner:** Adrian
**Public musician site:** `https://gigs.greenwayband.com/<last-name>/<mm-dd-yy>/`
**Private admin site:** `https://gigadmin.greenwayband.com/`

## Objective

Give Adrian one private home page where he can find every deployed wedding by couple, date, or venue and open the Full Gig Sheet and MC Cue Sheet. Keep the musician-facing Band Sheet and Listening Room separate and easy to share.

## Current truth

- Matey's Band Sheet and Listening Room are live and safe to send.
- Matey's Full and MC pages are unlinked, but unlinked is not secure. Anyone with those URLs can currently fetch them.
- The public service worker currently includes the Full and MC pages in its offline cache.
- Matey is the only wedding on the shared dated-URL system. Older weddings remain on separate Netlify sites and need an inventory before migration.
- The permanent public source is `/Users/adrianjoseph/Desktop/greenway-gigs/`.

## Approved architecture

- Build the admin portal as a separate private static app, not inside the public marketing site and not inside the public gig hostname.
- Serve it at `gigadmin.greenwayband.com` behind Cloudflare Access. Access must be checked before any private HTML or asset is served.
- Allow only `adrian@greenwayband.com`.
- Require a WebAuthn biometric check so Safari can use iPhone Face ID. Keep email-based account recovery and re-enrollment available. Do not use a shared password or a client-side password overlay.
- Host the private static files on an isolated origin with its public fallback hostname disabled. Cloudflare Workers Static Assets is the recommended first implementation.
- Use a generated wedding registry for version one. Do not add a database until Adrian wants browser-based editing or multiple administrators.
- Keep public musician URLs unchanged. The public landing page continues to expose only Band Sheet and Listening Room.

## Visible product

The private home page is white/cream Greenway styling and includes:

1. Search by couple, date, or venue.
2. A newest-first list of weddings.
3. One private wedding record with Full and MC buttons.
4. Reference links to the public Band Sheet and Listening Room.
5. A clear sign-out control.

Default access experience: Adrian unlocks once per browser session, then moves through the portal without repeated Face ID prompts. The exact session length is selected during Stage 1 verification.

## Stage 1: protected shell

Build the empty admin app and generated registry structure in a separate project. Configure the Adrian-only Cloudflare Access policy, Face ID/WebAuthn requirement, recovery path, custom hostname, and blocked origin fallback. Use sample records with no private wedding information for security testing.

**Gate:** an unauthenticated request cannot fetch the shell, registry, HTML, or assets through either the custom hostname or an origin hostname. Adrian can unlock it with Face ID on iPhone and can recover access through his verified email.

Cloudflare DNS, Access policy activation, and the first production deployment remain explicit owner-approval actions.

## Stage 2: move Matey private pages

After Stage 1 passes:

- Copy Matey's Full and MC pages into the protected portal.
- Remove Full and MC from the public deployment source.
- Remove them from the public service worker's core cache.
- Make the old public Full and MC URLs return `404` or `403`.
- Keep the public landing, Band Sheet, Listening Room, audio, dated path, and old-link transitions working.

**Gate:** private content is available only after authentication, old public URLs fail closed, and the musician link works exactly as before.

## Stage 3: archive and future workflow

- Inventory older one-off gig sites without changing them.
- Add each approved historical wedding to the generated registry.
- Update the gig-sheet generator so every new deployment publishes public pages to the musician site, private pages to the admin site, and one metadata record to the archive.
- Add duplicate-path and missing-file checks before either deployment.

**Gate:** a new test wedding appears in search automatically, every link resolves to the correct audience, and a partial deploy cannot remove another wedding.

## Acceptance criteria

- Anonymous visitors cannot fetch private HTML, registry data, or private assets.
- Adrian can unlock the portal with Face ID on his iPhone.
- Recovery works without a shared password.
- Search finds weddings by couple, date, and venue.
- Each wedding exposes protected Full and MC pages plus public Band and Listening references.
- New gig generation updates the archive automatically.
- `gigs.greenwayband.com/<last>/<date>/` remains the musician-facing address.
- No Supabase, Stripe, Twilio, CRM, or marketing-site authentication code is introduced.

## Build scope

**Modify in the fresh session:** a new isolated admin project; Cloudflare configuration only after explicit approval; the public gig source only in Stage 2; gig-sheet generation instructions only in Stage 3.

**Read only:** this plan, `docs/CURRENT_STATE.md`, D17-D20, the current public deployment configuration, and Cloudflare's current Access/WebAuthn documentation.

**Off limits:** the paused Astro marketing rebuild, `netlify.toml`, Growth Hour, Command Center CRM, proposal sites, older wedding sites before the Stage 3 inventory, and all unrelated working-tree changes.

## Security references

- Apple passkeys and Face ID: `https://support.apple.com/en-ie/guide/iphone/iphf538ea8d0/ios`
- Cloudflare Access independent MFA/WebAuthn: `https://developers.cloudflare.com/cloudflare-one/access-controls/access-settings/independent-mfa/`
- Cloudflare Access request authorization: `https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/`
- Cloudflare Workers Static Assets pricing: `https://developers.cloudflare.com/workers/platform/pricing/`
