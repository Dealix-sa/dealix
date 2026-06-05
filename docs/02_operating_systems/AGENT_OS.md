# Agent OS

> **Status:** `BETA` · **Plane:** Decision + Trust · **Owner:** Founder · **Last reviewed:** 2026-06-05
>
> No agent without an operating contract.

---

## Purpose

Govern every AI agent in Dealix: what it can do, what it cannot, and a full record
of what it did.

## Functions

- Agent registry
- Permissions
- Prompts
- Logs
- Fallback
- Cost tracking
- Approval boundaries

## Every agent must have a contract

Each agent has an `.agent-contract.md` containing:

```
name
purpose
allowed inputs
allowed outputs
allowed tools
forbidden actions
approval class
logging
tests
owner
rollback
```

## Approval classes (shared with Governance OS)

| Class | Needs approval? |
|---|---|
| A0 Internal draft | No |
| A1 Internal analysis | No |
| A2 Customer-facing draft | Yes, before sending |
| A3 External action | Yes, always |
| A4 Financial / legal / security | Yes + log |
| A5 Destructive action | Forbidden unless explicitly authorized |

## LLM logging contract

Every AI call records:

```json
{
  "task_type": "offer_review",
  "model": "provider/model",
  "cost_estimate": 0.02,
  "latency_ms": 1200,
  "input_class": "customer_data",
  "approval_required": true,
  "output_hash": "..."
}
```

## Model routing (cost rules)

| Task | Model type |
|---|---|
| Simple classification | cheap / fast |
| First-draft writing | cheap / mid |
| Strategic decision | premium |
| Sensitive code | premium + review |
| Customer data | model with policy + logs |
| Legal document | draft only + human review |

## Forbidden

Auto WhatsApp, bulk email, scraping, pricing changes without docs, publishing case
studies without approval, deleting data without a log.

## Deeper references

- `AGENTS.md`, `core/agents/`, `docs/10_agents/`, `docs/16_agents/`
- `docs/06_llm_gateway/`, `docs/09_llm_gateway/`
