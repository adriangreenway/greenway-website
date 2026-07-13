# Proposal System — proposals.greenwayband.com

Per-client proposal microsites. One folder per client, deployed as static pages to the
Netlify site `greenway-proposals`. This is a **third track**, independent of the Astro
rebuild, the Squarespace embed, and the greenwayband.com go-live hold. Deploying a
proposal touches nothing on greenwayband.com.

Last verified: 2026-07-13.

## Where things live

| What | Where | Notes |
|---|---|---|
| **Deploy source (canonical)** | `~/Desktop/greenway-proposals/` | Its own git repo. THE directory. |
| Stale trap — never use | `~/greenway-proposals/` | Frozen ~Apr 2026, missing proposals. Deploying it would wipe live pages. |
| Stale trap — never use | this repo's `public/proposals/` | Legacy remnant (one old copy of ally-byrne). Proposals do NOT ship with the Astro site. |
| Template | `docs/proposals/TEMPLATE.html` (this repo) | Wedding template, garcia-generation design. |
| Pricing + approved content | `docs/proposals/PRICING_AND_CONTENT.md` | Real observed prices, testimonial pool, copy rules. |
| Workflow skill | `.claude/skills/create-proposal/SKILL.md` | The end-to-end runbook. |

The deploy folder also holds non-proposal pages (`brand-guide`, `brand-guide-v2`,
`social-direction`, …). **Every deploy publishes the entire folder**, so anything new
sitting in it rides along. Always list ride-alongs in the pre-deploy summary to Adrian.

## Netlify facts

- Site name `greenway-proposals`, production URL `https://proposals.greenwayband.com`
- Site ID `c6041c94-c26c-4ab8-ae5f-96c43addb081`, account ID `6998e8045f88f2bba5524bf7`
- **Not linked to GitHub.** No build hooks. `git push` deploys nothing. CLI deploys only.
- DNS for the subdomain already exists in Cloudflare. Never touch DNS for proposals.
- Auth: `op read 'op://Greenway Dev/Netlify Personal Access Token/credential'`
  (1Password CLI is signed in as adrian@greenwayband.com; `op read` occasionally
  returns empty on first call — check token length and retry once).

## Deploy runbook

1. **Pre-deploy safety diff.** A `--prod` deploy replaces the whole site atomically.
   Confirm local is a superset of live and see exactly what will change:
   ```bash
   export NETLIFY_AUTH_TOKEN=$(op read 'op://Greenway Dev/Netlify Personal Access Token/credential')
   SITE=c6041c94-c26c-4ab8-ae5f-96c43addb081
   DEPLOY_ID=$(curl -s -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN" \
     "https://api.netlify.com/api/v1/sites/$SITE" \
     | python3 -c "import sys,json;print(json.load(sys.stdin)['published_deploy']['id'])")
   curl -s -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN" \
     "https://api.netlify.com/api/v1/deploys/$DEPLOY_ID/files" \
     | python3 -c "import sys,json;[print(f['path']) for f in json.load(sys.stdin)]" | sort
   ```
   Compare against `ls ~/Desktop/greenway-proposals`. Anything live but missing
   locally = STOP and investigate. Note the `DEPLOY_ID` — it is the rollback point.
2. **Deploy** (from the folder itself — never from a directory containing another
   `netlify.toml`, or the CLI runs that project's build):
   ```bash
   cd ~/Desktop/greenway-proposals
   netlify deploy --prod --dir ~/Desktop/greenway-proposals \
     --site c6041c94-c26c-4ab8-ae5f-96c43addb081 \
     --message "Add proposal: <slug>"
   ```
   (`--site` is required: this folder's `.netlify/state.json` is empty.)
3. **Check the output.** "CDN requesting N files" must equal the number of files you
   added/changed. N too big = something unexpected is shipping; investigate before
   telling Adrian it's done.
4. **Verify live.** `curl -sL https://proposals.greenwayband.com/<slug>` → HTTP 200 +
   correct `<title>`. Spot-check two existing proposals still return 200.
   Never curl a slug **before** deploying — the site serves
   `Cache-Control: max-age=3600`, so a pre-deploy 404 can get cached at the edge.
5. **Commit** in `~/Desktop/greenway-proposals` (its own repo): `Add proposal: <slug>`.

## Revisions and rollback

- Revising a sent proposal: overwrite the same `<slug>/index.html`, redeploy. URL
  stays valid for the client. Client browsers may show the old version for up to
  1 hour (`max-age=3600`).
- Rollback: every deploy is kept. Re-publish the previous deploy in the Netlify UI
  (app.netlify.com → greenway-proposals → Deploys), or redeploy the folder from git.

## Slug convention

Lowercase last name (`garcia`, `thompson`, `bielitz`). First-last if ambiguous or a
collision (`ally-byrne`, `ashley-eastin`). Hyphenated org name for corporate
(`the-united-way`, `opengroup`). Content lives at `<slug>/index.html`; the URL is
`proposals.greenwayband.com/<slug>`.
