# Revenue Control System

> Revenue is governed, not just chased.

## Inputs

- Qualified leads (from `docs/sales/` motion)
- Proposals (from `docs/sales/PROPOSAL_FAST_TEMPLATE.md`)
- Signed scopes / POs / payments

## Outputs

- Cash collected
- Pipeline value, weighted by stage probability
- MRR (active retainers)
- Loss reasons (for the Friction Log)

## Rules

1. **No full delivery without payment, PO, or written approval.**
2. Every proposal has a written follow-up date.
3. Every lead has a `next_action` and a `next_action_date`.
4. Discounts above **20%** require explicit CEO approval, in writing,
   citing the reason (volume, strategic value, retainer attached, etc.).
5. Discounts above **40%** are refused outright.
6. We do not collect bad revenue (see `BAD_REVENUE_FILTER.md`).
7. Refunds follow `docs/finance/REFUND_POLICY.md`.

## Stage Probability Weights

For pipeline value calculation:

| Stage | Probability |
|-------|-------------|
| New | 5% |
| Qualified | 15% |
| Contacted | 25% |
| Replied | 40% |
| Sample Sent | 55% |
| Call Booked | 65% |
| Proposal Sent | 75% |
| Paid | 100% |
| Delivered | 100% |
| Retainer | 100% (MRR) |
| Lost | 0% |

Pipeline value = Σ (amount × probability) over open stages.

## Metrics

- Cash collected (daily, weekly, monthly)
- Cash expected (30 / 60 / 90 days)
- Pipeline value (qualified, weighted)
- Proposal-to-payment conversion rate
- Average deal size (Sprint, Retainer)
- MRR (active retainers, net new)
- Gross margin estimate (Sprint and Retainer separately)

## Evidence

- `dealix-ops-private/revenue/cash_collected.csv`
- `dealix-ops-private/revenue/pipeline_value.csv`
- `dealix-ops-private/revenue/mrr_tracker.csv`
- `dealix-ops-private/revenue/invoices/`
- `dealix-ops-private/revenue/receipts/`

## Verifier

- Weekly: `make weekly-close` reconciles pipeline → cash actuals.
- Monthly: `MONTHLY_STRATEGY_REVIEW.md` audits proposal-to-payment rate.

## Review cadence

- Daily: pipeline + cash + overdue
- Weekly: full scorecard
- Monthly: pricing experiments + offer ladder review
