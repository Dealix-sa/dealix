# Billing Policy

How Dealix invoices and collects.

## Invoices
- Issued on the day of close (Stage 7 → 8).
- Includes scope summary, payment terms, and bank or payment-link details.
- Compliant with Saudi e-invoicing requirements.

## Payment terms
- Sprints: 100% on signature.
- Pilots: 50% on signature, 50% on milestone.
- Retainers: monthly in advance.
- Enterprise: net-30 maximum; founder approval for longer terms.

## Currency
- SAR primary. USD only by explicit agreement.

## Records
- Every invoice stored in `dealix-ops-private/revenue/invoices/`.
- Every payment matched and stored in `dealix-ops-private/revenue/payments/`.
- Every receipt stored in `dealix-ops-private/revenue/receipts/`.

## Rule
Work does not start before payment terms are recorded in writing and the first installment is received.
