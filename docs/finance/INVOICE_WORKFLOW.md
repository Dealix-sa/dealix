# سير عمل الفواتير — Invoice Workflow

> Proposal accepted → invoice issued → payment received → revenue recognized.

## Purpose
Make the invoice lifecycle deterministic. Every issued invoice has a known state and a known artifact.

## Owner
Founder/CEO (until finance lead hired).

## Inputs
- Accepted proposal record.
- Customer billing details (collected per `BILLING_POLICY.md`).
- Payment rules (`PAYMENT_RULES.md`).
- Cash rules (`docs/revenue/CASH_RULES.md`).
- Existing flow (`docs/revenue/INVOICE_FLOW.md`).

## Outputs
- Issued invoice file in `dealix-ops-private/finance/invoices/INV-YYYY-NNNN.pdf`.
- Status entries in invoice tracker (`dealix-ops-private/finance/invoices/index.csv`).
- Receipt file once paid.
- Recognized revenue entry per `CASH_RULES.md`.

## Rules
1. Invoices are issued within 1 business day of acceptance.
2. Invoice numbers are sequential, unique, never reused.
3. Status transitions are written: Issued → Sent → Reminded → Paid → Recognized.
4. Voiding an invoice requires a credit note; silent edits are forbidden.
5. Reconciliation runs Weekly (per `docs/revenue/PAYMENT_RECONCILIATION.md`).

## Metrics
- Invoice lag (acceptance → sent): target ≤ 1 business day.
- DSO (sent → paid): target ≤ 21 days.
- Reconciliation discrepancies per month: target 0.

## Cadence
Per invoice. Weekly reconciliation.

## Evidence
`dealix-ops-private/finance/invoices/`.

## Verifier
`make invoice-workflow-verify` — checks every accepted proposal has an invoice issued within 1 business day, and every paid invoice has a receipt and recognition entry.

## Runtime Command
`make invoice-issue proposal=<id>` and `make invoice-pay invoice=<id>`.

---

## The Workflow

```
ACCEPTED ─▶ ISSUED ─▶ SENT ─▶ REMINDED* ─▶ PAID ─▶ RECOGNIZED
                                  │
                                  ▼
                                LATE ─▶ COLLECTIONS (per PAYMENT_RULES.md)
                                  │
                                  ▼
                          VOIDED (with credit note)
```

## State definitions

### Issued
- Invoice file generated with all `BILLING_POLICY.md` required content.
- Number assigned (sequential).
- Stored in `dealix-ops-private/finance/invoices/`.

### Sent
- Sent to the customer's billing contact.
- Sent timestamp recorded.

### Reminded
- One of: day-7, day-14, day-21 reminder sent.
- Each reminder logged in the invoice's history.

### Late
- Past due date by ≥ 1 day.
- Triggers the late policy in `PAYMENT_RULES.md`.

### Paid
- Funds cleared per `docs/revenue/CASH_RULES.md`.
- Receipt file generated.
- Stage transition in `docs/revenue/PIPELINE_STAGES.md` to "Paid".

### Recognized
- Revenue moved from deferred to recognized at the milestone defined in `CASH_RULES.md`.
- Logged in `dealix-ops-private/finance/revenue-recognized-YYYY-MM.csv`.

### Voided
- Original invoice retained.
- A credit note is issued referencing the original.
- A new corrected invoice is issued if appropriate.

## Index format
```
invoice_id,issue_date,due_date,customer_anon,sar_net,sar_vat,sar_total,status,paid_date,recognized_date,notes
INV-2026-0001,2026-05-23,2026-06-06,Customer-A1,90000,13500,103500,Sent,,,
```

## Reconciliation cadence
- Weekly on Sunday: match bank statement entries to invoices.
- Discrepancies are logged and resolved within 7 days.
- Monthly close requires zero open discrepancies.

## What the workflow does NOT do
- Auto-send dunning emails on a marketing cadence.
- Generate invoices for proposals not yet accepted.
- Reuse invoice numbers across years.

## Coordination with delivery
- Sprint kickoff is scheduled after deposit invoice is paid.
- Sprint final tranche invoice is issued at acceptance, not at start.
- Retainer monthly invoices are issued on the 1st of each service month.

## Audit trail
Each invoice has a complete history file:
```
invoice_id: INV-2026-0001
events:
  - issued: YYYY-MM-DD by Founder
  - sent: YYYY-MM-DD HH:MM
  - reminded_day7: YYYY-MM-DD
  - paid: YYYY-MM-DD amount SAR
  - recognized: YYYY-MM-DD per milestone <name>
```

## القواعد العربية
1. تصدر الفاتورة خلال يوم عمل واحد من القبول.
2. الأرقام تسلسلية فريدة لا تُعاد.
3. الإلغاء يتم بإشعار دائن، لا بتعديل صامت.

## Cross-links
- `BILLING_POLICY.md`
- `PAYMENT_RULES.md`
- `REFUND_POLICY.md`
- `docs/revenue/CASH_RULES.md`
- `docs/revenue/INVOICE_FLOW.md`
- `docs/revenue/PAYMENT_RECONCILIATION.md`
- `docs/revenue/PAYMENT_PATH.md`
