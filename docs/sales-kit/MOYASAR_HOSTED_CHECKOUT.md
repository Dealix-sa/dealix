# Dealix — Moyasar Hosted Checkout (بدون Backend)

**المشكلة:** الـ backend لسه غير منشور، ما تقدر تستقبل payments عبر API.
**الحل:** Moyasar يوفّر **hosted invoices** — رابط دفع جاهز بدون أي code.
**الوقت:** setup سريع، ثم تستقبل فلوس فوراً.

> **تنبيه مهم — الـ 1 ريال:** أي فاتورة بقيمة `1.00 SAR` (الـ `pilot_1sar` charge) المذكورة في هذا الملف هي **اختبار داخلي للتحقّق من قناة الدفع فقط** — يدفعها الفريق بنفسه للتأكد أن Moyasar والـ webhook والبنك يعملون. **هي ليست عرضاً تجارياً للعملاء.** عرض الدخول للعميل هو **Revenue Proof Sprint بـ 499 ريال (مرة واحدة)**.

> **الأسعار القانونية الوحيدة:** Free Mini Diagnostic 0 ← Revenue Proof Sprint 499 ريال (مرة واحدة) ← Data-to-Revenue Pack 1,500 ← Growth Ops Monthly 2,999/شهر ← Support OS Add-on 1,500/شهر ← Executive Command Center 7,500/شهر ← Agency Partner OS مخصّص.

---

## الطريقة 1 — Moyasar Invoices API (الأسرع)

### الخطوة 1: تأكد حسابك Moyasar verified
1. افتح: https://dashboard.moyasar.com
2. Settings → Business → تأكد من:
   - CR uploaded (أو وثيقة عمل حر)
   - Bank account linked
   - Account active

### الخطوة 2 (داخلي): اختبار التحقّق `pilot_1sar`
> هذه خطوة تحقّق داخلية — يدفعها الفريق بنفسه، **ليست للعملاء**.
1. Moyasar Dashboard → Invoices → **Create Invoice**
2. املأ:
   - **Amount:** `1.00 SAR` — اختبار داخلي للتحقّق من قناة الدفع (`pilot_1sar`)
   - **Description:** `Dealix internal payment-channel test — pilot_1sar`
   - **Customer email:** بريد الفريق
   - **Expires:** 7 days
3. Save → احصل على Invoice ID و Payment URL، ادفعها بنفسك، وتأكد أن الفلوس وصلت البنك والـ webhook اشتغل.

### الخطوة 3: أنشئ فاتورة العميل (Revenue Proof Sprint)
1. Moyasar Dashboard → Invoices → **Create Invoice**
2. **Amount:** `499.00 SAR` — عرض الدخول للعميل (Revenue Proof Sprint، مرة واحدة).
3. **Description:** `Dealix — Revenue Proof Sprint`
4. أرسل الرابط للعميل بعد موافقته:
```
رابط الدفع: https://invoice.moyasar.com/invoices/inv_xxxx
المبلغ: 499 ريال — Revenue Proof Sprint (مرة واحدة)
```

**النتيجة:** العميل يدفع ← Moyasar يخبرك ← الفلوس تصل بنكك خلال 24 ساعة.

---

## 🔄 الطريقة 2 — Invoice API via curl (للأتمتة الخفيفة)

استخدمها لو تبغى توليد روابط من CLI بدون backend كامل:

```bash
# Set your keys
export MOYASAR_SECRET=sk_live_xxxxxxxxx   # من Moyasar Dashboard → API Keys

# Internal payment-channel verification charge (pilot_1sar) — NOT a customer offer
curl -X POST https://api.moyasar.com/v1/invoices \
  -u "$MOYASAR_SECRET:" \
  -d "amount=100" \
  -d "currency=SAR" \
  -d "description=Dealix internal payment-channel test — pilot_1sar" \
  -d "callback_url=https://dealix.me/thank-you.html" \
  -d "metadata[plan]=pilot_1sar_internal_test" \
  -d "metadata[customer_email]=$TEAM_EMAIL"
```

**Response مثال:**
```json
{
  "id": "inv_abc123",
  "amount": 100,
  "url": "https://invoice.moyasar.com/invoices/inv_abc123",
  "status": "initiated"
}
```

**انسخ `url` → أرسله للعميل.**

---

## قوالب Invoices الجاهزة

### اختبار داخلي — pilot_1sar (1 ريال، ليس عرض عميل)
```bash
curl -X POST https://api.moyasar.com/v1/invoices \
  -u "$MOYASAR_SECRET:" \
  -d "amount=100" \
  -d "currency=SAR" \
  -d "description=Dealix internal payment-channel test — pilot_1sar"
```

### Revenue Proof Sprint (499 ريال — عرض الدخول للعميل)
```bash
curl -X POST https://api.moyasar.com/v1/invoices \
  -u "$MOYASAR_SECRET:" \
  -d "amount=49900" \
  -d "currency=SAR" \
  -d "description=Dealix — Revenue Proof Sprint (one-time)"
```

### Data-to-Revenue Pack (1,500 ريال)
```bash
curl -X POST https://api.moyasar.com/v1/invoices \
  -u "$MOYASAR_SECRET:" \
  -d "amount=150000" \
  -d "currency=SAR" \
  -d "description=Dealix — Data-to-Revenue Pack"
```

### Growth Ops Monthly (2,999 ريال/شهر)
```bash
curl -X POST https://api.moyasar.com/v1/invoices \
  -u "$MOYASAR_SECRET:" \
  -d "amount=299900" \
  -d "currency=SAR" \
  -d "description=Dealix — Growth Ops Monthly (اشتراك شهري)"
```

### Executive Command Center (7,500 ريال/شهر)
```bash
curl -X POST https://api.moyasar.com/v1/invoices \
  -u "$MOYASAR_SECRET:" \
  -d "amount=750000" \
  -d "currency=SAR" \
  -d "description=Dealix — Executive Command Center (اشتراك شهري)"
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

## Flow كامل (Live الآن بدون backend)

```
1. عميل يفتح: https://dealix.me/pricing.html
   ↓
2. يختار "Revenue Proof Sprint — 499 ريال"
   ↓
3. يضغط الـ CTA → (رابط تواصل معك على WhatsApp/Calendly)
   ↓
4. أنت تنشئ invoice 499 ريال يدوياً
   ↓
5. ترسل الرابط للعميل بعد موافقته
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
| 2026-05-18 | (فريق Dealix) | — | 1 SAR | inv_test01 | paid | pilot_1sar (اختبار داخلي) |
| 2026-05-19 | [اسم العميل] | [الشركة] | 499 SAR | inv_abc123 | paid | Revenue Proof Sprint |
| ... | ... | ... | ... | ... | ... | ... |

---

## الخلاصة

**الواقع:** تقدر تستلم أول 10 عملاء بدون backend deploy كامل.
**الطريقة:** Moyasar hosted invoices + manual onboarding.
**الميزة:** تركّز على البيع + Customer Success، ما تنشغل في deploy.
**متى الـ backend الكامل:** بعد أول 5-10 عملاء.

**الآن:**
1. افتح Moyasar dashboard.
2. أنشئ فاتورة `pilot_1sar` (1 ريال) بـ email الفريق — **اختبار داخلي للتحقّق فقط**.
3. افتح الرابط وادفعها بنفسك.
4. تأكد الفلوس وصلت البنك والـ webhook اشتغل.
5. بعد نجاح الاختبار، أنشئ فاتورة 499 ريال (Revenue Proof Sprint) لأول عميل.
