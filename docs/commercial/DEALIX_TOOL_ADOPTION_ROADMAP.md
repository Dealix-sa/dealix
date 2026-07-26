# Dealix Tool Adoption Roadmap

Status: proposed  
Operating principle: smallest useful stack first.

## Phase 0: Freeze the policy

Before installing anything, confirm these invariants:

- `EXTERNAL_SEND_ENABLED=false`
- all outbound is draft-only
- no cold WhatsApp
- no secrets in repo
- no public local LLM endpoint
- all generated claims require proof

## Phase 1: Registry and scoring

Add `tool_registry.json` and generate ranked reports:

```bash
python scripts/commercial/score_tool_stack.py   --registry dealix/strategy_execution/tool_registry.json   --output reports/tool_stack/ranked_tool_stack.md
```

Founder output:

- top P0 tools
- adoption blockers
- cost/risk flags
- safe next action per tool

## Phase 2: Internal-only autonomy

Adopt only tools that improve internal execution:

- Ollama for local/private cheap inference
- LangGraph for deterministic strategy workflows
- markitdown for document ingestion
- Firecrawl for allowed-source research
- n8n for approvals and safe routing

Outputs must be reports, drafts, queues, and proof logs only.

## Phase 3: Approval workflows

Connect approval cards before any live connector:

- approve target
- approve message
- approve channel
- approve source evidence
- approve rate limits
- approve opt-out/suppression rule

No approval means no send.

## Phase 4: Growth without bans

Use tools for value-based distribution:

- Saudi opportunity snapshots
- B2G readiness checklists
- revenue leak scanner drafts
- proof-pack summaries
- partner intro drafts
- SEO report drafts
- LinkedIn/X/newsletter/video drafts

Never auto-post or blast.

## Phase 5: Production hardening

Only after the first proof pack and real demand:

- observability with Phoenix or Langfuse
- analytics with PostHog
- dashboards with Metabase
- durable workflows with Temporal if cron/n8n are insufficient
- CRM with Twenty if the lead base is active enough

## Do not do now

- installing all 50 tools
- exposing Ollama/vLLM publicly
- WhatsApp live sending
- autonomous email campaigns
- building a large CRM before lead volume exists
- replacing the current backend stack

## Success metric

A good adoption decision should increase one of these without increasing compliance risk:

- founder execution speed
- lead quality
- proof quality
- draft quality
- technical trust
- local/privacy control
- repeatable revenue workflow
