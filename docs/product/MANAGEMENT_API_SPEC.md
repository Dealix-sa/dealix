# Management API Spec (design)

Turn **management** into software: readiness, requests, governance, quality, proof, learning. Paths are **indicative**—normalize under `/api/v1/` when implementing.

## Readiness

- `GET /readiness/company`  
- `GET /readiness/services`  
- `POST /readiness/service-score`  

## Requests

- `POST /requests`  
- `GET /requests`  
- `POST /requests/{id}/decision`  

## Clients

- `POST /clients`  
- `GET /clients/{id}/health`  
- `GET /clients/{id}/capability-roadmap`  

## Governance

- `POST /governance/check`  
- `POST /governance/approval`  
- `GET /governance/events`  

## Quality

- `POST /quality/score`  
- `GET /quality/reviews`  

## Proof

- `POST /proof-pack/generate`  
- `GET /proof-ledger`  

## Learning

- `POST /post-project-review`  
- `GET /feature-candidates`  

**Auth / audit / PII:** every route must satisfy [`API_GOVERNANCE.md`](API_GOVERNANCE.md), [`RUNTIME_GOVERNANCE.md`](../governance/RUNTIME_GOVERNANCE.md), [`DATA_GOVERNANCE_BY_DESIGN.md`](DATA_GOVERNANCE_BY_DESIGN.md).

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
