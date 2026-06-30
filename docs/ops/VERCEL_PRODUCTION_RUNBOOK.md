# Dealix Vercel Production Runbook

This runbook defines the correct Vercel role for Dealix and the minimum checks required before using Vercel as a public production surface.

## Executive decision

Vercel should be used for:

- public web surface
- Next.js SaaS frontend previews
- lightweight FastAPI preview/probe deployment when needed
- pull request preview deployments

Railway should remain the canonical production backend for:

- API with Postgres
- workers and daily loops
- command-room data generation
- Company OS / Revenue OS background jobs

## Current Vercel project

Project: `dealix`

Current framework detected by Vercel: `fastapi`.

The current production deployment is a backend/API surface, not the final public website surface. The final setup should split these concerns:

| Surface | Platform | Domain |
|---|---|---|
| Public website / SaaS frontend | Vercel | `dealix.me`, `www.dealix.me` |
| API / workers / Postgres-backed OS | Railway | `api.dealix.me` |
| Preview API if needed | Vercel | `dealix-*.vercel.app` |

## Mandatory production environment variables

Set these in Vercel Project Settings → Environment Variables.

```env
APP_ENV=production
ENVIRONMENT=production
APP_LOG_LEVEL=INFO
LOG_LEVEL=INFO

APP_URL=https://dealix.me
BASE_URL=https://dealix.me
DEALIX_API_BASE=https://api.dealix.me
CORS_ORIGINS=https://dealix.me,https://www.dealix.me,https://api.dealix.me,https://dealix.vercel.app

EXTERNAL_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
```

If the FastAPI surface is deployed to production on Vercel, also set real production secrets:

```env
APP_SECRET_KEY=<generated-64-byte-hex>
JWT_SECRET_KEY=<generated-64-byte-hex>
API_KEYS=<comma-separated-client-api-keys>
ADMIN_API_KEYS=<comma-separated-admin-api-keys>
```

Generate secrets locally with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Vercel system environment compatibility

Dealix runtime settings support Vercel system environment variables:

| Vercel variable | Dealix behavior |
|---|---|
| `VERCEL_ENV=production` | maps to `APP_ENV=production` |
| `VERCEL_ENV=preview` | maps to `APP_ENV=staging` |
| `VERCEL_GIT_COMMIT_SHA` | surfaces as `/health.git_sha` |

This prevents production from reporting `env=development` and `git_sha=unknown` when Vercel system env vars are available.

## Recommended final Vercel architecture

Create a separate Vercel project for the frontend:

```text
Project name: dealix-web
Root directory: apps/web
Framework: Next.js
Production domain: dealix.me
Environment variable: NEXT_PUBLIC_DEALIX_API_BASE=https://api.dealix.me
```

Keep the existing `dealix` FastAPI project only if it is used for staging/API preview.

## Post-deploy smoke checks

Run after every deployment:

```bash
curl -fsS https://dealix.vercel.app/health
curl -fsS https://dealix.vercel.app/version
curl -fsS https://dealix.vercel.app/api/v1/meta
curl -fsS https://dealix.vercel.app/api/v1/business/pricing
```

Expected for production:

```text
/health.status = ok
/health.env = production
/health.git_sha != unknown
runtime errors = 0
live outbound = disabled unless a separate controlled-live PR is approved
```

## What must not be public

Do not expose demo/deprecated endpoints as sales proof without a visible warning or a real-data replacement.

Specifically, any command-center endpoint that returns demo forecasts or ROI estimates must remain internal until it is backed by real ledgers and proof packs.

## Deployment strategy

The preferred Vercel CI flow is:

```bash
vercel pull --yes --environment=production
vercel build --prod
vercel deploy --prebuilt --prod
```

For PR previews:

```bash
vercel pull --yes --environment=preview
vercel build
vercel deploy --prebuilt
```

## Acceptance criteria

Vercel production is accepted only when:

- `/health` returns `env=production`.
- `/health` returns a non-unknown git SHA.
- runtime error scan is clean.
- Vercel public frontend points to the Railway API base.
- outbound remains draft-only by default.
- custom domain routing is split clearly between web and API.
