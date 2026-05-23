# Weekly Automation Runbook

## Purpose
Automate the weekly CEO review, comparison, bottleneck analysis, and learning decision.

## Owner
Sami / Founder CEO.

## Review Cadence
Weekly.

## Inputs
- pipeline_tracker.csv
- mrr_tracker.csv
- approval_log.csv
- weekly_metrics.csv

## Outputs
- founder/weekly_ceo_review.md
- learning/weekly_intelligence_review.md
- weekly_reviews/YYYY-MM-DD.md
- recommended playbook update

## Rules
- Weekly review must produce one learning decision.
- Weekly review must recommend one playbook, checklist, template, pricing, message, or trust update.
- The week is not closed until one system improvement is committed.
- Private operating data stays in dealix-ops-private.

## Metrics
- Weekly review generated.
- Learning decision generated.
- Playbook update completed.
- Bottlenecks reduced week over week.

## Evidence
- weekly_reviews/YYYY-MM-DD.md
- metrics_history/weekly_metrics.csv
- Git commit for system improvement
- GitHub Actions pass

## Last Reviewed
YYYY-MM-DD
