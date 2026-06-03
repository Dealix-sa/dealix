# Revenue Data Model

## Purpose
Define the canonical revenue data model: how an opportunity becomes a proposal becomes cash becomes MRR.

## States

```
[Lead] -> [Qualified] -> [Sample sent] -> [Proposal sent] -> [Verbal yes] -> [PO/Payment] -> [Cash collected] -> [Delivered] -> [Retainer offer]
                                                                                                                                |
                                                                                                                                +-> [MRR row]
```

## Tables

### `pipeline/pipeline_tracker.csv`
Columns: `company, sector, contact, stage, priority, next_action, last_touch, notes`
- `stage` ∈ {New, Qualified, Sample sent, Proposal sent, Verbal yes, Closed-won, Closed-lost}.
- `priority` ∈ {A, B, C}.

### `revenue/revenue_action_log.csv`
Columns: `date, lead_or_client, action, type, status, next_action, evidence`
- One row per outbound or follow-up action.
- `evidence` is a private path or note (never a public URL).

### `sales/proposal_tracker.csv`
Columns: `date, client, offer, amount_sar, status, follow_up_date, decision_maker, next_action, notes`
- `offer` ∈ the 5-rung product ladder.
- `status` ∈ {Draft, Sent, Negotiating, Verbal yes, Closed-won, Closed-lost, Withdrawn}.

### `revenue/cash_collected.csv`
Columns: `date, client, offer, amount_sar, payment_method, status, notes`
- One row per confirmed payment.
- `status` ∈ {Pending bank confirm, Confirmed, Refunded}.

### `revenue/pipeline_value.csv`
Columns: `company, offer, stage, deal_value_sar, probability, weighted_value, next_action`
- `weighted_value = deal_value_sar * probability`.

### `revenue/mrr_tracker.csv`
Columns: `client, plan, monthly_amount_sar, status, start_date, next_renewal, notes`
- One row per active retainer.

## Derived metrics
- Total cash collected = sum(cash_collected.amount_sar where status = Confirmed).
- Weighted pipeline = sum(pipeline_value.weighted_value).
- MRR = sum(mrr_tracker.monthly_amount_sar where status = Active).

## Dual logging rule
A row in `revenue_action_log.csv` is not enough on its own when money or material commitment changes hands. The same event must also appear in:
- `cash_collected.csv` (for payments), or
- `proposal_tracker.csv` (for proposals), or
- `evidence/execution_evidence_ledger.csv` (for everything else).
