# Gig-sheet live clock: the shared memory (Netlify Function)

Canonical copy of the one function behind the live clock
(`docs/gig-sheets/LIVE_CLOCK_PLAN.md`). The deploy folder
`~/Desktop/greenway-gigs/` is not a git repo, so this folder is the versioned
source; copy from here when shipping.

## What it is

`clock.mjs` keeps one small record per wedding in Netlify Blobs (store
`gig-clock`, key = the wedding path like `/hess/10-03-26/`): which schedule row
Adrian marked as "now", when, and when it was set. Band phones `GET` it every
30 s on the wedding day; only a `POST` carrying the key can change it.

The key is the Netlify site env var `GIG_CLOCK_KEY` on the `greenway-gigs`
site, also saved in 1Password as `Greenway Gig Clock Key`. It is never written
into any file. Adrian's phone learns it once by opening any sheet with
`#clock=<key>` on the end of the address (the page stores it and strips it).

## Ship steps (done 2026-10-02 with Hess, prod deploy `6ac055e08a5287db91f91756`; kept for a rebuild of the folder)

The function is site-wide: a new wedding needs only the page markup (GIG_SHEET_SYSTEM.md, Live clock). Nothing here repeats per wedding.

1. Copy `clock.mjs` and `package.json` to `~/Desktop/greenway-gigs/.functions/`
   and run `npm install` there. The dot in `.functions` matters: the Netlify
   CLI skips dot-folders and `node_modules` when it uploads `--dir .`, so the
   function source and its packages never become public files.
2. Add to `~/Desktop/greenway-gigs/netlify.toml` (owner-approved change):

   ```toml
   [functions]
     directory = ".functions"
     node_bundler = "esbuild"
   ```

3. Draft deploy first, from inside the folder, no `--prod`:
   `netlify deploy --dir . --site 8205364b-6929-454b-bfe0-51afaeb02636`.
   Read the upload count, confirm `/.functions/clock.mjs` 404s on the draft URL
   and `/.netlify/functions/clock?w=/example/01-01-26/` returns `{}`.
4. Then the normal whole-folder production deploy with the two-way live diff
   (GIG_SHEET_SYSTEM.md, "Critical deploy hazard").

Proven on draft deploy `6ac04d60ce01f17b0446ee3c` (2026-10-02): "Finished hashing 2 files and 1 functions", source files 404, function 200/400/401/405/413 as designed, a keyless phone picked up a stored tap.

## Rotate the key

Generate a new value into the 1Password item (`Greenway Dev` vault), then set it
on Netlify with the value never printed:

```bash
NETLIFY_SITE_ID=8205364b-6929-454b-bfe0-51afaeb02636 netlify env:set GIG_CLOCK_KEY "$(op read 'op://Greenway Dev/Greenway Gig Clock Key/password')" --secret --context production --context deploy-preview --context branch-deploy
```

Learned 2026-10-02: `env:set` has no `--site` flag (use `NETLIFY_SITE_ID`), a
`--secret` value needs explicit non-dev `--context`s, and the function only sees
a new or changed value after the next deploy, so rotate, then redeploy the whole
gigs folder, then have Adrian open a sheet once with the new `#clock=<key>`. Any
phone holding the old key is locked out from that deploy on.
