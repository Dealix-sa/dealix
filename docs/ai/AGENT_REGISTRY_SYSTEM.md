# Agent Registry System

`registries/agent_registry.yaml` is the source of truth for every AI
agent that runs inside Dealix. Each agent must declare:

- `id`, `name`, `purpose`
- `approval_class_max` — the highest approval class the agent can ever
  request (A0/A1/A2/A3).
- `tools` — declared tools only; an agent that uses an undeclared tool
  fails the `tool_misuse` eval suite.
- `outputs` — artifacts/states the agent writes.
- `external_action_allowed` — must be `false` if `approval_class_max`
  is A3.
- `kill_switch`, `eval_required`, `audit_required` — must be `true`.

## Verifier

```
make agent-registry
```

Runs `scripts/verify_agent_registry.py`, which enforces the rules above.
