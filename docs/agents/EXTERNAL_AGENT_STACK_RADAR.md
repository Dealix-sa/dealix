# Dealix External Agent Stack Radar

## Purpose

This document records the external repositories, frameworks, and agent-platform patterns Dealix should learn from without blindly copying or vendoring them.

The goal is to turn the current AI-agent wave into Dealix-native operating infrastructure:

```text
Loops + Data Connectors + Agent Skills + Safety Runtime + Command Room + Proof Pack
```

## Executive decision

Do **not** import external agent frameworks directly into Dealix yet.

Instead:

1. Absorb the patterns.
2. Build small Dealix-native contracts first.
3. Keep runtime dependencies stable.
4. Add external runtimes only after a narrow use case proves the need.
5. Keep all external actions behind approval, provenance, and safety gates.

## Priority radar

| External repo / pattern | Use now | Do not do yet | Dealix surface |
|---|---|---|---|
| LangGraph | Durable loops, checkpoints, human-in-the-loop, long-running state | Do not add runtime until one loop needs graph resumability | Loop OS, Revenue, Brain, Delivery |
| OpenAI Agents SDK | Multi-agent handoffs, guardrails, sandbox patterns | Do not make it the only provider runtime | Agent Workbench, Research, Builder Agents |
| Model Context Protocol | Standard connector protocol and SDK ecosystem | Do not connect production DB/email/WhatsApp directly | MCP Gateway, Data Connectors, Trust OS |
| NVIDIA NeMo Agent Toolkit | Enterprise reference for teams of agents, telemetry, evaluation | Do not overengineer before loops stabilize | Enterprise Agent Stack, Observability |
| CrewAI | Role/task/crew/flow mental model | Do not add autonomous crews before deterministic scripts mature | Agent Skills, Revenue Team, Delivery Team |
| AutoGen / Microsoft Agent Framework lineage | Agent-to-agent collaboration and human checkpoints | Avoid unsafe local/browser control planes | PR Agents, CI Fix Agents, Agent Workbench |
| PydanticAI | Typed output contracts | Do not create incompatible schema sprawl | Ledgers, Reports, Approval Cards |
| LlamaIndex | Knowledge and RAG architecture | Do not add vector DB until real data volume requires it | Company Brain, Proof Pack, Knowledge Base |
| LiteLLM | Provider routing, fallback, model gateway | Do not centralize secrets/logs before key handling is mature | AI Router, Cost Control |
| Langfuse / Phoenix / Weave-style observability | Trace/provenance concepts | Do not log sensitive prompts/customer data without redaction | Trust OS, Proof Pack, Audit Logs |
| Firecrawl / Crawl4AI-style ingestion | Web-to-markdown research ingestion pattern | Do not crawl aggressively or bypass protections | Market Watch, Prospect Research |

## Dealix-native architecture to build

```text
Dealix Agentic Operating System
├── Loop Registry
│   ├── revenue-loop
│   ├── brain-loop
│   ├── delivery-loop
│   ├── trust-loop
│   └── market-watch-loop
├── Data Connector Layer
│   ├── csv/manual
│   ├── hubspot
│   ├── gmail-drafts
│   ├── public-web
│   ├── exa/firecrawl-style adapters later
│   └── mcp-gateway later
├── Agent Workbench
│   ├── research agent
│   ├── scoring agent
│   ├── draft agent
│   ├── trust review agent
│   ├── proposal agent
│   ├── delivery agent
│   └── proof agent
├── Safety Runtime
│   ├── no auto send
│   ├── approval cards
│   ├── opt-out / opt-in gates
│   ├── source_url required
│   ├── no fake ROI
│   └── no fake testimonials
└── Observability / Proof
    ├── reports/latest.json
    ├── provenance logs
    ├── audit events
    ├── command room
    └── proof packs
```

## Adoption rules

Before Dealix imports any external runtime or SDK, require:

```text
commercial_use_case:
license_review:
security_review:
data_handling_review:
runtime_dependency_review:
ci_impact:
fallback_plan:
owner:
rollback_plan:
```

## Immediate implementation order

1. Generate and maintain `reports/agents/external_agent_stack_radar.md`.
2. Add `docs/agents/DEALIX_AGENTIC_OS_ADOPTION_MATRIX.md`.
3. Add `docs/agents/DEALIX_MCP_GATEWAY_POLICY.md` before enabling MCP.
4. Add a small `data_connectors` interface before adding any web/crawl/exa dependency.
5. Add a `loop_registry` before adding LangGraph or similar runtime.
6. Add provenance fields to every generated artifact.

## Hard stop rules

Stop before merge if any change:

- enables external sending
- adds unreviewed network tools
- exposes secrets to prompts
- vendors an external repo wholesale
- adds large runtime dependencies without a narrow use case
- adds crawling/scraping without source policy
- adds MCP tools without gateway controls
- logs customer data without redaction
