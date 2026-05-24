# Postgres على Railway — قالب postgres-ssl (إنتاج Dealix)

مرجع آلي: [`dealix/config/railway_postgres_canonical.yaml`](../../dealix/config/railway_postgres_canonical.yaml)  
مرجع API/UI: [`RAILWAY_PRODUCTION_SETTINGS_AR.md`](RAILWAY_PRODUCTION_SETTINGS_AR.md) · [`railway.toml`](../../railway.toml)

---

## صورة المصدر (Source Image)

| البند | القيمة في مشروعك |
|--------|------------------|
| **Registry** | `ghcr.io/railwayapp-templates/postgres-ssl` |
| **Tag الحالي (مثال)** | `:18` (قالب Railway الرسمي SSL) |
| **تحديث متاح** | `:18.4` (Minor Update في لوحة Railway — موصى للإنتاج) |
| **بدائل شائعة** | `:16.14`, `:17.10`, `:latest` (اليوم يشير لـ 16 على `:latest`) |

القالب يضيف **SSL داخل الحاوية** (شهادات تُنشأ عند `init`؛ تجديد تلقائي قبل انتهاء 30 يوماً). التفاصيل الكاملة: [postgres-ssl على GitHub](https://github.com/railwayapp-templates/postgres-ssl).

**ملاحظة المنفذ:** الحاوية تستمع على **5432** داخلياً (ثابت في القالب). `PGPORT` في Variables لا يغيّر منفذ الاستماع داخل الصورة — Railway يوجّه الـ TCP Proxy للمنفذ 5432.

---

## الشبكة (Networking)

### داخل شبكة Railway (موصى لخدمة API)

| النوع | القيمة |
|--------|--------|
| **Private DNS** | `postgres.railway.internal` |
| **اسم مختصر** | `postgres` |
| **الاستخدام** | عبر `DATABASE_URL` كـ **Variable Reference** من خدمة Postgres |

### من الإنترنت (أدوات خارجية فقط)

| النوع | مثال من لوحتك |
|--------|----------------|
| **Public TCP Proxy** | `shinkansen.proxy.rlwy.net:18087` → `:5432` |
| **تحذير** | لا تضع هذا الرابط في Git؛ يتغيّر عند إعادة توليد الدومين |

---

## متغيرات خدمة Postgres (يضيفها Railway)

هذه تظهر في **Variables** لخدمة قاعدة البيانات (قيم سرية — لا تُنسخ إلى المستودع):

| المتغير | الغرض |
|---------|--------|
| `PGDATA` | مسار بيانات Postgres على الـ volume |
| `PGDATABASE` / `POSTGRES_DB` | اسم القاعدة |
| `PGHOST` | host للاتصال (داخلي/مرجع) |
| `PGPASSWORD` / `POSTGRES_PASSWORD` | كلمة مرور |
| `PGPORT` | منفذ في سلسلة الاتصال (غالباً 5432) |
| `PGUSER` / `POSTGRES_USER` | مستخدم |
| `SSL_CERT_DAYS` | عمر شهادة SSL (افتراضي القالب ~820 يوماً) |
| `RAILWAY_DEPLOYMENT_DRAINING_SECONDS` | سلوك Railway عند النشر |

**متغيرات لا تنتمي عادةً لخدمة Postgres:** مفاتيح التطبيق (`MOYASAR_*`, `GROQ_*`, `MINIMAX_*`, …) — ضعها على **خدمة API** فقط، أو استخدم **Shared Variables** مع ربط **Variable Reference** على الخدمة الصحيحة.

---

## ربط خدمة API (dealix)

### مرجع ديناميكي (إلزامي)

في خدمة **dealix** (API):

```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

إذا سمّيت خدمة Postgres باسم آخر، استبدل `Postgres` باسم الخدمة في Railway.

Dealix يحوّل تلقائياً `postgresql://` → `postgresql+asyncpg://` في [`core/config/settings.py`](../../core/config/settings.py).

### شبكة API (من لوحتك)

| البند | القيمة |
|--------|--------|
| **دومين عام** | `https://api.dealix.me` |
| **Target port** | **8080** (منفذ `PORT` الذي تحقنه Railway) |
| **Private DNS** | `dealix.railway.internal` |
| **Healthcheck** | `/healthz` (من `railway.toml`) |

---

## إصلاح انحرافات UI الشائعة (خدمة API)

| الإعداد في Railway UI | عندك الآن (خطأ) | الصحيح |
|------------------------|-----------------|--------|
| **Pre-deploy** | `echo "no migration needed"` | **فارغ** أو `sh /app/scripts/railway_predeploy.sh` |
| **Start Command** | `./start.sh` | **فارغ** (يستخدم Dockerfile `CMD /app/start.sh`) |
| **config-as-code** | — | [`railway.toml`](../../railway.toml) يفرض predeploy الصحيح إن لم يُستبدل في UI |

تحقق:

```bash
python scripts/verify_railway_production_config.py \
  --ui-start-command "./start.sh" \
  --ui-predeploy 'echo "no migration needed"'
bash scripts/railway_ui_alignment.sh
```

---

## ترحيل Alembic

| الطريقة | الأمر / المتغير |
|---------|------------------|
| **افتراضي آمن** | predeploy يطبع `SKIP` |
| **ترحيل عند كل نشر** | `RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1` + `DATABASE_URL` على API |
| **مرة واحدة** | `bash scripts/railway_prod_bootstrap.sh` (مع `DATABASE_URL` محلياً أو في CI) |

---

## PITR / pgBackRest (اختياري — القالب فقط)

مفعّل **فقط** عند تعيين `WAL_ARCHIVE_BUCKET` (+ S3 credentials). بدونها السلوك = Postgres SSL عادي.

أهم المتغيرات (من وثائق القالب):

| المتغير | الغرض |
|---------|--------|
| `WAL_ARCHIVE_BUCKET` | يفعّل الأرشفة |
| `WAL_ARCHIVE_ENDPOINT` / `_REGION` / `_KEY` / `_SECRET` | S3-compatible |
| `WAL_RECOVER_FROM_*` | استعادة من fork |
| `POSTGRES_RECOVERY_TARGET_TIME` | PITR لوقت محدد |

لا تفعّل PITR إلا إذا فهمت سياسة الاحتفاظ — Dealix لا يتطلب PITR للإطلاق الأساسي.

---

## MiniMax / AI Runtime على Railway (خدمة API)

```bash
MINIMAX_API_KEY=sk-api-...
MINIMAX_BASE_URL=https://api.minimax.io/v1
MINIMAX_MODEL=MiniMax-M2.7
AI_PRIMARY_PROVIDER=minimax
AI_FALLBACK_PROVIDER=openai
DEALIX_LLM_PROFILE=minimax
```

تفاصيل: [`LLM_PROVIDERS_SETUP.md`](../LLM_PROVIDERS_SETUP.md) · [`FOUNDER_RAILWAY_LAUNCH_QUICK_AR.md`](FOUNDER_RAILWAY_LAUNCH_QUICK_AR.md)

---

## تحقق بعد الربط

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/health/deep | jq '.checks.postgres'
python scripts/railway_launch_env_check.py   # مع تصدير DATABASE_URL محلياً إن لزم
```

---

## مراجع

- قالب postgres-ssl: https://github.com/railwayapp-templates/postgres-ssl  
- [`docs/RAILWAY_DEPLOY_GUIDE_AR.md`](../RAILWAY_DEPLOY_GUIDE_AR.md)  
- [`DEPLOYMENT.md`](../../DEPLOYMENT.md)
