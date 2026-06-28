# INTEGRATIONS

**Last verified: 2026-06-27.** This file lists external touchpoints and **secret LOCATIONS only —
never secret values.**

## 1. Book form → CRM `lead-intake` (the only backend touchpoint)
- **Where:** `src/components/BookForm.astro` (`<script>` submit handler).
- **Endpoint:** `POST https://command.greenwayband.com/.netlify/functions/lead-intake`
- **Body:** JSON. Field → key mapping (verified):

  | Form field | JSON key | Required | Notes |
  |---|---|---|---|
  | Your name | `partner1_name` | ✅ | |
  | Partner's name | `partner2_name` | | |
  | Email | `email` | ✅ | regex-validated client-side |
  | Phone | `phone` | | |
  | Event date | `event_date` | ✅ | `YYYY-MM-DD` (HTML `type="date"`) |
  | Venue (if known) | `venue` | | |
  | Estimated guest count | `guest_count` | | range string, e.g. `100-150` |
  | How did you hear about us? | `referral_source` | | select |
  | *(hidden honeypot)* | `_gotcha` | | must be empty; sent as `''` |

- **Spam trap:** a visually hidden `_gotcha` input. If filled, the form shows a fake success and
  does **not** POST.
- **UX:** client validation for the 3 required fields; on success the form fades out and a
  "Thank you" confirmation fades in; on network error it shows an inline retry message pointing to
  `adrian@greenwayband.com`.
- **No secrets** are used by the form — it's an unauthenticated public POST to the CRM function.
  Any auth/validation/storage happens server-side in the **separate** CRM repo (`greenway-crm`),
  not here.

## 2. Netlify (hosting)
- **Site id:** `57df0a8e-c32d-4954-9507-f9f3b1f90e53` (in `.netlify/state.json`, gitignored).
- **Build:** `npm run build`, publish `dist` (`netlify.toml`).
- **Deploy branch:** **`dev`** (strong inference — the live redirect rule exists only on `dev`;
  confirm in the Netlify UI). **UNKNOWN / to verify** via the Netlify dashboard.
- **Redirect (active):** `netlify.toml` 301-redirects `https://greenway-website.netlify.app/*` →
  `https://greenwayband.com/:splat` (`force = true`). Because production is still Squarespace,
  this currently sends staging traffic to the old site (see docs/PROJECT_STATE.md).
- **Security headers** (`netlify.toml`): `X-Frame-Options: DENY`, `X-Content-Type-Options:
  nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`.

## 3. Cloudflare (DNS — read-only context; DO NOT change without approval)
- **Zone id:** `bcd1a65100066b5e6f2190afc77fd8e9`
- **Account id:** `fe59812014feb92ff5a43ea304b16e58`
- **Nameservers:** carter / coraline.
- **Records (as recorded):** `A` records → Squarespace; `command` subdomain `CNAME` → the CRM's
  Netlify site; `MX` → Google Workspace.
- **Launch** = flip the `greenwayband.com` A record from Squarespace to Netlify (reversible in
  minutes). Owner-approved action only.

## 4. Fonts (Fontsource, build-time)
- `@fontsource-variable/bodoni-moda` and `@fontsource/plus-jakarta-sans` (300/400/500/600),
  imported in `BaseLayout.astro`. Self-hosted at build; no external CDN call.

## Secrets / env
- **No environment variables are referenced anywhere** in `src/` or config (verified by grep for
  `import.meta.env` / `process.env` / `PUBLIC_`). Therefore **no `.env.example` is needed** for
  this repo today. `.gitignore` excludes `.env*` defensively.
- Secret *locations* that exist but hold no site secrets: `.netlify/state.json` (site id only,
  gitignored). Any real secrets (Supabase, etc.) live in the **separate CRM project**, not here.

## Boundary reminder
The website shares only a Supabase **database** (used by the CRM, not the site) and the Cloudflare
**DNS zone** with the Command Center CRM and the personal "Kai" app. Do not import code from or
into those projects.
