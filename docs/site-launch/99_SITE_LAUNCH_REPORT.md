# Site Launch Report

_Date: 2026-06-04_

## Approach (honest scope)
The Dealix marketing site (`apps/web`, Next.js 15 app-router) **already exists**
and already ships a strong SEO surface. Rewriting it inside this change set
would risk the production build without a way to fully verify every route here.
So this work **did not rewrite the site**. Instead it:

1. Added a `site-commercial-verify` CI workflow that hard-gates commercial
   readiness + SEO-surface presence and runs the web build as a best-effort,
   non-blocking informational job.
2. Documented the commercial content (verticals, offers, pricing, trust) in
   `docs/commercial-launch/` so it can be lifted into site pages safely in a
   focused follow-up.

## Existing SEO surface (verified present)
- `apps/web/app/robots.ts` — robots rules (blocks AI crawlers, allows public routes)
- `apps/web/app/sitemap.ts` — dynamic sitemap with priorities
- `apps/web/app/manifest.ts` — web manifest
- `apps/web/app/layout.tsx` — metadata (title template, description, OpenGraph,
  Twitter card, alternate AR/EN languages)
- `apps/web/app/page.tsx` — JSON-LD structured data
- Tailwind brand system (navy/gold), security headers in `next.config.js`,
  bilingual AR (`/ar/*`) routes.

## Build result
The web build is exercised by the `web-build` job in
`.github/workflows/site-commercial-verify.yml` (`npm install && npm run verify`).
It is marked `continue-on-error` so a pre-existing front-end issue does not mask
the commercial readiness gate. It was **not** run as part of this change locally;
the report does not claim a passing front-end build.

## Recommended safe follow-up (separate PR)
Add these routes using the documented content, one file at a time, verifying
`npm run verify` after each: `/commercial`, `/verticals/*`, `/pricing`, `/trust`,
`/contact` (intake-only form, no external send when backend not ready).

## Go / No-Go
**GO:** ship the existing site; use `docs/commercial-launch/` content for pages.
**NO-GO:** website auto-submit; any contact form that sends externally before the
backend + go-live prerequisites are in place.
