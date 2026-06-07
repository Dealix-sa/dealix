# 🚀 Dealix — انشر الآن (Go-Live النهائي المُتحقَّق)

> **التاريخ:** 2026-06-07 · **الفرع:** `claude/beautiful-knuth-4AFzc` (PR #679)
> **الحالة:** كل ملفات النشر **متحقَّقة وصحيحة ومتسقة على `dealix.me`**. ما ينقص = مفاتيحك فقط.
> هذا المستند هو **المصدر الوحيد الموثوق** للنشر الحي — يلغي الـ runbooks القديمة المتضاربة.

---

## ✅ ما هو جاهز بالفعل (تحققت منه بنفسي)

| المكوّن | الحالة | الدليل |
|---|---|---|
| `railway.json` (API) | ✅ Dockerfile + uvicorn + healthcheck `/healthz` | متحقَّق |
| `frontend/railway.json` + `frontend/Dockerfile` | ✅ multi-stage، ARGs على `dealix.me`/`api.dealix.me` | متحقَّق |
| `railway_deploy.yml` (API workflow) | ✅ يقلع عند توفر `RAILWAY_TOKEN` + smoke كامل | متحقَّق |
| `railway_deploy_frontend.yml` | ✅ ينشر `frontend/` + smoke لـ `dealix.me/ar` | متحقَّق |
| عقد البيئة | ✅ `check_env_contract.py` exit 0 | متحقَّق |
| توحيد النطاق | ✅ صفر `dealix.sa` في ملفات النشر | متحقَّق |
| أمان Next.js | ✅ 15.5.19 (0 ثغرات CRITICAL/HIGH) | متحقَّق |

**الخلاصة:** ما راح تعدّل أي كود. تضيف مفاتيح فقط، وكل شي يشتغل تلقائياً.

---

## الخطوة 1 — جهّز الأسرار (٥ دقائق)

شغّل هذا على جهازك لتوليد مفاتيح حقيقية (**لا تستخدم القيم في أي مكان عام**):

```bash
python3 -c "import secrets; \
print('APP_SECRET_KEY =', secrets.token_hex(32)); \
print('JWT_SECRET_KEY =', secrets.token_hex(32)); \
print('API_KEYS       = dlx_'+secrets.token_hex(16)); \
print('ADMIN_API_KEYS = dlxadm_'+secrets.token_hex(16))"
```

> **لماذا هذي بالذات؟** `api/main.py::_validate_production_secrets` **يرفض إقلاع الإنتاج** بدونها — هذي ليست اختيارية.

---

## الخطوة 2 — Railway: المشروع + قاعدة البيانات (١٠ دقائق)

1. ادخل [railway.app](https://railway.app) → **New Project**.
2. **+ New → Database → PostgreSQL** (Railway يحقن `DATABASE_URL` تلقائياً للخدمات في نفس المشروع).
3. أنشئ خدمتين من الـ repo (`Dealix-sa/dealix`, فرع `main` بعد الدمج):
   - خدمة **`dealix`** (الـ API) — Railway يلتقط `railway.json` (Dockerfile root).
   - خدمة **`web`** (الواجهة) — Root Directory = `frontend/` — يلتقط `frontend/railway.json`.

---

## الخطوة 3 — متغيّرات بيئة خدمة الـ API (`dealix`)

في Railway → خدمة `dealix` → **Variables**، الصق:

```bash
# ── [إلزامي — لا يقلع بدونها] ──
ENVIRONMENT=production
APP_SECRET_KEY=<من الخطوة 1>
JWT_SECRET_KEY=<من الخطوة 1>
API_KEYS=<من الخطوة 1>
ADMIN_API_KEYS=<من الخطوة 1>

# ── [إلزامي للوظائف] ──
DATABASE_URL=${{Postgres.DATABASE_URL}}      # مرجع Railway التلقائي
CORS_ORIGINS=https://dealix.me,https://www.dealix.me
DEALIX_APPROVAL_STORE_BACKEND=postgres        # موافقات دائمة (إصلاح Phase 0)
RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1              # ⚠️ حرج: ينشئ جداول DB أول نشر

# ── [اختياري — يُفعّل ميزات إضافية عند توفره] ──
ANTHROPIC_API_KEY=sk-ant-...                   # تقييم ذكي + صياغة درافتات
GOOGLE_MAPS_API_KEY=...                         # اكتشاف عملاء سعوديين بأرقام حقيقية
MOYASAR_SECRET_KEY=sk_live_...                  # تحصيل مدفوعات حقيقي
POSTHOG_API_KEY=phc_...                          # تحليلات
SENTRY_DSN=https://...                            # مراقبة الأخطاء
```

---

## الخطوة 4 — متغيّرات خدمة الواجهة (`web`)

القيم الافتراضية في `frontend/Dockerfile` صحيحة أصلاً، لكن ثبّتها صراحةً:

```bash
NEXT_PUBLIC_API_URL=https://api.dealix.me
NEXT_PUBLIC_SITE_URL=https://dealix.me
NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1
```

---

## الخطوة 5 — مفتاح GitHub للنشر التلقائي (دقيقتان)

1. Railway → **Account → Tokens** → أنشئ توكن باسم `github-deploy`.
2. GitHub → `Dealix-sa/dealix` → **Settings → Secrets and variables → Actions → New repository secret**:
   - `RAILWAY_TOKEN` = `<التوكن>`
3. (اختياري) إن اختلفت أسماء الخدمات، أضف repo variables:
   - `RAILWAY_SERVICE_NAME=dealix` · `RAILWAY_FRONTEND_SERVICE=web`

> بمجرد إضافة `RAILWAY_TOKEN`، أي push لـ `main` ينشر تلقائياً (workflows جاهزة). أو شغّلها يدوياً: **Actions → "Deploy to Railway" → Run workflow**.

---

## الخطوة 6 — تحويل DNS (بعد نجاح أول نشر)

عند مزوّد نطاق `dealix.me`:

| النوع | الاسم | القيمة |
|---|---|---|
| CNAME | `@` أو `www` | `<frontend>.up.railway.app` (من Railway → web → Settings → Domains) |
| CNAME | `api` | `<api>.up.railway.app` (من Railway → dealix → Settings → Domains) |

في Railway: لكل خدمة → **Settings → Networking → Custom Domain** → أضف `dealix.me` (web) و`api.dealix.me` (dealix). Railway يصدر شهادة TLS تلقائياً.

> التفاصيل الكاملة: `docs/ops/DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md`.

---

## الخطوة 7 — التحقق (بعد النشر + DNS)

```bash
# الـ API حي + طبقة الثقة
python3 scripts/dealix_smoke_test.py --base-url https://api.dealix.me
curl -s https://api.dealix.me/healthz | python3 -m json.tool
curl -s https://api.dealix.me/api/v1/meta -o /dev/null -w "meta=%{http_code}\n"

# الواجهة حية
curl -s -o /dev/null -w "ar=%{http_code}\n" https://dealix.me/ar

# بوابة الإطلاق التجاري الشاملة
bash scripts/verify_dealix_commercial_go_live.sh
```

**نجاح =** `/healthz` يرجع `version`، `/api/v1/meta`=200، `dealix.me/ar`=200، والـ workflow smoke أخضر.

---

## ملخص مدخلاتك (مرتّبة بالأولوية)

| # | المدخل | يفتح | إلزامي للإطلاق؟ |
|---|---|---|---|
| 1 | المفاتيح الأربعة (الخطوة 1) | إقلاع الإنتاج | **نعم** |
| 2 | `RAILWAY_TOKEN` | النشر التلقائي | **نعم** |
| 3 | PostgreSQL (إضافة Railway) | `DATABASE_URL` + حفظ دائم | **نعم** |
| 4 | وصول DNS لـ `dealix.me` | الموقع على نطاقك | **نعم** |
| 5 | `ANTHROPIC_API_KEY` | ذكاء التقييم/الصياغة | لا (لكن مهم) |
| 6 | `GOOGLE_MAPS_API_KEY` | عملاء حقيقيون بأرقام | لا (لكن مهم) |
| 7 | `MOYASAR_SECRET_KEY` | تحصيل مدفوعات | لا (لاحقاً) |

---

## ماذا لو ما عندك Railway بعد؟

كل ملفات النشر جاهزة ومتحقَّقة. لحظة ما تضيف المفاتيح أعلاه، الإطلاق يصير أمر واحد. لا يوجد عمل كود متبقٍّ من جهتي لهذي المرحلة.
