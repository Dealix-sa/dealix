# Railway production deployment runbook

The production service is connected to `main` on `api.dealix.me`. This
document is the **canonical** order of operations for deploys; the
verifier `scripts/verify_railway_readiness.py` enforces the static parts.

## 1. Pre-deploy gate

Before any push to `main`:

```bash
make production-certification
```

Must print:

```
DEALIX PRODUCTION CERTIFICATION: PRODUCTION-GATED READY
```

`make production-certification` runs (in order):

1. `production-env-check`  — env names + conflict rules (CI-safe).
2. `railway-readiness`     — Railway config + frontend secret scan.
3. `live-send-safety`      — WhatsApp/email/payments gates wired.
4. `everything`            — orchestrator → `docs/ops/DEALIX_FINAL_READINESS_REPORT.md`.

## 2. Railway environment variables

These must be set on the Railway service (Settings → Variables). They are
**never** committed to git; the verifier only checks for presence.

### Required
- `APP_ENV=production`
- `APP_SECRET_KEY` — 32-byte hex
- `JWT_SECRET_KEY` — 32-byte hex
- `API_KEYS` — comma-separated production API keys
- `ADMIN_API_KEYS` — comma-separated admin API keys
- `DEALIX_INTERNAL_TOKEN` — strong random (preferred for `/api/v1/internal/*`)
- `DEALIX_PRIVATE_OPS=/app/private_ops`
- `DATABASE_URL` — Railway-provided Postgres URL
- `CORS_ORIGINS=https://dealix.me,https://www.dealix.me,https://api.dealix.me`
- `PUBLIC_BASE_URL=https://api.dealix.me`

### Live-send kill switches (start SAFE)
- `WHATSAPP_MOCK_MODE=true`
- `WHATSAPP_ALLOW_LIVE_SEND=false`
- `WHATSAPP_DAILY_LIMIT=10`

Flip to live mode **only** after:
- Founder approval recorded in the audit log.
- `make live-send-safety` is PASS.
- A successful dry-run via `whatsapp_safe_send.safe_send_text` with
  `approval_status="approved"` and `is_opted_out=False`.

### Optional (warn-if-missing)
- `GROQ_API_KEY`, `GOOGLE_SEARCH_API_KEY`, `GOOGLE_SEARCH_CX`
- `HUBSPOT_ACCESS_TOKEN`, `MOYASAR_SECRET_KEY`
- `POSTHOG_HOST`
- `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM`
- `GREEN_API_INSTANCE_ID`, `GREEN_API_TOKEN`

## 3. Railway service settings

- **Branch**: `main`
- **Auto deploy**: enabled
- **Wait for CI**: **enabled** (do not deploy without GitHub Actions green)
- **Domain**: `api.dealix.me`
- **Target port**: `8080` (also set `PORT=8080` if Railway does not inject)
- **Predeploy**: `sh /app/scripts/railway_predeploy.sh`
- **Start command**: leave blank (Dockerfile CMD = `./start.sh`)
- **Healthcheck**: `/healthz`, timeout `300`
- **Restart**: `ON_FAILURE`, max retries `3`

## 4. GitHub branch protection

Settings → Branches → `main` → require these status checks before merge:

- `dealix-production-certification`
- `ci`
- `docker-build`

## 5. Deploy

```bash
git push origin <branch>            # opens a PR
gh pr create --draft                # CI runs production certification
# After CI green + review → squash-merge to main
# Railway picks up the deploy automatically (Wait for CI is on)
```

## 6. Post-deploy smoke

```bash
curl -fsSL https://api.dealix.me/healthz | jq

DEALIX_INTERNAL_TOKEN=<from Railway> \
  python scripts/smoke_internal_api.py \
    --base https://api.dealix.me \
    --require-auth
```

Expected:
- `/healthz` → 200, `status=ok`.
- `/api/v1/internal/ceo/summary` with token → 200, `kill_switches.is_live_send_allowed=false`.
- Same endpoint without token → 403.

## 7. Rollback

```bash
# Railway dashboard → Deployments → click previous green deploy → Redeploy
# Or:
git revert <bad-sha> && git push origin main
```

`scripts/railway_predeploy.sh` runs `alembic upgrade head` before every
deploy. **Do not** add destructive migrations. If a forward migration is
not safely reversible, ship a no-op forward + a separate cleanup PR.
