# تعريف MRR — MRR Definition

> What counts as MRR. Recurring retainer only. Not projects.

## Purpose
A precise MRR definition that survives a board question or a self-deception attempt.

## Owner
Founder/CEO.

## Inputs
- Active Revenue Desk retainers.
- Active Dealix OS licenses (monthly-recognized portion).
- Cash rules (`docs/revenue/CASH_RULES.md`).
- Pipeline stages (`docs/revenue/PIPELINE_STAGES.md`).

## Outputs
- Monthly MRR figure (the third critical number in `FINANCE_COMMAND_CENTER.md`).
- MRR movement breakdown: new, expansion, contraction, churn.

## Rules
1. MRR includes only recurring monthly retainer revenue. Project revenue is excluded.
2. MRR is recognized for a month only when the service month begins and the payment is cleared.
3. Annual licenses (Dealix OS) contribute 1/12 of their net annual fee to MRR.
4. Discounts reduce MRR proportionally.
5. MRR figures are recomputed monthly from scratch, never carried forward without re-verification.

## Metrics
- MRR (SAR/month).
- Net new MRR (this month).
- Gross churn (SAR/month lost).
- Expansion MRR (existing customers paying more).
- Logo count (active retainer customers).

## Cadence
Computed Monthly on the 1st. Verified before publishing to Board Pack.

## Evidence
`dealix-ops-private/finance/mrr-YYYY-MM.md`.

## Verifier
`make mrr-verify` — recomputes MRR from active retainers and checks against the published figure.

## Runtime Command
`make mrr-compute month=YYYY-MM`

---

## What counts

### Counts as MRR
- Revenue Desk retainers active in the service month with payment cleared.
- 1/12 of Dealix OS annual licenses, active and paid, in the service month.
- Expansion: existing retainer customer paid more this month than last month (above the original retainer band).

### Does NOT count as MRR
- One-off Signal Sample fees.
- Revenue Sprint or Managed Pilot fees (these are project revenue).
- Deposits for upcoming retainers (deferred until the service month begins).
- Verbal commitments without cleared payment.
- "Committed" but not paid retainer months.

## Computation

```
MRR(month M) = Σ (retainer fee_i × in_service(i, M)) + (1/12) × Σ (OS_fee_j × in_service(j, M))
```

Where:
- `in_service(i, M)` = 1 if customer i's retainer is active and paid for month M, else 0.
- Discounts reduce the fee proportionally before summing.

## Movement breakdown

| Component | Definition |
|---|---|
| MRR start | MRR figure on the 1st of last month |
| New MRR | retainers that started service this month |
| Expansion MRR | existing retainers that increased fee this month |
| Contraction MRR | existing retainers that decreased fee this month |
| Churned MRR | retainers that ended service this month |
| MRR end | MRR start + new + expansion - contraction - churn |

## Reconciliation
MRR figure is reconciled against:
- `dealix-ops-private/finance/invoices/index.csv` paid invoices in the service month.
- The active retainer list maintained by the founder.

Discrepancies > 1% trigger a recompute.

## Customer concentration in MRR
- If one customer is > 30% of MRR, this is flagged in Monthly Strategy Review.
- > 50% triggers a risk note in the Board Pack.

## Trust handling
- A refund within the same month reverses MRR for that month.
- A refund crossing months is logged as churn in the refund month.

## What "active" means
- The customer has a current retainer agreement.
- The current service month's invoice is paid (cleared).
- The customer has not given written cancellation notice that takes effect this month.

## القواعد العربية
1. MRR يشمل الاحتفاظ الشهري المتكرر فقط. المشاريع لا تُحتسب.
2. الاعتراف يكون عند بداية شهر الخدمة وتحصيل الدفعة.
3. الترخيص السنوي يساهم بـ 1/12 شهريًا.

## Cross-links
- `FINANCE_COMMAND_CENTER.md`
- `CASH_CONTROL.md`
- `docs/revenue/CASH_RULES.md`
- `docs/revenue/OFFER_LADDER.md`
- `docs/founder/BOARD_PACK_TEMPLATE.md`
