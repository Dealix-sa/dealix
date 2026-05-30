# Dealix Railway Founder OS Runbook

> يصف هذا الـ runbook إعداد ثلاث خدمات على Railway من نفس الريبو:
> الـ API، وعامل Founder OS الدائم، وWatchdog مجدول. يتوافق مع
> `railway.toml` / `railway.json` / `Dockerfile` الموجودة في الجذر.

## الخدمات المطلوبة

| الخدمة | النوع | Public Domain | Start Command |
|---|---|---|---|
| `dealix` (API) | Web | `api.dealix.me` | (فارغ) — Dockerfile `CMD /app/start.sh` |
| `web` | Web | الواجهة | حسب الواجهة |
| `Postgres` | Database | لا | Railway Postgres |
| `founder-os-worker` | Worker دائم | لا | `python scripts/founder_os_worker.py` |
| `dealix-watchdog` | Cron `*/15 * * * *` | لا | `python scripts/railway_watchdog.py` |

## 1) خدمة الـ API

الـ API محكوم بالفعل بـ `railway.toml` / `railway.json`:

- Builder: `DOCKERFILE` (`Dockerfile` في الجذر)
- Healthcheck Path: `/healthz` (موجود في `api/routers/health.py`)
- Restart Policy: `ON_FAILURE`, retries = 3
- preDeploy: `scripts/railway_predeploy.sh` (هجرات Alembic عند ضبط
  `RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1` فقط)

**لا تضع Start Command يدوياً** — يكفي `CMD /app/start.sh`
(`uvicorn api.main:app`).

متغيرات خدمة الـ API:

```
APP_ENV=production
ENVIRONMENT=production
APP_URL=https://api.dealix.me
BASE_URL=https://api.dealix.me
RAILWAY_DOCKERFILE_PATH=Dockerfile
PYTHONUTF8=1
PYTHONIOENCODING=utf-8
DATABASE_URL=${{Postgres.DATABASE_URL}}
APP_SECRET_KEY=<secret طويل>
JWT_SECRET_KEY=<secret طويل>
API_KEYS=<api key قوي>
ADMIN_API_KEYS=<admin key قوي>
DEALIX_ADMIN_API_KEY=<admin key قوي>
RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1   # عند الرغبة بتشغيل alembic upgrade head
```

> استخدم `DATABASE_URL` الداخلي (وليس `DATABASE_PUBLIC_URL`) لتفادي رسوم
> egress عبر الـ TCP proxy.

## 2) خدمة Founder OS Worker

أنشئ خدمة جديدة من نفس الريبو، اسمها `founder-os-worker`، **بدون** public domain:

- Builder: Dockerfile
- Start Command: `python scripts/founder_os_worker.py`
- Restart Policy: `ON_FAILURE`

متغيرات:

```
APP_ENV=production
ENVIRONMENT=production
DATABASE_URL=${{Postgres.DATABASE_URL}}
APP_URL=https://api.dealix.me
DEALIX_API_URL=https://api.dealix.me
PYTHONUTF8=1
PYTHONIOENCODING=utf-8
FOUNDER_OS_ENABLED=true
HERMES_AGENTS_ENABLED=true
AGENT_RUNTIME=railway
AGENT_MODE=founder_os
AGENT_APPROVAL_MODE=required
AUTO_SEND_ENABLED=false
EXTERNAL_OUTREACH_ENABLED=false
FOUNDER_OS_INTERVAL_SECONDS=900
```

> هذا Worker دائم وليس Cron — Railway توصي بعدم استخدام Cron للعمليات
> الطويلة.

## 3) خدمة Watchdog (Cron)

أنشئ خدمة `dealix-watchdog`، **بدون** public domain:

- Start Command: `python scripts/railway_watchdog.py`
- Cron Schedule: `*/15 * * * *` (أقصر فاصل مدعوم 5 دقائق)

متغيرات:

```
APP_URL=https://api.dealix.me
DEALIX_API_URL=https://api.dealix.me
DEALIX_HEALTH_PATH=/healthz
```

## 4) خدمة الواجهة (web)

```
NEXT_PUBLIC_API_URL=https://api.dealix.me
API_BASE_URL=https://api.dealix.me
APP_URL=https://api.dealix.me
```

## فحوص الصحة (Health Checks)

- `https://api.dealix.me/healthz`
- `https://api.dealix.me/version`
- `https://api.dealix.me/api/v1/meta`
- `https://api.dealix.me/docs`

المخرج المتوقع من `/healthz`:

```json
{ "status": "ok", "service": "dealix-api" }
```

لوغ الـ Worker المتوقع:

```json
{ "service": "founder-os-worker", "status": "started",
  "approval_mode": "required", "external_actions_allowed": false }
```

لوغ الـ Watchdog المتوقع:

```json
{ "service": "dealix-watchdog", "result": { "ok": true } }
```

## ضمان التشغيل 24/7

لا يوجد ضمان مطلق، لكن أقوى إعداد عملي:

- Restart policy: `ON_FAILURE`
- Worker منفصل عن الـ API
- Watchdog Cron كل 15 دقيقة
- Postgres كخدمة منفصلة
- عدم استخدام `DATABASE_PUBLIC_URL` داخل الـ API
- أي إرسال خارجي يحتاج approval
