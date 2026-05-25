# مركز قيادة المالية — Finance Command Center

> The finance dashboard + the 3 critical numbers: cash, MRR, runway.

## Purpose
A single finance page the founder reads after the CEO and Revenue Command Centers each morning. Three numbers visible without scrolling.

## Owner
Founder/CEO (until a finance lead is hired; then co-owned).

## Inputs
- Bank balances (`CASH_CONTROL.md`).
- Recognized revenue (`docs/revenue/CASH_RULES.md`).
- MRR (`MRR_DEFINITION.md`).
- Cost base (`FINANCIAL_MODEL_V1.md`).
- Invoices and receipts (`INVOICE_WORKFLOW.md`).

## Outputs
- Daily snapshot in `dealix-ops-private/finance/YYYY-MM-DD.md`.
- Weekly summary in `dealix-ops-private/weekly/`.
- Monthly close.

## Rules
1. Updated daily before 9:00 AM Riyadh.
2. The three critical numbers (cash, MRR, runway) are computed fresh from primary sources.
3. No number on this page is repeated from yesterday; either confirmed or updated.
4. No projection appears on this page — projections live in `FINANCIAL_MODEL_V1.md`.
5. Alert thresholds in `CASH_CONTROL.md` are checked each refresh.

## Metrics
- Cash (SAR).
- MRR (SAR/month).
- Runway (days).
- Burn (SAR/month, trailing 30 days).
- Net cash movement this week.

## Cadence
Daily. Weekly summary. Monthly close.

## Evidence
`dealix-ops-private/finance/`.

## Verifier
`make finance-command-verify` — checks today's snapshot exists and cash/MRR/runway are all present.

## Runtime Command
`make finance-daily`

---

## The Page

```
# Finance Command Center — YYYY-MM-DD

## The three numbers
Cash: SAR X,XXX,XXX
MRR:  SAR XX,XXX / month
Runway: NNN days

## This week
Cash in (received): SAR X
Cash out (paid): SAR X
Net: +/- SAR X

## This month so far
Recognized revenue: SAR X
Burn: SAR X
Net: +/- SAR X

## Alert state
[ ] Green (runway ≥ 180 days)
[ ] Yellow (runway 90–179 days)
[ ] Orange (runway 60–89 days — action triggered)
[ ] Red (runway < 60 days — emergency protocol)

## Receivables open
| Invoice | Customer (anon) | SAR | Days outstanding |
|---|---|---|---|

Total: SAR X | DSO: D days

## Payables open (next 30 days)
| Payee | SAR | Due |
|---|---|---|
```

## What this page is NOT
- Not a forecast (lives in `FINANCIAL_MODEL_V1.md`).
- Not a board pack (lives in `docs/founder/BOARD_PACK_TEMPLATE.md`).
- Not for external sharing.

## Discipline rules
- Customer names are anonymized labels here.
- VAT amounts are separated from net amounts.
- Foreign currency amounts are also shown in SAR at the day's rate.

## Escalation map
| Runway | Action |
|---|---|
| ≥ 180 days | Green; normal operations |
| 90–179 days | Yellow; founder time shifts toward A-tier Revenue |
| 60–89 days | Orange; CASH_CONTROL emergency protocol step 1 |
| < 60 days | Red; CASH_CONTROL emergency protocol step 2; brief advisor |

## How the three numbers are computed

### Cash
Sum of cleared balances in all Dealix accounts as of refresh time.

### MRR
Per `MRR_DEFINITION.md` — sum of monthly recurring retainer fees recognized for the current calendar month.

### Runway
`Cash / mean_burn_30d`, in days. `mean_burn_30d` is the trailing 30 days net cash out (excluding capital injections and customer deposits classified as deferred revenue).

## القواعد العربية
1. الأرقام الثلاثة الحرجة: نقد، MRR، مدرج نقدي.
2. لا توقعات في هذه الصفحة. التوقعات في النموذج المالي.
3. عتبات التنبيه تُفحص في كل تحديث.

## Cross-links
- `CASH_CONTROL.md`
- `MRR_DEFINITION.md`
- `FINANCIAL_MODEL_V1.md`
- `FINANCIAL_DASHBOARD.md`
- `docs/founder/CEO_COMMAND_CENTER.md`
