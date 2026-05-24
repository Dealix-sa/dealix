# Finance Hub — INDEX

CEO-facing capital decisions. This hub is **not** the accounting system —
that lives in [`docs/operating_finance/`](../operating_finance/) — and it is
**not** the customer-facing invoicing flow, which lives in
[`docs/revenue/INVOICE_FLOW.md`](../revenue/INVOICE_FLOW.md). What lives here:
how the CEO decides where to put time and money to gain the most leverage.

## Read in this order

1. [CAPITAL_ALLOCATION_SYSTEM](CAPITAL_ALLOCATION_SYSTEM.md) — quarterly buckets and gates
2. [ROI_PRIORITY_MATRIX](ROI_PRIORITY_MATRIX.md) — scoring rubric for any spend over the threshold
3. [FOUNDER_HOUR_ROI](FOUNDER_HOUR_ROI.md) — how to price a founder hour
4. [HIRE_VS_AUTOMATE_VS_PARTNER](HIRE_VS_AUTOMATE_VS_PARTNER.md) — three-way decision matrix

## Cross-references to existing systems

- [`docs/operating_finance/`](../operating_finance/) — accounting + bookkeeping + tax
- [`docs/enterprise/CAPITAL_LEDGER_V2.md`](../enterprise/CAPITAL_LEDGER_V2.md) — capital asset ledger
- [`docs/revenue/INVOICE_FLOW.md`](../revenue/INVOICE_FLOW.md) — customer billing
- [`docs/revenue/PAYMENT_RECONCILIATION.md`](../revenue/PAYMENT_RECONCILIATION.md) — paid event reconciliation
- [`docs/board_decision_system/`](../board_decision_system/) — board-level capital decisions

## Where the data lives

| Class | Location |
|---|---|
| Quarterly allocations (sensitive) | PRIVATE_OPS `ceo/capital_allocations.csv` |
| Hire / automate / partner log (sensitive) | PRIVATE_OPS `ceo/hire_vs_automate_log.csv` |
| ROI scores per initiative (CSV) | PRIVATE_OPS `ceo/capital_allocations.csv` (`roi_estimate` column) |

## Non-negotiables

This hub records intent and decisions. It never carries customer funds. It
never commits to payment terms with customers. Money movement still flows
through [`docs/revenue/INVOICE_FLOW.md`](../revenue/INVOICE_FLOW.md) + the
Moyasar verifier. See [`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
