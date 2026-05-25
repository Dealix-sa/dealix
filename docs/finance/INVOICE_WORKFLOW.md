# Invoice Workflow

> A pre-defined path from "scope signed" to "cash received".

## Workflow

```
Scope signed
  │
  ▼
Founder triggers invoice creation
  │
  ▼
Invoice produced from template (BILLING_POLICY required fields)
  │
  ▼
Invoice number assigned (sequential)
  │
  ▼
Invoice PDF stored in dealix-ops-private/revenue/invoices/
  │
  ▼
Invoice sent to customer (email + WhatsApp confirmation)
  │
  ▼
Logged in dealix-ops-private/revenue/cash_collected.csv (status: ISSUED)
  │
  ▼
Reminder cadence runs (see PAYMENT_RULES.md)
  │
  ▼
Payment received → status: PAID
  │
  ▼
Receipt issued + stored in dealix-ops-private/revenue/receipts/
  │
  ▼
Delivery start authorised
```

## Invoice Template

`templates/INVOICE_TEMPLATE.md` (canonical) + PDF generator.

## Required Fields per Invoice Row

```
- invoice_no: INV-yyyy-NNNN
  issue_date: yyyy-mm-dd
  due_date: yyyy-mm-dd
  customer_legal_name: "..."
  customer_address: "..."
  customer_tax_number: "..."
  po_number: "..."
  scope_summary: "..."
  line_items:
    - description: "..."
      quantity: N
      unit_price: SAR
      total: SAR
  subtotal: SAR
  vat_rate: 0 / 15
  vat_amount: SAR
  total: SAR
  payment_terms: "Net 7 / Pre-paid"
  bank_account: "..."
  iban: "..."
  notes: "..."
```

## Reconciliation

- Daily: founder checks bank for incoming.
- Match payment → invoice by reference.
- Update `cash_collected.csv` and issue receipt.
- Unmatched payment > 48h: contact customer.

## Audit Trail

For every invoice, the audit trail captures:

- Scope signature evidence
- Invoice PDF
- Sent email metadata
- Reminder timestamps
- Payment reference
- Receipt PDF

Stored under `dealix-ops-private/revenue/invoices/<invoice_no>/`.

## Anti-Patterns

- Verbal scope → no invoice.
- Two invoices for the same scope.
- Invoice without VAT determination.
- Sending invoice from a personal email instead of the company channel.
