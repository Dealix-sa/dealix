# Dealix Agentic OS Adoption Matrix

## Goal

Translate external AI-agent ecosystem lessons into practical Dealix operating-system layers without turning the repo into a dependency dump.

## Matrix

| Layer | External inspiration | Dealix implementation now | Runtime later? |
|---|---|---|---|
| Loop execution | LangGraph, AgentSPEX, Loop Engineering | Dependency-free loop contracts, reports, Make targets | Yes, after loops need resumability |
| Multi-agent workbench | OpenAI Agents SDK, AutoGen, CrewAI | Role map, handoff rules, approval states | Yes, after deterministic scripts stabilize |
| Data connectors | MCP, LlamaIndex, Firecrawl, Exa-style sources | Connector contract with provenance fields | Yes, behind gateway/security policy |
| Enterprise agent teams | NeMo Agent Toolkit | Reference architecture for telemetry/evals/framework neutrality | Later |
| Typed outputs | PydanticAI | Required schema fields for ledgers/artifacts/reports | Optional |
| Model routing | LiteLLM | Provider-neutral AI router design and budget policy | Optional proxy later |
| Observability | Langfuse/Phoenix/Weave/AgentSight | Run provenance, audit logs, proof-pack traceability | Tooling later |
| Security gateway | MCP security research, AutoJack lessons | No direct tool exposure; approval-first tool gateway | Required before external actions |

## Dealix practical translation

### 1. Loops before agents

Do not create autonomous agents first. Create loops first:

```text
loop_name
goal
inputs
steps
verifier
outputs
stop_condition
approval_required
safety_gates
reports
```

### 2. Connectors before crawling

Every external data source must return:

```text
source_name
source_url
retrieved_at
retrieval_method
confidence
evidence_hash
license_or_terms_note
sensitive_data_status
```

### 3. Gateway before MCP

MCP is useful only after Dealix has:

```text
approved_tool_registry
permission_scopes
tool_manifest_review
timeouts
network allowlist
secret redaction
audit log
human approval for external actions
```

### 4. Provenance before automation

Every agent/loop output must explain:

```text
what was used
what was generated
what was verified
what remains assumption
who approved
what changed after approval
```

## Highest-value build sequence

1. `agent-stack-radar` report generator.
2. `loop-registry` file and validator.
3. `data-connector-contract` file and validator.
4. `mcp-gateway-policy` docs and manifest schema.
5. `provenance-report` schema.
6. Optional runtime adapter PR after a real use case proves it.

## Business impact

This turns Dealix from “AI scripts” into a credible enterprise operating-system company:

- safer client delivery
- clearer product architecture
- lower dependency risk
- better proof packs
- stronger sales narrative
- easier future integrations
- credible enterprise governance
