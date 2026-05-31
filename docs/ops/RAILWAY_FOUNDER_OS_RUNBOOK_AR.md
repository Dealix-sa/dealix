# Dealix Railway Founder OS — إطلاق المنتج + تشغيل 24/7

**تاريخ الإنشاء:** 2026-05-30 | **الحالة:** إعداد الإطلاق | **المسؤول:** المؤسس (Sami/Bassam)

---

## نظرة عامة: الخدمات الثلاث

أنت تشغّل **ثلاث خدمات منفصلة** على Railway تعمل معاً:

| الخدمة | النوع | المهمة | الحالة الحالية |
|---|---|---|---|
| **dealix-api** | Web Service | API الرئيسي ✓ | موجود (يحتاج تشكيل env) |
| **founder-os-worker** | Worker (دائم) | حلقة تشخيصات كل 15 دقيقة | جديد (في الريبو، لم يُنشأ بعد على Railway) |
| **dealix-watchdog** | Cron Job | تفتيش الانجراف كل 15 دقيقة | جديد (في الريبو، لم يُنشأ بعد على Railway) |
| **Postgres** | Database | قاعدة البيانات | موجودة |

---

## المرحلة 1: مراجعة الحالة الحالية (قبل البدء)

### الخطوة P1.1 — تحقق من خدمة API الحالية

اذهب إلى **Dashboard → dealix-api** (أو cv، حسب الاسم):

- **Source:** Dealix-sa/dealix ✓
- **Builder:** Dockerfile ✓ (أو عدّل إلى `RAILWAY_DOCKERFILE_PATH=Dockerfile`)
- **Start Command:** فارغ ✓ (Dockerfile يستخدم `/app/start.sh` تلقائياً)
- **Pre-deploy:** `sh /app/scripts/railway_predeploy.sh` ✓
- **Healthcheck Path:** `/healthz` ✓
- **Healthcheck Timeout:** 300 ✓
- **Restart Policy:** ON_FAILURE ✓
- **Max Retries:** 3 ✓

✅ إذا كل هذا أخضر، انتقل إلى **P1.2**. إذا أحمر، عدّل الآن.

### الخطوة P1.2 — تحقق من وجود قاعدة البيانات

- اذهب إلى **Dashboard → Postgres** (أو اسمها في مشروعك)
- انسخ `DATABASE_URL` منها (سيكون شيء مثل `postgresql+asyncpg://user:pass@host:5432/db`)
- ستستخدمها في الخطوة التالية

---

## المرحلة 2: تشكيل متغيرات البيئة لـ dealix-api

### الخطوة P2.1 — متغيرات الإنتاج الإجبارية

افتح **dealix-api → Variables**. تأكد من وجود **جميع** هذه المتغيرات:

```
APP_ENV=production
ENVIRONMENT=production
APP_URL=https://api.dealix.me
BASE_URL=https://api.dealix.me
RAILWAY_DOCKERFILE_PATH=Dockerfile
PYTHONUTF8=1
PYTHONIOENCODING=utf-8
```

### الخطوة P2.2 — الأسرار (المفاتيح الحساسة)

اضغط **+ Variable** لكل واحد من هذه الأسرار. **استخدم محرر مختلف جديد** (كلمات مرور عشوائية قوية):

```bash
# لتوليد أسرار قوية، شغّل هذا محلياً:
python -c "import secrets; print(secrets.token_hex(32))"
```

أضف هذه المتغيرات:

```
APP_SECRET_KEY=<secret_64_hex_1>           # مثال: a1b2c3d4...
JWT_SECRET_KEY=<secret_64_hex_2>           # مثال: x9y8z7w6...
API_KEYS=<api_key_1>,<api_key_2>          # مثال: key1,key2
ADMIN_API_KEYS=<admin_key_1>,<admin_key_2> # مثال: admin1,admin2
DEALIX_ADMIN_API_KEY=<same_as_admin_key_1>
```

### الخطوة P2.3 — ربط قاعدة البيانات (الأهم!)

اضغط **+ Variable Reference** (ليس text input عادي).

اختر:
- **Variable Name:** `DATABASE_URL`
- **Reference:** اختر Postgres service → `DATABASE_URL`

**هذا يضمن:**
- لا تستخدم `DATABASE_PUBLIC_URL` (يسبب egress fees)
- الاتصال آمن عبر الشبكة الداخلية

### الخطوة P2.4 — متغيرات API اختيارية لكن مشروعة

```
REDIS_URL=<redis_connection_or_empty>
SENTRY_DSN=<sentry_dsn_or_empty>
DEALIX_API_BASE=https://api.dealix.me  # للـ smoke tests
DEALIX_API_KEY=<same_api_key_1>
```

---

## المرحلة 3: اختبر API بعد التعديل

### الخطوة P3.1 — أعد نشر API

افتح **dealix-api → Deploy** اضغط **Redeploy** (إذا لم يبدأ بشكل تلقائي).

انتظر حتى يصبح أخضر ويقول "Active".

### الخطوة P3.2 — اختبارات smoke

افتح terminal محلي وشغّل:

```bash
curl -fsS https://api.dealix.me/healthz
# يجب أن يعطيك:
# {
#   "status": "ok",
#   "service": "dealix",
#   "version": "3.0.0",
#   "env": "production"
# }

curl -fsS https://api.dealix.me/version
# يجب أن يعطيك معلومات الإصدار

curl -fsS 'https://api.dealix.me/healthz?deep=1'
# اختبار عميق للـ DB والـ dependencies
```

إذا عملت جميعها، **API جاهز** ✓

---

## المرحلة 4: أنشئ خدمة Founder OS Worker

### الخطوة P4.1 — أنشئ الخدمة

اذهب إلى **Dashboard الرئيسي → + New → Service**.

اختر **GitHub Repo** → اختر **Dealix-sa/dealix**.

### الخطوة P4.2 — إعدادات الخدمة

```
Service Name: founder-os-worker
Environment: production
```

### الخطوة P4.3 — الإعدادات المتقدمة (Settings)

في قسم **Deploy**:

```
Source:        GitHub Repo (Dealix-sa/dealix)
Builder:       Dockerfile
Dockerfile Path: Dockerfile (default)
Start Command: python scripts/founder_os_worker.py
(ترك باقي الحقول بـ default)
```

### الخطوة P4.4 — Networking

```
Public Networking: OFF (لا تريد domain عام لـ worker)
```

### الخطوة P4.5 — Restart Policy

```
Restart Policy:   ON_FAILURE
Max Retries:      10  (أكثر من API لأن errors متوقعة في diagnostic scripts)
```

### الخطوة P4.6 — Environment Variables

اضغط **+ Variable** وأضف:

```
APP_ENV=production
ENVIRONMENT=production
DATABASE_URL=${{Postgres.DATABASE_URL}}  (reference، ليس نص عادي)
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
FOUNDER_OS_RUN_VERIFY=0
FOUNDER_OS_RUN_DIGEST=0
```

**أيضاً** انسخ نفس الأسرار من dealix-api:
```
APP_SECRET_KEY=<same_value>
JWT_SECRET_KEY=<same_value>
API_KEYS=<same_value>
ADMIN_API_KEYS=<same_value>
DEALIX_ADMIN_API_KEY=<same_value>
```

### الخطوة P4.7 — انتظر البناء والنشر

اضغط **Save** وانتظر البناء يصبح أخضر. يجب أن ترى في **Logs** حلقة JSON كل 15 دقيقة:

```json
{
  "service": "founder-os-worker",
  "external_actions_allowed": false,
  "doctrine_enforced": true
}
```

✅ إذا ظهرت، الـ worker يعمل!

---

## المرحلة 5: أنشئ خدمة Dealix Watchdog (Cron)

### الخطوة P5.1 — أنشئ الخدمة

اذهب إلى **Dashboard الرئيسي → + New → Service**.

اختر **GitHub Repo** → اختر **Dealix-sa/dealix**.

### الخطوة P5.2 — الإعدادات

```
Service Name: dealix-watchdog
Environment: production
```

### الخطوة P5.3 — Deploy Settings

```
Source:         GitHub Repo (Dealix-sa/dealix)
Builder:        Dockerfile
Dockerfile Path: Dockerfile
Start Command:  python scripts/watchdog_drift_check.py
```

### الخطوة P5.4 — Networking

```
Public Networking: OFF
```

### الخطوة P5.5 — Cron Schedule

في قسم **Deploy** (أو Advanced)، ابحث عن **Cron**:

```
Cron Schedule: */15 * * * *
(يعني: كل 15 دقيقة)
```

### الخطوة P5.6 — Environment Variables

```
APP_ENV=production
ENVIRONMENT=production
DEALIX_API_BASE=https://api.dealix.me
DEALIX_HEALTH_PATH=/healthz
```

### الخطوة P5.7 — انتظر تشغيل الـ Cron الأول

راجع **Logs**. يجب أن ترى:

```json
{
  "service": "dealix-watchdog",
  "result": {
    "ok": true
  }
}
```

✅ إذا كانت النتيجة `"ok": true`، الـ watchdog يعمل!

---

## المرحلة 6: اختبارات التحقق النهائية

### الخطوة P6.1 — اختبار API مجدداً

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/version
curl -fsS 'https://api.dealix.me/api/v1/meta'  # يثبت أن GTM surfaces قيد الاستخدام
```

### الخطوة P6.2 — تحقق من سجلات Worker

افتح **founder-os-worker → Logs**. يجب أن تشوف:

```
{"service": "founder-os-worker", "status": "started", ...}
{"service": "founder-os-worker", "timestamp": "2026-05-30T...", "cycle": {...}}
```

كل 15 دقيقة.

### الخطوة P6.3 — تحقق من سجلات Watchdog

افتح **dealix-watchdog → Logs**. يجب أن ترى نتيجة cron كل 15 دقيقة:

```
{"service": "dealix-watchdog", "result": {"ok": true}}
```

### الخطوة P6.4 — تحقق من عدم وجود أخطاء التكرار

في كل خدمة، تأكد من عدم رؤية حلقة من الأخطاء المتكررة (restarts بسرعة).

---

## المرحلة 7: شهادة الإطلاق

### قائمة الفحص النهائية

```
□ dealix-api الأخضر مع متغيرات env كاملة
□ dealix-api /healthz استجاب 200
□ dealix-api /api/v1/meta استجاب 200
□ founder-os-worker أخضر وينبعث JSON كل 15 دقيقة
□ founder-os-worker logs تظهر external_actions_allowed=false
□ dealix-watchdog أخضر وتشغيل cron نجح
□ dealix-watchdog logs تظهر "ok": true
□ لا توجد حلقات restart سريعة على أي خدمة
□ CI/tests تمر بنجاح (أو موثقة)
```

إذا جميع العلامات ✓:

## 🚀 **الإطلاق جاهز**

---

## الملحقات

### الملحق A — أوامر التحقق المحلية

```bash
# تحقق من صحة الـ worker code محلياً
python -m compileall scripts/founder_os_worker.py

# اختبر الـ worker لدورة واحدة (INTERVAL=0 يعني exit بعد دورة)
FOUNDER_OS_INTERVAL_SECONDS=0 python scripts/founder_os_worker.py

# تشغيل اختبارات الـ doctrine
python -m pytest tests/test_founder_os_worker_safe.py -v
python -m pytest tests/test_no_live_send.py tests/test_no_live_charge.py -v

# تحقق من سطح Railway
python scripts/verify_railway_surfaces.py
```

### الملحق B — روابط الوثائق الأخرى

- **مصفوفة الخدمات الكاملة:** `docs/ops/RAILWAY_SERVICE_ENV_MATRIX_AR.md`
- **سياسة الإنتاج:** `docs/ops/RAILWAY_PRODUCTION_POLICY_AR.md`
- **قائمة فحص النشر:** `docs/RAILWAY_DEPLOY_CHECKLIST.md`
- **دستور التجارة (الـ 11 rule):** `docs/00_constitution/NON_NEGOTIABLES.md`

### الملحق C — الخدمات المستقبلية (Out of Scope)

هذه الجلسة غطت:
- ✅ تشكيل dealix-api
- ✅ founder-os-worker (monitoring)
- ✅ dealix-watchdog (drift detection)

المراحل القادمة (إذا لزم):
- ⬜ Web frontend service + DNS
- ⬜ وصل المبيعات (offers, Proof Packs)
- ⬜ تنبيهات Slack للـ watchdog

### الملحق D — طلب المساعدة

إذا واجهت مشكلة:

1. افتح سجلات الخدمة (Logs) وابحث عن error stack
2. شغّل الأوامر من الملحق A محلياً
3. راجع البيئة variables مقابل القسم P2
4. إذا زالت أم، فتح issue في GitHub مع السجلات

---

**آخر تحديث:** 2026-05-30  
**الإصدار:** 1.0 (founder-os-worker + watchdog)
