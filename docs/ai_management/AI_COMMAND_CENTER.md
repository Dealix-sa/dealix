---
title: AI Command Center
owner: Founder / AI Governance Lead
status: active
last_review: 2026-05-23
---

# AI Command Center — مركز قيادة حوكمة الذكاء الاصطناعي

## Purpose

Single index for every AI-related control in Dealix. Maps the NIST AI Risk Management Framework functions (Govern, Map, Measure, Manage) to specific Dealix docs and owners. If a regulator or enterprise auditor asks "how do you govern AI?" this is where the walk-through starts.

## NIST AI RMF mapping

| RMF function | Dealix docs |
|---|---|
| Govern | [AI_SUPPLIER_POLICY.md](./AI_SUPPLIER_POLICY.md), [AI_CHANGE_MANAGEMENT.md](./AI_CHANGE_MANAGEMENT.md), [docs/05_governance_os/GOVERNANCE_OS.md](../05_governance_os/GOVERNANCE_OS.md) |
| Map | [AI_SYSTEM_INVENTORY.md](./AI_SYSTEM_INVENTORY.md), [AI_THREAT_MODEL.md](./AI_THREAT_MODEL.md) |
| Measure | [AI_EVALUATION_POLICY.md](./AI_EVALUATION_POLICY.md), [docs/06_llm_gateway/AI_RUN_LEDGER.md](../06_llm_gateway/AI_RUN_LEDGER.md) |
| Manage | [AI_RISK_REGISTER.md](./AI_RISK_REGISTER.md), [AI_HUMAN_OVERSIGHT.md](./AI_HUMAN_OVERSIGHT.md), [AI_INCIDENT_RESPONSE.md](./AI_INCIDENT_RESPONSE.md), [AI_AGENT_RELEASE_GATE.md](./AI_AGENT_RELEASE_GATE.md) |

## OWASP LLM Top 10 mapping

The risk register references OWASP LLM Top 10 categories: prompt injection, insecure output handling, training data poisoning, model DoS, supply chain, sensitive data disclosure, insecure plugin design, excessive agency, overreliance, model theft. See [AI_RISK_REGISTER.md](./AI_RISK_REGISTER.md).

## Ownership

| Domain | Doc | Owner |
|---|---|---|
| Inventory | [AI_SYSTEM_INVENTORY.md](./AI_SYSTEM_INVENTORY.md) | AI Governance Lead |
| Risk | [AI_RISK_REGISTER.md](./AI_RISK_REGISTER.md) | AI Governance Lead |
| Evaluation | [AI_EVALUATION_POLICY.md](./AI_EVALUATION_POLICY.md) | AI Governance Lead |
| Oversight | [AI_HUMAN_OVERSIGHT.md](./AI_HUMAN_OVERSIGHT.md) | Founder |
| Change | [AI_CHANGE_MANAGEMENT.md](./AI_CHANGE_MANAGEMENT.md) | AI Governance Lead |
| Incident | [AI_INCIDENT_RESPONSE.md](./AI_INCIDENT_RESPONSE.md) | Founder |
| Supplier | [AI_SUPPLIER_POLICY.md](./AI_SUPPLIER_POLICY.md) | Founder |
| Threat model | [AI_THREAT_MODEL.md](./AI_THREAT_MODEL.md) | AI Governance Lead |
| Release gate | [AI_AGENT_RELEASE_GATE.md](./AI_AGENT_RELEASE_GATE.md) | Founder |

Related: [docs/agents/AGENT_REGISTRY.md](../agents/AGENT_REGISTRY.md), [docs/trust/TRUST_COMMAND_CENTER.md](../trust/TRUST_COMMAND_CENTER.md), [docs/06_llm_gateway/LLM_GATEWAY.md](../06_llm_gateway/LLM_GATEWAY.md).

## Operations

1. Inventory updated whenever an AI use is added or removed.
2. Risk register reviewed monthly; high-risk items reviewed weekly.
3. Evaluation runs on cadence defined per system (see policy).
4. Incidents trigger response within the timelines in [AI_INCIDENT_RESPONSE.md](./AI_INCIDENT_RESPONSE.md).

## Evidence

- Each linked doc carries its own evidence trail.
- Aggregate AI posture report compiled quarterly for internal review.

## Owner & cadence

- AI Governance Lead owns the index.
- Founder owns the highest-tier decisions.
- Monthly review; quarterly external-facing posture refresh.

## AR — ملخّص

مركز قيادة حوكمة الذكاء الاصطناعي يربط دالات إطار NIST AI RMF (الحوكمة، التعيين، القياس، الإدارة) بوثائق ديليكس، ويُشير إلى مخاطر OWASP LLM Top 10 في سجل المخاطر. كل مجال له مالك وإيقاع. القيمة التقديرية ليست قيمة مُتحقَّقة.
