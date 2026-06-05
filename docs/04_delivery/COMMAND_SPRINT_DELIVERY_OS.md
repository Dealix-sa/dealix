# Command Sprint Delivery OS — نظام تسليم سبرنت القيادة

**Status: BETA**

> Purpose — الغرض: the end-to-end delivery playbook for the Dealix Command Sprint, the first commercial offer of the Saudi-first AI Business Operating System. It runs intake through the eight modules to a delivered Proof Pack and an upsell recommendation, with explicit approval gates. Cross-link: [CUSTOMER_FOLDER_TEMPLATE.md](./CUSTOMER_FOLDER_TEMPLATE.md), [PROOF_PACK_TEMPLATE.md](./PROOF_PACK_TEMPLATE.md), [../05_founder/FOUNDER_DAILY_COMMAND.md](../05_founder/FOUNDER_DAILY_COMMAND.md), [../03_governance/HUMAN_APPROVAL_POLICY.md](../03_governance/HUMAN_APPROVAL_POLICY.md), [../03_governance/CLAIMS_REGISTER.md](../03_governance/CLAIMS_REGISTER.md).

كتاب تشغيل متكامل لتسليم سبرنت القيادة من الاستقبال حتى حزمة الإثبات وتوصية الترقية، مع بوابات اعتماد صريحة. الذكاء يستكشف ويحلّل ويوصي، والمهام المُحدَّدة تُنفِّذ، والمؤسس يعتمد كل التزام خارجي حرج.

---

## Engagement rhythm — إيقاع التكليف

The sprint runs across five working days. Each module names its inputs, its outputs, its approval gate, and what the client receives. No module advances on an opportunity without a matching proof event recorded.

يمتد السبرنت على خمسة أيام عمل. كل وحدة تسمّي مدخلاتها ومخرجاتها وبوابة اعتمادها وما يستلمه العميل. لا تتقدّم أي وحدة على فرصة دون حدث إثبات مُسجَّل.

| Day — اليوم | Modules — الوحدات |
|---|---|
| 1 | Intake + Market Intelligence Lite |
| 2 | Revenue Map + Proof Register opened |
| 3 | Executive Command Brief + Approval Register |
| 4 | Next Action Board + Delivery Lite |
| 5 | Upsell Recommendation + Proof Pack handover |

---

## Intake — الاستقبال

**Inputs — المدخلات:** signed engagement, source passport (`client_upload` / `crm_export` / `manual_entry` — never `scraped`), named workflow owner on the client side, one primary workflow to focus.

**Outputs — المخرجات:** engagement ID, customer folder created per [CUSTOMER_FOLDER_TEMPLATE.md](./CUSTOMER_FOLDER_TEMPLATE.md), lawful basis recorded.

**Approval gate — بوابة الاعتماد:** the source passport is the contract. If the client cannot declare data ownership and allowed use, the sprint does not begin.

**Client receives — يستلم العميل:** confirmation of scope, the disclosure line, and the single focus workflow in writing.

---

## Module 1 — Market Intelligence Lite — ذكاء السوق المُصغَّر

**Inputs:** client sector, public market context, the focus workflow.

**Outputs:** a short, sourced read of the sector and the opportunity space around the focus workflow. Aggregated patterns and methodology only — no confidential metrics, no scraping behind login.

**Approval gate:** any external-facing phrasing is checked against the Claims Register before it can appear in a deliverable.

**Client receives:** a market context section, evidence-tagged, with sources named.

المخرجات: قراءة قطاعية موجزة مُسنَدة بالمصادر، أنماط مُجمَّعة ومنهجية فقط، دون مقاييس سرية ودون استخلاص خلف تسجيل الدخول.

---

## Module 2 — Revenue Map — خريطة الإيرادات

**Inputs:** client pipeline / accounts data via the data layer (`data_os`), DQ score, the focus workflow.

**Outputs:** a map of opportunities by stage — what is happening across the revenue surface, where value is stuck, where dormant value sits.

**Approval gate:** DQ baseline reviewed. A DQ score that is too low means a data-readiness problem, surfaced honestly, not papered over.

**Client receives:** the Revenue Map answering question one — *What is happening?* — with every figure tier-tagged.

المخرجات: خريطة الفرص حسب المرحلة تجيب على السؤال الأول — ماذا يحدث؟ — وكل رقم موسوم بدرجته.

---

## Module 3 — Proof Register — سجل الإثبات

**Inputs:** every work item completed in modules 1–2, with its source reference.

**Outputs:** an evidence log. Each entry carries a tier: estimated / observed / verified / client_confirmed. No fake proof. A value item rises from estimated only with a source reference, and to client_confirmed only with a client confirmation reference.

**Approval gate:** evidence tiers are reviewed before any value figure is reported.

**Client receives:** transparency into what is evidenced versus estimated. See [PROOF_PACK_TEMPLATE.md](./PROOF_PACK_TEMPLATE.md).

---

## Module 4 — Executive Command Brief — الموجز القيادي التنفيذي

**Inputs:** the Revenue Map, the Proof Register, governance flags.

**Outputs:** a one-surface executive read — pipeline state, top risks, blocked items, and what should happen next. This is the answer to question five — *What is the next action?*

**Approval gate:** the brief states facts only; any figure not traceable to a ledger is removed.

**Client receives:** the Executive Command Brief, the centerpiece of the sprint.

---

## Module 5 — Approval Register — سجل الاعتماد

**Inputs:** every proposed action that touches a customer or makes a claim.

**Outputs:** a register answering *Who approves?* Each item has a class (external action / claim / send / data use), an owner, and a decision line.

**Approval gate:** this module *is* the gate. Nothing customer-facing leaves Dealix or the client's name without a recorded approval. See [../03_governance/HUMAN_APPROVAL_POLICY.md](../03_governance/HUMAN_APPROVAL_POLICY.md).

**Client receives:** clarity on who approves what, and the assurance that Dealix never auto-sends and never acts externally on their behalf without explicit approval.

المخرجات: سجل يجيب على — من يعتمد؟ — لا تخرج أي مادة موجهة للعميل دون اعتماد مُسجَّل، ولا إرسال تلقائي مطلقاً.

---

## Module 6 — Next Action Board — لوحة الإجراء التالي

**Inputs:** the brief, the approval register, the focus workflow.

**Outputs:** a prioritized board of next actions, each with an owner, a deadline, and a definition of done. This answers *What should happen next?*

**Approval gate:** actions that require external contact are marked and routed to the Approval Register before execution.

**Client receives:** an actionable board, not a report that sits unread.

---

## Module 7 — Delivery Lite — التسليم المُصغَّر

**Inputs:** the approved next actions, the client's chosen channels.

**Outputs:** drafts prepared for the approved actions — never sent automatically. Each draft is checked for forbidden patterns (no cold WhatsApp automation, no bulk outreach, no scraped data) and for safe claim wording.

**Approval gate:** every draft waits for an explicit founder/client approval line before any send. Dealix prepares; the human approves; the deterministic workflow executes.

**Client receives:** approval-ready drafts and a clear record that nothing went out without sign-off.

المخرجات: مسودات جاهزة للاعتماد لا تُرسَل تلقائياً، مفحوصة من الأنماط المحظورة ومن سلامة الصياغة.

---

## Module 8 — Upsell Recommendation — توصية الترقية

**Inputs:** the full sprint record, the Proof Register, observed value tiers.

**Outputs:** a recommended next step — a retainer path or a deeper module — justified by evidenced opportunities, never by guaranteed outcomes.

**Approval gate:** the recommendation is checked against the Claims Register; no revenue or ROI is stated as fact.

**Client receives:** an honest recommendation framed as evidenced opportunities, with the choice left to them.

---

## Handover — التسليم النهائي

The sprint closes with the Proof Pack delivered per [PROOF_PACK_TEMPLATE.md](./PROOF_PACK_TEMPLATE.md), the customer folder finalized per [CUSTOMER_FOLDER_TEMPLATE.md](./CUSTOMER_FOLDER_TEMPLATE.md), and the value ledger entries tier-tagged. Every customer-facing artifact ends with the disclosure line.

يُختَم السبرنت بتسليم حزمة الإثبات، وإغلاق مجلد العميل، وقيود سجل القيمة الموسومة بدرجاتها. كل مادة موجهة للعميل تنتهي بسطر الإفصاح.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
