# Company Data Architecture
## Purpose
Define how Dealix stores, validates, reads, and uses company operating data.
## Owner
Sami / Founder CEO.
## Review Cadence
Weekly during first 90 days, monthly after.
## Data Principle
Public repo contains systems, templates, checks, and demo data.
Private ops contains real leads, clients, proposals, payments, approvals, and delivery evidence.
## Source of Truth
| Domain | Source of Truth | Public/Private |
|---|---|---|
| Pipeline | pipeline/pipeline_tracker.csv | Private |
| Revenue Actions | revenue/revenue_action_log.csv | Private |
| Cash | revenue/cash_collected.csv | Private |
| Pipeline Value | revenue/pipeline_value.csv | Private |
| MRR | revenue/mrr_tracker.csv | Private |
| Expenses | finance/expenses.csv | Private |
| Approvals | trust/approval_log.csv | Private |
| Stage | stage/stage_exit_checklist.csv | Private |
| Evidence | evidence/execution_evidence_ledger.csv | Private |
| Weekly Metrics | metrics_history/weekly_metrics.csv | Private |
| Demo Dashboard | dashboard_data/demo/*.demo.json | Public |
| Real Dashboard | dashboard_data/company_metrics.json | Local/Private only |
## Rules
- Real customer, lead, payment, and delivery data never enters public repo.
- Public repo may contain demo data only.
- Every CSV must have a schema.
- Every generated report must trace back to source files.
- Every stage advancement requires evidence.
- Every public claim requires approval and evidence.
## Data Quality Dimensions
- Completeness
- Freshness
- Consistency
- Traceability
- Privacy boundary
- Decision usefulness
## Evidence
- schema files
- validators
- audit reports
- GitHub checks
- private ops audit
