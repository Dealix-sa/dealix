---
title: Revenue Metrics
owner: Founder
status: active
last_review: 2026-05-23
---

# Revenue Metrics — مقاييس الإيرادات

## Purpose

Define every metric Dealix tracks, with its formula and source. No ambiguity. No two reports using the same name for different things.

## Metric catalog

| Name | Formula | Source | Window |
|---|---|---|---|
| Pipeline value | Σ (deal price × stage probability) for open deals | pipeline table + [PIPELINE_STAGES.md](./PIPELINE_STAGES.md) | live |
| Cash collected | Σ payments received | invoices + bank confirmations | rolling 30, 90, 365 days |
| MRR | Σ active retainer monthly fees | retainer agreements | live |
| Win rate | paid_deals / proposals_sent | pipeline log | 4-week rolling |
| Stage conversion: Reply → Sample | samples_sent / replies_in | pipeline log | 4-week rolling |
| Stage conversion: Sample → Proposal | proposals_sent / samples_sent | pipeline log | 4-week rolling |
| Stage conversion: Proposal → Paid | payments / proposals_sent | pipeline log | 4-week rolling |
| Average deal size | cash_collected / paid_deals | bank + pipeline | rolling 90 days |
| Refusal rate | refusals / leads_qualified | refusal log | rolling 30 days |
| Refund rate | refunds_issued / deals_delivered | refund + delivery logs | rolling 90 days |
| Sprint velocity | sprints_delivered_per_week | delivery log | rolling 4 weeks |
| Retainers active | count of active monthly agreements | retainer registry | live |

## Rules

1. Every metric is defined once, here. If a doc cites a metric, it links to this page.
2. Cash collected is the only revenue figure used externally; pipeline value is internal only.
3. ROI and value-impact claims for clients use estimated/observed/verified framing per [docs/08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md](../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md).

## What we never report

- Aggregated revenue across clients in a public artifact without consent and A3 approval.
- Projected revenue as if observed.
- A vanity metric (followers, impressions) framed as a business metric.

## Reporting outputs

- Daily: revenue log row in `dealix-ops-private/revenue/log/`.
- Weekly: summary in `dealix-ops-private/revenue/weekly/`.
- Quarterly: investor-style summary (private) including trend lines.

## Cross-links

- [REVENUE_COMMAND_CENTER.md](./REVENUE_COMMAND_CENTER.md)
- [PIPELINE_STAGES.md](./PIPELINE_STAGES.md)
- [OFFER_EVOLUTION_SYSTEM.md](./OFFER_EVOLUTION_SYSTEM.md)
- [docs/08_value_os/VALUE_LEDGER.md](../08_value_os/VALUE_LEDGER.md)

## Owner & cadence

- Founder. Definitions reviewed quarterly. Source schema review whenever pipeline tooling changes.

## AR — ملخّص

مقاييس الإيرادات تعريفات واحدة لكل مقياس مع الصيغة والمصدر والنافذة. النقد المُحصَّل هو الرقم الخارجي الوحيد، أما قيمة الأنبوب فداخلية. لا تقارير غرور، ولا أرقام مُسقَطة بصيغة مُلاحَظة. القيمة التقديرية ليست قيمة مُتحقَّقة.
