# The Greenway Band — Website

The public marketing website for **The Greenway Band**, a premium Houston live wedding/event
band. Built with [Astro](https://astro.build) as a static site, hosted on Netlify with DNS on
Cloudflare.

This repo is the **public site only**. It is intentionally separate from the band's CRM
("Command Center") and other internal apps — see
[docs/INTEGRATIONS.md](docs/INTEGRATIONS.md) and the boundary note in
[CLAUDE.md](CLAUDE.md).

## Requirements
- **Node** `>=22.12.0` (see `package.json` `engines`)
- **npm** (this repo uses `package-lock.json`)

## Install
```sh
npm install
```

## Run locally
```sh
npm run dev      # Astro dev server, default http://localhost:4321
```

## Build & preview
```sh
npm run build    # outputs static site to ./dist/
npm run preview  # serves the built ./dist/ locally
```

These four (`dev`, `build`, `preview`, `astro`) are the **only** scripts defined in
`package.json`. There is no test suite and no configured `astro check`.

## Deployment (overview)
- Hosted on **Netlify** (site id `57df0a8e-c32d-4954-9507-f9f3b1f90e53`); build command
  `npm run build`, publish directory `dist` (see `netlify.toml`).
- **Production target** is `greenwayband.com`, which is **currently still a Squarespace site**.
  Launch = flip the Cloudflare A record from Squarespace to Netlify (reversible in minutes).
- `netlify.toml` currently 301-redirects `greenway-website.netlify.app/*` →
  `greenwayband.com/:splat`. **Note:** because production is still Squarespace, this redirect
  makes the staging URL bounce to the old Squarespace site. See
  [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md).
- Do **not** deploy, push, or change DNS without explicit owner approval.

## Documentation
Project docs live in [`/docs`](docs/). Start with:
- [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md) — verified current state (read this first)
- [CLAUDE.md](CLAUDE.md) — operating manual, design tokens, conventions
- [docs/CODE_WORKFLOW.md](docs/CODE_WORKFLOW.md) — how to work in this repo
- [docs/TASKS.md](docs/TASKS.md) — what's next
