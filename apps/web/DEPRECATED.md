# apps/web — DEPRECATED

**Status:** Deprecated as of 2026-06-07. **Do not add features here.**

The canonical public website + customer/founder app is **`frontend/`** (Next.js
15, bilingual AR/EN, brand-aligned, with the public marketing pages, the
custom-solution intake, pricing, trust, and the founder dashboards).

`apps/web/` was a parallel thin Next.js surface (value-engine, safety, sandbox,
control-plane, status). It has no public marketing depth and duplicates concerns
now owned by `frontend/`. Keeping two web apps is the fragmentation the
activation spine removes — see `docs/architecture/CANONICAL_MAP.md`.

## What to do instead
- New public pages / forms / pricing → `frontend/src/app/[locale]/…`.
- Unique `apps/web/` views still wanted (e.g. control-plane, kill-switch) →
  port into `frontend/` under an authenticated route, then delete here.

## Before removing this directory
Verify nothing deploys it: check `.github/workflows/` (e.g.
`railway_deploy_frontend.yml`, `generate-web-lockfile.yml`) and any Railway
service still pointed at `apps/web/` — repoint to `frontend/` first.
