# Railway Recovery Runbook — Dealix

**Purpose:** Step-by-step recovery for when Railway deployment fails.
**Audience:** Sami Assiri (founder), on mobile or desktop.
**Last updated:** 2026-06-30

---

## Known failure modes

| Symptom | Root cause | Section |
|---------|-----------|---------|
| "Subscription past due" in Railway UI | Billing not paid | Step 1 |
| Build pulls `ghcr.io/railwayapp-temp` | Source disconnected from GitHub | Step 2 |
| App crashes at startup with SECURITY error | Missing production env vars | Step 3 |
| Healthcheck timeout on `/healthz` | App booting but env vars wrong | Step 3 |
| 502/503 from api.dealix.me | App not deployed or crashed | Steps 2–4 |

---

## Step 1 — Pay Railway billing

1. Open https://railway.app
2. Go to **Billing** in account settings.
3. Pay outstanding balance.
4. Confirm subscription is active before proceeding.

> Do NOT skip this step. Railway will not build or deploy while billing is overdue.

---

## Step 2 — Fix service source

1. Open your Railway project → select the `dealix` service.
2. Click **Settings → Source**.
3. If source shows `ghcr.io/railwayapp-temp` or any Docker image URL:
   - Click **Disconnect** or **Change source**.
   - Select **GitHub Repo**.
   - Connect `Dealix-sa/dealix`.
   - Set branch to `main`.
   - Set root directory to `/` (repo root).
   - Set Dockerfile path to `Dockerfile`.
4. Save settings.

---

## Step 3 — Set required production variables

In Railway → service → **Variables**, set every variable below.
**Never paste secret values into chat, GitHub issues, or any markdown file.**

### Generate secret values locally first

Run this on your own machine (terminal or Codespaces), never in Railway logs:

```bash
python3 - <<'PY'
import secrets
print('APP_SECRET_KEY=' + secrets.token_hex(32))
print('JWT_SECRET_KEY=' + secrets.token_hex(32))
print('API_KEYS=' + secrets.token_urlsafe(32))
print('ADMIN_API_KEYS=' + secrets.token_urlsafe(32))
PY
```

Copy each value and paste it directly into the Railway variable field.

### Required variables

```
APP_ENV=production
ENVIRONMENT=production
DATABASE_URL=${{Postgres.DATABASE_URL}}
APP_SECRET_KEY=<paste generated value>
JWT_SECRET_KEY=<paste generated value>
API_KEYS=<paste generated value>
ADMIN_API_KEYS=<paste generated value>
CORS_ORIGINS=https://dealix.me,https://www.dealix.me,https://api.dealix.me
APP_URL=https://api.dealix.me
BASE_URL=https://api.dealix.me
DEALIX_API_BASE=https://api.dealix.me
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

### Attach Postgres (if not already attached)

1. In Railway project, click **+ New** → **Database** → **PostgreSQL**.
2. In the `dealix` service variables, set `DATABASE_URL=${{Postgres.DATABASE_URL}}`.
   Railway resolves this reference automatically.

---

## Step 4 — Redeploy

1. In Railway → `dealix` service → click **Deploy** (or push a new commit to `main`).
2. Watch the build logs. Look for:
   - `Successfully built` — Docker build passed.
   - `Uvicorn running on http://0.0.0.0:8000` — app started.
   - No `SECURITY:` error in startup logs.
3. Watch deploy logs. Look for healthcheck success:
   - `Health check passed` — Railway confirms `/healthz` returned 200.

---

## Step 5 — Validate locally before redeploy (optional but recommended)

From Codespaces or local terminal with the same env vars set:

```bash
make railway-env-check
```

Expected output:

```
RAILWAY_PRODUCTION_ENV=READY
Required production variables are present and non-placeholder.
```

If you see `RAILWAY_PRODUCTION_ENV=FAIL`, fix the listed variable names before deploying.

---

## Step 6 — Production smoke test

After Railway shows deployment success:

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/api/status
```

Expected `/healthz` response: HTTP 200 with `{"status": "ok"}` or similar.

Expected `/api/status` response must include:
```json
{
  "external_send_enabled": false,
  "outbound_mode": "draft_only"
}
```

If `/healthz` returns 502/503, check Railway logs for the startup error.

---

## Step 7 — Confirm GitHub deployment status

Railway posts a deployment status back to GitHub on each deploy.
Check: https://github.com/Dealix-sa/dealix/deployments

Green check = deployment succeeded.
Red X = check Railway build/deploy logs for the error.

---

## Safety rules during recovery

- Do NOT remove `_validate_production_secrets` from `api/main.py` to make the app boot.
- Do NOT set `APP_ENV=development` in production to bypass the secret guard.
- Do NOT enable live outbound (`EXTERNAL_SEND_ENABLED=true`) during recovery.
- If you cannot fix Railway from the UI, open a support ticket at https://railway.app/help.

---

## Escalation path

| Issue | Action |
|-------|--------|
| Railway billing blocked | Pay manually at railway.app/billing |
| GitHub source cannot be connected | Check Dealix-sa org → Settings → GitHub App permissions |
| Postgres plugin missing | Add new PostgreSQL plugin in Railway project |
| App still crashes after env vars set | Read Railway deploy logs; share error (no secret values) with engineer |
| Custom domain api.dealix.me not resolving | Check DNS → CNAME → Railway domain settings |
