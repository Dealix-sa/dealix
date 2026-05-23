# Agent Registry System

The Agent Registry is the source of truth for every AI agent Dealix runs. No agent runs unless it is registered. Every agent has an id, a purpose, a maximum approval class, a tool list, an allowed-write list, and an owner.

**Source of truth:** `registries/agent_registry.yaml`
**Owner:** Founder + Engineering Lead
**Trust gate:** A2 — additions, removals, and approval-class changes require founder approval.

## Why a registry

Agents accumulate. Without a registry, the surface area of "what can do what" grows opaque. The registry makes the agent surface enumerable, testable, and kill-switchable.

This addresses two OWASP LLM Top 10 risks directly:

- **Excessive agency.** An agent's allowed tools, allowed writes, and maximum approval class are explicit and enforced.
- **Prompt injection.** Tools the agent does not have cannot be invoked by injection; the registry is the allowlist.

## Schema

```yaml
agents:
  - id: brand_guardian
    name: Brand Guardian
    purpose: Lint copy for hype, guarantees, PII, disclosure
    approval_class_max: A1
    tools:
      - copy_lint
      - read_doc
      - write_review_note
    outputs:
      - review_decision
      - rationale
    external_action_allowed: false
    kill_switch: true
    eval_required: true
    audit_required: true
    owner: marketing_lead
    allowed_write_targets:
      - $PRIVATE_OPS/brand_guardian_reviews.csv
    version: 1.4.0
    last_reviewed_by: founder
    last_reviewed_at: 2026-04-01T08:00:00Z
```

## Required fields

| Field | Notes |
|-------|-------|
| `id` | Stable, snake_case |
| `name` | Display name |
| `purpose` | One sentence |
| `approval_class_max` | A0, A1, or A2. Never A3. |
| `tools` | Allowlist of tool ids |
| `outputs` | Allowlist of artifact types |
| `external_action_allowed` | Default false; true only with founder rationale |
| `kill_switch` | Always true |
| `eval_required` | Always true |
| `audit_required` | Always true |
| `owner` | Named role |
| `allowed_write_targets` | Explicit CSV / artifact paths in `$PRIVATE_OPS` |

## Lifecycle

| Stage | Action |
|-------|--------|
| Propose | Engineer drafts agent spec in PR |
| Eval | Eval gate runs (`docs/evals/EVAL_GATE_V1.md`) |
| Approve | Founder approves at A2 |
| Activate | Agent is enabled in runtime |
| Monitor | Audit + eval cadence |
| Retire | Founder retires; registry marks `status: retired` |

## Kill switch

Every agent has a kill switch. Triggers:

- Eval-fail above threshold.
- Cost-spike above guardrail (`docs/finance/AI_UNIT_ECONOMICS_SYSTEM.md`).
- Policy-violation count above threshold.
- Founder manual override.

The kill switch is implemented at the runtime layer; the policy engine refuses to dispatch tasks to a killed agent.

## Failure modes

- **Drift between registry and runtime:** runtime accepts agents not in the registry. Detection: nightly diff. Recovery: deny, audit, founder review.
- **Approval-class escalation:** an agent attempts an action above its `approval_class_max`. Detection: policy engine. Recovery: deny, audit, agent paused.
- **Tool-allowlist bypass:** an agent invokes a tool not in its `tools`. Detection: policy engine. Recovery: deny, audit, agent paused.

## Recovery path

If the registry is corrupted or out of sync with runtime, the founder halts all agent dispatch until reconciliation. Manual fallback continues.

## Metrics

- Registered agent count.
- Active agent count.
- Kill-switch activations per quarter.
- Drift incidents per quarter (target: 0).

## Disclaimer

The registry is a control surface, not a guarantee of correctness. Every agent is monitored and may be killed. Estimated value is not Verified value.
