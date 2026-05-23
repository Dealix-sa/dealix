# Dealix CLI Runbook

## Purpose
Define how the founder operates Dealix from a single command interface.

## Owner
Sami / Founder CEO.

## Review Cadence
Weekly.

## Inputs
- Private ops repo.
- Public Dealix repo.
- Pipeline tracker.
- Revenue tracker.
- Approval log.
- Trust logs.

## Outputs
- Daily CEO Brief.
- Weekly Intelligence Review.
- Decision Queue.
- Dashboard data.
- Verification result.

## Commands

### Daily
```bash
python -m dealix_cli daily --private-ops ../dealix-ops-private
```
Generates:
* `founder/daily_brief.md`
* `founder/decision_queue.md`
* `learning/weekly_intelligence_review.md`
* `dashboard_data/company_metrics.json`

### Weekly
```bash
python -m dealix_cli weekly --private-ops ../dealix-ops-private
```
Runs weekly generation and private ops checks.

### Dashboard
```bash
python -m dealix_cli dashboard --private-ops ../dealix-ops-private
python -m http.server 8080
```
Open:
`http://localhost:8080/internal_dashboard/ceo_dashboard_v2.html`

### Verify
```bash
python -m dealix_cli verify --private-ops ../dealix-ops-private
```
Runs public and private operating checks.

## Rules
* Do not commit real dashboard JSON.
* Do not commit private client or lead data.
* Run daily before starting execution.
* Run weekly before closing the week.
* Run verify before every PR.

## Metrics
* Daily command success rate.
* Weekly command success rate.
* Verification pass rate.
* Dashboard freshness.
* Decision queue usage.

## Evidence
* Generated daily brief.
* Generated dashboard JSON.
* GitHub Actions.
* Private ops verification logs.

## Last Reviewed
YYYY-MM-DD
