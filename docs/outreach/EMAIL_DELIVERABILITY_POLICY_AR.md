# Email Deliverability Policy — سياسة قابلية التسليم

جزء من: Dealix Market Production OS — انظر [docs/market_os/MARKET_PRODUCTION_OS_AR.md](../market_os/MARKET_PRODUCTION_OS_AR.md)

> القاعدة: الإنتاج عالٍ (250 draft/day)، والإرسال منخفض ومتدرّج. سمعة الدومين أصل لا يُستبدل — لا تحرقه من أجل دفعة واحدة.

المخطط المرتبط: [`schemas/email_account.schema.json`](../../schemas/email_account.schema.json) · [`schemas/suppression.schema.json`](../../schemas/suppression.schema.json)

---

## 1. لماذا هذه السياسة

متطلبات مرسلي Gmail (Google) تنصّ على:
- مصادقة SPF/DKIM (أو DKIM على الأقل) لكل المرسلين؛ وSPF + DKIM + **DMARC** للمرسلين بكثافة (≈5,000 رسالة/يوم فأكثر).
- one-click unsubscribe في الرسائل التسويقية واحترام طلب الإلغاء خلال يومين.
- إبقاء معدّل بلاغات الـ spam **تحت 0.3%** (والأفضل أقل من 0.1%).
- تحذير صريح من شراء القوائم أو الإرسال لمن لم يشتركوا لأنه يضرّ سمعة الدومين.

نظام CAN-SPAM (الولايات المتحدة) يشترط: عدم تضليل الـ headers أو الـ subject، عنوان بريدي/هوية مرسِل صحيحة،
آلية opt-out واضحة تُحترم خلال 10 أيام عمل، وحظر ممارسات مثل harvesting.

في السعودية: نظام حماية البيانات الشخصية (PDPL) يحكم التعامل مع البيانات الشخصية؛ نلتزم به ولا نخزّن PII في ملفات يتم رفعها.

> هذه إشارة سياسة تشغيلية، ليست استشارة قانونية. أي قرار تنظيمي يمرّ على مراجعة قانونية.

---

## 2. Checklist قبل أي إرسال (بوابة إلزامية)

لا تُرسل أي دفعة قبل أن تكون كل هذه `true` على الحساب المُرسِل:

- [ ] SPF configured
- [ ] DKIM configured
- [ ] DMARC configured
- [ ] custom tracking domain (نطاق تتبّع مخصّص، لا نطاق المزوّد المشترك)
- [ ] one-click unsubscribe (RFC 8058) في كل رسالة
- [ ] reply-to صالح ومراقَب
- [ ] عنوان بريدي / هوية مرسِل صحيحة (CAN-SPAM)
- [ ] suppression list مُفعّلة ومفحوصة قبل الإرسال
- [ ] bounce handling فعّال
- [ ] spam rate مُراقَب

الحقول المقابلة في `email_account.schema.json`: `spf_configured`, `dkim_configured`, `dmarc_configured`,
`custom_tracking_domain`, `one_click_unsubscribe`, `physical_address_present`, `health_status`.

---

## 3. عتبات الصحة (Health Thresholds)

| المؤشر | الحد | الإجراء عند التجاوز |
|---|---|---|
| bounce rate | < 3% | أوقف الدفعة، نظّف القائمة، راجع المصدر |
| spam complaint rate | < 0.1–0.3% | أوقف الإرسال على الحساب، حقّق |
| unsubscribe rate | مُراقَب | إذا ارتفع، راجع الاستهداف والرسالة |
| provider warnings | صفر | إيقاف فوري + تحقيق |
| positive reply rate | يتحسّن | إن تراجع، أوقف أسوأ القطاعات |

عند أي تجاوز، `email_account.health_status` يصبح `watch` أو `paused`. الحساب `paused` لا يُرسل حتى المعالجة.

---

## 4. السمعة كأصل

- ابدأ بحسابات/نطاقات إرسال منفصلة عن نطاق الشركة الأساسي عند الحاجة.
- نوّع الدفعات عبر القطاعات وlا ترسل نفس النص لآلاف فجأة.
- راقب `reports/outreach/DOMAIN_HEALTH_REVIEW.md` يوميًا.

---

## 5. ما الذي يكسر السمعة فورًا (ممنوع)

شراء قوائم · إرسال لمن لم تتحقّق من ملاءمتهم · subject مضلّل · Re:/Fwd: كاذبة · إرسال بلا unsubscribe ·
تجاهل opt-out · رفع المعدّل فجأة · تجاهل bounce spike.

انظر أيضًا: [SENDING_RAMP_PLAN_AR](SENDING_RAMP_PLAN_AR.md) · [COLD_EMAIL_COMPLIANCE_AR](COLD_EMAIL_COMPLIANCE_AR.md) · [UNSUBSCRIBE_POLICY_AR](UNSUBSCRIBE_POLICY_AR.md).

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
