# Agent Registry System

Source of truth: `registries/agent_registry.yaml`.
Reader: `api/internal/agent_registry_reader.py`.
Verifier: `scripts/verify_agent_registry.py`.

## Required fields per agent

`id, name, purpose, approval_class_max, tools, outputs,
external_action_allowed, kill_switch, eval_required`.

## Invariants

- `kill_switch: true` for every agent (no exceptions).
- `eval_required: true` for every agent.
- `external_action_allowed: true` is allowed only if
  `approval_class_max == A0`.
- No A3 agent may have `external_action_allowed: true`.

## Operational controls

The internal API exposes:

- `GET  /api/v1/internal/control/agents` — full registry with enabled state.
- `POST /api/v1/internal/control/agents/{id}/disable` — turn the agent off.
- `POST /api/v1/internal/control/agents/{id}/enable` — turn the agent on.

Disable/enable events are written to the audit CSV with
`approval_class=A1, policy_result=control_plane`.
