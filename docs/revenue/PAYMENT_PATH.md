# مسار الدفع — Payment Path

> Invoice → cash. Who, what, when, evidence.

## Purpose
Compress the time from "proposal accepted" to "cash cleared." Make every step assignable and verifiable.

## Owner
Founder/CEO.

## Inputs
- Accepted proposal record.
- Customer billing details (collected at acceptance).
- Invoice workflow (`docs/finance/INVOICE_WORKFLOW.md`).
- Payment rules (`docs/finance/PAYMENT_RULES.md`).
- Billing policy (`docs/finance/BILLING_POLICY.md`).

## Outputs
- Issued invoice file (`dealix-ops-private/finance/invoices/`).
- Payment receipt file once cleared.
- Stage transitions to "Invoiced" and "Paid" in `PIPELINE_STAGES.md`.

## Rules
1. Invoice is issued within 1 business day of proposal acceptance.
2. Each step has a single owner and a target time.
3. Reminders are sent on a fixed cadence (day 7, day 14, day 21). No silent waiting beyond day 21.
4. Late payments past 30 days trigger the late payment policy in `docs/finance/PAYMENT_RULES.md`.
5. Delivery does not start until at least the deposit per `CASH_RULES.md` is cleared.

## Metrics
- Invoice issue lag (acceptance → invoice issued): target ≤ 1 business day.
- DSO (invoice → cash cleared): target ≤ 21 days.
- Late payment rate: track.

## Cadence
Per opportunity. Aggregate weekly in `REVENUE_COMMAND_CENTER.md`.

## Evidence
`dealix-ops-private/finance/invoices/` and `receipts/`.

## Verifier
`make payment-path-verify` — checks every accepted proposal has invoice issued within 1 business day and every paid invoice has a receipt file.

## Runtime Command
`make payment-path-snapshot`

---

## The Path

| Step | Owner | Target time | Artifact |
|---|---|---|---|
| 1. Proposal accepted in writing | Founder | day 0 | acceptance message saved |
| 2. Collect billing details | Founder | day 0–1 | customer billing record |
| 3. Issue invoice | Founder (or finance once delegated) | day 1 | invoice PDF + tracking ID |
| 4. Send invoice with payment instructions | Founder | day 1 | sent timestamp |
| 5. Reminder #1 (if unpaid) | Founder | day 7 | reminder log entry |
| 6. Reminder #2 (if unpaid) | Founder | day 14 | reminder log entry |
| 7. Reminder #3 + late notice | Founder | day 21 | late notice per `PAYMENT_RULES.md` |
| 8. Payment cleared | Bank/Processor → Founder | varies | receipt file |
| 9. Mark stage "Paid" | Founder | day cleared | pipeline transition |
| 10. Schedule kickoff | Founder | day cleared + 1 | kickoff doc |

## Invoice content (per `BILLING_POLICY.md`)
- Customer legal name + VAT number (if applicable).
- Dealix legal name + VAT number.
- SAR amount; VAT line; total.
- Payment terms: net 0 (deposit), net 14 (retainer monthly), net 14 (sprint final).
- Bank transfer details and accepted card processor.
- Reference number.
- Disclosure footer: "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" (on customer-facing summary, not the legal invoice line).

## Reminder templates
Day 7: friendly status check; confirm receipt of invoice; offer help.
Day 14: clear restatement of amount, terms, bank details; note delivery starts only after deposit cleared.
Day 21: late notice referencing `PAYMENT_RULES.md`; outline the late fee policy if applicable; offer call.

## What is NOT in the payment path
- Automated dunning emails on a marketing cadence.
- "Pay or we cancel everything" threats.
- Charging late fees that were not disclosed in the original proposal.

## Receipt file format
```
Payment receipt: <invoice id>
Customer (anonymized for repo): Customer-XX
Date received: YYYY-MM-DD
Amount SAR: <amount>
Currency: SAR
Cleared via: bank transfer / card / wire
Recognized revenue date: YYYY-MM-DD (per CASH_RULES.md)
Stage transition: Invoiced → Paid on YYYY-MM-DD
```

## Coordination with delivery
- Sprint kickoff is scheduled within 7 days of cleared deposit.
- Sprint final tranche invoice is issued at acceptance (`docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`).
- Retainer invoices are issued the 1st of each service month.

## Currency and tax
- Default SAR. VAT per `BILLING_POLICY.md`.
- Foreign currency invoices: noted explicitly, conversion to SAR at recognition per `CASH_RULES.md`.

## القواعد العربية
1. الفاتورة تصدر خلال يوم عمل واحد من قبول العرض.
2. التذكيرات على إيقاع ثابت: 7، 14، 21 يومًا.
3. التسليم لا يبدأ قبل تحصيل العربون.

## Cross-links
- `PIPELINE_STAGES.md`
- `CASH_RULES.md`
- `docs/finance/INVOICE_WORKFLOW.md`
- `docs/finance/PAYMENT_RULES.md`
- `docs/finance/BILLING_POLICY.md`
