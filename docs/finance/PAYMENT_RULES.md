# Payment Rules

## Per-Invoice Workflow
1. Generate invoice (template in `templates/`)
2. Add VAT line (15%) — never bundled
3. Add bank transfer + Stripe + Tabby links
4. Send invoice → log in `revenue/invoices/`
5. Track payment received → log in `revenue/cash_collected.csv`
6. Send receipt within 24 hours of payment
7. Update pipeline tracker: stage → `paid`

## Receipt Of Payment
- Bank transfer: confirm via bank notification (not just client's claim)
- Stripe/Tabby: rely on platform confirmation webhook
- Cash: handed-in receipt + same-day deposit

## Payment Confirmation Discipline
- No work starts on "the payment is coming"
- No work continues past month-end if invoice unpaid
- "Sent" ≠ "received" — confirm via the bank/platform

## Reconciliation
- Daily: check incoming bank notifications, mark invoices paid
- Weekly: reconcile `revenue/cash_collected.csv` against bank statement
- Monthly: end-of-month statement reconciliation

## Overdue Process
- Day +1 overdue: gentle reminder
- Day +7: founder-personal follow-up
- Day +14: pause delivery (for retainer), formal payment request
- Day +30: late fee applied, escalation
- Day +60: dispute escalation, advisor consulted

## Currency
- All invoices in SAR
- Foreign-currency conversion (rare) at TT bank rate on invoice date
- No "USD-equivalent" pricing

## Tax Posture
- VAT 15% on all invoices
- Tax invoice format per ZATCA requirements
- Annual return filed
- Retain financial records 10 years (per `DATA_RETENTION_POLICY.md`)

## Bank Account
- Dedicated business account (no commingling with personal)
- Secondary account for redundancy (per `RISK_REGISTER.md` R-001)
- Founder-only signatory until first hire

## What This Refuses
- Personal account deposits (compliance gap)
- Crypto / unregulated channels
- "We'll skip the invoice for this one"
- Backdating invoices
- Charging different prices to different customers for the same rung without documented experiment
