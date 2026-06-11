# ZATCA-aware invoicing notes

## Position
Dealix is NOT a tax invoice provider. ZATCA-compliant invoices are issued by the customer's accounting system. Dealix's invoice stubs are operational placeholders only.

## What customers actually need
- A KSA-licensed accounting system (Zoho Books, Wafeq, ERPNext + KSA add-ons, SAP Business One with KSA localization, etc.).
- ZATCA Fatoora portal credentials.
- Phase-1 / Phase-2 e-invoicing integration as required for their entity.
- A finance owner who handles VAT filing.

## Dealix's role
- Provide the line items (setup, monthly retainer, change orders) for the customer's accounting system to bill.
- Track the deal status (`deals.ledger.json`) so the customer knows what to invoice.
- Reconcile what was billed vs. what was delivered during the monthly review.

## Out of scope
- Dealix does not issue ZATCA UUIDs.
- Dealix does not generate QR codes for tax invoices.
- Dealix does not file VAT returns.

## When customer asks Dealix to "send the invoice"
Politely redirect to their accounting team. Dealix can provide the data; Dealix does not issue the document.
