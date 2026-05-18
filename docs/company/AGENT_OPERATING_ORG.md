# Agent Operating Org — منظومة التشغيل بالوكلاء

This document describes how Dealix is run as a largely self-operating company through a hierarchy of AI agents, and where the human boundary sits. It is operating-model documentation and is freeze-compliant: it describes how work is organized, not new product scope.

هذه الوثيقة تشرح كيف تُدار Dealix كشركة شبه ذاتية التشغيل عبر تسلسل هرمي من الوكلاء، وأين يقع الحد البشري. هي وثيقة لنموذج التشغيل ومتوافقة مع التجميد التجاري: تصف كيف يُنظَّم العمل، لا نطاق منتج جديد.

## 1. The Operating Principle — مبدأ التشغيل

Agents do the work; the founder approves the few things doctrine reserves for a human. Research, drafting, qualification, delivery preparation, proof assembly, QA, ledgers, reporting, and monitoring all run through agents. The founder sets direction and signs off on three classes of action only: an external message, an invoice or charge, and the publishing of a customer name or case. The company is self-operating within doctrine — automated up to an external send or a charge, with the founder as the sole approval node for those. This is a governance feature, not a limitation: it keeps every customer-facing action attributable to a named human.

الوكلاء ينفّذون العمل؛ والمؤسس يعتمد البنود القليلة التي يحفظها المبدأ التشغيلي للإنسان. البحث، والصياغة، والتأهيل، والتحضير للتسليم، وتجميع الأدلة، وضبط الجودة، والسجلات، والتقارير، والمراقبة، كلها تجري عبر الوكلاء. المؤسس يحدد الاتجاه ويعتمد ثلاثة أصناف من الإجراءات فقط: رسالة خارجية، فاتورة أو تحصيل، ونشر اسم عميل أو حالته. الشركة ذاتية التشغيل ضمن المبدأ — مؤتمتة حتى حدود الإرسال الخارجي أو التحصيل، والمؤسس هو نقطة الاعتماد الوحيدة لهذه. هذه ميزة حوكمة لا قيد، إذ تُبقي كل إجراء يواجه العميل منسوبًا لإنسان بالاسم.

## 2. The Org Chart — الهيكل التنظيمي

Three tiers. Tier 0 is the founder. Tier 1 is the orchestrator. Tier 2 is the specialist team across four divisions.

ثلاث طبقات. الطبقة 0 المؤسس. الطبقة 1 المنسّق. الطبقة 2 فريق المتخصصين عبر أربع شُعب.

| Tier — الطبقة | Agent — الوكيل | Role — الدور |
|---|---|---|
| 0 | Founder — المؤسس | Sets direction, approves external sends and charges, owns go/no-go gates — يحدد الاتجاه ويعتمد الإرسال والتحصيل ويملك بوابات المضي |
| 1 | dealix-pm | Orchestrator. Owns the 90-day plan, dispatches all specialists, runs the cadence, enforces the freeze and the gates — المنسّق: يملك خطة الـ90 يومًا، ويوزّع المتخصصين، ويدير الإيقاع، ويُنفِّذ التجميد والبوابات |
| 2 — Revenue الإيرادات | dealix-growth | Demand and founder media — الطلب وإعلام المؤسس |
| 2 — Revenue | dealix-research | Market and account intelligence — استخبارات السوق والحسابات |
| 2 — Revenue | dealix-sales | Qualification and proposals — التأهيل والعروض |
| 2 — Revenue | dealix-partnerships | Agency wedge, partner and affiliate program — مدخل الوكالات وبرنامج الشركاء والإحالات |
| 2 — Customer العميل | dealix-onboarding | Onboarding-to-value — الإدخال حتى القيمة |
| 2 — Customer | dealix-delivery | The 7-Day Sprint and Proof Pack — سبرنت الأيام السبعة وحزمة الإثبات |
| 2 — Customer | dealix-success | Retention and expansion — الاحتفاظ والتوسّع |
| 2 — Ops & Finance العمليات والمالية | dealix-finance | Invoicing preparation, cash, VAT/ZATCA, commissions — تحضير الفوترة والنقد والضريبة والعمولات |
| 2 — Ops & Finance | dealix-ops | Daily operating loop and ledgers — حلقة التشغيل اليومية والسجلات |
| 2 — Ops & Finance | dealix-analyst | KPIs, dashboards, reviews — المؤشرات ولوحات القياس والمراجعات |
| 2 — Governance & Quality الحوكمة والجودة | dealix-governance | Doctrine and approval guardian; can block other agents — حارس المبدأ والاعتماد؛ يقدر على إيقاف وكلاء آخرين |
| 2 — Governance & Quality | dealix-qa | Deliverable QA and capital grading — ضبط جودة المخرجات وتصنيف الجاهزية |
| 2 — Governance & Quality | dealix-content | Bilingual docs and copy — الوثائق والنصوص ثنائية اللغة |
| 2 — Governance & Quality | dealix-engineer | Freeze-bounded: verification and config only, no new product code — مقيّد بالتجميد: تحقق وضبط إعدادات فقط، لا شيفرة منتج جديدة |

## 3. The Orchestration Flow — تدفّق التنسيق

A unit of work moves on a fixed path. A trigger arrives. dealix-pm scopes it and dispatches the right specialists, in parallel where the tasks are independent. Outputs pass through dealix-governance and dealix-qa for review. If the result crosses the human boundary, it is queued for founder approval; otherwise it proceeds. Every step is recorded to a ledger.

تتحرك وحدة العمل على مسار ثابت. يصل مُحفِّز. يحدد dealix-pm نطاقه ويوزّع المتخصصين المناسبين، بالتوازي حين تكون المهام مستقلة. تمر المخرجات عبر dealix-governance وdealix-qa للمراجعة. إذا تجاوزت النتيجة الحد البشري وُضعت في طابور اعتماد المؤسس؛ وإلا مضت. كل خطوة تُسجَّل في سجل.

Worked example: a new lead arrives. dealix-research builds the account dossier. dealix-sales runs qualification and drafts the proposal. dealix-onboarding prepares the onboarding pack. dealix-delivery runs the 7-Day Sprint and assembles the Proof Pack. dealix-qa grades the deliverable. dealix-success drafts the expansion path. The proposal send, the invoice, and any case publication are queued for the founder; everything else completes inside the agent team.

مثال تطبيقي: يصل عميل محتمل. يبني dealix-research ملف الحساب. يُجري dealix-sales التأهيل ويصيغ العرض. يُحضّر dealix-onboarding حزمة الإدخال. ينفّذ dealix-delivery سبرنت الأيام السبعة ويجمّع حزمة الإثبات. يُصنّف dealix-qa المخرَج. يصيغ dealix-success مسار التوسّع. إرسال العرض والفاتورة وأي نشر للحالة تُوضع في طابور المؤسس؛ وكل ما عداها يكتمل داخل فريق الوكلاء.

## 4. The Human Boundary — الحد البشري

Five actions are never automated. Each requires founder sign-off before it occurs:

خمسة إجراءات لا تُؤتمت أبدًا. كل منها يتطلب توقيع المؤسس قبل وقوعه:

- Sending any external message — إرسال أي رسالة خارجية.
- Charging a customer or sending an invoice — تحصيل مبلغ من عميل أو إرسال فاتورة.
- Publishing a customer name, logo, or case — نشر اسم عميل أو شعاره أو حالته.
- Waiving a launch gate — إسقاط بوابة إطلاق.
- Lifting the Commercial Freeze — رفع التجميد التجاري.

Agents draft, prepare, and queue these actions; they never execute them. Dealix does not send messages on a customer's behalf without explicit approval, and there is no live-charge path.

الوكلاء يصيغون هذه الإجراءات ويحضّرونها ويضعونها في الطابور؛ ولا ينفّذونها. لا ترسل Dealix رسائل نيابة عن عميل دون موافقة صريحة، ولا يوجد مسار تحصيل مباشر.

## 5. Operating Cadence Mapped to Agents — الإيقاع التشغيلي مسندًا للوكلاء

- Daily — يوميًا: dealix-ops assembles the daily scorecard and updates the ledgers; dealix-pm clears the approval queue with the founder — يجمّع dealix-ops البطاقة اليومية ويحدّث السجلات؛ ويخلي dealix-pm طابور الاعتماد مع المؤسس.
- Weekly — أسبوعيًا: dealix-analyst drafts the weekly review; dealix-pm runs the cadence meeting and the friction-log review — يصيغ dealix-analyst المراجعة الأسبوعية؛ ويدير dealix-pm اجتماع الإيقاع ومراجعة سجل الاحتكاك.
- Monthly — شهريًا: dealix-analyst drafts the monthly review; dealix-pm runs the gate reviews; dealix-finance prepares the cash and VAT/ZATCA close — يصيغ dealix-analyst المراجعة الشهرية؛ ويدير dealix-pm مراجعات البوابات؛ ويُعدّ dealix-finance إقفال النقد والضريبة.

All figures in these reviews are estimated until verified; agents label them as estimates and never present a conversion rate or ROI as fact.

كل الأرقام في هذه المراجعات تقديرية حتى تُتحقَّق؛ يُعنونها الوكلاء كتقديرات ولا يقدّمون نسبة تحويل أو عائدًا كحقيقة.

## 6. Escalation & Guardrails — التصعيد والضوابط

dealix-governance can block any agent output that violates a non-negotiable or drifts from `../MONEY_LADDER.md` or `../NARRATIVE_STANDARD.md` — including any output describing scraping, cold WhatsApp automation, LinkedIn automation, or bulk outreach as an offered service, or implying guaranteed sales. Blocked work returns to its specialist for correction. Anything ambiguous escalates to dealix-pm, and if still unresolved, to the founder. No agent overrides governance.

يقدر dealix-governance على إيقاف أي مخرَج وكيل يخالف بندًا غير قابل للتفاوض أو ينحرف عن `../MONEY_LADDER.md` أو `../NARRATIVE_STANDARD.md` — بما في ذلك أي مخرَج يصف الكشط أو أتمتة الواتساب البارد أو أتمتة لينكدإن أو التواصل بالجملة كخدمة معروضة، أو يوحي بمبيعات مضمونة. يعود العمل الموقوف إلى متخصصه للتصحيح. أي أمر غامض يُصعَّد إلى dealix-pm، وإن بقي دون حسم، إلى المؤسس. لا وكيل يتجاوز الحوكمة.

## 7. Canonical References — المراجع المرجعية

- `../MONEY_LADDER.md`
- `../NARRATIVE_STANDARD.md`
- `../00_constitution/NON_NEGOTIABLES.md`
- `../ops/COMMERCIAL_FREEZE.md`
- `../launch/LAUNCH_MASTER_INDEX.md`
- `../90_DAY_BUSINESS_EXECUTION_PLAN.md`
- `.claude/agents/` — the directory where the agent definitions live — المجلد الذي تقيم فيه تعريفات الوكلاء.

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
