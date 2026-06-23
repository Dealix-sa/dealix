# Frontend Surface Decision

## Decision
**apps/web** is the canonical frontend for Dealix.

## Evidence
- `frontend/` directory was deleted on main (commit 62991222)
- `apps/web/` has a working Next.js app with Dockerfile, package.json, and build passes
- `apps/web/` has login, signup, layout, analytics (PostHog, Sentry), and API client
- `frontend/` was a legacy Vite app that has been fully removed

## docker-compose.prod.yml Changes
- Removed the `frontend` service (was referencing deleted `frontend/Dockerfile`)
- Kept `web` service (builds from `apps/web/`)
- Updated Caddy `DEALIX_FRONTEND_UPSTREAM` default to `web:3000`
- Updated Caddy `depends_on` to reference `web` instead of `frontend`

## CI Impact
- Any CI that references `frontend/Dockerfile` should be updated to use `apps/web/Dockerfile`
- The Railway frontend service should use `apps/web/` as build context

## Owner
CTO / Release Engineer