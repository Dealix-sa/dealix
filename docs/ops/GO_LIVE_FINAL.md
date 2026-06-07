# قائمة الإطلاق النهائية الموحّدة — Dealix Go-Live Master Checklist

**المسؤول:** سامي العسيري | **آخر تحديث:** 2026-06-07
**الغرض:** هذا هو المستند الوحيد الذي تطبعه وتضع علامة عليه يوم الإطلاق. قسمان: ما بُني في الريبو، وما تحتاج تفعله أنت فقط.

> مستندات مرجعية مكملة (لا تُلغيها هذه القائمة):
> [PRODUCTION_READINESS_CHECKLIST.md](PRODUCTION_READINESS_CHECKLIST.md) · [MOYASAR_KYC_CHECKLIST.md](MOYASAR_KYC_CHECKLIST.md) · [RAILWAY_SERVICE_ENV_MATRIX_AR.md](RAILWAY_SERVICE_ENV_MATRIX_AR.md)

---

## ✅ القسم أ — مكتمل في الريبو | Already Built

هذه البنود موجودة ومختبرة. تحقق منها بصرياً — لا إجراء مطلوب منك لتفعيلها.

### الموقع العام (Next.js 15)
- [x] موقع Next.js 15 ثنائي اللغة (ar/en، RTL للعربي) — 15+ صفحة عامة تحت `frontend/src/app/[locale]/`
- [x] الرئيسية `/` — صادقة، بلا إحصاءات مختلَقة، بلا شهادات عملاء وهمية
- [x] الخدمات `/services` — السلّم الخماسي كاملاً
- [x] الأسعار `/pricing` — مصدر واحد: `auto_client_acquisition/service_catalog/registry.py` (`OFFERINGS`) + `frontend/src/content/pricing.ts` (IDs وأسعار متزامنة)
- [x] نموذج Custom AI intake — `/custom` → `POST /api/v1/public/custom-brief` (draft-first، مُنضَّم لمراجعة المؤسس قبل أي إرسال)
- [x] صفحة عودة الدفع `/checkout/return` (Moyasar callback)
- [x] صفحات الثقة والامتثال — `/trust` · `/privacy` · `/terms` باللغتين

### مسار الدفع
- [x] `CheckoutPanel` موصول بـ `POST /api/v1/checkout` (بلا مفتاح Admin)
- [x] تسلسل كامل: اختر العرض → `CheckoutPanel` → Moyasar → `/checkout/return`
- [x] Webhook endpoint: `POST /api/v1/webhooks/moyasar` موجود ومختبر

### الهوية البصرية والمصداقية
- [x] الهوية موحّدة — Navy `#001F3F` + Gold `#D4AF37` + Sand `#F4F0E8`؛ لوحة الخضراء القديمة محذوفة
- [x] لا شعارات عملاء مختلَقة، لا إحصاءات قبل الإطلاق، لا شهادات وهمية

### الحوكمة والاختبارات
- [x] اختبارات العقيدة — 34/34 ناجحة (مصدر: `dealix/commercial_ops/doctrine.py`)
  - `tests/test_*doctrine*` · `tests/test_no_cold_whatsapp.py`
  - `tests/test_no_scraping_engine.py` · `tests/test_no_guaranteed_claims.py`
- [x] CI — Gitleaks (free CLI) + Trivy v0.36.0 أخضر
- [x] لا أسرار في الريبو
- [x] لا مفاتيح Admin داخل متغيرات `NEXT_PUBLIC_*`

### أدوات التشغيل اليومي
- [x] لوحة المؤسس — `/ops/founder`
- [x] محرك التواصل الدافئ — `scripts/warm_list_outreach.py` (مسودات فقط، لا إرسال تلقائي)

---

## ⏳ القسم ب — إجراءات المؤسس (صلاحيات خارجية) | Founder-Only Actions

هذه الخطوات تتطلب وصولك الشخصي لمنصات خارجية — لا يُنفّذها الكود.

---

### ب-1 — Railway: خدمة الـ API

افتح Railway → مشروعك → خدمة `dealix-api` → Variables وأضف:

```
# إلزامي — أمان النظام
DATABASE_URL=               # Railway Postgres → Copy → Database URL (تلقائي عند الربط)
REDIS_URL=                  # Railway Redis → Copy → Redis URL (تلقائي عند الربط)
APP_SECRET_KEY=             # python -c "import secrets; print(secrets.token_hex(32))"
JWT_SECRET_KEY=             # نفس الأمر، قيمة مختلفة
ADMIN_API_KEYS=             # مفتاحان على الأقل مفصولان بفاصلة؛ احفظهما في 1Password
APP_URL=https://dealix.me   # يستخدمه webhook callback

# Moyasar — بعد إكمال KYC فقط
MOYASAR_SECRET_KEY=sk_live_xxxx
MOYASAR_WEBHOOK_SECRET=     # python -c "import secrets; print(secrets.token_hex(32))"
MOYASAR_LIVE_MODE=1         # لا تُفعّل قبل اكتمال KYC وتسجيل Webhook

# إشعارات
DEALIX_FOUNDER_EMAIL=       # بريدك لتلقي الإشعارات الداخلية
RESEND_API_KEY=             # من resend.com

# اختياري — موصى به
SENTRY_DSN=                 # من sentry.io لتتبع الأخطاء
```

---

### ب-2 — Railway: خدمة الواجهة (Frontend)

افتح Railway → مشروعك → خدمة `dealix-frontend` → Variables وأضف:

```
NEXT_PUBLIC_API_URL=https://api.dealix.me
NEXT_PUBLIC_SITE_URL=https://dealix.me
NEXT_PUBLIC_DEALIX_ADMIN_API_KEY=    # إحدى قيم ADMIN_API_KEYS — مطلوب لعمل /ops/founder
```

> تنبيه: `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` مطلوب لتشغيل لوحة `/ops/founder` على المتصفح. لا تضع أي مفاتيح Admin خاصة أخرى في متغيرات `NEXT_PUBLIC_*`.

---

### ب-3 — DNS (عند مزود دومينك)

| السجل | النوع | الوجهة |
|-------|-------|---------|
| `dealix.me` | A أو CNAME | Railway Frontend Service URL |
| `api.dealix.me` | A أو CNAME | Railway API Service URL |

انسخ الـ URL من Railway → كل خدمة → Settings → Domains. بعد الضبط انتظر 5–60 دقيقة ثم تحقق بالأوامر في بند Go/No-Go.

---

### ب-4 — Moyasar: إكمال KYC وتسجيل Webhook

- [ ] ادخل `dashboard.moyasar.com` → Settings → Verification
- [ ] أكمل KYC: سجل تجاري + هوية وطنية + حساب بنكي سعودي باسم الشركة + شهادة ضريبة القيمة المضافة
- [ ] بعد القبول: احصل على `sk_live_...` من API Keys وضعه في Railway
- [ ] سجّل Webhook في Moyasar:
  - URL: `https://api.dealix.me/api/v1/webhooks/moyasar`
  - Events: `payment_paid` · `payment_failed` · `payment_refunded`
  - Secret: نفس قيمة `MOYASAR_WEBHOOK_SECRET` في Railway بالضبط — أي اختلاف يُنتج 401
- [ ] فعّل `MOYASAR_LIVE_MODE=1` في Railway بعد اكتمال الخطوات أعلاه فقط

تفاصيل KYC الكاملة: [MOYASAR_KYC_CHECKLIST.md](MOYASAR_KYC_CHECKLIST.md)

---

### ب-5 — GitHub Actions Secrets

في الريبو → Settings → Secrets and Variables → Actions، أضف:

| اسم السر | القيمة |
|---------|--------|
| `DEALIX_API_BASE` | `https://api.dealix.me` |
| `DEALIX_API_KEY` | أحد مفاتيح `ADMIN_API_KEYS` |
| `DEALIX_ADMIN_API_KEY` | أحد مفاتيح `ADMIN_API_KEYS` |
| `RESEND_API_KEY` | نفس القيمة في Railway |

> بدون هذه الأسرار، workflows الـ CI تتخطى الخطوات بأمان — لا تفشل.

---

### ب-6 — بيانات أوّلية (مرة واحدة)

- [ ] استورد `docs/ops/lead_machine/TODAY_15_TARGETS.csv` في لوحة War Room
- [ ] شغّل `python scripts/warm_list_outreach.py` → مسودات في `data/outreach/warm_list_drafts.md` — راجعها قبل أي إرسال

---

## بند Go/No-Go — قبل الإعلان العام | Launch Gate

نفّذ هذه الأوامر الثلاثة. إذا فشل أي منها، لا تُعلن الإطلاق.

```bash
# 1. صحة API
curl https://api.dealix.me/healthz
# المتوقع: {"status":"ok"}

# 2. الموقع العام
curl -o /dev/null -sw "%{http_code}" https://dealix.me/ar
# المتوقع: 200

# 3. مسار الدفع — وضع تجريبي
python scripts/verify_moyasar_e2e.py
# المتوقع: جميع الخطوات ناجحة، exit 0
```

تحقق بصري إضافي:
- [ ] `https://dealix.me/ar` يظهر الصفحة الرئيسية بالعربية بشكل صحيح
- [ ] `https://dealix.me/pricing` يعرض الأسعار الصحيحة كما في `registry.py`
- [ ] نموذج `/custom` يُرسِل للـ API ويُعيد رسالة تأكيد — ولا يُرسَل للعميل تلقائياً
- [ ] `/ops/founder` يفتح بدون خطأ (يتطلب `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY`)

---

## ترتيب التنفيذ الموصى به | Recommended Sequence

| الترتيب | الخطوة | الوقت التقديري |
|---------|-------|----------------|
| 1 | Railway API — إضافة متغيرات البيئة الإلزامية (ب-1) | 15 دقيقة |
| 2 | Railway Frontend — إضافة متغيرات البيئة (ب-2) | 5 دقائق |
| 3 | Railway — تأكيد deploy أخضر لكلا الخدمتين | 10 دقائق |
| 4 | DNS — ضبط السجلات وانتظار الانتشار (ب-3) | 5–60 دقيقة |
| 5 | Moyasar — KYC وربط Webhook (ب-4) | 1–3 أيام عمل |
| 6 | GitHub Actions — إضافة أسرار CI (ب-5) | 5 دقائق |
| 7 | تنفيذ بند Go/No-Go | 5 دقائق |
| 8 | الإعلان العام | بعد نجاح الخطوة 7 فقط |

---

## قواعد ثابتة ليوم الإطلاق | Hard Rules

- لا دفع حي (`MOYASAR_LIVE_MODE=1`) قبل اكتمال KYC Moyasar وتسجيل Webhook واختباره.
- لا إعلان عام للموقع قبل نجاح بند Go/No-Go الثلاثي.
- لا إرسال خارجي تلقائي بأي شكل — كل تواصل مع العملاء يمر بمراجعة المؤسس.
- كل مخرجات نموذج `/custom` تبقى مسودة حتى يعتمدها المؤسس صراحةً.

---

## روابط مرجعية سريعة

| الغرض | المرجع |
|-------|--------|
| لوحة المؤسس | `/ops/founder` |
| كيت الاتصال اليومي | [`docs/ops/CALL_KIT_AR.md`](CALL_KIT_AR.md) |
| قائمة KYC Moyasar التفصيلية | [`docs/ops/MOYASAR_KYC_CHECKLIST.md`](MOYASAR_KYC_CHECKLIST.md) |
| متغيرات Railway الكاملة | [`docs/ops/RAILWAY_SERVICE_ENV_MATRIX_AR.md`](RAILWAY_SERVICE_ENV_MATRIX_AR.md) |
| جاهزية الإنتاج الشاملة | [`docs/ops/PRODUCTION_READINESS_CHECKLIST.md`](PRODUCTION_READINESS_CHECKLIST.md) |
| Proof Pack SOP | [`docs/PILOT_DELIVERY_SOP.md`](../PILOT_DELIVERY_SOP.md) |
| مسودّات الشبكة الدافئة | `data/outreach/warm_list_drafts.md` |

---

*مراجع ذات صلة: [GO_LIVE_CHECKLIST_AR.md](GO_LIVE_CHECKLIST_AR.md) · [FOUNDER_A_TO_Z_LAUNCH_RUNBOOK_AR.md](FOUNDER_A_TO_Z_LAUNCH_RUNBOOK_AR.md)*

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value**
