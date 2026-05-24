# Railway Production Deployment

This doc is the deployment-side companion to
`docs/ops/DEALIX_FINAL_READINESS_REPORT.md`. It explains how the repo
maps onto Railway and where every safety toggle lives.

## 1. Topology

- **Builder**: `DOCKERFILE` (defined in both `railway.toml` and `railway.json`).
- **Image**: `python:3.12-slim-bookworm`, non-root user `app`.
- **Start**: `/app/start.sh` (CMD in the Dockerfile). Do NOT set a
  custom Start Command in the Railway UI.
- **Predeploy**: `sh /app/scripts/railway_predeploy.sh` — runs
  `alembic upgrade head` only when `RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1`
  AND `DATABASE_URL` is set.
- **Healthcheck**: `GET /healthz` with a 300s timeout.
- **Target port**: container reads `$PORT` (Railway injects it; default
  8000 locally, 8080 in Railway).

## 2. Required variables

These MUST be set in Railway → Variables (never committed):

| Name | Why |
|---|---|
| `APP_ENV` | Must equal `production`. Many guardrails switch on this. |
| `DEALIX_INTERNAL_TOKEN` | Every `/api/v1/internal/*` request requires it. |
| `JWT_SECRET_KEY` | Signs JWTs. Long random string, rotated quarterly. |
| `DEALIX_PRIVATE_OPS` | Path to the private_ops runtime tree. Use a Volume mount if you want persistence. |
| `DATABASE_URL` | Postgres URL. The app auto-rewrites `postgres://` → `postgresql+asyncpg://`. |

## 3. Live-integration toggles

These default to **safe** values. They are intentionally only flipped
by hand after `make live-send-safety` passes.

| Name | Default | When to change |
|---|---|---|
| `WHATSAPP_MOCK_MODE` | `true` | Set `false` only after the safety gate is green and a daily limit is set. |
| `WHATSAPP_ALLOW_LIVE_SEND` | `false` | Set `true` only after the safety gate is green AND `WHATSAPP_MOCK_MODE=false`. |
| `WHATSAPP_DAILY_LIMIT` | unset → blocked | Set to a number you'd accept as worst-case. Start with 10. |
| `EMAIL_ALLOW_LIVE_SEND` | `false` | Same rule as WhatsApp. |
| `EMAIL_MOCK_MODE` | `true` | Same rule as WhatsApp. |
| `MOYASAR_ALLOW_LIVE_CAPTURE` | `false` | Even when live, pricing commits ESCALATE per policy. |
| `MOYASAR_MOCK_MODE` | `true` | Same rule. |

## 4. Wait for CI

Settings → Source → "Wait for CI" must be **ON**. The workflow that
satisfies the gate is `.github/workflows/dealix-production-certification.yml`.
If that workflow ever stops running or stops being required, Railway
will deploy whatever pushes to `main` — defeating the whole layer.

## 5. Healthcheck route

`/healthz` is intentionally separate from `/health`. `/healthz` returns
a fast 200 with the git SHA (no auth, no DB hit) so Railway never
misclassifies a slow DB as a dead app. Any change to its semantics
must be matched in `verify_railway_readiness.py`.

## 6. After a successful deploy

```bash
# 1. Liveness
curl -fsS https://api.dealix.me/healthz

# 2. Internal route must REJECT unauthenticated calls
curl -i https://api.dealix.me/api/v1/internal/ceo/summary
# Expect: HTTP/2 401 or 403 (never 200)

# 3. With token (only from a sealed environment)
curl -H "X-Dealix-Internal-Token: $DEALIX_INTERNAL_TOKEN" \
  https://api.dealix.me/api/v1/internal/ceo/summary
```

If step 2 returns 200, stop the deployment immediately and rotate
`DEALIX_INTERNAL_TOKEN`.

## 7. Rollback

Railway "Redeploy previous deployment" is the canonical rollback. The
predeploy hook only runs `alembic upgrade head`, so downgrades are
manual: open a PR that includes the downgrade migration and let the
gate certify it before redeploy.

## 8. References

- Railway docs — https://docs.railway.app
- `docs/ops/DEALIX_FINAL_READINESS_REPORT.md` — the gate definition
- `docs/security/RAILWAY_SECRET_HANDLING.md` — secret hygiene
- `docs/security/LIVE_INTEGRATION_KILL_SWITCHES.md` — kill-switch matrix
