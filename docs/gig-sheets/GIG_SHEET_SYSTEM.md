# Gig Sheet System

Per-wedding offline microsites for gig day: what the band needs, what the emcee/DJ
needs, and (when practice tracks exist) a Listening Room for the band to learn
live songs. This is a **separate track** from proposals, the Astro rebuild, and
the Squarespace embed. Deploying a gig sheet touches nothing else.

Last verified: 2026-07-21.

## Where things live

| What | Where | Notes |
|---|---|---|
| Deploy source | a scratch folder you build fresh each time (e.g. this session's scratchpad) | Not git-tracked. Each gig sheet is its own throwaway Netlify site, not a shared repo. |
| Reference example | `docs/gig-sheets/EXAMPLE/` (this repo) | Most recent full-featured build (Ditta/Johnson). Copy and adapt — see its README. |
| Workflow skill | `.claude/skills/create-gig-sheet/SKILL.md` | The end-to-end runbook. |
| Source material | Gmail (search + `get_thread` FULL_CONTENT), plus any timeline/questionnaire PDFs Adrian attaches | Never the sole source — cross-check both. |

There is no shared "gig-sheets" Netlify site. Each wedding gets its **own** Netlify
site, created fresh the first time you deploy it.

## Netlify facts

- Account: "Proposal Landing Page" (same Netlify account as `greenway-proposals`,
  but each gig sheet is its own separate site, not a folder inside that site).
- No 1Password token needed — the Netlify CLI already has stored auth on this
  machine. Just run `netlify deploy`.
- Site naming, current convention: `greenway-<lastname>` (e.g. `greenway-dass`,
  `greenway-ditta`). Two lastnames if there's a collision risk
  (`greenway-kaylynn-cameron`, `greenway-lutz-provenza`). Older sites used
  `{mon}-{day}-{venue}` (e.g. `apr-11-woodlands`, `mar-21-galvez`) — don't reuse
  that pattern for new sites, but recognize it if Adrian references an old one.
- Production URL is always `https://<site-name>.netlify.app` — there is no custom
  domain for gig sheets.

## Build + deploy runbook

1. **Check for an existing site first.** `netlify sites:list | grep -i <lastname>`.
   If a site already exists for this couple, you're revising it — deploy to that
   site ID, don't create a second one.
2. **Build the pages** in a scratch folder (see the create-gig-sheet skill for what
   goes in each page). Structure: `index.html`, `gig.html`, `band.html`, `mc.html`
   (if there's a separate MC/DJ), `listen.html` (if there are practice tracks),
   `manifest.json`, `sw.js`. `sw.js`'s `CORE` array must list every page you're
   shipping, or that page breaks offline.
3. **First deploy for a new couple** — creates the site:
   ```bash
   netlify deploy --prod --dir <scratch-folder> --site greenway-<lastname>
   ```
   Netlify will create the site with that name if it doesn't exist. Confirm the
   name it actually gave you (Netlify may append characters if the exact name is
   taken) and record the site ID for later revisions.
4. **Revisions** — always deploy by site ID, not by name, once you know it:
   ```bash
   netlify deploy --prod --dir <scratch-folder> --site <site-id>
   ```
5. **Verify live.** `curl -s https://<site-name>.netlify.app/<page> | grep -c "<fact you just added>"`
   for every page you touched. For anything visual (new player controls, layout),
   open it in the Browser pane and check it directly — don't just curl.
6. **Audio files.** If you're adding a practice track, convert it to MP3 first
   (`ffmpeg -i input.wav -codec:a libmp3lame -b:a 192k output.mp3`) — raw WAVs from
   Ableton are 50MB+ and slow to load on a phone at the venue. Only include songs
   the band actually plays live (see the skill's LIVE vs TRACK rule) — never a
   track a DJ/emcee vendor is covering.
7. **After a meaningful build or revision**, pull the live pages back down into
   `docs/gig-sheets/EXAMPLE/` if this one is now the most complete example (more
   pages, a new feature like seek controls) — that keeps the reference current for
   next time, since these sites aren't git-tracked anywhere else.

## Naming and slugs

Lowercase last name of the couple, or both if there's a collision
(`greenway-lutz-provenza`). No date or venue in the name — the header inside the
pages carries the date; the URL should stay simple.
