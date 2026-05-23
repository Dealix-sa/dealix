# MVP Data Model (Concept)

Objects/tables for the first product spine:

```text
Client
Project
ServicePackage
DataSource
Dataset
Record
Account
Opportunity
Draft
Workflow
Approval
GovernanceEvent
AuditEvent
ProofEvent
Report
CapitalAsset
FeatureCandidate
```

## Relationships

```text
Client has Projects
Project has ServicePackage
Project has DataSources
Dataset has Records
Record can become Account
Account can become Opportunity
Draft belongs to Account / Project
GovernanceEvent belongs to Project
ProofEvent belongs to Project
CapitalAsset created from Project
FeatureCandidate created from repeated task
```

Deeper schema draft: [`ADVANCED_DATA_MODEL.md`](ADVANCED_DATA_MODEL.md).

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
