# CEO Dashboard Data Model

## Purpose
Define the data contract for Dealix CEO Dashboard.

## Owner
Sami / Founder CEO.

## Review Cadence
Weekly.

## Inputs
- pipeline_tracker.csv
- mrr_tracker.csv
- approval_log.csv
- generated bottlenecks
- generated company metrics

## Outputs
- dashboard_data/company_metrics.json
- CEO dashboard view
- decision queue
- weekly operating review

## Rules
- Real private data must not be committed to the public repo.
- JSON exports with real metrics should stay local or private.
- Demo JSON may be committed only if it contains fake data.
- Dashboard decisions must trace back to evidence.

## Metrics
- Dashboard generated successfully.
- Daily brief generated successfully.
- Decision queue generated successfully.
- Bottlenecks detected.
- Private/public boundary preserved.

## Evidence
- dashboard_data/company_metrics.json
- founder/daily_brief.md
- founder/decision_queue.md
- learning/weekly_intelligence_review.md

## Last Reviewed
2026-05-23
