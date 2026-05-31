# Hermes Framework Decision Matrix

Hermes should not add orchestration libraries randomly. Each framework has a role and should be introduced only when the repository needs that capability.

## Current foundation

Dealix already has FastAPI, Pydantic, Docker, CI, provider SDKs, and local AI gateway configuration. The first Hermes layer is therefore intentionally lightweight:

- JSON manifest.
- Governance policy.
- Review artifact schema.
- Local runner.
- CI verification.

## Decision matrix

| Need | Recommended tool | Reason |
| --- | --- | --- |
| Provider fallback and routing | LiteLLM | Centralizes model aliases, retries, and fallback model groups. |
| Structured human review checkpoints | LangGraph | Useful when Hermes needs persisted graph state and review pauses. |
| Guardrails and tracing around model-native agents | OpenAI Agents SDK | Useful for input/output checks, handoffs, and traces. |
| Simple role-based agent teams | CrewAI | Useful when agents can be expressed as roles, crews, and tasks. |
| Software engineering workspace automation | OpenHands-style sandboxing | Useful only if Hermes later needs isolated coding workspaces. |

## Adoption rules

1. Start with the local Hermes runner before adding runtime orchestration.
2. Add a framework only if it replaces custom complexity.
3. Keep every new runtime behind review artifacts first.
4. Prefer read-only data connectors before writable integrations.
5. Add telemetry before adding live operational behavior.

## Recommended sequence

### Step 1: LiteLLM gateway

Already included in this PR. Use it for model fallback and cost control.

### Step 2: Review artifact store

Keep JSONL first. Move to Postgres only after the schema stabilizes.

### Step 3: LangGraph checkpoints

Add when Hermes needs multi-step workflows with founder review in the middle.

### Step 4: Agents SDK guardrails

Add when an agent receives untrusted inputs or creates customer-facing outputs.

### Step 5: CrewAI crews

Add when a repeatable role/task process becomes stable enough to express as a crew.

## Source-informed notes

- LiteLLM documents fallback from one model group to another after retry failure.
- OpenAI Agents SDK documents guardrails for checking inputs and outputs around agent runs.
- CrewAI documents crews as groups of agents with tasks and processes.

Hermes should use these capabilities incrementally, not all at once.
