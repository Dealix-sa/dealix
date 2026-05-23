---
title: AI Change Management
owner: AI Governance Lead
status: active
last_review: 2026-05-23
---

# AI Change Management — إدارة تغييرات الذكاء الاصطناعي

## Purpose

Define how prompt changes, model version changes, retrieval changes, and tool wiring changes are proposed, gated, deployed, and reverted. Maps to NIST AI RMF "Govern" function.

## What counts as a change

| Class | Examples |
|---|---|
| Prompt | system prompt edit, few-shot edit, output schema edit |
| Model | provider switch, version bump, parameter change |
| Retrieval | corpus update, embedding model change, chunking change |
| Tool wiring | new tool exposed to agent, permission widening |
| Policy | redaction list update, claim-safety filter change |

## Gating workflow

1. **Proposal** — change author files a PR with: rationale, expected effect, affected systems, eval plan, rollback plan.
2. **Review** — AI Governance Lead checks the proposal against [AI_RISK_REGISTER.md](./AI_RISK_REGISTER.md). New risks added.
3. **Eval** — eval set per [AI_EVALUATION_POLICY.md](./AI_EVALUATION_POLICY.md) is run on the candidate; results attached.
4. **Approval** — required approver per tier:
   - T1: AI Governance Lead.
   - T2: AI Governance Lead + Trust Lead.
   - T3: Founder.
5. **Deploy** — version is recorded in [docs/06_llm_gateway/AI_RUN_LEDGER.md](../06_llm_gateway/AI_RUN_LEDGER.md).
6. **Watch** — first 7 days, sampling rate is doubled.
7. **Rollback** — pre-defined; can be triggered by any failed eval or any incident per [AI_INCIDENT_RESPONSE.md](./AI_INCIDENT_RESPONSE.md).

## Versioning

- Every prompt has a version string committed to [docs/06_llm_gateway/PROMPT_REGISTRY.md](../06_llm_gateway/PROMPT_REGISTRY.md).
- Every model bind has a version; routing is logged via [docs/06_llm_gateway/MODEL_ROUTING.md](../06_llm_gateway/MODEL_ROUTING.md).
- The run ledger references prompt and model versions per call.

## Non-negotiables

- No prompt change reaches production without a PR. No "quick fix" in a runtime UI.
- No model version is silently picked up; pinned versions only.
- No new tool is exposed to an agent without a permission review per [docs/agents/AGENT_PERMISSIONS.md](../agents/AGENT_PERMISSIONS.md).

## Evidence

- Change log committed alongside code.
- Eval results attached to the PR.
- Rollback events logged with cause.

## Owner & cadence

- AI Governance Lead owns the workflow.
- Reviewed quarterly; ad hoc on any incident.

## AR — ملخّص

إدارة تغييرات الذكاء الاصطناعي تغطي الموجّهات، النماذج، الاسترجاع، توصيل الأدوات، السياسات. كل تغيير يمرّ ببوّابة: مقترح، مراجعة، تقييم، موافقة حسب مستوى الخطر، نشر، مراقبة 7 أيام بمعدّل عيّنات مضاعف، وقاعدة تراجع جاهزة. لا تعديل في الإنتاج بلا PR. القيمة التقديرية ليست قيمة مُتحقَّقة.
