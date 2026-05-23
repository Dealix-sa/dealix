# Approval Audit Log Contract

## Purpose
Ensure every Founder Console approval action is auditable.

## Required Fields

- approval_id
- type
- actor
- decision
- reason
- approval_class
- risk_level
- policy_result
- evidence
- source_endpoint
- timestamp
- external_action_allowed

## Rules

- No approval action without audit.
- A2/A3 requires explicit actor.
- Reject and Needs Edit also write audit.
- External action is only allowed when policy permits.

## Storage

- Bootstrap: append-only CSV at `/opt/dealix-ops-private/trust/approval_decisions.csv`.
- Canonical (next): Postgres table `approval_decisions` with the same schema.

## Endpoint Mapping

| Endpoint | Decision | external_action_allowed |
|----------|----------|--------------------------|
| `POST /api/v1/internal/approvals/{id}/approve` | approve | true if policy allows |
| `POST /api/v1/internal/approvals/{id}/reject` | reject | always false |
| `POST /api/v1/internal/approvals/{id}/request-edit` | needs_edit | always false |
