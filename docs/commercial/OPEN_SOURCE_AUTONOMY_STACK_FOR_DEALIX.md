# Dealix Open-Source Autonomy Stack

Status: proposed PR pack  
Mode: draft-only, approval-first  
Scope: internal planning, research, scoring, content drafts, proof packs, and safe growth operations.

## Executive intent

This document converts the founder-provided list of 50 open-source/self-hosted GitHub repositories into a Dealix adoption system. The goal is not to install 50 tools. The goal is to turn them into a governed registry that helps Dealix decide what to adopt, defer, or reject.

Dealix should treat this stack as an internal capability map for:

- strategy execution
- lead intelligence
- human-in-the-loop outreach approvals
- local/private LLM workflows
- market-entry research
- content and growth loops
- compliance and proof logging
- engineering trust

## Core rule

Every tool must fit the Dealix operating loop:

```text
Inputs -> AI analysis -> Draft outputs -> Human approval gate -> Action
```

External actions are blocked unless the founder explicitly approves the action. The default mode is draft-only.

## P0 adoption set

The first practical stack is intentionally small:

1. Ollama: private/local model runtime for low-cost classification and drafts.
2. LangGraph: stateful strategy execution workflows.
3. n8n: approval workflows and connector orchestration.
4. Firecrawl: allowed-source web intelligence and market snapshots.
5. markitdown: document-to-markdown ingestion.
6. Dify: visual agent/RAG workflows if it speeds up iteration.
7. Ragas or Phoenix/Langfuse: quality evaluation and tracing before client-facing claims.

## P1 near-term set

Use after P0 is stable:

- Twenty for CRM when 5 active leads exist.
- Cal.com for discovery booking.
- AnythingLLM or PrivateGPT for private internal RAG.
- Metabase for dashboards after reporting tables exist.
- Qdrant or pgvector for embeddings.
- EvolutionAPI only after opt-in, rate-limit, suppression, and approval center exist.

## P2 and P3 reference set

Most other tools are reference or later-stage integrations. Do not add them until there is a direct Dealix workflow that needs them.

## Safety gates

Blocked by default:

- cold WhatsApp blasts
- mass LinkedIn automation
- terms-violating scraping
- fake proof or fake testimonials
- guaranteed revenue claims
- government access claims
- hardcoded secrets
- public Ollama/vLLM endpoints
- live sends, posts, PR merges, payments, or production changes without approval

## Implementation files

- `dealix/strategy_execution/tool_registry.json`: structured registry of the 50 tools.
- `scripts/commercial/score_tool_stack.py`: standard-library scoring report generator.
- `reports/tool_stack/README.md`: report destination and operating notes.
- `docs/commercial/DEALIX_TOOL_ADOPTION_ROADMAP.md`: phased implementation roadmap.

## Decision

Use the list as a governed registry, not as an install list.
