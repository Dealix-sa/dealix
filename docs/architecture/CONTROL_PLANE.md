# Hermes Control Plane

The control plane is the only legitimate entry point for any agent /
tool / workflow call inside Dealix. Any request that does not flow
through `dealix.hermes.control_plane.runtime.ControlPlaneRuntime.dispatch`
is illegitimate and must be rejected upstream.

## Order of evaluation

1. `kill_switch` — agent, tool, capability disabled?
2. `sovereignty_gate` — what level (S0–S5) is this action?
3. `trust_gate` — overclaim, leak, unapproved pricing?
4. `data_gate` — workspace + sensitivity caps?
5. `tool_gate` — does the agent hold the capability?
6. `runtime_modes` — does the global mode allow this?
7. `approval_gate` — if sovereign approval is required, queue and pause.
8. Execute.
9. `outcome_gate` — Outcome must be recorded before the request closes.
10. `audit_gate` — append an immutable record.

## Failure modes

| Failure | Result |
| --- | --- |
| Kill switch fired | `RuntimeOutcome.KILLED` |
| Any policy blocker | `RuntimeOutcome.DENIED` |
| Sovereign approval required | `RuntimeOutcome.QUEUED_FOR_APPROVAL` |
| Missing Outcome after execute | `RuntimeOutcome.DENIED` |

## Bootstrapping

Dealix always boots in `RuntimeMode.DRAFT_ONLY`. Promotion to higher
modes is itself an S2 action and requires Sami.
