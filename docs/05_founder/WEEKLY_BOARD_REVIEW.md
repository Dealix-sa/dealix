# Weekly Board Review — المراجعة الأسبوعية للمجلس

**Status: INTERNAL**

> Purpose — الغرض: the weekly board/exec review template for Dealix. It rolls up the daily command logs into a decision-grade review: metrics, proof, approvals, blockers, decisions, and next-week commitments. Cross-link: [FOUNDER_DAILY_COMMAND.md](./FOUNDER_DAILY_COMMAND.md), [LAUNCH_GO_NO_GO.md](./LAUNCH_GO_NO_GO.md), [../06_growth/GROWTH_METRICS.md](../06_growth/GROWTH_METRICS.md), [../03_governance/HUMAN_APPROVAL_POLICY.md](../03_governance/HUMAN_APPROVAL_POLICY.md).

قالب مراجعة أسبوعية على مستوى المجلس التنفيذي. يحوّل سجلات المؤسس اليومية إلى مراجعة قابلة للقرار: المؤشرات، الإثبات، الموافقات، المعوّقات، القرارات، والتزامات الأسبوع القادم. كل قسم له ما يقابله بالعربية بنفس البنية.

---

## How to run — كيفية التشغيل

- Cadence — الإيقاع: once per week, fixed day, fixed time.
- Inputs — المدخلات: the five end-of-day logs from [FOUNDER_DAILY_COMMAND.md](./FOUNDER_DAILY_COMMAND.md), the Value Ledger, the Proof Register, the Approval Register.
- Rule — القاعدة: every metric must be sourced to a ledger. Numbers without a source do not enter the review. No projection is presented as fact.

---

## 1. Metrics review — مراجعة المؤشرات

Pull the canonical metrics from [../06_growth/GROWTH_METRICS.md](../06_growth/GROWTH_METRICS.md). For each, record this week's value, last week's value, and the delta:

| Metric — المؤشر | This week | Last week | Delta | Source ledger |
|---|---|---|---|---|
| New inquiries — استفسارات جديدة | | | | pipeline |
| Qualified opportunities — فرص مؤهلة | | | | pipeline |
| Command Sprints delivered — سبرنتات مُسلَّمة | | | | engagement registry |
| Proof score average — متوسط درجة الإثبات | | | | Proof Register |
| Value confirmed (client_confirmed) — قيمة مؤكدة | | | | Value Ledger |
| Approvals decided / pending — موافقات | | | | Approval Register |

Value figures carry their tier. Only `client_confirmed` items may be described as realized; everything else stays estimated or observed.

---

## 2. Proof additions — إضافات الإثبات

- New Proof Register sections completed this week, per engagement.
- Any evidence tier upgrade (estimated → observed → verified → client_confirmed) with its source/confirmation reference.
- Any case-safe summary drafted, and whether customer approval to publish was obtained. No public case study without customer approval.

State proof as evidenced opportunities, never as guaranteed outcomes.

---

## 3. Approvals log — سجل الموافقات

Per [../03_governance/HUMAN_APPROVAL_POLICY.md](../03_governance/HUMAN_APPROVAL_POLICY.md):

- Count of approvals requested, approved, rejected, revised this week, by class (external action / claim / send / data use).
- Any item that sat pending more than one working day — and why.
- Confirmation that zero external actions occurred without a logged approval. If any exception is found, it is a P1 governance incident and leads this section.

---

## 4. Blockers — المعوّقات

For each blocker carried across days this week:

- What it blocks (engagement, pipeline stage, or launch item).
- Status: LIVE / BETA / BLOCKED / FUTURE.
- Owner and the single next action to clear it.
- Whether it touches a non-negotiable (data, claims, approval, channel). Governance blockers outrank revenue blockers.

---

## 5. Decisions — القرارات

Record each decision taken in the review as a durable entry:

- Decision text (AR + EN), one line each.
- Rationale and the evidence it rests on.
- Owner and date.
- Reversibility: one-way door or two-way door.

Decisions without a named owner are not decisions; they are wishes.

---

## 6. Next-week commitments — التزامات الأسبوع القادم

- Up to five committed outcomes for next week, each with an owner and a measurable signal of done.
- Each commitment maps to a ledger entry it will produce or a launch item it advances.
- Carry-over commitments are marked as such; chronic carry-over is itself reviewed.

---

## Launch linkage — الارتباط بالإطلاق

Until launch, this review also walks the open items in [LAUNCH_GO_NO_GO.md](./LAUNCH_GO_NO_GO.md): which gate items moved to GO this week, which remain NO-GO, and the single blocking owner for each. The board does not declare launch readiness in the daily rhythm; it is declared only here, against the gate.

---

## Cross-references — مراجع متقاطعة

- Daily inputs to this review: [FOUNDER_DAILY_COMMAND.md](./FOUNDER_DAILY_COMMAND.md).
- Metric definitions: [../06_growth/GROWTH_METRICS.md](../06_growth/GROWTH_METRICS.md) *(create if missing)*.
- Launch gate: [LAUNCH_GO_NO_GO.md](./LAUNCH_GO_NO_GO.md).
- Approval classes: [../03_governance/HUMAN_APPROVAL_POLICY.md](../03_governance/HUMAN_APPROVAL_POLICY.md).
- Claim discipline: [../03_governance/CLAIMS_REGISTER.md](../03_governance/CLAIMS_REGISTER.md).
