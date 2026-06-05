# Customer Folder Template — Dealix Delivery Folder — قالب مجلّد العميل

This document describes the per-customer delivery folder a Command Sprint produces at `customers/{company}/`. Status: INTERNAL. It is the structural backbone of the runbook [`COMMAND_SPRINT_DELIVERY_OS.md`](./COMMAND_SPRINT_DELIVERY_OS.md) and the offer it serves, [`../01_go_to_market/COMMAND_SPRINT_OFFER.md`](../01_go_to_market/COMMAND_SPRINT_OFFER.md). Module readiness is fixed by [`../00_platform_truth/MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md).

يصف هذا المستند مجلّد التسليم الخاص بكل عميل الذي يُنتجه سبرنت القيادة في `customers/{company}/`. الحالة: INTERNAL. وهو العمود الهيكلي للدليل [`COMMAND_SPRINT_DELIVERY_OS.md`](./COMMAND_SPRINT_DELIVERY_OS.md) والعرض الذي يخدمه [`../01_go_to_market/COMMAND_SPRINT_OFFER.md`](../01_go_to_market/COMMAND_SPRINT_OFFER.md). وجاهزية الأنظمة محدّدة في [`../00_platform_truth/MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md).

---

## When the folder is created — متى يُنشأ المجلّد

A real customer folder is created **only after payment is confirmed.** Before payment there is no folder and no delivery work. The folder uses an anonymized company slug, and no committed file inside it contains PII — no email, phone, national ID, or real personal name (non-negotiable #6). PII, when operationally necessary, stays out of the committed repository.

يُنشأ مجلّد العميل الحقيقي **بعد تأكيد الدفع فقط.** قبل الدفع لا يوجد مجلّد ولا عمل تسليم. ويستخدم المجلّد اسماً مختصراً مجهول الهوية، ولا يحتوي أي ملف محفوظ بداخله على بيانات تعريف شخصية — بلا بريد أو هاتف أو هوية وطنية أو اسم حقيقي (المبدأ غير القابل للتفاوض رقم 6). والبيانات الشخصية، عند الحاجة التشغيلية، تبقى خارج المستودع المحفوظ.

---

## The eleven files — الملفات الأحد عشر

Each file maps to a day of the SLA. "Complete" means the stated bar is met and the file is logged in `08_delivery_log.md`.

كل ملف يقابل يوماً من اتفاقية الخدمة. و"مكتمل" يعني تحقّق المعيار المذكور وتسجيل الملف في `08_delivery_log.md`.

- **`00_intake.md` — Intake.** Purpose: scope, inputs, and customer context captured at start. Complete when: the customer has confirmed the intake and the inputs are listed with their source.
- **`01_company_intelligence.md` — Company intelligence.** Purpose: the sourced company brief. Complete when: every fact carries a source and nothing relies on scraping or bulk collection.
- **`02_diagnostic_summary.md` — Diagnostic summary.** Purpose: the short read of where revenue clarity is missing. Complete when: each finding traces to an input in `00`–`01`.
- **`03_command_sprint_scope.md` — Scope.** Purpose: the locked scope of this sprint. Complete when: the customer has approved it (scope gate) before D3.
- **`04_revenue_map.md` — Revenue Map.** Purpose: revenue lines and evidenced opportunities. Complete when: every opportunity is labeled an estimate, never a promised number.
- **`05_proof_register.md` — Proof Register.** Purpose: each claim paired with its source. Complete when: no claim in the sprint is un-sourced (#4).
- **`06_next_action_board.md` — Next Action Board.** Purpose: the ordered next actions the customer can own. Complete when: each action has an owner and a clear first step.
- **`07_executive_command_brief.md` — Executive Command Brief.** Purpose: the one-page decision read. Complete when: it stands alone and references the files behind it.
- **`08_delivery_log.md` — Delivery log.** Purpose: who did what and when across all seven days, with approval timestamps. Complete when: all three governance gates are recorded and it contains no PII (#6).
- **`09_proof_pack.md` — Proof Pack.** Purpose: the seven-question evidence pack the customer receives. Complete when: it follows [`PROOF_PACK_TEMPLATE.md`](./PROOF_PACK_TEMPLATE.md) and the publish-permission field is set (default: not permitted).
- **`10_upsell_recommendation.md` — Upsell Recommendation.** Purpose: the pointer to the monthly tiers, written only when the offer's gate is open. Complete when: it restates no price and links to the offer.

— **`00_intake.md` — الاستلام.** الغرض: النطاق والمدخلات وسياق العميل عند البداية. مكتمل حين: يؤكّد العميل الاستلام وتُذكر المدخلات بمصادرها.
— **`01_company_intelligence.md` — استخبارات الشركة.** الغرض: موجز الشركة الموثّق المصدر. مكتمل حين: تحمل كل حقيقة مصدراً ولا يعتمد شيء على الكشط أو الجمع الجماعي.
— **`02_diagnostic_summary.md` — الملخّص التشخيصي.** الغرض: القراءة القصيرة لموضع غياب وضوح الإيراد. مكتمل حين: تعود كل نتيجة إلى مُدخل في `00`–`01`.
— **`03_command_sprint_scope.md` — النطاق.** الغرض: النطاق المثبَّت لهذا السبرنت. مكتمل حين: يعتمده العميل (بوابة النطاق) قبل D3.
— **`04_revenue_map.md` — خريطة الإيراد.** الغرض: خطوط الإيراد والفرص المُثبتة بالأدلة. مكتمل حين: تُوسَم كل فرصة كتقدير لا كرقم موعود.
— **`05_proof_register.md` — سجل الإثبات.** الغرض: كل ادعاء مقروناً بمصدره. مكتمل حين: لا ادعاء بلا مصدر في السبرنت (#4).
— **`06_next_action_board.md` — لوحة الإجراء التالي.** الغرض: الإجراءات التالية المرتّبة التي يملكها العميل. مكتمل حين: لكل إجراء مالك وخطوة أولى واضحة.
— **`07_executive_command_brief.md` — موجز القيادة التنفيذي.** الغرض: قراءة القرار من صفحة واحدة. مكتمل حين: يقف وحده ويشير إلى الملفات خلفه.
— **`08_delivery_log.md` — سجل التسليم.** الغرض: مَن فعل ماذا ومتى عبر الأيام السبعة مع أوقات الاعتماد. مكتمل حين: تُسجَّل بوابات الحوكمة الثلاث ولا يحتوي بيانات شخصية (#6).
— **`09_proof_pack.md` — حزمة الإثبات.** الغرض: حزمة الأدلة بالأسئلة السبعة التي يستلمها العميل. مكتمل حين: تتبع [`PROOF_PACK_TEMPLATE.md`](./PROOF_PACK_TEMPLATE.md) ويُضبط حقل إذن النشر (الافتراض: غير مسموح).
— **`10_upsell_recommendation.md` — توصية الترقية.** الغرض: المؤشّر إلى الباقات الشهرية، يُكتب فقط عند فتح بوابة العرض. مكتمل حين: لا يعيد ذكر سعر ويربط بالعرض.

---

## PII discipline — انضباط البيانات الشخصية

Committed logs and deliverables carry anonymized labels only. Where a name or contact is operationally needed, it is held outside the committed repository and never written into `08_delivery_log.md` or any file 00–10 that is committed. Acceptance against these bars is checked in [`DELIVERY_ACCEPTANCE_CRITERIA.md`](./DELIVERY_ACCEPTANCE_CRITERIA.md).

السجلات والتسليمات المحفوظة تحمل تسميات مجهولة الهوية فقط. وحين يُحتاج اسم أو وسيلة تواصل تشغيلياً، تُحفظ خارج المستودع ولا تُكتب أبداً في `08_delivery_log.md` أو أي ملف 00–10 محفوظ. والقبول وفق هذه المعايير يُفحص في [`DELIVERY_ACCEPTANCE_CRITERIA.md`](./DELIVERY_ACCEPTANCE_CRITERIA.md).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
