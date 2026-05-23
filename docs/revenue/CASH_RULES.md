---
title: Cash Rules
owner: Founder
status: active
last_review: 2026-05-23
---

# Cash Rules — قواعد النقد

## Purpose

How Dealix collects, holds, and refunds money. Written so anyone can answer a buyer's payment question without inventing.

## Currency

- KSA buyers: SAR only.
- Non-KSA buyers (rare, opt-in): USD via a documented vendor; pricing tracks SAR band with FX disclosure.

## Invoicing

- Invoice issued from a registered Saudi entity (`dealix-ops-private/legal/entity.md`).
- VAT applied per ZATCA rules.
- Invoice carries scope reference, evidence policy reference, and payment terms.
- All invoices are filed under `dealix-ops-private/invoices/YYYY/`.

## Payment terms by rung

| Rung | Term |
|---|---|
| Free Diagnostic | n/a |
| Revenue Sprint (499) | 100% in advance |
| Data Pack (1,500) | 50% advance, 50% at handover |
| Managed Ops (2,999–4,999/mo) | Monthly in advance, net-0 |
| Custom AI (5,000–25,000) | 40% on signature, 40% at midpoint milestone, 20% at handover |

## Refund triggers

A refund is owed when **any** of the following is true:

1. The deliverable falls outside the signed scope and Dealix cannot rectify within the original SLA.
2. Dealix breaches a non-negotiable (e.g., includes PII in a deliverable to a non-authorized recipient).
3. A control fails in a way that materially harms the buyer's interest.

Refund amounts:

- Sprint: full diagnostic fee.
- Data pack: pro-rata against unmet milestones.
- Managed ops: pro-rata for the unused portion of the current month.
- Custom AI: pro-rata against approved milestones; in-flight work product remains with Dealix unless otherwise agreed.

## Approvals

| Refund size | Approval level |
|---|---|
| ≤ 500 SAR | A1 |
| 501–10,000 SAR | A2 |
| > 10,000 SAR | A3 |

## Disputes

1. Raised in writing.
2. Founder responds within 5 business days.
3. Reference: [docs/offers/revenue_sprint/TERMS.md](../offers/revenue_sprint/TERMS.md).

## Evidence

- Invoice file, payment confirmation, bank transaction reference for every cash event.
- Refund file with approval and bank reference.

## Cross-links

- [REVENUE_CONTROL_SYSTEM.md](./REVENUE_CONTROL_SYSTEM.md) — R-06, R-07.
- [BAD_REVENUE_FILTER.md](./BAD_REVENUE_FILTER.md)
- [docs/revenue/INVOICE_FLOW.md](./INVOICE_FLOW.md) — existing flow doc.
- [docs/trust/APPROVAL_MATRIX.md](../trust/APPROVAL_MATRIX.md)

## Owner & cadence

- Founder. Reviewed quarterly; updated whenever pricing changes.

## AR — ملخّص

قواعد النقد تحدّد العملة (الريال للسعودية)، الفوترة عبر كيان سعودي، شروط الدفع لكل درجة من السُلَّم، ومُحفّزات الاسترداد. الموافقات حسب الحجم. كل حدث نقدي يحمل دليلًا في المستودع الخاص. القيمة التقديرية ليست قيمة مُتحقَّقة.
