# 💳 Dealix — Moyasar Hosted Checkout (بدون Backend)

**المشكلة:** Railway backend لسه غير منشور، ما تقدر تستقبل payments عبر API.
**الحل:** Moyasar يوفّر **hosted invoices** — رابط دفع جاهز بدون أي code.
**الوقت:** 5 دقائق setup، ثم تستقبل فلوس فوراً.

---

## 🚀 الطريقة 1 — Moyasar Invoices API (الأسرع)

### الخطوة 1: تأكد حسابك Moyasar verified
1. افتح: https://dashboard.moyasar.com
2. Settings → Business → تأكد من:
   - ✅ CR uploaded (أو وثيقة عمل حر)
   - ✅ Bank account linked
   - ✅ Account active

### الخطوة 2: أنشئ Invoice يدوياً (UI)
1. Moyasar Dashboard → Invoices → **Create Invoice**
2. املأ (راجع `docs/OFFER_LADDER_AND_PRICING.md` للأسعار المعتمدة):
   - **Amount:** `499.00 SAR` (7-Day Revenue Proof Sprint) أو `1500.00` (Data-to-Revenue Pack)
   - **Description:** `Dealix — 7-Day Revenue Proof Sprint`
   - **Customer email:** email العميل
   - **Expires:** 7 days
3. Save → احصل على:
   - **Invoice ID:** `inv_xxxx`
   - **Payment URL:** `https://invoice.moyasar.com/invoices/inv_xxxx`

### الخطوة 3: أرسل الرابط للعميل
عبر WhatsApp / Email / LinkedIn:
```
رابط الدفع: https://invoice.moyasar.com/invoices/inv_xxxx
المبلغ: 499 ريال
الخدمة: 7-Day Revenue Proof Sprint
المدة: 7 أيام — تقرير تشخيصي + مسودات رسائل جاهزة لموافقتك + Proof Pack
```

**النتيجة:** العميل يدفع → Moyasar يخبرك → الفلوس تصل بنكك خلال 24 ساعة.

---

## 🔄 الطريقة 2 — Invoice API via curl (للأتمتة الخفيفة)

استخدمها لو تبغى توليد روابط من CLI بدون backend كامل:

```bash
# Set your keys
export MOYASAR_SECRET=sk_live_xxxxxxxxx   # من Moyasar Dashboard → API Keys

# Create an invoice for the 499 SAR 7-Day Revenue Proof Sprint
curl -X POST https://api.moyasar.com/v1/invoices \
  -u "$MOYASAR_SECRET:" \
  -d "amount=49900" \
  -d "currency=SAR" \
  -d "description=Dealix — 7-Day Revenue Proof Sprint" \
  -d "callback_url=https://voxc2.github.io/dealix/thank-you.html" \
  -d "metadata[plan]=sprint_499" \
  -d "metadata[customer_email]=$CUSTOMER_EMAIL"
```

**Response مثال:**
```json
{
  "id": "inv_abc123",
  "amount": 49900,
  "url": "https://invoice.moyasar.com/invoices/inv_abc123",
  "status": "initiated"
}
```

**انسخ `url` → أرسله للعميل.**

---

## 📝 قوالب Invoices الجاهزة

### 7-Day Revenue Proof Sprint (499 ريال)
```bash
curl -X POST https://api.moyasar.com/v1/invoices \
  -u "$MOYASAR_SECRET:" \
  -d "amount=49900" \
  -d "currency=SAR" \
  -d "description=Dealix — 7-Day Revenue Proof Sprint"
```

### Data-to-Revenue Pack (1,500 ريال)
```bash
curl -X POST https://api.moyasar.com/v1/invoices \
  -u "$MOYASAR_SECRET:" \
  -d "amount=150000" \
  -d "currency=SAR" \
  -d "description=Dealix — Data-to-Revenue Pack"
```

### Managed Revenue Ops (2,999 ريال/شهر)
```bash
curl -X POST https://api.moyasar.com/v1/invoices \
  -u "$MOYASAR_SECRET:" \
  -d "amount=299900" \
  -d "currency=SAR" \
  -d "description=Dealix — Managed Revenue Ops — اشتراك شهر أول"
```

### Executive Command Center (7,500 ريال/شهر)
```bash
curl -X POST https://api.moyasar.com/v1/invoices \
  -u "$MOYASAR_SECRET:" \
  -d "amount=750000" \
  -d "currency=SAR" \
  -d "description=Dealix — Executive Command Center — اشتراك شهر أول"
```

**ملاحظة:** المبلغ في Moyasar API بالـ **halalas** (1 SAR = 100 halalas).

---

## 🔔 Webhook بدون Backend

لأتمتة basic (تنبيه عند الدفع):

### الخيار 1 — Zapier (5 دقائق setup)
1. https://zapier.com → Create Zap
2. Trigger: **Webhooks by Zapier** → Catch Hook
3. انسخ Webhook URL
4. في Moyasar Dashboard → Webhooks → أضف الرابط
5. Action: Send you Email/WhatsApp/Slack عند كل دفعة

### الخيار 2 — Discord/Slack webhook مباشر
Moyasar يدعم webhooks مباشرة. أرسل إشعار لـ Slack:
1. Slack → Incoming Webhooks → Create
2. Moyasar → Webhooks → paste Slack URL

**النتيجة:** إشعار فوري على كل دفعة بدون أي code.

---

## 💰 Flow كامل (Live الآن بدون Railway)

```
1. عميل يفتح: https://voxc2.github.io/dealix/pricing.html
   ↓
2. يختار "7-Day Revenue Proof Sprint — 499 ريال"
   ↓
3. يضغط الـ CTA → (رابط تواصل معك على WhatsApp/Calendly)
   ↓
4. أنت تنشئ invoice يدوياً (30 ثانية)
   ↓
5. ترسل الرابط للعميل عبر WhatsApp
   ↓
6. العميل يدفع → Moyasar يرسل webhook لـ Zapier
   ↓
7. Zapier يرسل لك WhatsApp/Email
   ↓
8. تتواصل مع العميل، تبدأ onboarding manually
   ↓
9. الفلوس تصل بنكك خلال 24 ساعة
```

**ما يحتاج:** Railway، backend، API، كود.
**يحتاج:** Moyasar account + 5 دقائق setup + رد سريع.

---

## 📊 Track Payments يدوياً

حتى backend يصير live، استخدم Google Sheet بسيط:

| التاريخ | العميل | الشركة | المبلغ | Invoice ID | Status | Plan |
|---------|---------|---------|---------|------------|---------|------|
| 2026-04-24 | عبدالله | Lucidya | 499 SAR | inv_abc123 | paid | sprint_499 |
| ... | ... | ... | ... | ... | ... | ... |

---

## 🎯 الخلاصة

**الواقع:** تقدر تستلم أول 10 عملاء بدون Railway deploy.
**الطريقة:** Moyasar hosted invoices + manual onboarding.
**الميزة:** تركّز على البيع + Customer Success، ما تنشغل في deploy.
**متى Railway:** بعد أول 5-10 عملاء (لما الأتمتة تصير قيمة حقيقية).

**الآن:**
1. افتح Moyasar dashboard
2. Create invoice تجريبي بمبلغ صغير بـ email نفسك للتحقق من المسار
3. افتح الرابط + اختبر الدفع
4. تأكد الفلوس وصلت بنكك

**هذا Launch حقيقي.** Railway يصير polish لاحقاً.
