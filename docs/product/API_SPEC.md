# API Spec — ideal vs implemented

## Ideal (north star)

| Area | Ideal endpoint |
|------|----------------|
| Data | `POST /api/v1/data/import-preview` |
| Data | `POST /api/v1/data/quality-score` |
| Revenue | `POST /api/v1/revenue/score-accounts` |
| Knowledge | `POST /api/v1/knowledge/search` |
| Governance | `POST /api/v1/governance/check` |
| Reports | `POST /api/v1/reports/proof-pack` |

## Implemented today (representative)

| Purpose | Actual path |
|---------|-------------|
| CSV preview | `POST /api/v1/revenue-data/csv-preview` |
| Commercial engagements | `POST /api/v1/commercial/engagements/lead-intelligence-sprint` |
| Company brain | `POST /api/v1/company-brain/query` |
| Governance dashboard | `GET /api/v1/governance/risk-dashboard` |
| Service readiness | `GET /api/v1/commercial/service-readiness/{service_id}` |
| Readiness gates | `POST /api/v1/commercial/readiness-gates/check` |

Gap list shrinks as routers align naming; do not break clients without versioning.

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
