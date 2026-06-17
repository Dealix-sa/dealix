# Delivery OS — Project and service delivery system — نظام التسليم

## Purpose — الغرض

Delivery OS runs the work after a customer says yes. It creates the customer folder from a standard template, sequences the seven-day sprint, and records what was done, by whom, and against which service-level commitment. AI analyzes scope and recommends the delivery plan; deterministic workflows create the folder, set the SLA timers, and maintain the Delivery Log; the human approves anything that becomes an external deliverable. The system enforces a seven-day SLA on the Command Sprint and feeds completed results into Proof OS so every project ends with evidence. No project is closed without a Proof Pack, and no engagement runs without being booked as a Capital Asset the business can reuse.

نظام التسليم يدير العمل بعد موافقة العميل. ينشئ مجلد العميل من قالب موحّد، ويرتّب سبرنت الأيام السبعة، ويسجّل ما أُنجز ومن أنجزه ومقابل أي التزام بمستوى الخدمة. يحلّل الذكاء الاصطناعي النطاق ويوصي بخطة التسليم؛ وتنشئ المسارات الحتمية المجلد، وتضبط مؤقتات اتفاقية الخدمة، وتحفظ سجل التسليم؛ ويعتمد الإنسان أي مُخرَج خارجي. يفرض النظام اتفاقية خدمة من سبعة أيام على سبرنت القيادة، ويغذّي النتائج المكتملة إلى نظام الإثبات بحيث ينتهي كل مشروع بدليل. لا يُغلق مشروع بلا حقيبة إثبات، ولا يُشغَّل ارتباط دون تسجيله كأصل رأسمالي يعيد العمل استخدامه.

## Status — الحالة

Delivery OS | INTERNAL | 7-day sprint runbook; customer folder template

نظام التسليم | INTERNAL | دليل تشغيل سبرنت سبعة أيام؛ قالب مجلد العميل

## Inputs — المدخلات

- Approved offer and scope from Revenue OS — العرض والنطاق المعتمدان من نظام الإيراد
- Company intelligence from Market Intelligence OS — استخبارات الشركة من نظام استخبارات السوق
- Approval gates from Governance OS — بوابات الاعتماد من نظام الحوكمة

## Outputs — المخرجات

- Customer folder created from the standard template — مجلد العميل المُنشأ من القالب الموحّد
- Delivery Log: tasks, owners, SLA status — سجل التسليم: المهام، المُلّاك، حالة اتفاقية الخدمة
- Completed results handed to Proof OS — النتائج المكتملة المسلّمة لنظام الإثبات

## Guardrails — الضوابط

- No project without Proof Pack (10): the Pack closes the project — لا مشروع بلا حقيبة إثبات
- No project without Capital Asset (11): each engagement registers a reusable asset — لا مشروع بلا أصل رأسمالي
- No external action without approval (8): deliverables ship only after sign-off — لا إجراء خارجي بلا اعتماد
- No PII in logs (6): the Delivery Log uses anonymized references — لا بيانات شخصية في السجلات

## Cross-links — روابط

- [`../00_platform_truth/MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md)
- [`REVENUE_OS.md`](./REVENUE_OS.md) · [`PROOF_OS.md`](./PROOF_OS.md) · [`CLIENT_OS.md`](./CLIENT_OS.md) · [`GOVERNANCE_OS.md`](./GOVERNANCE_OS.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
