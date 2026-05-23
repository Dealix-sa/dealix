# Payment Rules

> Payment is part of the offer, not an afterthought.

## The Cash-Before-Delivery Rule

Sprints and Pilots: payment or signed PO is received before any
delivery hour is spent on the customer's work. The only exception is
a written T3 founder approval citing the named retainer or strategic
asset it secures.

## Follow-up Cadence

For any invoice or PO not received within the agreed window:

| Day from due date | Action |
|-------------------|--------|
| Day 0 (due) | Auto-reminder sent (polite) |
| Day +3 | Founder personal note |
| Day +7 | Founder phone call |
| Day +14 | Founder final note with "next step" |
| Day +21 | Escalate: founder offers payment plan, or pauses delivery |
| Day +30 | Add to `overdue_invoices.csv`; founder decides on legal step |

## Accepted Payment Methods

- Bank transfer (SARIE / IBAN) — preferred.
- Wire (USD/SAR) for international clients.
- Local payment processor (when set up) — for retainers.
- **Not accepted:** cash, cheque, "settle via barter".

## Payment Reference

Every payment must reference the invoice number. Payments without
reference are matched manually and flagged.

## Receipt Issuance

Receipts are issued within 24h of payment receipt and stored in
`dealix-ops-private/revenue/receipts/`.

## Currency Risk

For USD invoices:
- Mark FX rate at invoice issuance.
- Track FX impact in the monthly finance review.

## Failed Payment Handling

- Bank rejection → 24h response, re-issue with corrected details.
- Customer rejection / refusal to pay despite signed scope:
  - Founder personal escalation.
  - If unresolved at day +30: legal counsel consultation.
- Logged as an incident if the customer cites quality or trust grounds.

## Audit

- Monthly: reconcile `cash_collected.csv` to bank statement.
- Quarterly: spot-check 5 invoices end-to-end.
