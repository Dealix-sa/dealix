# قواعد النقد — Cash Rules

> When cash counts as revenue. Payment terms. Refund policy reference.

## Purpose
Define unambiguously when money becomes revenue. Stop the founder from celebrating signed-but-unpaid deals.

## Owner
Founder/CEO.

## Inputs
- Pipeline stages (`PIPELINE_STAGES.md`).
- Invoice workflow (`docs/finance/INVOICE_WORKFLOW.md`).
- MRR definition (`docs/finance/MRR_DEFINITION.md`).
- Refund policy (`docs/finance/REFUND_POLICY.md`).

## Outputs
- Recognized revenue list per month (`dealix-ops-private/finance/revenue-recognized-YYYY-MM.csv`).
- Deferred revenue list (cash received but not yet recognized).

## Rules
1. Revenue is recognized when both: (a) cash has cleared the Dealix account; AND (b) the delivery condition associated with the payment has occurred.
2. Deposits are deferred revenue until the corresponding delivery milestone is reached.
3. Retainer revenue is recognized monthly per `MRR_DEFINITION.md`, never as a lump.
4. Verbal acceptance does not move the opportunity to "Paid."
5. Signed-but-unpaid invoices remain in "Invoiced" stage; they are not Paid.
6. Refunds reverse recognized revenue in the month the refund is paid, not the month of the original deal.

## Metrics
- Cash received (rolling 30d).
- Revenue recognized (rolling 30d).
- Deferred revenue balance.
- Days sales outstanding (DSO) on invoiced amounts.

## Cadence
Daily cash check (`docs/finance/CASH_CONTROL.md`). Monthly recognition close.

## Evidence
`dealix-ops-private/finance/`.

## Verifier
`make cash-rules-verify` — checks every recognized item has cash-cleared + delivery-milestone evidence.

## Runtime Command
`make recognize-revenue month=YYYY-MM`

---

## When cash counts as revenue

### Signal Sample
- 100% paid upfront.
- Cash cleared = deferred revenue.
- Recognition: on sample delivery (Sample report sent and accepted).

### Revenue Sprint
- 50% on signing → deferred revenue until sprint mid-point.
- 50% on acceptance → recognized when sprint acceptance is signed.
- Each tranche is recognized at its associated milestone.

### Managed Pilot
- Same structure as Revenue Sprint: 50% / 50% with milestone recognition.

### Revenue Desk (Retainer)
- Paid monthly in advance.
- Each monthly payment becomes recognized revenue on the first day of the service month.
- 3-month minimum cancellation policy in `docs/finance/REFUND_POLICY.md`.

### Dealix OS
- Annual license paid in advance.
- Recognition: 1/12 per month over the license period.
- Onboarding sprint follows the Revenue Sprint recognition pattern.

## Banned recognition patterns
- Recognizing a deal based on a verbal yes.
- Recognizing a deal because the invoice was issued.
- Recognizing the full retainer year as month-one revenue.
- Recognizing a refundable deposit as revenue before the refund window closes.

## Payment cleared definition
"Cleared" means the funds are available in the Dealix bank account, not "scheduled," "pending," or "in transit." For card payments, this means past the processor settlement window. For bank transfers, this means the receiving bank confirms availability.

## Currency
- Default: SAR.
- Foreign currency: explicitly stated in the invoice; converted to SAR at the day's mid-market rate for recognition.

## Tax treatment
- VAT handled per `docs/finance/BILLING_POLICY.md`.
- Recognition is on the pre-VAT amount.

## Refund interaction
- A refund within 30 days of payment reverses both cash and (if applicable) recognized revenue.
- Refund policy details in `docs/finance/REFUND_POLICY.md`.
- Refunds count against the north star: a refunded sprint subtracts 1 PSDE in the refund month.

## "Bad revenue" filter
A payment that clears and matches a delivery is still rejected if any of the following apply (see `BAD_REVENUE_FILTER.md`):
- Engagement requires a banned tactic.
- Engagement prevents all evidence creation.
- Engagement is below margin floor without a declared bet.

## القواعد العربية
1. الإيراد يُعترف به عند تحقق شرطين: تحصيل النقد + بلوغ معلم التسليم.
2. الدفعات المقدمة إيرادات مؤجلة حتى المعلم.
3. الموافقة الشفوية لا تنقل الفرصة إلى "مدفوع".

## Cross-links
- `PIPELINE_STAGES.md`
- `BAD_REVENUE_FILTER.md`
- `docs/finance/INVOICE_WORKFLOW.md`
- `docs/finance/MRR_DEFINITION.md`
- `docs/finance/REFUND_POLICY.md`
