# Dealix Founder / CEO Operating System

> نظام تشغيل المؤسس على Railway: API + Worker دائم + Watchdog. هذا المستند
> يصف الإيقاع اليومي والخدمات؛ الإعداد التفصيلي على Railway في
> `RAILWAY_FOUNDER_OS_RUNBOOK_AR.md`.

## الغرض

تحويل Dealix إلى نظام تشغيل مؤسسي يخدم المؤسس يومياً:

- ماذا نبيع؟ ولمن؟
- ما المخاطر؟ وما التدفق النقدي؟
- ما التالي؟ وما الذي لا يجب فعله بدون موافقة؟

## الإيقاع اليومي

| الوقت | النشاط | المخرج |
|---|---|---|
| صباحاً | Founder OS digest (`scripts/dealix_morning_digest.py --print`) | أولويات اليوم |
| منتصف اليوم | Revenue check | العملاء / الفرص / العروض |
| نهاية اليوم | CEO review | قرارات + مخاطر + next actions |

## مبادئ التشغيل (متوافقة مع doctrine)

1. لا إرسال خارجي بدون موافقة (`AUTO_SEND_ENABLED=false`، `AGENT_APPROVAL_MODE=required`).
2. لا live charge في الاختبارات.
3. لا ادعاءات تجارية بلا proof.
4. كل قرار له audit trail.
5. Postgres هو مصدر الحقيقة التشغيلي.
6. الـ Worker منفصل عن الـ API.
7. الـ Watchdog مستقل عن الـ Worker.

## الخدمات (Railway)

| الخدمة | النوع | Public Domain | Start Command |
|---|---|---|---|
| `dealix` (API) | Web | `api.dealix.me` | (فارغ) — Dockerfile `CMD /app/start.sh` |
| `web` | Web | الواجهة | حسب الواجهة |
| `Postgres` | Database | لا | Railway Postgres |
| `founder-os-worker` | Worker دائم | لا | `python scripts/founder_os_worker.py` |
| `dealix-watchdog` | Cron `*/15 * * * *` | لا | `python scripts/railway_watchdog.py` |

> ملاحظة: الـ API يُشغَّل عبر `Dockerfile`/`Procfile` (`uvicorn api.main:app`).
> لا تَضع Start Command يدوياً على خدمة الـ API.

## ما الذي يفعله الـ Worker

`scripts/founder_os_worker.py` يدور كل `FOUNDER_OS_INTERVAL_SECONDS` (افتراضي 900)
ويُشغّل أوامر تشخيص للقراءة فقط، ويطبع heartbeat بصيغة JSON:

- `scripts/dealix_status.py`
- `scripts/dealix_morning_digest.py --print` (عرض فقط — لا إرسال)
- `scripts/verify_reference_library_70.py`

يفرض على العمليات الفرعية `AUTO_SEND_ENABLED=false` و`EXTERNAL_OUTREACH_ENABLED=false`.

## ما الذي يفعله الـ Watchdog

`scripts/railway_watchdog.py` يفحص `GET ${APP_URL}/healthz` ويُرجع رمز خروج
غير صفري عند الفشل حتى تُسجَّل المهمة كفاشلة على Railway.

## KPI Dashboard

| المحور | KPI |
|---|---|
| Revenue | MRR, ARR, pipeline SAR, close rate |
| Finance | runway, burn, gross margin, CAC, payback |
| Operations | uptime, failed jobs, queue depth |
| Product | active endpoints, docs health, API latency |
| Sales | leads, demos, proposals, signed clients |
| Governance | approvals, blocked actions, risk notes |
