# Dealix — Railway Founder-OS Runbook (دليل التشغيل التنفيذي)

دليل واحد لتشغيل Dealix على Railway كنظام تجاري حيّ ومراقَب 24/7: خدمة **API**
العامة + **Founder-OS Worker** دائم + **Watchdog** مجدول. هذا الملف يكمّل ولا
يكرّر المراجع القائمة:

- `docs/ops/RAILWAY_SERVICE_ENV_MATRIX_AR.md` — مصفوفة الخدمات والمتغيرات (API/frontend/web).
- `docs/RAILWAY_DEPLOY_CHECKLIST.md` — قائمة فحص الإطلاق خطوة بخطوة.
- `docs/ops/RAILWAY_PRODUCTION_POLICY_AR.md` — سياسة الإنتاج (predeploy / migrations).

> **الضمانة العقائدية (11 non-negotiables):** الـ Worker والـ Watchdog لا يرسلان
> أي شيء خارجياً، لا ينفذان أي شحن/فوترة، ويعملان دائماً في وضع
> `AGENT_APPROVAL_MODE=required`. هذا مفروض بالكود في `scripts/founder_os_worker.py`
> ومحميّ باختبار `tests/test_founder_os_worker_safe.py`.

---

## 1) خريطة الخدمات

| Service | النوع | Public Domain | Start Command | الغرض |
|---|---|---|---|---|
| `dealix-api` | Web | `api.dealix.me` | فارغ (Dockerfile = `/app/start.sh`) | الـ API العام + healthchecks |
| `founder-os-worker` | Worker دائم | لا | `python scripts/founder_os_worker.py` | نبضة تشخيص للقراءة فقط كل 15 دقيقة |
| `dealix-watchdog` | Cron | لا | `python scripts/watchdog_drift_check.py` | كشف الانحراف + فحص `/health` للإنتاج |
| `Postgres` | Database | لا | — | التخزين (Railway Postgres) |

> **ملاحظة CI:** السجل الرسمي `dealix/config/railway_services.json` يثبّت ثلاث
> خدمات فقط (`dealix-api`, `dealix-frontend`, `dealix-apps-web`) ويفحصها
> `scripts/verify_railway_surfaces.py`. لذلك **لا تُضِف** الـ worker/cron إلى ذلك
> السجل — تُنشأ يدوياً من واجهة Railway كما هو موثّق هنا، وتعيد استخدام
> نفس الـ Dockerfile في الجذر مع Start Command مختلف فقط.

---

## 2) خدمة API — الإعداد النهائي

الخدمة التي عليها `api.dealix.me`:

- **Settings → Build:** Builder = **Dockerfile**. عند الحاجة أضف
  `RAILWAY_DOCKERFILE_PATH=Dockerfile`.
- **Custom Build Command:** فارغ.
- **Start Command:** فارغ. الـ Dockerfile يشغّل `/app/start.sh`
  (`uvicorn api.main:app` على `$PORT` الديناميكي من Railway).
- **Pre-deploy Command:** `sh /app/scripts/railway_predeploy.sh` (يتخطى
  الـ migrations افتراضياً ما لم تضبط `RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1`).
- **Healthcheck Path:** `/healthz`.

### ربط Postgres (لا تستخدم public URL)

من خدمة API → Variables → **Add Variable Reference** → اختر
`Postgres → DATABASE_URL`، فيصبح:

```
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

> لا تستخدم `DATABASE_PUBLIC_URL` داخل API — يمر عبر public endpoint وقد يسبب
> رسوم egress.

### متغيرات API المطلوبة

التطبيق يرفض الإقلاع في الإنتاج بأسرار ضعيفة/ناقصة
(`api/main.py::_validate_production_secrets`). تأكد من:

```
APP_ENV=production
APP_URL=https://api.dealix.me
DATABASE_URL=${{Postgres.DATABASE_URL}}
APP_SECRET_KEY=<64-byte hex>
JWT_SECRET_KEY=<strong, ≥32 chars>
API_KEYS=<comma-separated>
ADMIN_API_KEYS=<comma-separated>
```

توليد الأسرار:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 3) إنشاء خدمة `founder-os-worker`

**New Service → GitHub Repo → `Dealix-sa/dealix`**، الاسم `founder-os-worker`.

- **Builder:** Dockerfile (نفس الجذر).
- **Start Command:** `python scripts/founder_os_worker.py`
- **Public Networking:** لا تضف دومين.
- **Restart Policy:** `ON_FAILURE`، Max Retries: 10.

### متغيرات الـ Worker

```
APP_ENV=production
DATABASE_URL=${{Postgres.DATABASE_URL}}
APP_URL=https://api.dealix.me
PYTHONUTF8=1
PYTHONIOENCODING=utf-8
AGENT_APPROVAL_MODE=required
FOUNDER_OS_INTERVAL_SECONDS=900
# اختيارية (مطفأة افتراضياً للتحكم في التكلفة/الضجيج):
# FOUNDER_OS_RUN_VERIFY=1     # يشغّل verify_reference_library_70.py
# FOUNDER_OS_RUN_DIGEST=1     # يشغّل dealix_morning_digest.py --print (طباعة فقط، لا إرسال)
```

> الـ Worker يفرض داخلياً `AUTO_SEND_ENABLED=false` و
> `EXTERNAL_OUTREACH_ENABLED=false` على كل أمر فرعي — لا حاجة لضبطها يدوياً،
> ولا يمكن تجاوزها من البيئة.

السلوك المتوقع: كل 15 دقيقة سطر JSON منظّم يحوي
`"external_actions_allowed": false` ونتائج تشخيص للقراءة فقط.

---

## 4) إنشاء خدمة `dealix-watchdog` (Cron)

**New Service → GitHub Repo → `Dealix-sa/dealix`**، الاسم `dealix-watchdog`.

- **Start Command:** `python scripts/watchdog_drift_check.py`
- **Cron Schedule:** `*/15 * * * *` (أو `0 * * * *` كل ساعة).
- **Public Networking:** لا.

### متغيرات الـ Watchdog

```
DEALIX_API_BASE=https://api.dealix.me
APP_ENV=production
```

الـ watchdog القائم يفحص: قيم الـ hard-gates الافتراضية، تزامن سجل الخدمات،
حالة `/health` و`git_sha`، تسرّب tokens ممنوعة في `landing/`، وانحراف Article 13.
يخرج بكود غير صفري عند أي انحراف — فيظهر تشغيل الـ cron كـ **failed run** =
تنبيه مبكر.

---

## 5) ترتيب الإطلاق

1. ادفع الفرع → افتح **draft PR** → انتظر CI أخضر.
2. اضبط متغيرات API + مرجع Postgres → تأكد أن deploy أخضر وأن الـ smoke ينجح.
3. أنشئ `founder-os-worker` → تأكد من نبضة JSON ثابتة بلا restart loop.
4. أنشئ `dealix-watchdog` → تأكد أن تشغيل الـ cron أخضر.
5. ادمج عندما تكون الخدمات الثلاث خضراء.

---

## 6) اختبارات النجاح (بعد النشر)

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/version
curl -fsS 'https://api.dealix.me/healthz?deep=1'
curl -fsS https://api.dealix.me/api/v1/meta   # يثبت بقاء docs/registry داخل الصورة
```

- **Worker logs:** كل دورة JSON مع `"external_actions_allowed": false`.
- **Watchdog logs:** تشغيل ناجح (`DEALIX_WATCHDOG_VERDICT` نظيف، exit 0).

---

## 7) ضمان التشغيل 24/7 (أقوى إعداد عملي)

- Restart policy `ON_FAILURE`، Max Retries مرتفع للخدمات الدائمة.
- فصل الـ Worker عن الـ API (كل منهما يفشل/يعاد تشغيله مستقلاً).
- Watchdog cron كل 15 دقيقة كطبقة كشف مستقلة.
- Postgres كخدمة منفصلة، والاتصال عبر `DATABASE_URL` الداخلي فقط.
- أي إرسال خارجي يبقى خلف موافقة الـ founder (`AGENT_APPROVAL_MODE=required`).

---

## 8) Rollback

- API: من Railway → Deployments → اختر آخر deploy أخضر → **Redeploy/Rollback**.
- Worker/Cron: أوقف الخدمة من Railway؛ النظام يبقى آمناً لأنها لا ترسل/لا تشحن.
- الكود: ارجع الـ commit على الفرع وادفع؛ Railway يعيد البناء تلقائياً.
