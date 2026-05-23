# Agent Registry System

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> The agent registry is the single source of truth for every Dealix
> agent. This document describes the registry contract and the
> minimum every agent must satisfy.

The agent registry lives at `registries/agent_registry.yaml`. It is
read by the Founder Console, the policy adapter, the eval gate,
and the trust ledger. Every Dealix agent must appear in the
registry; an agent that is not registered cannot be invoked.

## Operating Principles

- Every agent is registered. No agent runs outside the registry.
- Every agent has a maximum approval class. A3 is banned across
  the registry; the registry enforces A1 or A2 only.
- Every agent has a kill switch. Any operator can pause any agent
  at any time without a meeting.
- Every agent has audit and eval requirements. Agents that do not
  satisfy them are disabled.
- Every agent has an owner. Ownership is a human role, not a
  service.
- Every agent has allowed write targets. An agent that writes
  outside its allowed targets is treated as a failure mode.

## Registry Schema

The registry is a YAML file with the following per-agent contract.

| Field                       | Type        | Purpose                                                                 |
|-----------------------------|-------------|-------------------------------------------------------------------------|
| `id`                        | string      | Stable id used by the audit ledger and policy adapter.                   |
| `name`                      | string      | Human-readable name.                                                     |
| `purpose`                   | string      | One- or two-sentence purpose statement.                                  |
| `approval_class_max`        | enum        | `A1` (read/assist) or `A2` (draft/queue). `A3` is banned.                |
| `tools`                     | list        | Tool ids the agent may invoke.                                           |
| `outputs`                   | list        | CSV / markdown paths the agent writes.                                   |
| `external_action_allowed`   | bool        | Always `false`.                                                          |
| `kill_switch`               | bool        | Always `true`.                                                           |
| `eval_required`             | bool        | True unless the agent itself runs the eval gate.                         |
| `audit_required`            | bool        | Always `true`.                                                           |
| `owner`                     | string      | Human role accountable for the agent.                                    |
| `allowed_write_targets`     | list        | Path prefixes the agent may write to.                                    |
| `enabled`                   | bool        | The registry-level kill switch.                                          |

Banned values:

- `approval_class_max: A3`
- `external_action_allowed: true`
- `kill_switch: false`
- `audit_required: false`

## Approval Classes

Dealix uses two classes only.

- **A1 — read/assist.** The agent reads, observes, surfaces, scores,
  or recommends. It does not draft external-facing artefacts and
  does not queue actions that could touch the outside world.
- **A2 — draft/queue.** The agent drafts artefacts (proposals,
  outreach, content) and queues them for human approval. It does
  not execute external action.

A3 (autonomous external action) is banned. The policy adapter
denies any action with `approval_class: A3`.

## Tools

Each agent has a tool list. Tools are concrete capabilities such
as `outreach_drafter`, `account_scoring_model`, `policy_adapter`,
`audit_appender`. Tools are themselves audited; the agent registry
records which tools an agent may invoke, and the policy adapter
enforces the list.

A tool not in the agent's tool list is denied. An agent that
attempts to invoke a denied tool generates a high-severity audit
entry and a kill-switch flag.

## Outputs

Each agent has a list of output paths. These paths live in the
private ops runtime under `/opt/dealix-ops-private` or
`$PRIVATE_OPS`. They are typically CSV or Markdown files. The
registry's `allowed_write_targets` field is the broader path
prefix; the `outputs` list is the specific files.

An agent that writes outside its allowed write targets generates a
high-severity audit entry, is paused via the kill switch, and the
incident response agent opens a ticket.

## Kill Switches

Every agent has two levels of kill switch.

- **Per-agent.** The registry `enabled` field. Setting it to `false`
  prevents the agent from being invoked.
- **Per-output.** A targeted pause that prevents the agent from
  writing to a specific output path.

Either kill switch can be triggered by:

- The founder (always).
- The agent's named owner.
- The Trust Guardian or Eval Guardian when a high-severity flag is
  raised.

A pause writes a trust ledger entry.

## Eval Requirements

Each agent that produces customer-facing or trust-impacting outputs
has `eval_required: true`. The Eval Guardian (registry id
`eval_guardian`) runs the relevant eval suites against the agent's
outputs before they are queued for approval.

Eval suites cover at minimum:

- Claims safety (no guaranteed-outcome wording).
- Brand voice.
- Proof safety (no unapproved customer references).
- Suppression and policy adherence.

An eval-required agent whose latest run failed cannot release new
outputs until the regression is resolved.

## Audit Requirements

Every agent has `audit_required: true`. Every invocation, every
output, and every failure produces an audit ledger entry. The audit
ledger is append-only.

Audit entries include:

- `agent_id`
- `invocation_id`
- `timestamp`
- `approval_class`
- `tool_calls`
- `outputs_written`
- `eval_status`
- `policy_decisions`
- `error_state`

## Owners

Each agent has a human owner. Ownership is not a placeholder; the
owner is accountable for:

- Reviewing the agent's outputs on a defined cadence.
- Responding to kill-switch flags within an agreed window.
- Approving registry changes that affect the agent.
- Participating in the quarterly agent review.

## Allowed Write Targets

Each agent has a tightly scoped list of write target prefixes. For
example, the Brand Guardian's allowed write targets are `[brand/]`;
the Distribution Operator's are `[outreach/]`. An agent that
attempts to write outside these prefixes is denied at the runtime
level.

## Registry Changes

Changing the registry — adding an agent, raising a max approval
class, expanding allowed write targets — requires:

- A written rationale.
- Founder approval.
- An entry in the registry change log.
- An updated eval suite, if the change affects outputs.
- An updated audit ledger schema, if the change affects audit
  fields.

A registry change without these is reverted by the verifier
`scripts/verify_agent_registry.py`.

## Verifiers

The verifier set that enforces the registry contract:

- `scripts/verify_agent_registry.py` — schema and contract.
- `scripts/verify_policy_as_code.py` — registry / policy alignment.
- `scripts/verify_eval_gate.py` — eval gate alignment.
- `scripts/verify_prompt_output_quality.py` — output quality.
- `scripts/verify_company_os.py` — composite.

All verifiers must report PASS before any registry change can
merge.

## Banned Patterns

- Adding an agent with `approval_class_max: A3`.
- Adding an agent with `external_action_allowed: true`.
- Adding an agent without a kill switch.
- Adding an agent without an owner.
- Adding an agent that writes to multiple unrelated paths.
- Adding an agent whose purpose statement implies guaranteed
  outcomes.

## Tenant Mirrors

For R5 (Founder Console) and R6 (Enterprise) tenants, the tenant
may receive a mirror of the registry. The mirror:

- Is a subset of the Dealix registry, never a superset.
- Cannot include `A3`.
- Cannot override the kill switch.
- Records its differences from the Dealix registry in a tenant
  policy mirror file.

A tenant mirror that attempts to add A3 is denied at provisioning.

## Quarterly Review

Each quarter, the founder and named agent owners review the
registry:

- Are all agents still needed?
- Are all approval classes still appropriate?
- Are all tool lists still tight?
- Are all eval suites still passing?
- Are all audit entries clean?

Review output is recorded in `registries/agent_registry_review.md`.

## Per-Agent Documentation

Each agent in the registry has a per-agent document in `docs/ai/`
named after the agent. The per-agent document expands the registry
entry with:

- Failure modes.
- Specific eval tests.
- Owner responsibilities.
- KPIs.
- Cross-agent dependencies.

## Cross-References

- Trust contract: `policies/dealix_control_policy.yaml`.
- Eval gate: `evals/gates/dealix_agent_eval_gate.yaml`.
- Founder Console: `apps/web/`.
- Private ops runtime contract:
  `docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md`.

## Why a Registry, Not Code

Code defines what an agent can do. The registry defines what an
agent is allowed to do. The two together form a contract that a
human can read, audit, and reason about. The registry exists so
that an outside reviewer — buyer, regulator, partner — can
understand the agent landscape without reading the source.

A registry that an outside reviewer can read is the foundation of
the trust contract Dealix offers. Every other piece of the
operating system depends on it being accurate, tight, and
honest.
