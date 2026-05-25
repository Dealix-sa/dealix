# سياسة الفوترة — Billing Policy

> Currency. VAT. Terms. Invoice contents.

## Purpose
Define how Dealix bills, in one place, so proposals and invoices match.

## Owner
Founder/CEO.

## Inputs
- VAT regulatory guidance (Saudi ZATCA rules as in force on the invoice date).
- Customer billing details collected at proposal acceptance.
- Offer ladder (`docs/revenue/OFFER_LADDER.md`).

## Outputs
- Invoice template content (used by `INVOICE_WORKFLOW.md`).
- Billing FAQ (this file, used in customer-facing communication).

## Rules
1. Default currency is SAR. Foreign currency is allowed by exception, with a written reason.
2. VAT is applied per Saudi rules in force. The VAT line is explicit on every invoice.
3. Payment terms are stated in the proposal AND repeated on the invoice. No discrepancies allowed.
4. Invoices include a unique reference and a paid-stamp upon settlement.
5. Customer details on the invoice match the proposal exactly. Late corrections require an issued credit note.

## Metrics
- Invoice error rate (corrections required): target ≤ 2%.
- Currency conversion incidents (foreign currency disputes): target 0.
- VAT compliance audit findings: 0.

## Cadence
Reviewed Annually. Updated immediately if VAT rules change.

## Evidence
This file + per-invoice files in `dealix-ops-private/finance/invoices/`.

## Verifier
`make billing-policy-verify` — checks every issued invoice has VAT line, currency, payment terms matching proposal.

## Runtime Command
`make billing-audit month=YYYY-MM`

---

## Currency
- Default: SAR (Saudi Riyal).
- Foreign currency: USD or EUR allowed by exception, after founder approval and conversion footnote.
- SAR equivalent of any foreign currency invoice is shown for internal recognition (`docs/revenue/CASH_RULES.md`).

## VAT (Saudi ZATCA rules)
- Standard VAT rate as in force on the invoice issue date applies.
- VAT line is shown separately on the invoice.
- Customers with a valid VAT registration: VAT charged and remitted normally.
- Foreign customers (services exported): zero-rated where the rules allow; documented per ZATCA guidance.
- The VAT registration number of Dealix appears on every invoice.

## Payment terms
| Rung | Payment terms |
|---|---|
| Signal Sample | 100% upfront on signing |
| Revenue Sprint | 50% on signing, 50% on acceptance |
| Managed Pilot | 50% on signing, 50% on acceptance |
| Revenue Desk (retainer) | Monthly in advance, 3-month minimum |
| Dealix OS | Annual in advance |

Late payment policy is in `PAYMENT_RULES.md`.

## Invoice contents (required)
1. Invoice number (sequential, unique).
2. Issue date and due date.
3. Dealix legal name, address, VAT number.
4. Customer legal name, address, VAT number (if applicable).
5. Description of services, period, scope reference (proposal id).
6. Net amount in SAR (and original currency if applicable).
7. VAT line.
8. Total amount.
9. Payment terms (matching proposal).
10. Bank transfer details and accepted card processor.
11. Reference number for the payment.

## Optional but recommended
- Customer-facing summary above the legal lines:
  > Engagement reference: <proposal id>. Scope: <one sentence>. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

## Credit notes
- A credit note is issued when an invoice is corrected after sending.
- The original invoice is not silently amended; a credit note + new invoice is the pattern.

## Discount handling
- Discounts > 10% must appear as a discount line on the invoice, not as a reduced unit price.
- Discount reasons are logged on the proposal file.

## What is NOT allowed
- Splitting one engagement across multiple customers without written authorization from all parties.
- Issuing invoices in the name of a related entity without disclosure.
- Charging fees not previously disclosed in the proposal (e.g., surprise "setup" fees).

## Customer billing FAQ (excerpt for customer-facing use)
- "Can we pay in installments?" — Per offer ladder; retainers are monthly; sprints are 50/50.
- "Can we delay first deposit?" — No. Delivery starts after deposit clears per `docs/revenue/CASH_RULES.md`.
- "Can the invoice be in our parent's name?" — Yes, with written authorization.

## القواعد العربية
1. العملة الافتراضية ريال سعودي. أي عملة أجنبية بإقرار خاص.
2. ضريبة القيمة المضافة تُطبَّق وفق قواعد هيئة الزكاة والضريبة والجمارك.
3. شروط الدفع في العرض والفاتورة متطابقة. أي اختلاف يُصحَّح بإشعار دائن.

## Cross-links
- `INVOICE_WORKFLOW.md`
- `PAYMENT_RULES.md`
- `REFUND_POLICY.md`
- `docs/revenue/CASH_RULES.md`
- `docs/revenue/OFFER_LADDER.md`
