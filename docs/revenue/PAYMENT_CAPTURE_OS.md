# Payment Capture OS

The CEO-layer view on cash capture. Extends the operational mechanics in
[`INVOICE_FLOW`](INVOICE_FLOW.md) and [`PAYMENT_RECONCILIATION`](PAYMENT_RECONCILIATION.md)
with a discipline for **shortening the cycle from approved proposal → paid
invoice**.

## The cycle

```
Proposal accepted
  → Invoice issued        (target: same day)
  → Payment link sent     (target: same day; through approval gate)
  → First reminder        (T+3 if unpaid)
  → Second reminder       (T+7 if unpaid)
  → CEO call              (T+10 if unpaid)
  → Payment received      (Moyasar event recorded in proof ledger)
```

## Inputs

- Existing payment events from [`auto_client_acquisition/payment_ops/`](../../auto_client_acquisition/payment_ops/)
- [`INVOICE_FLOW`](INVOICE_FLOW.md) — the operational invoicing pipeline
- [`PAYMENT_RECONCILIATION`](PAYMENT_RECONCILIATION.md) — reconciliation against the bank
- Moyasar verifier (existing)

## KPIs

| KPI | Target | Source |
|---|---|---|
| Days from proposal accept → invoice | ≤ 1 | timestamps in proof ledger |
| Days from invoice → paid | ≤ 14 | proof ledger |
| Reminder send rate | 100% of unpaid > 3 days | approval-center log |
| Failed-payment recovery rate | ≥ 80% within 30 days | renewal scheduler |

Live targets in [`dealix/execution_assurance/registry.yaml`](../../dealix/execution_assurance/registry.yaml).

## Generator

Daily refresh is part of the daily brief: `data/founder_briefs/ceo_daily_brief_<date>.md`
contains the cash position section.

## Cross-references

- [INVOICE_FLOW](INVOICE_FLOW.md)
- [PAYMENT_RECONCILIATION](PAYMENT_RECONCILIATION.md)
- [REVENUE_FACTORY_LIVE_DATA](REVENUE_FACTORY_LIVE_DATA.md)
- [DEAL_DESK_SYSTEM](DEAL_DESK_SYSTEM.md)

## Non-negotiables

Reminder messages flow through the approval center. Refunds, credits, and
payment-term changes require a deal-desk decision. Dealix never carries
customer funds; Moyasar processes the payment. See
[`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
