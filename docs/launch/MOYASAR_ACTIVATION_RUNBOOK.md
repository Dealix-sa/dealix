# Dealix — دليل تفعيل Moyasar · Moyasar Activation Runbook

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-18
**وثائق مرافقة / Companion docs:** `../sales-kit/MOYASAR_HOSTED_CHECKOUT.md` · `../sales-kit/RAILWAY_MOYASAR_STEP_BY_STEP.md` · `FIRST_PILOT_PLAYBOOK.md` · `../ops/MANUAL_PAYMENT_SOP.md`

---

## الغرض · Purpose

الكود الخاص بتكامل Moyasar **مكتمل**. ما تبقّى ليس برمجة — بل تفعيل حساب وضبط متغيّر بيئة واحد. هذه الوثيقة هي الخطوات بالترتيب لتشغيل قناة الدفع.

The Moyasar integration code is **complete**. What remains is not engineering — it is account activation and one environment variable. This document is the ordered runbook to switch the payment rail on.

> **ملاحظة سعرية / Price note:** أي ذكر لسعر "1 SAR" في الوثائق الأقدم هو وضع اختبار فقط (test-mode). هذه الوثيقة تنسخ أي سعر اختباري قديم: عرض العميل الرسمي هو **499 SAR** (`revenue_proof_sprint_499`). فاتورة الاختبار وحدها تستخدم وضع الاختبار. This runbook supersedes any "1 SAR" price in the older docs — the test invoice is test-mode only; the customer offer is 499 SAR.

---

## ما هو متاح الآن بدون Moyasar · Available NOW without Moyasar

لا تنتظر تفعيل Moyasar لتحصيل أول Pilot. الـ`orchestrator` يدعم اليوم قناتين:

- **`bank_transfer`** — تحويل بنكي مع رفع إثبات يدوي (manual evidence upload).
- **`cash_in_person`** — استلام نقدي/مباشر.

تأكيد الدفع دائمًا **بمبادرة المؤسس** (founder-initiated) — لا يوجد تأكيد تلقائي. أول Pilot المدفوع بـ499 SAR يمكن تحصيله اليوم بهذه الطريقة. راجع [`../ops/MANUAL_PAYMENT_SOP.md`](../ops/MANUAL_PAYMENT_SOP.md).

Do not wait for Moyasar to collect the first pilot. `payment_ops/orchestrator.py` already supports `bank_transfer` (with manual evidence upload) and `cash_in_person` today. Payment confirmation is always founder-initiated.

---

## الخطوات · The Runbook

### 1. إجراء المؤسس — تفعيل حساب Moyasar · Founder action — verify the account

- رفع السجل التجاري (commercial registration).
- ربط الحساب البنكي (bank account link).
- إكمال تفعيل الحساب (account activation) داخل لوحة Moyasar.

هذه الخطوة بشرية بالكامل ولا يمكن أتمتتها. راجع [`../ops/MOYASAR_KYC_CHECKLIST.md`](../ops/MOYASAR_KYC_CHECKLIST.md) لقائمة مستندات الـKYC.

### 2. ضبط الـwebhook · Configure the webhook URL

في لوحة Moyasar، وجّه الـwebhook إلى نقطة المطابقة (reconciliation endpoint). المعالجة تتم في `auto_client_acquisition/payment_ops/reconciliation.py`:

- تحقق توقيع **HMAC-SHA256** على كل حدث وارد.
- المعالجة **idempotent** — تكرار نفس الحدث لا يُنشئ سجلًا مزدوجًا.

### 3. ضبط متغيّر البيئة · Set the env var

على بيئة النشر (Railway):

```
DEALIX_MOYASAR_MODE=live
```

حتى يُضبط هذا المتغيّر، بوابة `_enforce_no_live_charge` في `auto_client_acquisition/payment_ops/orchestrator.py` **ترفض** أي شحنة من نوع `moyasar_live`. هذه ليست خطأً — إنها تطبيق مباشر لغير القابل للتفاوض `no_live_charge`. الرفض هو السلوك الصحيح قبل التفعيل.

Until this variable is set, the `_enforce_no_live_charge` gate refuses any `moyasar_live` charge. That refusal is the `no_live_charge` non-negotiable working as designed.

### 4. تنفيذ الـcutover · Run the cutover script

```
python scripts/moyasar_live_cutover.py
```

### 5. التحقق بفاتورة اختبار · Verify with a small test invoice

- أنشئ فاتورة اختبار صغيرة (test-mode — ليست سعر عميل).
- طابق النتيجة:

```
python scripts/reconcile_moyasar.py
```

تأكد أن الحدث وصل، أن التوقيع تحقّق، وأن السجل ظهر مرة واحدة فقط.

---

## قائمة التحقق · Cutover checklist

| # | الخطوة · Step | المالك · Owner | الحالة · Status |
|---|---|---|---|
| 1 | تفعيل حساب Moyasar (CR + بنك) | Sami | ☐ |
| 2 | webhook موجّه لنقطة المطابقة | Sami | ☐ |
| 3 | `DEALIX_MOYASAR_MODE=live` على Railway | Sami | ☐ |
| 4 | `moyasar_live_cutover.py` نُفّذ | Sami | ☐ |
| 5 | فاتورة اختبار طُوبقت بنجاح | Sami | ☐ |

---

## مبدأ حاكم · Governing principle

التحصيل عبر Moyasar لا يغيّر القاعدة: **تأكيد الدفع بمبادرة المؤسس فقط**. القناة الجديدة تضيف خيارًا — لا تلغي بوابة موافقة.

Enabling Moyasar does not change the rule: payment confirmation stays founder-initiated. The new rail adds an option; it never removes an approval gate.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
