# Payment Capture OS

> Money in. The system that takes a proposal acceptance and turns it into cash collected.

## 1. Flow

```
Proposal accepted (out of band)
  ↓
Invoice drafted (Finance Copilot)
  ↓
Invoice reviewed by founder
  ↓
Invoice issued to customer (manual)
  ↓
Payment received (bank event)
  ↓
Reconciled and recorded
  ↓
Audit + delivery handover
```

## 2. Invoicing

- KSA VAT-aware.
- Bilingual layout (AR + EN).
- Light-mode brand template.
- Linked to proposal reference.

## 3. Payment

- Payment methods agreed in contract (bank transfer, partner channels).
- No card data stored in Dealix.
- Receipts logged in audit.

## 4. Receivables

| Bucket | Action |
|---|---|
| 0-15 days | none |
| 15-30 days | polite reminder draft |
| 30-60 days | escalated reminder + founder note |
| 60+ days | founder action, optional pause of delivery |

Reminder drafts are queued for founder approval — never auto-sent.

## 5. Trust

- No commitment of refunds, discounts, payment plans without founder approval (non-negotiable #4).
- Reconciliation events recorded against the audit log.
- VAT records exportable for KSA tax authority.

## 6. KPI

| KPI | Target |
|---|---|
| Days to cash (invoice → paid) | tracked weekly |
| % receivables 0-30 days | ≥ 80 % |
| Reconciliation accuracy | 100 % |
