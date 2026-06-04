# Commercial Metrics Dashboard

> Reply and revenue metrics are **manual inputs or samples**. The system never
> assumes real revenue. Source config: `config/commercial_metrics.json`.

## System-generated (from the daily batch)
- `drafts_generated`, `founder_review_count`
- `rejected_quality`, `rejected_compliance`, `needs_research`
- channel / vertical / language distribution
- `safety_violations` (must be 0)

## Manual-input metrics (founder fills)
- `approved_manual`, `manual_sent`
- `replies_positive`, `replies_negative`, `reply_rate`
- `qualified_calls`, `diagnostics_sold`, `pilots_sold`, `retainers_started`
- `revenue_pipeline_sar`, `realized_revenue_sar`
- `top_vertical`, `top_channel`, `top_objection`

## Daily snapshot
```bash
python scripts/commercial_metrics_summary.py
```
Reads `outputs/commercial_launch/<today>/daily_metrics.json` and merges the
metric schema. Manual metrics default to zero samples until the founder enters
real values.

## Health checks
- `safety_violations == 0`
- `rejected_compliance` trend stable or falling
- `founder_review_count` ≥ a workable daily approve volume
