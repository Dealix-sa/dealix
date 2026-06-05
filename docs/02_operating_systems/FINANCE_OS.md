# 08 — Finance OS — نظام المال

**الحالة — Status: `BETA` (تدفّق الدفع مبني؛ وحدات الاقتصاد ومحاسبة الفواتير قيد التشغيل / `FUTURE` للأجزاء المتقدمة)**

> Finance OS لا يَعِد بإيرادات. يقيس الوحدة الاقتصادية الحقيقية ويمنع التسعير الخاسر قبل أن يحدث.

## الغرض — Purpose

نظام المال هو الطبقة التي تُحوّل النشاط التشغيلي إلى **اقتصاد وحدة (unit economics)** قابل للقياس: كم يكلّف اكتساب العميل، كم هامش كل خدمة، ومتى يصبح التسعير خاسرًا. هدفه أن يكون كل ريال داخل أو خارج **مرئيًا، مُبرَّرًا، ومُتحقَّقًا** — لا تقديرًا متفائلًا.

## القيمة — Value

- يمنع التسعير تحت التكلفة عبر **قاعدة الـ >20 ساعة/شهر**.
- يربط كل عميل مدفوع بـ **مجلد تسليم + Proof Pack** قبل الاعتراف بالإيراد.
- يحوّل MRR والهامش وCAC/LTV من تقدير ذهني إلى لوحة قابلة للمراجعة.

## القدرات — Capabilities

- **التسعير والعروض (Pricing & Offers):** منطق تسعير الـ Command Sprint والـ Managed.
- **محاسبة الفواتير (Invoice awareness):** وعي بمتطلبات الفوترة الإلكترونية لهيئة الزكاة والضريبة والجمارك (**ZATCA e-invoicing**) — الوعي قائم، التكامل الكامل `FUTURE`.
- **المدفوعات (Payments):** تدفّق **Moyasar** المبني في الريبو (hosted checkout + webhook persistence). لا يوجد سحب مباشر تلقائي — كل عملية مرتبطة بفاتورة وموافقة.
- **مؤشرات (Metrics):** MRR، الهامش (margin)، CAC/LTV، التحصيل (collections)، اقتصاد الوحدة.

## المُدخلات والمُخرجات — Inputs / Outputs

| المُدخل | المُخرج |
|---|---|
| سعر العرض + ساعات التسليم الفعلية | هامش محسوب لكل عملية |
| أحداث الدفع (Moyasar webhook) | حالة فاتورة + اعتراف إيراد |
| تكلفة الاكتساب + قيمة العميل | CAC / LTV |
| سجل التسليم | تأكيد ربط Proof Pack |

## البوابات والقواعد — Gates / Rules

- **هامش الـ Sprint ≥ 70%** بعد استخدام القوالب (template reuse).
- **هامش الـ Managed ≥ 60%**.
- **قاعدة الـ >20 ساعة/شهر:** أي خدمة تستهلك أكثر من 20 ساعة شهريًا من وقت المؤسس ولا يُغطّيها السعر = **تسعير خاسر، يُعاد فورًا**.
- **لا اعتراف بإيراد بلا مجلد تسليم + Proof Pack.**
- **لا وعود بإيراد أو ROI كحقيقة** — كل رقم مستقبلي «مُقدَّر / estimated».
- **لا سحب مباشر تلقائي** — كل دفعة عبر فاتورة وموافقة.

## الاتصالات — Connections to other OS

- **Proof OS** — لا اعتراف بإيراد بلا Proof Pack: [../07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md)
- **Value OS** — التمييز بين القيمة المُقدَّرة والمُتحقَّقة: [../08_value_os/VALUE_OS.md](../08_value_os/VALUE_OS.md)
- **Governance OS** — أي إجراء مالي = Approval Class A4: [GOVERNANCE_OS.md](GOVERNANCE_OS.md)
- تدفّق الفواتير والتحصيل الفعلي: [../revenue/INVOICE_FLOW.md](../revenue/INVOICE_FLOW.md) · [../revenue/PAYMENT_RECONCILIATION.md](../revenue/PAYMENT_RECONCILIATION.md)
- سياسة التسعير: [../knowledge-base/pricing_policy_ar_en.md](../knowledge-base/pricing_policy_ar_en.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
