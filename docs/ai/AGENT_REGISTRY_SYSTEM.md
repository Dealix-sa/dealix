# Agent Registry System

Source of truth: [`registries/agent_registry.yaml`](../../registries/agent_registry.yaml).

Every agent that interacts with the Dealix runtime MUST appear here. The
verifier (`scripts/verify_agent_registry.py`) blocks CI if an agent is
missing a required field or violates a safety default.

## Required fields

| Field | Why |
|---|---|
| `id` | Stable identifier used in the audit log. |
| `name` | Human label for the console. |
| `purpose` | One-sentence justification. |
| `approval_class_max` | Max class the agent may request. NEVER A3. |
| `tools` | Bounded list — limits blast radius. |
| `outputs` | What the agent produces. |
| `external_action_allowed` | MUST be `false`. |
| `kill_switch` | MUST be `true`. Founder can disable from console. |
| `eval_required` | MUST be `true`. Outputs run the eval gate. |
| `audit_required` | MUST be `true`. Every decision logged. |
| `owner` | Human accountable. |
| `data_access_level` | Which private-runtime subtree the agent may read. |
| `allowed_write_targets` | Whitelist of files the agent may append to. |

## Adding an agent

1. Append a new entry under `agents:` in the YAML.
2. Run `make agent-registry`.
3. Add docs row in `docs/ai/REVENUE_AGENT_SWARM.md` (if revenue agent)
   or a doc that explains the new agent's eval suite.

## Removing an agent

Removal requires founder approval recorded in
`approval_decisions.csv` and a matching CHANGELOG entry. Coding agents
must NOT remove entries autonomously.
