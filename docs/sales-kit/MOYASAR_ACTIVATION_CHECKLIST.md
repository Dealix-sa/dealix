# Moyasar Activation Checklist — One Page | تفعيل Moyasar في صفحة واحدة
<!-- Owner: Founder | Date: 2026-05-18 | Operating checklist — no new build -->

> الهدف: تفعيل استقبال أول دفعة حقيقية عبر Moyasar. هذه الصفحة تجمع الخطوات
> من `RAILWAY_MOYASAR_STEP_BY_STEP.md` و `MOYASAR_HOSTED_CHECKOUT.md` في
> ترتيب واحد قابل للتنفيذ. كل خطوة موسومة: **[مؤسس — يدوي]** أو
> **[جاهز في الكود]**.
>
> The single ordered path to go live on Moyasar. Steps are tagged
> **[FOUNDER — manual]** (only the founder can do it) or
> **[IN-REPO — done]** (already implemented and tested).

---

## A. حساب التاجر | Merchant account — **[FOUNDER — manual]**

> هذا هو الحاجز الوحيد الصلب على الإيراد. لا يمكن لأي مساعد آلي تنفيذه.

1. [ ] افتح `https://dashboard.moyasar.com` وأنشئ/فعّل الحساب.
2. [ ] Settings → Business: ارفع السجل التجاري (CR) أو وثيقة العمل الحر.
3. [ ] اربط الحساب البنكي (IBAN) وانتظر تأكيد Moyasar.
4. [ ] تأكّد أن حالة الحساب = `Active` (قد تستغرق KYC أيام عمل).
5. [ ] انسخ المفاتيح من API Keys: `pk_...` (publishable) و `sk_...` (secret).

> راجع `docs/ops/MOYASAR_KYC_CHECKLIST.md` لمتطلبات KYC الكاملة.

---

## B. متغيّرات البيئة على Railway | Env vars — **[FOUNDER — manual]**

6. [ ] على Railway → خدمة `dealix` → Variables، أضف:
   - `MOYASAR_SECRET_KEY` = `sk_...` (للوضع المباشر `sk_live_...`).
   - `MOYASAR_WEBHOOK_SECRET` = سرّ قوي تختاره أنت (يُستخدم لتوثيق الـ webhook).
   - `DEALIX_MOYASAR_MODE` = `live` — **فقط** عند الجاهزية للشحن الحقيقي.
7. [ ] للتفعيل المباشر استخدم المساعد التفاعلي:
   `python scripts/moyasar_live_cutover.py` — يتحقّق من شكل المفتاح ولا
   يخزّنه على القرص.

> **بوابة `NO_LIVE_CHARGE`:** بدون `DEALIX_MOYASAR_MODE=live` صريح، النظام
> يرفض طريقة الدفع `moyasar_live` ويبقى على التحويل البنكي اليدوي. هذا
> السلوك **[جاهز في الكود]** ومُغطّى باختبارات.

---

## C. تسجيل الـ Webhook | Register the webhook — **[FOUNDER — manual]**

8. [ ] افتح `https://dashboard.moyasar.com/webhooks` → `+ Add Webhook`.
9. [ ] **URL:** `https://<your-domain>.up.railway.app/api/v1/webhooks/moyasar`
10. [ ] **Events:** `payment_paid`, `payment_failed`, `payment_refunded`.
11. [ ] **Secret:** الصق نفس قيمة `MOYASAR_WEBHOOK_SECRET` من الخطوة 6.
12. [ ] احفظ، ثم اضغط `Send Test Event` وتأكّد أنه يظهر `Delivered`.

---

## D. ما هو جاهز في الكود | What is already done — **[IN-REPO — done]**

| المكوّن | المسار | الحالة |
|---------|--------|--------|
| عميل Moyasar (إنشاء فاتورة hosted) | `dealix/payments/moyasar.py` | جاهز |
| معالج الـ webhook | `api/routers/pricing.py` → `POST /api/v1/webhooks/moyasar` | جاهز |
| توثيق توقيع الـ webhook | `verify_webhook()` — مقارنة `secret_token` بزمن ثابت | جاهز |
| إزالة التكرار (idempotency) | `IdempotencyStore` (نافذة 7 أيام) | جاهز |
| إعادة المحاولة عند الفشل | DLQ(`webhooks`) — لا يُفقد أي حدث | جاهز |
| مطابقة المدفوعات | `auto_client_acquisition/payment_ops/reconciliation.py` | جاهز |
| رابط التدقيق payment→delivery | `payment_ops/delivery_audit_link.py` (`invoice.paid` chain) | جاهز |
| بوابة `NO_LIVE_CHARGE` | `payment_ops/orchestrator.py` | جاهز |
| اختبار 1 ريال | `docs/sales-kit/dealix_1_riyal_test.sh` | جاهز |

> **توثيق التوقيع — ملاحظة:** الـ webhook handler الحيّ في `pricing.py`
> يستخدم نموذج Moyasar للـ hosted invoices: حقل `secret_token` داخل جسم
> الطلب يُقارَن بـ `MOYASAR_WEBHOOK_SECRET` بزمن ثابت (`hmac.compare_digest`).
> وحدة `reconciliation.py` تدعم أيضاً توقيع HMAC عبر ترويسة
> `X-Moyasar-Signature` لمن يفعّله. كلا المسارين موثّقان.

---

## E. اختبار 1 ريال من طرف لطرف | 1 SAR end-to-end — **[FOUNDER — manual]**

13. [ ] شغّل: `bash docs/sales-kit/dealix_1_riyal_test.sh https://<your-domain>.up.railway.app`
14. [ ] افتح رابط الدفع وادفع ببطاقة Moyasar التجريبية
    (`4111 1111 1111 1111` · CVV `123` · `12/30` · OTP `1234`).
15. [ ] تأكّد من ظهور: الدفعة `paid` في لوحة Moyasar + `moyasar webhook
    received` في سجلّات Railway.
16. [ ] **لا تنفّذ شحناً حقيقياً قبل اكتمال A–E.**

---

## F. الخروج إلى الإنتاج | Go-live gate

- [ ] خطوات A–E كلها مكتملة.
- [ ] `DEALIX_MOYASAR_MODE=live` مضبوط على Railway.
- [ ] رابط الـ webhook في لوحة Moyasar مقلوب إلى نطاق الإنتاج.
- [ ] أول فاتورة حقيقية 499 ريال أُنشئت وأُرسلت يدوياً للعميل الأول.

> بعد أول دفعة مؤكّدة، يربط `kickoff-delivery` السلسلة القابلة للتدقيق
> `invoice.paid → proof.pack_requested → proof.pack_delivered` تلقائياً.
> راجع `docs/PILOT_DELIVERY_SOP.md`.

---

## الفجوة المتبقية | Outstanding gap

**حساب التاجر Moyasar (القسم A) هو الحاجز الوحيد المتبقّي.** كل العمل من
طرف الكود جاهز ومُختبر. لا يمكن لأي مساعد آلي إكمال KYC أو ربط الحساب
البنكي — هذا إجراء المؤسس وحده.

*Estimated outcomes are not guaranteed outcomes /
النتائج التقديرية ليست نتائج مضمونة.*
