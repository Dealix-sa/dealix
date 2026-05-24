# Dealix — Company Operational State (Live)

**Status:** LAUNCHED (backend + landing live). Blocked on Moyasar account activation for REVENUE VERIFIED.
**Last verified:** 2026-05-24
**Base URL:** https://api.dealix.me
**Landing:** https://voxc2.github.io/dealix/

> **Founder-blocked items:** the consolidated list of items only the founder can unblock now lives in [`../NEXT_FOUNDER_ACTIONS.md`](../NEXT_FOUNDER_ACTIONS.md). This document records technical state and verified facts only.

---

## Closure Pass — 2026-05-24

Evidence of the v5 closure pass that landed on branch `claude/sharp-sagan-TdtJw`:

1. **CompanyBrain real module shipped** — see [`auto_client_acquisition/company_brain_v6/`](../auto_client_acquisition/company_brain_v6/) (builder, schemas, service_matcher, risk_profile, timeline, next_best_action).
2. **Pre-commit hooks + Service Readiness Matrix validation active** — see [`../.pre-commit-config.yaml`](../.pre-commit-config.yaml) (gitleaks, bandit, mypy, ruff + `verify-service-readiness-matrix` + `export-service-readiness-json` local hooks).
3. **V5 System Overview doc exists** — see [`V5_SYSTEM_OVERVIEW.md`](V5_SYSTEM_OVERVIEW.md) (one-page map of every module, endpoint, CLI, workflow).
4. **5 sub-agent definitions in place** — see [`../.claude/agents/`](../.claude/agents/): `dealix-engineer`, `dealix-content`, `dealix-delivery`, `dealix-sales`, `dealix-pm`.
5. **Session-start hook + settings.json** — see [`../.claude/settings.json`](../.claude/settings.json) and [`../scripts/session_start_hook.sh`](../scripts/session_start_hook.sh) (added this session).

---

## Live Endpoints (verified)

| Endpoint | Status | Response |
|----------|--------|----------|
| `GET /healthz` | 200 | `{"status":"ok","service":"dealix"}` |
| `GET /health` | 200 | `{status, version:"3.0.0", env:"production", providers:[]}` |
| `GET /api/v1/pricing/plans` | 200 | Starter/Growth/Scale JSON |
| `POST /api/v1/public/demo-request` | 200 | Returns Calendly URL on valid payload |
| `POST /api/v1/public/partner-application` | 200 | Returns Arabic success message |
| `GET /docs` | 200 | FastAPI Swagger UI |
| `GET /openapi.json` | 200 | OpenAPI spec |
| `POST /api/v1/checkout` | 502 | **Blocked:** Moyasar `account_inactive_error` |

---

## What's Working

### Infrastructure
- Railway deploy: service `web`, environment `Dealix`, builder RAILPACK auto-detects Dockerfile
- Dynamic `$PORT` binding via Dockerfile `/app/start.sh`
- Database: Railway Postgres auto-linked via `DATABASE_URL=${{Postgres.DATABASE_URL}}`
- Env vars (all set via Railway GraphQL API):
  - APP_SECRET_KEY, ADMIN_TOKEN, LOG_LEVEL, ENVIRONMENT, APP_ENV
  - APP_URL, PUBLIC_BASE_URL, CORS_ORIGINS, CALENDLY_URL
  - MOYASAR_SECRET_KEY, MOYASAR_WEBHOOK_SECRET, MOYASAR_PUBLIC_KEY
  - POSTHOG_API_KEY, POSTHOG_HOST, POSTHOG_ENABLED
  - CALENDLY_OAUTH_CLIENT_ID, CALENDLY_PAT, CALENDLY_WEBHOOK_SECRET
- Startup healthcheck passing (tini + uvicorn via Dockerfile CMD)

### Application
- All routers mounted: health, pricing, public, webhooks, leads, sales, sectors, admin, agents
- Sentry SDK initialized on startup (waiting for DSN — see `NEXT_FOUNDER_ACTIONS.md`)
- PostHog analytics initialized
- DLQ + idempotency in place for webhooks
- Moyasar invoice client code verified functional (blocked only by account status)

### Landing
- GitHub Pages serves from `gh-pages` branch
- All 4 pages (home/marketers/pricing/partners) return 200
- `window.DEALIX_API_BASE = 'https://api.dealix.me'` baked in
- Demo form → backend → Calendly URL (verified round-trip)
- Partner form → backend (verified round-trip)

---

## Blocked by Sami (manual dashboard action)

> **Consolidated list with steps, expected outputs, and unlock chain:** see [`../NEXT_FOUNDER_ACTIONS.md`](../NEXT_FOUNDER_ACTIONS.md). The summary below stays for at-a-glance reading; it is not the source of truth for the founder's checklist.

### 1. Moyasar Account Activation (CRITICAL for revenue)
**Error:** `{"type":"account_inactive_error","message":"Entity not activated to use live account"}`

**Steps Sami must take:**
1. Open https://dashboard.moyasar.com
2. Settings → Business → complete all KYC fields:
   - Commercial Registration (CR) or freelance license
   - National ID / Iqama
   - Bank account (IBAN)
   - Business address
3. Submit for review — typically activated within 1-3 business days
4. Once active, rotate `MOYASAR_SECRET_KEY` in Moyasar → paste new key into Railway (use literal placeholder `<paste-from-dashboard>` in any committed doc)
5. Configure webhook:
   - URL: `https://api.dealix.me/api/v1/webhooks/moyasar`
   - Events: `payment_paid`, `payment_failed`, `payment_refunded`
   - Secret: use existing `MOYASAR_WEBHOOK_SECRET` from Railway or regenerate

**Alternative for testing today:** Sami creates a Moyasar **test** account key — switch Railway env var to test mode for full flow verification without touching real money.

### 2. SENTRY_DSN (not set)
1. Open https://sentry.io → create project "dealix"
2. Copy the DSN (starts with `https://...@...ingest.sentry.io/...`)
3. Send to ops → updated in Railway via GraphQL.

### 3. UptimeRobot (not configured)
Open https://uptimerobot.com → Add HTTPS monitor:
- URL: `https://api.dealix.me/health`
- Interval: 5 min
- Alert to phone/email
- Save

### 4. First LinkedIn DM (identity-only)
Ready in `docs/ops/launch_content_queue.md`. Sami opens LinkedIn → pastes → sends.

---

## Launch Truth Table

| Area | Status |
|------|--------|
| GitHub main + CI | VERIFIED READY (SHA ahead of 44cc3513e3) |
| Landing pages live | VERIFIED READY |
| Backend production | VERIFIED READY (api.dealix.me) |
| Demo form → backend | VERIFIED READY |
| Partner form → backend | VERIFIED READY |
| Moyasar live payments | BLOCKED (account activation) |
| Moyasar webhook | NOT READY (depends on above) |
| 1 SAR verified | NOT READY (depends on above) |
| Sentry DSN | EMPTY (waiting for DSN) |
| UptimeRobot | NOT READY |
| First DM sent | NOT READY (Sami identity) |
| CRM tracker | VERIFIED READY (`docs/ops/pipeline_tracker.csv`) |
| Launch content queue | VERIFIED READY (`docs/ops/launch_content_queue.md`) |

---

## Pipeline (Day 1 Seed — 5 priority leads)

See `docs/ops/pipeline_tracker.csv` — seeded with:
1. عبدالله العسيري · Lucidya · CEO (surname affinity priority)
2. Ahmad Al-Zaini · Foodics · CEO ($170M Series C)
3. Nawaf Hariri · Salla · CEO (70K+ merchants distribution)
4. Hisham Al-Falih · Lean Technologies · CEO (API-first B2B)
5. Ibrahim Manna · BRKZ · Founder ($30M debt contech)

All with personalized DMs ready in `launch_content_queue.md`. **No automated sends.**

---

## 3 Paying Customers/Day — Staged Math

```
Conversion per outbound (conservative, case-safe estimate):
  0.05 × 0.40 × 0.70 × 0.20 × 0.80 = 0.00224

Estimated touches required for 3 paid/day:
  3 / 0.00224 ≈ 1,340 touches/day
```

| Stage | Goal | Daily Touches | Channels | When |
|-------|------|---------------|----------|------|
| 1 | First customer | 25-50 | Founder-led | Now (Day 1-14) |
| 2 | 3 customers/week | 50-100 | Founder + first partner | Day 15-45 |
| 3 | 1 customer/day | 200-400 | Partners + SDR | Day 45-90 |
| 4 | 3 customers/day | 1,000+ | Full reseller channel | Day 90+ |

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## Next 24 Hours Execution Plan

### When Moyasar activates (Sami's work):
- Sami sends new key via the secure channel (use literal `<paste-from-dashboard>` in any committed doc)
- Ops updates Railway env → redeploy → 1 SAR test → verify webhook round-trip
- Mark **REVENUE VERIFIED**

### When Sami sends SENTRY_DSN:
- Add to Railway env via GraphQL → redeploy
- Trigger `/_test_sentry` → verify issue appears in Sentry UI

### When Sami has 10 minutes for UptimeRobot:
- Complete from `docs/ops/UPTIME_AND_ALERTS.md` — 10 min, then `UPTIME MONITOR ACTIVE`

### Outreach today (Sami):
- Open LinkedIn → send DM #1 (Abdullah) from `launch_content_queue.md`
- Update `docs/ops/pipeline_tracker.csv` row 1 with `sent_at` timestamp
- Schedule Day +2 reminder (48h rule)

### Content (Sami):
- Post 1 (founder launch) → LinkedIn personal account
- Same post → X/Twitter

---

## Contact Points

- **Backend:** https://api.dealix.me
- **Landing:** https://voxc2.github.io/dealix/
- **Demo booking:** https://calendly.com/sami-assiri11/dealix-demo
- **GitHub:** https://github.com/VoXc2/dealix
- **Pipeline tracker:** `docs/ops/pipeline_tracker.csv`
- **Content queue:** `docs/ops/launch_content_queue.md`
- **Founder action list:** [`../NEXT_FOUNDER_ACTIONS.md`](../NEXT_FOUNDER_ACTIONS.md)

---

## Final Executive Decision

**State:** LAUNCHED (technical) — blocked on Moyasar activation for REVENUE VERIFIED.

- Launch target A (LAUNCHED): REACHED
- Launch target B (REVENUE READY): Blocked on Moyasar account activation
- Launch target C (REVENUE VERIFIED): Depends on B
- Launch target D (ACQUISITION STARTED): Ready — waiting only on Sami's first send
- Launch target E (COMPANY OPERATING): Pipeline + content ready — daily loop documented

**One credential unlocks revenue:** the founder paths in [`../NEXT_FOUNDER_ACTIONS.md`](../NEXT_FOUNDER_ACTIONS.md) capture everything downstream that can be executed automatically once each blocker is removed.

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
