---
title: Agent Registry
owner: AI Governance Lead
status: active
last_review: 2026-05-23
---

# Agent Registry — سجل وكلاء ديليكس

## Purpose

The canonical list of every Dealix agent: identity, owner, purpose, permissions summary, and current status. No agent operates without a registry row. Mirrors the agent identity discipline in [docs/agentic_operations/AGENT_IDENTITY_LAYER.md](../agentic_operations/AGENT_IDENTITY_LAYER.md).

## Registry row schema

```yaml
agent_id: AGT-NNN
name: human name
owner: role
business_unit: delivery | sales | content | engineering | pm
purpose: one sentence
risk_tier: T1 | T2 | T3
autonomy_band: A1 | A2 | A3
inputs_allowed: [data classes]
tools_allowed: [tool ids]
tools_forbidden: [tool ids]
external_action: false  # always false in MVP
status: sandbox | active | paused | retired
linked_release_gate: file path in dealix-ops-private/ai_management/release_gates/
linked_permissions: row in AGENT_PERMISSIONS.md
last_eval_pass: YYYY-MM-DD
last_review: YYYY-MM-DD
```

## Standard agents (purpose only — populate registry file for current versions)

| Agent | Business unit | Purpose | Tier | Band |
|---|---|---|---|---|
| Delivery agent | delivery | Draft proof packs, scope outlines, sprint checklists | T2 | A2 |
| Sales agent | sales | Draft proposals, sample summaries, follow-up notes | T2 | A2 |
| Content agent | content | Draft case-safe summaries, sector report sections | T2 | A2 |
| Engineer agent | engineering | Draft code, tests, schema validations | T2 | A2 |
| PM agent | pm | Aggregate signals into weekly review draft | T1 | A1 |

All agents above are bound to A1–A3 only. A4+ external action is forbidden in MVP per [docs/agentic_operations/AGENT_OPERATING_LEVELS.md](../agentic_operations/AGENT_OPERATING_LEVELS.md).

## Operations

1. New agent requires a registry row before sandbox use.
2. Promotion to active requires the release gate at [docs/ai_management/AI_AGENT_RELEASE_GATE.md](../ai_management/AI_AGENT_RELEASE_GATE.md).
3. Quarterly re-attestation: each owner confirms the row reflects reality.
4. Retired agents keep a row with retirement date and a note on remaining data.

## Non-negotiables

- No unregistered agent runs.
- No agent has `external_action: true` in MVP.
- No agent inherits another agent's permissions implicitly; permissions are declared.

## Evidence

- Registry file: `dealix-ops-private/ai_management/agent_registry.yaml`.
- Cross-link to release gate files and eval results.

## Owner & cadence

- AI Governance Lead maintains the registry.
- Quarterly re-attestation; per-release updates.

## AR — ملخّص

سجل الوكلاء هو القائمة المعتمدة لكل وكيل: هوية، مالك، غرض، وحدة، مستوى خطر، نطاق استقلالية، مدخلات وأدوات مسموحة وممنوعة، حالة. كل وكيل في MVP محدّد بـ A1–A3 ولا إجراء خارجي. لا تشغيل بلا صف. القيمة التقديرية ليست قيمة مُتحقَّقة.
