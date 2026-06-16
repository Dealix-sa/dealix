# Dealix Architecture

## Layers

1. Frontend
2. API
3. Service OS modules
4. AI Gateway
5. Governance
6. Data layer
7. Observability
8. Integrations

## Core modules (repo mapping)

| Name in docs | Python packages |
|--------------|------------------|
| Strategy OS | `strategy_os` |
| Data OS | `data_os`, `revenue_data_intake` |
| Revenue OS | `revenue_os` |
| Customer OS | `support_os`, customer inbox routers |
| Operations OS | `workflow_os_v10`, `delivery_factory`, `bottleneck_radar` |
| Knowledge OS | `knowledge_os` (facade), `company_brain_mvp`, `support_os/knowledge_answer.py` |
| Governance OS | `governance_os`, `compliance_os` |
| Reporting OS | `reporting_os`, `executive_reporting` |
| Delivery OS | `delivery_os`, `service_sessions` |

See [`../commercial/CODE_MAP_OS_TO_MODULES_AR.md`](../commercial/CODE_MAP_OS_TO_MODULES_AR.md).

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
