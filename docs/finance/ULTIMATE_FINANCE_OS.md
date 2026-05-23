# Ultimate Finance OS

Two CSVs + a third for AI unit economics:

* `finance/payment_capture_queue.csv` — invoices awaiting payment.
* `finance/cash_collected.csv` — invoices paid.
* `finance/ai_unit_economics.csv` — per-agent cost vs. attributed revenue.

## Hard rules

* No agent may auto-issue an invoice.
* No agent may auto-change payment terms.
* No agent may auto-issue a refund.

All three are A3 actions in `policies/dealix_control_policy.yaml`.

## AI unit economics

`ai_unit_economics.csv` lets the founder see whether each agent is
actually paying for itself. Periodic rows are appended by a finance
worker (out of scope for this commit); the Founder Console renders the
row count today as a smoke check.
