# Invoice Workflow

## Trigger Events
- Signed scope (Sprint/Pack) → invoice within 24 hr
- Signed contract (retainer) → invoice within 24 hr
- Monthly recurrence (retainer) → invoice 5 days before period start
- Approved scope expansion → invoice within 24 hr

## Invoice Schema (every invoice must have)
```
invoice_id (unique, sequential)
client_name + tax_number (if applicable)
issue_date
due_date (on receipt)
period (for retainers)
line_items (each with description, quantity, unit_sar, total_sar)
subtotal_sar
vat_sar (15%)
total_sar
payment_methods (bank + Stripe + Tabby links)
notes (DPA reference, refund clause link)
```

## Generation
- Template in `templates/invoice_template.md`
- Filled by founder or invoice agent (when present)
- Reviewed by founder before send (A1)
- Saved to `revenue/invoices/{client}/{invoice_id}.pdf` (private)

## Sending
- Channel: email (preferred) or WhatsApp Business (if client prefers)
- Subject: `Invoice {invoice_id} — Dealix — {client_name}`
- Body: short, professional, links to payment methods

## Tracking
- Append to `revenue/invoices.csv` (private): invoice_id, client, amount, sent_at, due_at, status
- Status enum: `sent | viewed | paid | overdue | disputed | refunded | cancelled`

## Paid State
- Upon payment confirmation: update `revenue/cash_collected.csv` + invoice status → `paid`
- Send receipt within 24 hr
- Update pipeline tracker

## Overdue State
- Auto-flag in Daily Brief Money section
- Founder follow-up per Payment Rules cadence
- After day 30, late fee applies (if enforced)

## Disputes
- Capture dispute reason in `revenue/disputes/`
- Pause delivery pending resolution
- Founder + advisor review if disputed amount > SAR 5,000
- Resolution within 14 days target

## Refund Issuance
- Per `BILLING_POLICY.md`
- Founder approves
- Refund processed via original payment method
- Log refund in `revenue/refunds.csv` (private)
- Decrement `cash_collected.csv` (do not silently subtract — explicit refund row)

## Tax Invoice (ZATCA Compliance)
- Compliant tax invoice format
- Saudi VAT registration number on every invoice (once registered)
- E-invoicing per ZATCA Phase 2 requirements (when applicable)

## What This Workflow Refuses
- Sending without review
- Skipping VAT line
- Hand-edited invoice numbers (sequential, no gaps)
- Hidden discounts (always shown as a line item with reason)
- Combining multiple clients on one invoice
