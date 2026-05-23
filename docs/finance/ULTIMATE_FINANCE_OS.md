# Ultimate Finance OS

Two CSVs power finance:

- `${DEALIX_PRIVATE_OPS}/finance/cash_collected.csv`
- `${DEALIX_PRIVATE_OPS}/finance/payment_capture_queue.csv`

## Read endpoints

- `GET /api/v1/internal/finance/summary` — totals.
- The Finance page (`/finance`) renders cash, pipeline, weighted
  pipeline, payment follow-ups, MRR.

## Rules

- Cash is only recorded when the founder confirms the bank receipt.
- The payment_followup_agent drafts reminders; it never commits payment
  terms or grants discounts.
- Refunds are A3 — manual, founder-only.
