---
title: AI Agent Release Gate
owner: Founder
status: active
last_review: 2026-05-23
---

# AI Agent Release Gate — بوّابة إطلاق وكلاء الذكاء الاصطناعي

## Purpose

Define the binary gate every new or materially-changed agent must pass before it is allowed in any environment beyond a sandbox. Nothing else opens this door.

## Gate checklist

A release is **gated** unless every row is green.

| # | Requirement | Evidence |
|---|---|---|
| 1 | Registered in [docs/agents/AGENT_REGISTRY.md](../agents/AGENT_REGISTRY.md) with owner, purpose, and risk tier | registry row |
| 2 | Permissions scoped per [docs/agents/AGENT_PERMISSIONS.md](../agents/AGENT_PERMISSIONS.md), A2/A3 max | permissions row |
| 3 | Threat-model rows added for any new surface in [AI_THREAT_MODEL.md](./AI_THREAT_MODEL.md) | threat model section |
| 4 | Risk rows added in [AI_RISK_REGISTER.md](./AI_RISK_REGISTER.md), residual at or below medium | risk rows |
| 5 | Eval suite passes per [AI_EVALUATION_POLICY.md](./AI_EVALUATION_POLICY.md) and per [docs/agents/AGENT_EVALUATION.md](../agents/AGENT_EVALUATION.md) | eval result file |
| 6 | Human oversight points defined per [AI_HUMAN_OVERSIGHT.md](./AI_HUMAN_OVERSIGHT.md) | oversight row |
| 7 | Logging on per [docs/agents/AGENT_LOGGING.md](../agents/AGENT_LOGGING.md) | sample log lines |
| 8 | Handoff contract written per [docs/agents/AGENT_HANDOFFS.md](../agents/AGENT_HANDOFFS.md) | handoff doc |
| 9 | Rollback plan defined per [AI_CHANGE_MANAGEMENT.md](./AI_CHANGE_MANAGEMENT.md) | rollback section |
| 10 | Supplier vetted per [AI_SUPPLIER_POLICY.md](./AI_SUPPLIER_POLICY.md) if any new vendor introduced | supplier row |

## Approval

- Founder signs off the gate.
- Sign-off is a dated commit referencing the release version.

## What this gate does not do

- It does not authorize A4+ behavior. Autonomous external action is forbidden.
- It does not bypass [docs/05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md).
- It does not exempt the agent from the weekly sampling regime.

## Operations

1. The release author fills the gate file: `dealix-ops-private/ai_management/release_gates/AGT-NNN-vX.md`.
2. Each row links to evidence; missing evidence = gate not passed.
3. Founder signs in the same file.
4. Watch period of 14 days after release with doubled sampling.

## Evidence

- Release gate file per agent version.
- Linked eval, risk, threat, permission, logging artifacts.

## Owner & cadence

- Founder owns the gate.
- AI Governance Lead prepares the file.
- Per-release; reviewed at every change classified material under [AI_CHANGE_MANAGEMENT.md](./AI_CHANGE_MANAGEMENT.md).

## AR — ملخّص

بوّابة إطلاق الوكلاء قائمة عشر متطلّبات: تسجيل، صلاحيات، نموذج تهديد، سجل مخاطر، نجاح تقييم، نقاط إشراف، تسجيلات، عقد تسليم، خطّة تراجع، مورّد مفحوص. لا إطلاق بلا توقيع المؤسس وأدلة لكل صف. لا تخويل لإجراء خارجي ذاتي. القيمة التقديرية ليست قيمة مُتحقَّقة.
