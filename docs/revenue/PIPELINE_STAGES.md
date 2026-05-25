---
title: Pipeline Stages
owner: Founder
status: active
last_review: 2026-05-23
---

# Pipeline Stages — مراحل قمع الإيرادات

## Purpose

Define every stage of a Dealix opportunity, with entry and exit criteria. A deal cannot advance without meeting exit criteria. A deal at a stage too long triggers review.

## Stages

| # | Stage | Entry criteria | Exit criteria | Max time |
|---|---|---|---|---|
| 1 | Lead | Public source identifies a fit company | Named decision-maker contact captured | 3 days |
| 2 | DM | A1-approved outbound sent | Reply received or 7 days elapsed | 7 days |
| 3 | Reply | Buyer responded | 30-min call scheduled or sample requested | 5 days |
| 4 | Sample | Sample shared (rung 1 output) | Proposal requested or buyer declines | 7 days |
| 5 | Proposal | A1-approved proposal sent | Payment instruction issued, PO received, or decline | 10 days |
| 6 | Payment/PO | Invoice paid or PO signed | Delivery kicks off | 5 days |
| 7 | Delivery | Kickoff complete | Handover signed | per scope SLA |
| 8 | Feedback | Handover complete | Written feedback collected | 7 days |
| 9 | Retainer | Buyer expressed continued need | Retainer agreement signed | 14 days |

## Stage probabilities (for pipeline value)

| Stage | Probability |
|---|---|
| Lead | 5% |
| DM | 10% |
| Reply | 25% |
| Sample | 40% |
| Proposal | 60% |
| Payment/PO | 90% |
| Delivery | 100% (booked) |

Pipeline value = sum of (price × probability) across open opportunities. See [REVENUE_METRICS.md](./REVENUE_METRICS.md).

## Stage discipline

1. Each opportunity records the timestamp of stage entry.
2. Exceeding the max time without movement creates a "stale" flag in the daily report.
3. Stale opportunities get one of: a clear next step, a parked status with reason, or a closed-lost with reason.
4. No opportunity sits in two stages at once.

## Cross-links

- [REVENUE_CONTROL_SYSTEM.md](./REVENUE_CONTROL_SYSTEM.md) — controls applied per stage.
- [REVENUE_METRICS.md](./REVENUE_METRICS.md) — conversions between stages.
- [OFFER_LADDER.md](./OFFER_LADDER.md)
- [BAD_REVENUE_FILTER.md](./BAD_REVENUE_FILTER.md) — at stages 3 and 5.

## Owner & cadence

- Founder. Reviewed monthly; stage probabilities recalibrated quarterly.

## AR — ملخّص

تسع مراحل من الفرصة إلى الاحتفاظ. كل مرحلة لها معيار دخول ومعيار خروج وزمن أقصى. تجاوز الزمن يضع علامة "ثابتة" وتستوجب قرارًا: خطوة تالية، إيقاف، أو إغلاق خسارة. القيمة التقديرية ليست قيمة مُتحقَّقة.
