# Dealix — قائمة Go-Live النهائية الموحّدة

> هذا المستند هو المرجع الوحيد ليوم الإطلاق. يحلّ محل كل الملفات المتفرّقة.
> قسمان: ✅ مكتمل في الريبو · ⏳ إجراءات المؤسس (صلاحيات خارجية).

**آخر تحديث:** يونيو 2026 | **الفرع:** `claude/zen-mayer-TRJdJ` | **PR:** #678

---

## ✅ القسم أ — مكتمل في الريبو (لا تحتاج تفعله)

### الموقع العام
- [x] Next.js 15 ثنائي اللغة (ar/en، RTL للعربي) — 15+ صفحة عامة
- [x] الرئيسية `/` — صادقة، بلا إثباتات مختلَقة
- [x] الخدمات `/services` — السلّم الخماسي كاملاً
- [x] الأسعار `/pricing` — مصدر واحد `registry.py` + `content/pricing.ts`
- [x] نموذج الكوستم `/custom` → `POST /api/v1/public/custom-brief`
- [x] التشخيص المجاني `/dealix-diagnostic`
- [x] حجز التشخيص `/contact` → Calendly
- [x] من نحن `/about` · الشركاء `/partners` · تعلّم `/learn`
- [x] الثقة والامتثال `/trust` · الخصوصية `/privacy` · شروط الخدمة `/terms`
- [x] صفحة عودة الدفع `/checkout/return` (Moyasar callback)

### مسار الدفع
- [x] `CheckoutPanel` موصول بـ `POST /api/v1/checkout` (بلا مفتاح Admin)
- [x] تسلسل كامل: اختر العرض → `CheckoutPanel` → Moyasar → `/checkout/return`
- [x] Webhook: `POST /api/v1/webhooks/moyasar` موجود

### الهوية والمصداقية
- [x] كحلي `#001F3F` + ذهبي `#D4AF37` موحّدان في كل الملفات
- [x] إزالة كل الإثباتات المختلَقة (شعارات، إحصاءات، شهادات وهمية)
- [x] مفاتيح nav وfooter مُصلَحة

### الجودة
- [x] 34 اختبار يمرّ (العقيدة + custom-brief + لا واتساب بارد + لا scraping)
- [x] TypeScript: `npx tsc --noEmit` → نظيف
- [x] CI: Gitleaks CLI v8.24.0 (بلا ترخيص مدفوع) + Trivy v0.36.0

### عُدّة التشغيل اليومي
- [x] لوحة المؤسس `/ops/founder` (مع بطاقة إعداد المفتاح + بطاقة عدّة الاتصال)
- [x] `docs/ops/CALL_KIT_AR.md` — Top 10 أهداف + سكربتات عربية + ردود اعتراضات + مسودّات LinkedIn
- [x] `scripts/warm_list_outreach.py` — يولّد مسودّات `data/outreach/warm_list_drafts.md`
- [x] `docs/business/PRESS_RELEASE_AR.md` + `EN.md` — جاهزان للنشر بعد موافقة المؤسس

---

## ⏳ القسم ب — إجراءات المؤسس (صلاحيات خارجية)

### 1. Railway — خدمة الـ API

اذهب إلى Railway → خدمة API → Variables وأضف:

```
# إلزامي
DATABASE_URL=           # (Railway Postgres → Copy → Database URL)
REDIS_URL=              # (Railway Redis → Copy → Redis URL)
APP_SECRET_KEY=         # openssl rand -hex 32
JWT_SECRET_KEY=         # openssl rand -hex 32
ADMIN_API_KEYS=sk-admin-xxxx,sk-admin-yyyy   # أنشئ مفتاحين على الأقل
APP_ENV=production
APP_URL=https://dealix.me

# Moyasar (بعد إكمال KYC)
MOYASAR_SECRET_KEY=sk_live_xxxx
MOYASAR_WEBHOOK_SECRET=whsec_xxxx
MOYASAR_LIVE_MODE=1

# إشعارات (مهم)
DEALIX_FOUNDER_EMAIL=bassam.m.assiri@gmail.com
RESEND_API_KEY=re_xxxx

# اختياري لكن مفيد
SENTRY_DSN=https://xxx@sentry.io/xxx
```

### 2. Railway — خدمة الواجهة (Frontend)

```
NEXT_PUBLIC_API_URL=https://api.dealix.me
NEXT_PUBLIC_SITE_URL=https://dealix.me
NEXT_PUBLIC_DEALIX_ADMIN_API_KEY=sk-admin-xxxx   # ← نفس قيمة من ADMIN_API_KEYS
```

> **ملاحظة مهمة:** `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` يجعل لوحة `/ops/founder` تعمل. بدونه تظهر رسالة خطأ.

### 3. DNS (عند موفّر دومينك)

| السجل | النوع | القيمة |
|-------|-------|--------|
| `dealix.me` | CNAME / A | Railway Web Service URL |
| `api.dealix.me` | CNAME / A | Railway API Service URL |

> انسخ الـ domain من Railway → كل خدمة → Settings → Domain

### 4. Moyasar

1. اذهب إلى [moyasar.com](https://moyasar.com) → أكمل KYC (وثائق الشركة)
2. بعد القبول: احصل على `sk_live_...`
3. أضفه في Railway كـ `MOYASAR_SECRET_KEY`
4. سجّل Webhook:
   - URL: `https://api.dealix.me/api/v1/webhooks/moyasar`
   - Events: `payment.succeeded`, `payment.failed`
   - احفظ `MOYASAR_WEBHOOK_SECRET`

### 5. GitHub Actions Secrets

اذهب إلى GitHub → repo → Settings → Secrets → Actions:

| الاسم | القيمة |
|-------|--------|
| `DEALIX_API_BASE` | `https://api.dealix.me` |
| `DEALIX_API_KEY` | أحد مفاتيح `API_KEYS` |
| `DEALIX_ADMIN_API_KEY` | أحد مفاتيح `ADMIN_API_KEYS` |
| `RESEND_API_KEY` | مفتاح Resend |

> بدون هذه الأسرار، workflows الـ CI تتخطّى الخطوات بأمان (لا تفشل).

### 6. بيانات أوّلية (مرة واحدة)

- [ ] استورد `docs/ops/lead_machine/TODAY_15_TARGETS.csv` في War Room (`/ar/ops/war-room`)
- [ ] أنشئ `data/warm_list.csv` من الشبكة الشخصية (انسخ من `data/warm_list.csv.template`)
- [ ] شغّل `python scripts/warm_list_outreach.py` → مسودّات في `data/outreach/warm_list_drafts.md`

---

## ✔ فحص Go/No-Go (قبل الإعلان العام)

شغّل هذه الأوامر بالترتيب:

```bash
# 1. API يعمل
curl https://api.dealix.me/healthz
# → {"status":"ok"}

# 2. الواجهة تعمل
curl -o /dev/null -s -w "%{http_code}" https://dealix.me/ar
# → 200

# 3. Moyasar test mode
python scripts/verify_moyasar_e2e.py
# → ✓ Moyasar test payment round-trip OK

# 4. مسار الدفع كاملاً (اختبار يدوي)
# اذهب إلى https://dealix.me/ar/pricing
# اضغط "ابدأ Sprint 499 ريال" → أكمل بطاقة اختبار Moyasar
# تحقق من الوصول إلى /ar/checkout/return مع status=paid
```

---

## 🚀 تسلسل الإطلاق (يوم T-0)

```
09:00  → تحقق من Go/No-Go أعلاه
09:15  → انشر PRESS_RELEASE_AR.md على LinkedIn (يدوياً بعد مراجعة)
09:20  → أرسل أول DM يدوي لـ Lucidya (الأولوية — صلة العائلة)
09:30  → أرسل DM لـ Foodics
10:00  → شارك بوست LinkedIn الإطلاق (من docs/sales-kit/linkedin_longform_posts.md)
12:00  → راجع /ar/ops/founder — هل وصل أي lead؟
EOD    → رصيد الأهداف المتصل بها اليوم في docs/ops/CALL_KIT_AR.md
```

---

## 🔗 روابط مرجعية سريعة

| الغرض | الرابط |
|-------|--------|
| لوحة المؤسس | `/ar/ops/founder` |
| الموافقات | `/ar/approvals` |
| غرفة الإيراد | `/ar/ops/war-room` |
| عدّة الاتصال | `docs/ops/CALL_KIT_AR.md` |
| مسودّات الشبكة الدافئة | `data/outreach/warm_list_drafts.md` |
| سجل الاعتراضات | `docs/ops/objection_library_ar.md` |
| Playbooks القطاعات | `docs/ops/sector_playbooks.md` |
| Proof Pack SOP | `docs/PILOT_DELIVERY_SOP.md` |

---

_Dealix — Consistent. Confident. Distinctly Saudi._
