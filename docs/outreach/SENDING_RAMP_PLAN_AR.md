# Sending Ramp Plan — خطة التدرّج في الإرسال

جزء من: Dealix Market Production OS — انظر [docs/market_os/MARKET_PRODUCTION_OS_AR.md](../market_os/MARKET_PRODUCTION_OS_AR.md)

> الإنتاج 250 draft/day منذ اليوم 0. الإرسال يبدأ من ~0 ويتدرّج إلى 250/day فقط إذا بقيت المؤشرات صحية.
> هذه وثيقة **سياسة التدرّج**؛ دليل التشغيل اليومي في [SENDING_RAMP_OS_AR](SENDING_RAMP_OS_AR.md).

المخطط المرتبط: [`schemas/email_account.schema.json`](../../schemas/email_account.schema.json) · [`schemas/sending_batch.schema.json`](../../schemas/sending_batch.schema.json)

---

## 1. جدول التدرّج

| المرحلة | الإنتاج (drafts/day) | الإرسال (sends/day) | الشرط للانتقال |
|---|---|---|---|
| Week 0 | 250 | 0–20 | إكمال SPF/DKIM/DMARC + suppression + unsubscribe |
| Week 1 | 250 | 25–50 | bounce < 3% · لا شكاوى · لا تحذيرات |
| Week 2 | 250 | 50–100 | المؤشرات صحية + ردود إيجابية تبدأ |
| Week 3 | 250 | 100–150 | استقرار المؤشرات أسبوعًا كاملًا |
| Week 4 | 250 | 150–250 | فقط إذا كل المؤشرات صحية |

`email_account.warmup_stage` يعكس المرحلة، و`daily_send_cap` يفرض السقف.

---

## 2. عتبات الصحة (نفس بوابة التسليمية)

- bounce rate < 3%
- spam complaint rate < 0.1–0.3%
- unsubscribe rate مُراقَب
- positive reply rate يتحسّن
- صفر تحذيرات من المزوّد

أي تجاوز → خفّض المرحلة أو `pause` الحساب. الارتفاع التدريجي مشروط، لا تلقائي.

---

## 3. ماذا يوقف الإرسال فورًا

- bounce spike مفاجئ
- شكوى spam فوق العتبة
- تحذير من المزوّد
- نطاق `health_status = paused`
- اكتشاف مستلم في suppression بعد التخطيط

---

## 4. مبدأ التوزيع

- دفعات صغيرة موزّعة على القطاعات والحسابات، لا انفجار دفعة واحدة.
- نوّع النصوص (تسلسلات مختلفة) لتقليل أنماط الـ spam.
- راقب [reports/outreach/DOMAIN_HEALTH_REVIEW.md](../../reports/outreach/DOMAIN_HEALTH_REVIEW.md) و[DELIVERABILITY_REVIEW.md](../../reports/outreach/DELIVERABILITY_REVIEW.md) يوميًا.

انظر أيضًا: [EMAIL_DELIVERABILITY_POLICY_AR](EMAIL_DELIVERABILITY_POLICY_AR.md) · [SENDING_RAMP_OS_AR](SENDING_RAMP_OS_AR.md).

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
