# Autonomy Policy

Dealix uses five levels of autonomy. The autonomy level of an action is
distinct from its approval level (see `docs/control_plane/APPROVAL_ROUTING.md`).

## Levels

| Level | Name | Meaning |
|---|---|---|
| L0 | Manual | Human does the work end-to-end |
| L1 | Assisted | AI drafts, human edits |
| L2 | Semi-Auto | System executes internally; waits for approval to go external |
| L3 | Auto | System executes low-risk internal actions on its own |
| L4 | Prohibited | System must never execute |

## L4 — Prohibited Actions

- Contract changes
- NDA signing
- Refunds
- Legal commitments
- Regulator communication
- Sensitive data exports
- Guaranteed-revenue claims
- Full-compliance claims

## Combination Rule

The effective restriction on an action is the **stricter** of its
autonomy level and its approval level. A workflow tagged `L3` but routed
`A3` cannot auto-execute.

## Audit

Every L2/L3 execution and every L4 attempt is written to the audit log in
`dealix-ops-private/trust/audit_log.md` with `timestamp, actor, action,
inputs_hash, outcome`.
