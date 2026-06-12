# `landing/` — Legacy / Archived

> Status: **ARCHIVED.** Not the canonical website. Do not edit for new work.

This directory holds ~80 legacy static HTML pages from an earlier iteration of the
Dealix marketing site. It is kept for historical reference only and is **not**
deployed as the live marketing surface.

## Where the live site lives

The single canonical, launch-ready website is the Next.js App Router app in:

```
frontend/
```

- Arabic-first, bilingual (`frontend/src/app/[locale]/`).
- Home renders `frontend/src/components/gtm/CommercialLaunchHome`.
- Public funnel routes: `/[locale]`, `/services`, `/pricing`, `/offer`,
  `/dealix-diagnostic`, `/risk-score`, `/proof-pack`, `/partners`,
  `/trust-center`, `/learn`.
- Brand identity (Navy `#001F3F` + Gold `#D4AF37`) is applied via
  `frontend/tailwind.config.ts` and the design tokens under
  `design-systems/dealix/tokens/`.

The `apps/web/` app is a separate, thinner platform / control-plane **showcase**
(kept building for CI/Railway), not the marketing site.

## Guidance

- New marketing or funnel work goes in `frontend/`.
- Do not link to pages in this directory from the canonical site.
- If a page here is still needed, port it into `frontend/` rather than reviving
  the static HTML.
