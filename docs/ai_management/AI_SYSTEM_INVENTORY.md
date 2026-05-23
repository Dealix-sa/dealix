---
title: AI System Inventory
owner: AI Governance Lead
status: active
last_review: 2026-05-23
---

# AI System Inventory — حصر أنظمة الذكاء الاصطناعي

## Purpose

List every place Dealix uses an AI/LLM, who owns it, what data it touches, and what risk tier it carries. Maps to NIST AI RMF "Map" function. Without an inventory, there is no governance.

## Risk tiers

| Tier | Definition | Examples |
|---|---|---|
| T1 | Internal drafting, no client data, no external send | brainstorming, internal summaries |
| T2 | Touches client data, output reviewed by human before external use | proposal drafts, sample summaries |
| T3 | Influences a client-facing decision; A2-level oversight required | scoping recommendation, sector classification |
| T4 | Forbidden in MVP | autonomous external messaging, automated claims generation |

T4 systems are listed for completeness and explicitly marked forbidden, consistent with [docs/agentic_operations/AGENT_OPERATING_LEVELS.md](../agentic_operations/AGENT_OPERATING_LEVELS.md).

## Inventory schema (one row per system)

```yaml
system_id: AI-NNN
name: human name
owner: role
purpose: one sentence
inputs: [data classes]
outputs: [artifact types]
model_provider: name
model_id: version
hosting: cloud region
data_residency: KSA | other (justified)
risk_tier: T1 | T2 | T3
human_oversight: review point per AI_HUMAN_OVERSIGHT.md
eval_cadence: per AI_EVALUATION_POLICY.md
incident_owner: role
status: active | paused | retired
linked_threat_model: section in AI_THREAT_MODEL.md
linked_supplier_review: AI_SUPPLIER_POLICY.md row
```

## Operations

1. Adding any AI use requires a new row before first use, not after.
2. Retiring a system requires a row update with retirement date and last-output retention plan.
3. Inventory is reviewed monthly. Any drift between row and reality is a logged signal.
4. Every system is mapped to at least one row in [AI_RISK_REGISTER.md](./AI_RISK_REGISTER.md).

## Non-negotiables

- No AI use is added by anyone without filing a row.
- No T2 or T3 system sends external messages without approval per [AI_HUMAN_OVERSIGHT.md](./AI_HUMAN_OVERSIGHT.md).
- No PII is sent to a model unless redacted per [docs/06_llm_gateway/REDACTION_POLICY.md](../06_llm_gateway/REDACTION_POLICY.md).

## Evidence

- Inventory file: `dealix-ops-private/ai_management/inventory.yaml`.
- Cross-linked to [docs/06_llm_gateway/AI_RUN_LEDGER.md](../06_llm_gateway/AI_RUN_LEDGER.md) for runtime evidence.

## Owner & cadence

- AI Governance Lead maintains the inventory.
- Reviewed monthly. Audited quarterly.

## AR — ملخّص

حصر أنظمة الذكاء الاصطناعي يسجّل كل استخدام: المالك، البيانات، المزوّد، الإقامة، مستوى الخطر، نقطة الإشراف البشري، إيقاع التقييم. لا استخدام بلا صف، ولا T2/T3 يرسل خارجياً بلا موافقة، ولا PII بلا تنقيح. القيمة التقديرية ليست قيمة مُتحقَّقة.
