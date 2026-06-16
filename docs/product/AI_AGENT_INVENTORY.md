# AI Agent Inventory

| Agent | Capability | Tools | Data Access | Autonomy Level | Risk | Status |
|---|---|---|---|---:|---|---|
| DataQualityAgent | Data | data_os | datasets | 1 | Medium | MVP |
| RevenueAgent | Revenue | revenue_os | accounts | 2 | Medium | MVP |
| OutreachAgent | Revenue | drafts only | accounts + offer | 2 | High | MVP |
| KnowledgeAgent | Knowledge | retrieval | approved docs | 2 | High | Beta |
| ComplianceGuardAgent | Governance | governance_os | metadata | 3 | High | MVP |
| ReportingAgent | Reporting | reporting_os | project outputs | 2 | Medium | MVP |

## Autonomy Levels

```text
0 = passive helper
1 = analyze
2 = draft/recommend
3 = queue action for approval
4 = execute internal action
5 = external action
6 = autonomous external action
```

## Dealix MVP Rule

```text
Allowed: 0–3
Restricted: 4
Enterprise-only: 5
Forbidden: 6
```

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
