# Trust Guardian Agent

The Trust Guardian agent enforces the trust plane at the agent layer. It reviews proposed agent actions before dispatch, checks them against policy, and either passes or escalates.

**Source of truth:** `registries/agent_registry.yaml` entry `trust_guardian`
**Owner:** Founder + Engineering Lead
**Trust gate:** A1 — Trust Guardian is itself bounded; A2 actions still require founder approval.

## Spec

| Field | Value |
|-------|-------|
| `id` | `trust_guardian` |
| `name` | Trust Guardian |
| `purpose` | Pre-dispatch policy check on every agent action |
| `approval_class_max` | A1 |
| `tools` | `read_policy`, `read_agent_registry`, `read_proposed_action`, `write_decision`, `escalate_to_founder` |
| `outputs` | `policy_decision`, `escalation_record` |
| `external_action_allowed` | false |
| `kill_switch` | true |
| `eval_required` | true |
| `audit_required` | true |
| `owner` | engineering_lead |
| `allowed_write_targets` | `$PRIVATE_OPS/trust_decisions.csv`, `$PRIVATE_OPS/escalations.csv` |

## What it checks

For every proposed agent action:

1. Is the agent registered (`registries/agent_registry.yaml`)?
2. Is the action's approval class within the agent's `approval_class_max`?
3. Is every tool in the action within the agent's `tools`?
4. Is the action's write target within `allowed_write_targets`?
5. Does the action attempt an external send / publish without `external_action_allowed`?
6. Is the agent within its kill-switch state (not killed)?
7. Does the action breach any guardrail in `policies/dealix_control_policy.yaml`?

A `no` on any check is a hard deny with an audit row.

## NIST AI RMF posture

- **Govern.** The Trust Guardian implements organisational policy at runtime.
- **Map.** Every proposed action is mapped to a registered agent, approval class, and policy.
- **Measure.** Decision distribution and override rate are tracked.
- **Manage.** Denials and escalations feed back into policy review.

## Failure modes

- **False allow:** an action that should deny passes. Detection: weekly audit sample. Recovery: rule patch; eval suite extension; if systemic, kill switch.
- **False deny:** a legitimate action is blocked. Detection: agent operator feedback. Recovery: rule tuning; founder review.
- **Bypass:** an agent action reaches runtime without Trust Guardian check. Detection: runtime audit. Recovery: runtime fix; root cause filed.

## Recovery path

If the Trust Guardian itself becomes unreliable, the founder triggers fail-closed mode: all agent actions deny by default until the guardian is restored. Manual operation continues.

## Metrics

- Decisions per day.
- Deny rate (by reason).
- Escalation rate.
- Override rate (founder overrides a deny).

## Disclaimer

The Trust Guardian is a control surface, not a guarantee of correctness. Every external action remains gated by founder approval. Estimated value is not Verified value.
