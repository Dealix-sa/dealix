# Founder Daily Command — قيادة المؤسس اليومية

**Status: INTERNAL**

> Purpose — الغرض: the founder's daily operating rhythm for running Dealix as a Saudi-first AI Business Operating System. This is the internal cockpit that answers the five operating questions every working day. Cross-link: [WEEKLY_BOARD_REVIEW.md](./WEEKLY_BOARD_REVIEW.md), [LAUNCH_GO_NO_GO.md](./LAUNCH_GO_NO_GO.md), [../04_delivery/COMMAND_SPRINT_DELIVERY_OS.md](../04_delivery/COMMAND_SPRINT_DELIVERY_OS.md), [../03_governance/HUMAN_APPROVAL_POLICY.md](../03_governance/HUMAN_APPROVAL_POLICY.md).

إيقاع تشغيلي يومي للمؤسس. هذه الوثيقة داخلية ليست موجهة للعميل. الهدف أن يجيب المؤسس كل يوم على الأسئلة التشغيلية الخمسة دون فوضى ودون ادّعاءات بلا دليل.

---

## The five operating questions — الأسئلة التشغيلية الخمسة

Dealix runs on one rhythm. Every day, in order:

1. **What is happening?** — ما الذي يحدث؟ — pipeline state, live engagements, ledgers.
2. **What should happen next?** — ما الذي يجب أن يحدث تاليًا؟ — the top three actions.
3. **Who approves?** — من يوافق؟ — the approval queue and its owners.
4. **What is the evidence?** — ما الدليل؟ — proof additions, value tier movements.
5. **What is the next action?** — ما الإجراء التالي؟ — one committed action per engagement.

No day is closed until all five have an answer. Where there is no evidence, the answer is recorded as "no evidence yet" — never invented.

---

## Morning command brief — الموجز الصباحي (15 minutes)

Open the Executive Command Brief view (Command Sprint module 4 surface, internal mode). Read in this order:

- **Live engagements** — العمليات الجارية: each active Command Sprint with its current day and status (LIVE / BETA / BLOCKED).
- **Pipeline** — خط الفرص: new inquiries, qualified, proposal sent, won/lost since yesterday.
- **Ledger deltas** — تغيّرات السجلات: new Proof Register entries, Value Ledger tier changes, Capital assets deposited.
- **Risk flags** — تنبيهات المخاطر: any governance BLOCK, any claim flagged unsafe, any data passport issue.

The brief states facts only. If a number cannot be sourced to a ledger, it does not enter the brief.

---

## Approval queue review — مراجعة طابور الموافقات (10 minutes)

Per [../03_governance/HUMAN_APPROVAL_POLICY.md](../03_governance/HUMAN_APPROVAL_POLICY.md), every customer-facing external action, every claim, and every send waits in the Approval Register (Command Sprint module 5). Each morning:

- Read each pending item with its class (external action / claim / send / data use).
- Decide: approve, reject, or request revision. Record the decision and one-line reason.
- Confirm nothing was auto-sent overnight. Dealix never auto-sends; if the log shows a send, it must map to a prior logged approval.

An item older than one working day without a decision is itself a flag — review why it is stuck.

---

## Pipeline + proof review — مراجعة خط الفرص والإثبات (15 minutes)

- **Pipeline** — for each open opportunity: stage, next step, owner, and whether the next step needs approval.
- **Proof** — for each delivering engagement: which Proof Register sections are complete, which evidence tier (estimated / observed / verified / client_confirmed) each value item carries.

Enforce the discipline: a value item may only be raised from `estimated` to `verified` with a source reference, and to `client_confirmed` with a confirmation reference. See [../04_delivery/PROOF_PACK_TEMPLATE.md](../04_delivery/PROOF_PACK_TEMPLATE.md).

---

## Top three actions — أهم ثلاثة إجراءات

Choose exactly three actions for the day. More than three is a planning failure, not ambition. Each action names:

- The engagement or opportunity it serves.
- The expected output (a ledger entry, a sent-after-approval item, a deliverable section).
- Whether it requires an approval gate before execution.

Write them down. The Next Action Board (Command Sprint module 6) is the single source of truth for what is committed today.

---

## End-of-day log — سجل نهاية اليوم (10 minutes)

Close the day by recording, in the internal log:

- What ran and what completed (mapped to ledger entries).
- Which approvals were decided, and which remain pending and why.
- Any new proof or value movement, with its tier.
- Any blocker carried to tomorrow.
- The three actions for tomorrow, drafted (not final).

Silence and undocumented days erode trust faster than any single defect. The end-of-day log is the cheapest insurance against silent drift.

---

## Daily non-negotiables — محظورات يومية

- No claim enters any artifact without evidence or safe wording.
- No external customer-facing action without a logged founder approval.
- No auto-send, no cold WhatsApp automation, no scraping behind login.
- No revenue or ROI stated as fact — always estimated, observed, verified, or client_confirmed with its source.
- Distinguish LIVE / BETA / INTERNAL / DOCS_ONLY / FUTURE / BLOCKED in every status note.

---

## Cross-references — مراجع متقاطعة

- Weekly roll-up of these daily logs: [WEEKLY_BOARD_REVIEW.md](./WEEKLY_BOARD_REVIEW.md).
- Launch gate that this rhythm supports: [LAUNCH_GO_NO_GO.md](./LAUNCH_GO_NO_GO.md).
- Approval rules behind the queue review: [../03_governance/HUMAN_APPROVAL_POLICY.md](../03_governance/HUMAN_APPROVAL_POLICY.md).
- Claim discipline behind proof review: [../03_governance/CLAIMS_REGISTER.md](../03_governance/CLAIMS_REGISTER.md).
- Delivery rhythm being commanded: [../04_delivery/COMMAND_SPRINT_DELIVERY_OS.md](../04_delivery/COMMAND_SPRINT_DELIVERY_OS.md).
