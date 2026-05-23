# لوحة المالية — Financial Dashboard

> The dashboard layout: panels, refresh cadence, source data.

## Purpose
Specify what the financial dashboard looks like so anyone (founder, advisor, future finance lead) builds the same panels from the same data.

## Owner
Founder/CEO.

## Inputs
- `FINANCE_COMMAND_CENTER.md` daily snapshot.
- `CASH_CONTROL.md` daily entry.
- `MRR_DEFINITION.md` monthly figure.
- `FINANCIAL_MODEL_V1.md` scenarios.
- Invoice tracker (`INVOICE_WORKFLOW.md`).

## Outputs
- The dashboard (rendered or printed) in `dealix-ops-private/finance/dashboard/YYYY-WW.md` or PDF.
- Reference layout in this file.

## Rules
1. The dashboard has exactly the panels listed below. Adding a panel requires Monthly Strategy Review approval.
2. Each panel cites its source data file. No floating numbers.
3. Refresh cadence is per-panel (some daily, some monthly).
4. The dashboard is internal-only. Board Pack contains a curated subset.
5. No projections appear on the dashboard. Projections live in `FINANCIAL_MODEL_V1.md`.

## Metrics
- Dashboard refreshed daily (panels marked daily): coverage ≥ 95%.
- Dashboard discrepancies vs source: 0 tolerated.
- Time to refresh: ≤ 30 minutes weekly.

## Cadence
Daily for some panels; Weekly for trend panels; Monthly for closed-period panels.

## Evidence
`dealix-ops-private/finance/dashboard/`.

## Verifier
`make financial-dashboard-verify` — checks every panel has a source link and refresh date.

## Runtime Command
`make finance-dashboard-refresh`

---

## Panel layout

```
+--------------------+--------------------+--------------------+
| Panel A            | Panel B            | Panel C            |
| The Three Numbers  | This Week Cash     | Runway Forecast    |
+--------------------+--------------------+--------------------+
| Panel D                                                       |
| MRR Movement (this month)                                     |
+--------------------+--------------------+--------------------+
| Panel E            | Panel F            | Panel G            |
| Receivables        | Payables           | DSO Trend          |
+--------------------+--------------------+--------------------+
| Panel H                                                       |
| Capital Allocation Variance (this month)                      |
+--------------------+--------------------+--------------------+
| Panel I                                                       |
| Scenario Comparison (Base / Bull / Bear)                      |
+---------------------------------------------------------------+
```

## Panel definitions

### Panel A — The Three Numbers
- Cash, MRR, Runway.
- Refresh: Daily.
- Source: `FINANCE_COMMAND_CENTER.md`.

### Panel B — This Week Cash
- Cash in (received), cash out (paid), net.
- Refresh: Daily during the week.
- Source: `CASH_CONTROL.md` weekly aggregate.

### Panel C — Runway Forecast
- Runway days at current burn, plus delta vs last week.
- Refresh: Weekly.
- Source: `CASH_CONTROL.md`.

### Panel D — MRR Movement
- Start, +New, +Expansion, -Contraction, -Churn, End.
- Refresh: Monthly on the 1st.
- Source: `MRR_DEFINITION.md`.

### Panel E — Receivables
- Open invoices: count, total SAR, oldest age.
- Refresh: Daily.
- Source: `INVOICE_WORKFLOW.md` index.

### Panel F — Payables
- Open payables next 30 days: total SAR.
- Refresh: Weekly.
- Source: bank/AP records.

### Panel G — DSO Trend
- 4-week trailing DSO.
- Refresh: Weekly.
- Source: `INVOICE_WORKFLOW.md`.

### Panel H — Capital Allocation Variance
- For each tier: target % vs actual %.
- Refresh: Monthly.
- Source: `CAPITAL_ALLOCATION_SYSTEM.md`.

### Panel I — Scenario Comparison
- Base, Bull, Bear: revenue, burn, runway at current month vs projected.
- Refresh: Monthly.
- Source: `FINANCIAL_MODEL_V1.md`.

## What is NOT on the dashboard
- Customer-by-customer revenue (concentration is reported separately).
- Pipeline (lives in `docs/revenue/REVENUE_COMMAND_CENTER.md`).
- Marketing or content metrics.
- Personal expenses.

## Distribution
- Internal-only.
- A curated PDF goes into the Board Pack (`docs/founder/BOARD_PACK_TEMPLATE.md`).
- Customer names are anonymized in any shared copy.

## Quality bar
- Every number on the dashboard traces to a primary file.
- Every panel has a "last refreshed" timestamp.
- A stale panel (> 7 days for daily panels) is flagged red on the dashboard.

## القواعد العربية
1. لوحة المالية تحتوي اللوحات المذكورة فقط. إضافة لوحة تتطلب موافقة المراجعة الشهرية.
2. كل لوحة تستشهد بملف مصدرها.
3. لا توقعات على اللوحة. التوقعات في النموذج المالي.

## Cross-links
- `FINANCE_COMMAND_CENTER.md`
- `CASH_CONTROL.md`
- `MRR_DEFINITION.md`
- `FINANCIAL_MODEL_V1.md`
- `CAPITAL_ALLOCATION_SYSTEM.md`
- `INVOICE_WORKFLOW.md`
- `docs/founder/BOARD_PACK_TEMPLATE.md`
