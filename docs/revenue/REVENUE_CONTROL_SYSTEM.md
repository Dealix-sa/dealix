---
title: Revenue Control System
owner: Founder
status: active
last_review: 2026-05-23
---

# Revenue Control System — نظام ضوابط الإيرادات

## Purpose

Prevent bad revenue from entering the pipeline. Each control has a trigger, an action, and an evidence trail. Revenue that bypasses a control is treated as a near-miss incident.

## Controls

| ID | Control | Trigger | Action | Evidence |
|---|---|---|---|---|
| R-01 | Qualification gate | Lead enters pipeline | Score against [SCORING_RULES.md](../delivery/revenue_sprint/SCORING_RULES.md); reject < 70 | `lead_table.score` |
| R-02 | Decision-maker gate | Before proposal | Confirm contact has signing authority | `intake.decision_maker = true` |
| R-03 | Scope gate | Before proposal | Match request to [SCOPE.md](../offers/revenue_sprint/SCOPE.md); out-of-scope → custom or refuse | `proposal.scope_match` |
| R-04 | Bad-revenue filter | Before quote | Run against [BAD_REVENUE_FILTER.md](./BAD_REVENUE_FILTER.md) | `proposal.bad_revenue_check` |
| R-05 | Pricing gate | Before quote | Match price to [PRICING.md](../offers/revenue_sprint/PRICING.md); deviations require A2 | `proposal.price_band` |
| R-06 | Payment gate | Before delivery starts | Invoice paid (sprint) or first milestone paid (retainer) | bank transaction reference |
| R-07 | Refund gate | On refund request | Match against [CASH_RULES.md](./CASH_RULES.md) refund triggers | approval file |
| R-08 | Claim gate | Any revenue claim in public | A3 approval + evidence | approval file + [docs/trust/NO_OVERCLAIM_POLICY.md](../trust/NO_OVERCLAIM_POLICY.md) |
| R-09 | Capacity gate | Before accepting a new sprint | Confirm delivery slot available | capacity calendar |

## Operational steps

1. Every pipeline stage has at least one control attached.
2. Controls run automatically where possible; manually otherwise.
3. A control that has no recent evidence is treated as broken until tested.
4. Bypass requires founder + Trust Lead written approval, logged as an exception.

## Exception log

`dealix-ops-private/revenue/exceptions/YYYY-MM.md` — every bypass with justification and time-bound expiry.

## Cross-links

- [docs/trust/TRUST_CONTROL_SYSTEM.md](../trust/TRUST_CONTROL_SYSTEM.md)
- [PIPELINE_STAGES.md](./PIPELINE_STAGES.md)
- [CASH_RULES.md](./CASH_RULES.md)
- [BAD_REVENUE_FILTER.md](./BAD_REVENUE_FILTER.md)

## Owner & cadence

- Founder. Monthly control test, quarterly review.

## AR — ملخّص

نظام ضوابط الإيرادات يمنع الإيراد السيّئ من الدخول. كل ضابط له مُحفّز وإجراء ودليل. التجاوز يحتاج موافقة موثّقة وانتهاء صلاحية. كل ضابط بلا دليل حديث يُعتبر معطّلًا. القيمة التقديرية ليست قيمة مُتحقَّقة.
