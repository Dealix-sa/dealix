# Cash Rules

> Cash is the only fact. Forecasts are stories.

## The Five Cash Rules

1. **Cash before delivery.**
   For Sprints and Pilots, payment or PO must precede delivery start.
   The only exception is a written approval from the founder, citing
   the named retainer or strategic asset it secures.

2. **Cash on day 1 for retainers.**
   Retainers are pre-paid at the start of each month, not in arrears.
   Net 30 retainers are an exception and require founder approval.

3. **Cash collection is a first-class workflow.**
   Invoices are sent within 24 hours of scope sign-off.
   Follow-ups: day 3, day 7, day 14.
   Day 21: founder escalates personally.
   Day 30: deal flagged in `overdue_invoices.csv`.

4. **No refunds without root cause.**
   A refund is a learning event. Every refund is documented with:
   - what we promised
   - what we delivered
   - what the customer expected
   - what we will change
   See `docs/finance/REFUND_POLICY.md`.

5. **No discount without recorded reason.**
   See `REVENUE_CONTROL_SYSTEM.md` rule 4.

## Invoice Quality

Every invoice includes:

- Legal entity name
- Tax number (Saudi VAT registration if applicable)
- Scope statement (one paragraph)
- Deliverables
- Delivery date
- Payment due date
- Bank details
- Reference number

See `docs/revenue/INVOICE_FLOW.md` (existing) for the operational flow.

## Cash Discipline Anti-Patterns

- "We will invoice after delivery."
- "Let us start, and they will pay on Monday."
- "It is a small amount, no need for a PO."
- Splitting an invoice across pricing rungs to keep the headline number
  low.

## Verifier

`make weekly-close` checks:

- Are all paid deals reflected in `cash_collected.csv`?
- Are all overdue invoices flagged?
- Are all refunds documented with a root cause?
