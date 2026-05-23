---
title: Revenue Sprint Factory
owner: Delivery Lead
status: active
last_review: 2026-05-23
---

# Revenue Sprint Factory — مصنع سبرنت الإيرادات

## Purpose

The operational view of how one Revenue Sprint moves from paid invoice to handover. Stages, inputs, outputs, SLAs, owners. If a sprint slips, this page tells you which stage failed.

## Stages

| # | Stage | Input | Output | SLA | Owner |
|---|---|---|---|---|---|
| 1 | Intake | Paid invoice + completed intake form | Confirmed sector, ICP, geography, decision-maker context | 1 business day | Delivery Lead |
| 2 | Source plan | Intake | List of public sources to query, queries themselves | 1 business day | Delivery Lead |
| 3 | Lead surfacing | Source plan | Raw lead table (up to tier cap) | 2 business days | Agent + Delivery Lead |
| 4 | Scoring | Raw lead table | Scored table, top 5–10 marked | within stage 3 | Delivery Lead |
| 5 | Next-step pack | Scored table + intake | Outreach openers, talking points, qualifying questions | 1 business day | Delivery Lead |
| 6 | QA gate | All deliverables | Pass or rework list | 0.5 business day | Trust Lead or Delivery Lead (rotating) |
| 7 | Handover prep | QA pass | Report PDF, lead table files (.xlsx + .csv), pack | 0.5 business day | Delivery Lead |
| 8 | Handover review | All deliverables | 30-min session, written feedback | 30 min | Founder or Delivery Lead |
| 9 | Evidence pack | Handover acknowledgment | Evidence pack archived (private repo) | 1 business day | Delivery Lead |

Total: 5 to 7 business days end-to-end.

## Inputs to the factory

- Intake form (completed by buyer).
- Confirmed scope and tier.
- Capacity slot (booked at Reply stage, see [docs/revenue/PIPELINE_STAGES.md](../../revenue/PIPELINE_STAGES.md)).

## Outputs the factory produces

- Lead table (`.xlsx` + `.csv`) per [LEAD_TABLE_SCHEMA.md](./LEAD_TABLE_SCHEMA.md).
- Reviewed report PDF per [REPORT_TEMPLATE.md](./REPORT_TEMPLATE.md).
- Next-step pack (PDF + editable doc) per [OUTREACH_PACK_TEMPLATE.md](./OUTREACH_PACK_TEMPLATE.md).
- Handover note per [HANDOFF_TEMPLATE.md](./HANDOFF_TEMPLATE.md).
- Evidence pack in `dealix-ops-private/evidence/sprints/<sprint_id>/`.

## SLA discipline

1. Each stage timestamp logged on entry and exit.
2. If a stage runs over its SLA by more than 25%, an inline note is added and the founder is informed by EoD.
3. Cumulative slippage of more than one business day pushes the handover date; the buyer is notified within 4 hours of detection.

## Cross-links

- [DELIVERY_CONTROL_SYSTEM.md](./DELIVERY_CONTROL_SYSTEM.md)
- [DELIVERY_PLAYBOOK.md](./DELIVERY_PLAYBOOK.md)
- [CLIENT_INTAKE.md](./CLIENT_INTAKE.md)
- [QA_CHECKLIST.md](./QA_CHECKLIST.md)
- [docs/delivery/DELIVERY_LIFECYCLE.md](../DELIVERY_LIFECYCLE.md)

## Owner & cadence

- Delivery Lead. Reviewed after every sprint; structural review quarterly.

## AR — ملخّص

مصنع السبرنت تسع مراحل من الفاتورة المدفوعة إلى التسليم: استلام، خطّة مصادر، استكشاف، تسجيل، حزمة خطوة تالية، بوّابة جودة، تحضير تسليم، جلسة تسليم، حزمة أدلة. كل مرحلة بمدخل ومُخرج ومالك ومدة معيارية. مجموع المدة 5–7 أيام عمل، وأي انزلاق يُبلَّغ به المؤسس واليوم نفسه. القيمة التقديرية ليست قيمة مُتحقَّقة.
