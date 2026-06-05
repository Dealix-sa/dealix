# Command Sprint Delivery OS — Dealix Delivery Runbook — نظام تسليم سبرنت القيادة

This is the internal runbook for delivering one Command Sprint: a paid 7-day engagement that produces the customer's first mini Dealix Business OS. Status: INTERNAL — for founder and team use only, never handed to a customer as-is. The customer-facing offer it serves is [`../01_go_to_market/COMMAND_SPRINT_OFFER.md`](../01_go_to_market/COMMAND_SPRINT_OFFER.md). Each module's readiness is fixed by [`../00_platform_truth/MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md); Delivery OS itself is INTERNAL there.

هذا هو الدليل الداخلي لتسليم سبرنت قيادة واحد: ارتباط مدفوع مدّته 7 أيام يُنتج أول نظام أعمال مصغّر للعميل من Dealix. الحالة: INTERNAL — لاستخدام المؤسس والفريق فقط، ولا يُسلَّم للعميل كما هو. والعرض الموجّه للعميل الذي يخدمه هذا الدليل هو [`../01_go_to_market/COMMAND_SPRINT_OFFER.md`](../01_go_to_market/COMMAND_SPRINT_OFFER.md). وجاهزية كل نظام محدّدة في [`../00_platform_truth/MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md)؛ ونظام التسليم نفسه INTERNAL هناك.

---

## Binding rules — القواعد المُلزِمة

Delivery is bound by five non-negotiables. No sprint is "done" if any is broken:

- **#8 No external action without approval.** Dealix sends no message, no outreach, and takes no public step on the customer's behalf without written approval logged in the Approval Register.
- **#10 No project without a Proof Pack.** Every sprint ends with a Proof Pack ([`PROOF_PACK_TEMPLATE.md`](./PROOF_PACK_TEMPLATE.md)); without it the project is incomplete.
- **#11 No project without a Capital Asset.** Every sprint must register at least one reusable asset (a method, a template, a scored dataset pattern) for the firm.
- **#4 No fake or un-sourced claims.** Every claim in every deliverable carries a source. Estimates are labeled estimates.
- **#6 No PII in logs.** Committed logs use anonymized labels — no email, phone, national ID, or real personal names.

التسليم مُلزَم بخمسة مبادئ غير قابلة للتفاوض، ولا يكتمل سبرنت إذا خُرِق أيٌّ منها:

- **#8 لا إجراء خارجي دون اعتماد.** لا ترسل Dealix رسالة ولا تواصلاً ولا تتخذ خطوة علنية نيابة عن العميل دون اعتماد مكتوب مسجَّل في سجل الاعتماد.
- **#10 لا مشروع دون حزمة إثبات.** كل سبرنت ينتهي بحزمة إثبات ([`PROOF_PACK_TEMPLATE.md`](./PROOF_PACK_TEMPLATE.md))؛ وبدونها يكون المشروع ناقصاً.
- **#11 لا مشروع دون أصل رأسمالي.** كل سبرنت يجب أن يسجّل أصلاً واحداً قابلاً لإعادة الاستخدام (طريقة، قالب، نمط بيانات مُسجَّل) للشركة.
- **#4 لا ادعاءات مزيّفة أو بلا مصدر.** كل ادعاء يحمل مصدره، والتقديرات تُوسَم كتقديرات.
- **#6 لا بيانات تعريف شخصية في السجلات.** السجلات المحفوظة تستخدم تسميات مجهولة الهوية — بلا بريد أو هاتف أو هوية وطنية أو أسماء حقيقية.

---

## The 7-day SLA — اتفاقية مستوى الخدمة لسبعة أيام

Each day has one owner and produces exactly one artifact filed in the customer folder ([`CUSTOMER_FOLDER_TEMPLATE.md`](./CUSTOMER_FOLDER_TEMPLATE.md)). If a day slips, the slip is logged honestly in `08_delivery_log.md`; the SLA is a discipline, not a guarantee of business outcomes.

لكل يوم مالك واحد ويُنتج مستنداً واحداً فقط يُحفظ في مجلّد العميل ([`CUSTOMER_FOLDER_TEMPLATE.md`](./CUSTOMER_FOLDER_TEMPLATE.md)). وإن تأخّر يوم، يُسجَّل التأخّر بصدق في `08_delivery_log.md`؛ فالاتفاقية انضباط تشغيلي لا ضمان نتائج.

| Day — اليوم | Deliverable produced — التسليم المُنتَج | Folder file — ملف المجلّد |
|---|---|---|
| D1 | Intake + company intelligence — الاستلام واستخبارات الشركة | `00_intake.md`, `01_company_intelligence.md` |
| D2 | Diagnostic summary — الملخّص التشخيصي | `02_diagnostic_summary.md`, `03_command_sprint_scope.md` |
| D3 | Revenue Map — خريطة الإيراد | `04_revenue_map.md` |
| D4 | Proof Register — سجل الإثبات | `05_proof_register.md` |
| D5 | Next Action Board — لوحة الإجراء التالي | `06_next_action_board.md` |
| D6 | Executive Command Brief — موجز القيادة التنفيذي | `07_executive_command_brief.md` |
| D7 | Proof Pack + Upsell Recommendation — حزمة الإثبات وتوصية الترقية | `09_proof_pack.md`, `10_upsell_recommendation.md` |

The delivery log `08_delivery_log.md` runs across all seven days, recording who did what and when, with no PII.

سجل التسليم `08_delivery_log.md` يمتدّ عبر الأيام السبعة، ويسجّل مَن فعل ماذا ومتى، دون أي بيانات شخصية.

---

## Day-by-day — يوماً بيوم

- **D1 — Intake + company intelligence.** Create the customer folder only after payment is confirmed. Capture scope and inputs in `00_intake.md`. Build the company intelligence brief from sourced public and customer-provided material — no scraping, no bulk collection. Checkpoint: intake confirmed by the customer.
- **D2 — Diagnostic summary.** Reduce the intelligence into a short diagnostic and lock the scope in `03_command_sprint_scope.md`. Checkpoint: scope approved before any further work.
- **D3 — Revenue Map.** Map revenue lines and evidenced opportunities. Every opportunity is an estimate, never a promised number.
- **D4 — Proof Register.** Record each claim with its source so nothing in the final pack is un-sourced.
- **D5 — Next Action Board.** Convert findings into a small, ordered set of next actions the customer can own.
- **D6 — Executive Command Brief.** Assemble the one-page brief a decision-maker reads in minutes.
- **D7 — Proof Pack + Upsell Recommendation.** Produce the Proof Pack and, only if the offer's gate is met, the Upsell Recommendation.

- **D1 — الاستلام واستخبارات الشركة.** أنشئ مجلّد العميل بعد تأكيد الدفع فقط. سجّل النطاق والمدخلات في `00_intake.md`. وابنِ موجز الاستخبارات من مادة عامة ومقدَّمة من العميل وموثّقة المصدر — بلا كشط ولا جمع جماعي. نقطة التحقّق: تأكيد العميل للاستلام.
- **D2 — الملخّص التشخيصي.** اختصر الاستخبارات في تشخيص قصير وثبّت النطاق في `03_command_sprint_scope.md`. نقطة التحقّق: اعتماد النطاق قبل أي عمل لاحق.
- **D3 — خريطة الإيراد.** ارسم خطوط الإيراد والفرص المُثبتة بالأدلة. كل فرصة تقدير لا رقم موعود.
- **D4 — سجل الإثبات.** سجّل كل ادعاء مع مصدره كي لا يبقى شيء بلا مصدر في الحزمة النهائية.
- **D5 — لوحة الإجراء التالي.** حوّل النتائج إلى مجموعة صغيرة مرتّبة من الإجراءات التالية يملكها العميل.
- **D6 — موجز القيادة التنفيذي.** اجمع الموجز من صفحة واحدة يقرؤه صاحب القرار في دقائق.
- **D7 — حزمة الإثبات وتوصية الترقية.** أنتج حزمة الإثبات، ثم — فقط عند تحقّق بوابة العرض — توصية الترقية.

---

## Governance checkpoints — نقاط الحوكمة

Three approval gates protect the sprint, each logged in `08_delivery_log.md` with an anonymized label and timestamp:

1. **Payment gate (before D1):** no folder, no work until payment is confirmed.
2. **Scope gate (D2):** the customer approves the locked scope before D3 begins.
3. **External-action gate (anytime):** any step that leaves Dealix's own workspace — any message to a third party, any publish — requires explicit written approval (#8). Publishing of the Proof Pack defaults to **not permitted** until written approval is recorded.

ثلاث بوابات اعتماد تحمي السبرنت، كلٌّ مسجَّلة في `08_delivery_log.md` بتسمية مجهولة الهوية وطابع زمني:

1. **بوابة الدفع (قبل D1):** لا مجلّد ولا عمل قبل تأكيد الدفع.
2. **بوابة النطاق (D2):** يعتمد العميل النطاق المثبَّت قبل بدء D3.
3. **بوابة الإجراء الخارجي (في أي وقت):** أي خطوة تغادر مساحة عمل Dealix — أي رسالة لطرف ثالث، أي نشر — تتطلّب اعتماداً مكتوباً صريحاً (#8). ونشر حزمة الإثبات افتراضه **غير مسموح** حتى يُسجَّل اعتماد مكتوب.

---

## Handoff to upsell — التسليم إلى الترقية

The Upsell Recommendation (`10_upsell_recommendation.md`) is written only when the Sprint has done its job and the offer's gate is open: paid, Command Pack received, outputs reviewed, a clear decision reached, and both sides agreeing the weekly rhythm is useful. The recommendation points toward the monthly tiers without restating a price; prices live with the offer. Acceptance before any handoff is governed by [`DELIVERY_ACCEPTANCE_CRITERIA.md`](./DELIVERY_ACCEPTANCE_CRITERIA.md).

تُكتب توصية الترقية (`10_upsell_recommendation.md`) فقط حين يؤدّي السبرنت مهمّته وتُفتح بوابة العرض: دفع، واستلام Command Pack، ومراجعة المخرجات، وقرار واضح، واتّفاق الطرفين على أن الإيقاع الأسبوعي مفيد. وتشير التوصية إلى الباقات الشهرية دون إعادة ذكر سعر؛ فالأسعار مع العرض. والقبول قبل أي تسليم محكوم بـ[`DELIVERY_ACCEPTANCE_CRITERIA.md`](./DELIVERY_ACCEPTANCE_CRITERIA.md).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
