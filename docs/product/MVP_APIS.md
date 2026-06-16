# MVP APIs (Target Shape)

REST-style targets for the core spine (paths may be prefixed under `/api/v1` in product).

```text
POST /data/import-preview
POST /data/quality-score
POST /governance/check
POST /revenue/score-accounts
POST /revenue/draft-pack
POST /reporting/proof-pack
POST /delivery/qa-score
POST /capital/assets
GET  /founder/command-center
```

## Principle

Every response should support:

```text
result
risk_status
governance_status
audit_event_id (when persisted)
next_action
```

See [`MANAGEMENT_API_SPEC.md`](MANAGEMENT_API_SPEC.md).

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
