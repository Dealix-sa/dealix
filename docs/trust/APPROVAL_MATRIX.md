---
title: Approval Matrix
owner: Founder
status: active
last_review: 2026-05-23
---

# Approval Matrix — مصفوفة الموافقات

## Purpose

Define four approval levels and assign every category of decision to exactly one level. Removes "I wasn't sure if I needed to ask" as a failure mode.

## Levels

| Level | Meaning | Who approves | Time SLA |
|---|---|---|---|
| A0 | Auto. No approval needed. | Agent or operator runs it. | n/a |
| A1 | Founder click-approve. | Founder. | 24h |
| A2 | Founder written + counter-sign by Trust Lead. | Founder + Trust Lead. | 48h |
| A3 | A2 plus explicit external review (legal, advisor). Never auto-executes. | Founder + Trust Lead + external. | 5 business days |

## Categories

| Category | Level | Example |
|---|---|---|
| Internal note, draft, scratch | A0 | Agent drafts a lead summary into private repo. |
| Lead enrichment from public sources | A0 | Pulling a company's published number of branches. |
| Refund ≤ 500 SAR | A1 | Goodwill refund on a 499 SAR sprint. |
| Outbound proposal to a single buyer | A1 | Sending a tailored proposal to a CFO. |
| Refund 501–10,000 SAR | A2 | Disputed delivery, partial refund. |
| Signed contract or retainer | A2 | Monthly managed-ops agreement. |
| Public claim (LinkedIn post, case study) | A2 | A post citing a sprint outcome. |
| Compliance claim (PDPL, SDAIA alignment) | A3 | Stating "PDPL-aware" in a sales doc. |
| Revenue or ROI claim | A3 | Stating an estimated value for a sector. |
| Data export to a third party | A3 | Sending a lead table to a partner. |
| Regulator communication | A3 | Reply to a SDAIA, CITC, or DGA query. |
| Legal filing or response | A3 | Vendor contract clause negotiation. |

## Operational steps

1. Every action is tagged with its level before execution.
2. A0 actions still log to the AI Run Ledger; they just skip the queue.
3. A1 lives in the daily queue (see [TRUST_COMMAND_CENTER.md](./TRUST_COMMAND_CENTER.md)).
4. A2 and A3 require a written approval file under `dealix-ops-private/approvals/`.
5. A3 never executes from an automated workflow — humans push the button.

## Evidence

- A1: queue entry with timestamp and approver.
- A2: `approvals/AYYYY-NNN.md` with both signatures.
- A3: same file plus the external reviewer's note attached.

## Cross-links

- [AUTONOMY_POLICY.md](./AUTONOMY_POLICY.md) — what agents may run autonomously.
- [docs/05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md) — governance layer.
- [TRUST_CONTROL_SYSTEM.md](./TRUST_CONTROL_SYSTEM.md) — C-02, C-03, C-04.

## Owner & cadence

- Founder owns the matrix. Quarterly review.

## AR — ملخّص

مصفوفة الموافقات تُصنّف كل قرار إلى أربعة مستويات: A0 آلي، A1 موافقة بنقرة، A2 موافقة موقّعة، A3 موافقة موسّعة لا تُنفَّذ آليًا أبدًا. كل إجراء يُربط بمستواه قبل التنفيذ، ودليله محفوظ. القيمة التقديرية ليست قيمة مُتحقَّقة.
