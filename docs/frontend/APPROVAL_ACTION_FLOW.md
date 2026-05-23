# Approval Action Flow

## Purpose

Define how Founder Console approval actions work end-to-end so every
button in `/approvals` has a documented path through Trust Plane and
audit.

## Flow

```
Founder Console button
  → apps/web/lib/dealix-actions.ts
  → POST /api/v1/internal/approvals/{id}/{decision}
  → trust evaluator (policy + risk class)
  → approval_decisions audit log
  → queue status update
  → downstream worker picks the approved item
  → external action only if Trust Plane allowed it
```

The frontend never:

- writes to the database directly,
- calls external services (WhatsApp, email, payments) on its own,
- bypasses the approve / reject / needs-edit decision endpoints.

## Actions

| Action | Endpoint | Trust Class |
| --- | --- | --- |
| Approve | `POST /api/v1/internal/approvals/{id}/approve` | A2 |
| Reject | `POST /api/v1/internal/approvals/{id}/reject` | A2 |
| Request Edit | `POST /api/v1/internal/approvals/{id}/request-edit` | A2 |
| Escalate | _(planned — routes to founder mailbox)_ | A2 |
| Defer | _(planned — re-queues with new SLA)_ | A2 |

## Rules

- **A2 actions require explicit approval.** No background worker can
  approve on behalf of the founder.
- **A3 cannot be automated** under any circumstance. They surface in
  Founder Console but never auto-execute.
- **Every decision writes an audit row** with: timestamp, approval_id,
  decision, actor, reason, policy result, audit path.
- **No frontend button bypasses the Trust Plane.** If a button exists
  in `/approvals`, the corresponding endpoint must call the policy
  evaluator before mutating queue state.
- **Failures are surfaced.** If the audit write fails, the action
  reports failure to the founder — silent drops are not acceptable.

## Audit Schema

`approval_decisions` ledger row:

```
date, approval_id, type, decision, actor, reason, policy_result, audit_path
```

This ledger is the source of truth for "did Sami approve X?" questions
and feeds the production gate F5 check.
