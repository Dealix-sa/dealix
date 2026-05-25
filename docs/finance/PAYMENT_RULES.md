# قواعد الدفع — Payment Rules

> Accepted methods. Payment-on-acceptance rule. Late policy.

## Purpose
State who can pay how, when payments are due, and what happens on late payment. Customer-facing language goes into proposals; this file is the source.

## Owner
Founder/CEO.

## Inputs
- Billing policy (`BILLING_POLICY.md`).
- Cash rules (`docs/revenue/CASH_RULES.md`).
- Refund policy (`REFUND_POLICY.md`).
- Existing reconciliation doc (`docs/revenue/PAYMENT_RECONCILIATION.md`).

## Outputs
- Customer-facing payment instructions on invoices.
- Late payment notice template.
- Internal payment confirmation log.

## Rules
1. Payment is due on the terms in the proposal. There are no implicit grace periods.
2. Delivery does not start until the deposit (or applicable tranche) is cleared per `docs/revenue/CASH_RULES.md`.
3. Late payments past 30 days trigger the late notice and the late fee disclosed in the proposal.
4. Refunds follow `REFUND_POLICY.md` — not negotiated separately at the invoice stage.
5. Personal payment methods (the founder's personal card, etc.) are never used to receive customer payments.

## Metrics
- Late payment rate: target ≤ 10% of invoices.
- Average days overdue (when late): target ≤ 7 days.
- Disputed amounts: track separately.

## Cadence
Reviewed Annually. Late policy reviewed if late rate > 15% in a quarter.

## Evidence
Receipts in `dealix-ops-private/finance/receipts/`; late notices in `dealix-ops-private/finance/late/`.

## Verifier
`make payment-rules-verify` — checks every overdue invoice has a logged reminder per the cadence.

## Runtime Command
`make late-sweep`

---

## Accepted payment methods

| Method | Default? | Notes |
|---|---|---|
| Bank transfer (SAR) | Yes | Preferred for invoices ≥ SAR 25,000 |
| Bank transfer (USD/EUR by exception) | No | Foreign currency requires founder approval |
| Card payment via processor | Yes | For invoices ≤ SAR 25,000; processor fees absorbed by Dealix unless stated |
| Cheque | No | Not accepted |
| Cash | No | Not accepted |
| Cryptocurrency | No | Not accepted |

## Payment-on-acceptance rule
- For Signal Sample: 100% on signing. Work begins after cash clears.
- For Revenue Sprint / Managed Pilot: 50% on signing (deposit). Work begins after deposit clears. 50% on acceptance.
- For Revenue Desk: first month in advance, then monthly in advance.
- For Dealix OS: full annual fee in advance.

## Late payment policy

| Days past due | Action |
|---|---|
| 1–7 | Friendly reminder; confirm receipt and bank details |
| 8–14 | Formal reminder; restate amount, terms, bank details |
| 15–21 | Late notice; reference the late fee from proposal if applicable |
| 22–30 | Founder-to-DM direct contact; pause non-critical work |
| 31+ | Engagement on hold; legal review of contract terms; refund/credit handling per `REFUND_POLICY.md` |

## Late fee
- Default late fee: stated in each proposal; commonly 1% per month on outstanding amount.
- Late fee is disclosed in the proposal; never charged surprise.
- Late fee may be waived by founder for relationship reasons; waiver is logged.

## Disputed amounts
- A disputed amount is moved to a "Disputed" sub-status in the invoice tracker.
- Disputes are resolved within 14 days; longer disputes are escalated.
- During dispute: undisputed portion still due per terms.

## Personal vs business
- All payments are received into Dealix business accounts.
- Founder personal accounts are never used as a workaround.
- Card payments go through the registered processor.

## What is NOT allowed
- Receiving payment from a non-customer entity unless the customer authorizes in writing.
- Accepting payment for an engagement that has not signed a proposal.
- Combining multiple unrelated customer invoices into one bulk payment without reconciliation.

## القواعد العربية
1. الدفع وفق شروط العرض. لا فترات سماح ضمنية.
2. التسليم لا يبدأ قبل تحصيل الدفعة المعنية.
3. التأخر فوق 30 يومًا يعلّق العمل غير الحرج ويفعّل المراجعة.

## Cross-links
- `BILLING_POLICY.md`
- `INVOICE_WORKFLOW.md`
- `REFUND_POLICY.md`
- `docs/revenue/CASH_RULES.md`
- `docs/revenue/PAYMENT_RECONCILIATION.md`
