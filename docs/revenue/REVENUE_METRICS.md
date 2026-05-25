# مقاييس الإيرادات — Revenue Metrics

> Exact metric definitions. No two-interpretations metrics.

## Purpose
Make every revenue number computable and reproducible by anyone reading the repo. Eliminate ambiguity about what a metric means.

## Owner
Founder/CEO.

## Inputs
- Pipeline stages (`PIPELINE_STAGES.md`).
- Cash rules (`CASH_RULES.md`).
- Invoice workflow (`docs/finance/INVOICE_WORKFLOW.md`).
- MRR definition (`docs/finance/MRR_DEFINITION.md`).

## Outputs
- Metric definitions (this file).
- Weekly snapshot in `dealix-ops-private/kpi/YYYY-WW.json`.
- Trend reports for Monthly Strategy Review.

## Rules
1. Every metric has: name, definition, formula, window, source, owner.
2. A metric without a written definition does not appear in any report.
3. Definitions change only by Monthly Strategy Review decision; the change date is recorded.
4. Windows are explicit (rolling 30 days, calendar month, quarter, etc.).
5. "Approximately" is forbidden — round, or omit.

## Metrics covered
- Proposal-to-payment rate
- Delivery-to-retainer rate
- Average sprint value
- MRR (definition deferred to `docs/finance/MRR_DEFINITION.md`)
- Cash-in rate
- Pipeline coverage
- Stage conversion rates
- Customer concentration

## Cadence
Snapshot Weekly. Trend Monthly.

## Evidence
`dealix-ops-private/kpi/`.

## Verifier
`make revenue-metrics-verify` — checks each metric in the snapshot has a matching definition entry.

## Runtime Command
`make revenue-metrics-snapshot`

---

## Metric definitions

### Proposal-to-payment rate
- Definition: proposals that result in full payment / proposals sent.
- Window: rolling 30 days.
- Formula: `count(Paid in window) / count(Proposal sent in window)`.
- Source: `PIPELINE_STAGES.md` transitions.
- Target: ≥ 30%.

### Delivery-to-retainer rate
- Definition: sprints whose customer signed a Revenue Desk retainer within 14 days of acceptance / sprints completed.
- Window: rolling 90 days (small samples).
- Formula: `count(Retainer attached within 14d) / count(Sprint completed in window)`.
- Source: sprint records + retainer signing dates.
- Target: ≥ 30%.

### Average sprint value
- Definition: mean paid SAR per Revenue Sprint completed.
- Window: rolling 90 days.
- Formula: `sum(paid SAR for completed sprints) / count(completed sprints)`.
- Source: invoices.
- Target: tracked, not a hard threshold; grows with productization.

### Cash-in rate
- Definition: SAR cleared into Dealix account.
- Window: weekly, monthly, quarterly.
- Source: `docs/finance/CASH_CONTROL.md`.

### Pipeline coverage
- Definition: open SAR (sum of opportunities at Proposal sent or earlier with ICP-fit ≥ 6) / quarter's revenue target.
- Window: current quarter.
- Target: ≥ 3x quarterly target.

### Stage conversion rates
For each transition in `PIPELINE_STAGES.md`:
- Definition: count of opportunities that completed the transition in window / count that entered the source stage in window.
- Window: rolling 30 days.

### Customer concentration
- Definition: % of trailing-12-month revenue from the largest customer.
- Target: ≤ 30%.
- Above 30%: customer concentration risk flagged in Monthly Strategy Review.

### Days sales outstanding (DSO)
- Definition: mean days from invoice issued to payment cleared.
- Window: rolling 90 days.
- Target: ≤ 21 days.

### Refund rate
- Definition: refunded SAR / cash-in SAR.
- Window: rolling 90 days.
- Target: ≤ 2%.

## Snapshot schema
```json
{
  "week": "YYYY-WW",
  "metrics": [
    {"id": "REV-PROP-PAY", "value": 0.30, "window": "30d", "computed_at": "YYYY-MM-DD"},
    {"id": "REV-DEL-RET", "value": 0.35, "window": "90d", "computed_at": "YYYY-MM-DD"}
  ]
}
```

## What is NOT a revenue metric
- LinkedIn impressions on founder posts.
- Open rates on emails.
- Website visits.
- "Booked" or "verbal yes" deals.

These may be useful operationally but they do not enter revenue reporting.

## Change log
| Date | Metric | Change | Approver |
|---|---|---|---|
| YYYY-MM-DD | <metric> | <what changed> | Founder |

## القواعد العربية
1. كل مقياس له تعريف، نافذة، صيغة، مصدر، ومالك.
2. التعريفات تتغير عبر المراجعة الشهرية فقط، مع تسجيل تاريخ التغيير.
3. النوافذ صريحة (30 يومًا متحركة، شهر تقويمي، ربع، إلخ).

## Cross-links
- `PIPELINE_STAGES.md`
- `CASH_RULES.md`
- `docs/finance/MRR_DEFINITION.md`
- `docs/founder/CEO_KPI_TREE.md`
- `REVENUE_COMMAND_CENTER.md`
