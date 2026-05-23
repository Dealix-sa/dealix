---
title: AI Risk Register
owner: AI Governance Lead
status: active
last_review: 2026-05-23
---

# AI Risk Register — سجل مخاطر الذكاء الاصطناعي

## Purpose

For every AI system in [AI_SYSTEM_INVENTORY.md](./AI_SYSTEM_INVENTORY.md), enumerate the realistic risks, the mitigations in place, and the residual risk. References OWASP LLM Top 10 categories and feeds the NIST AI RMF "Manage" function.

## OWASP LLM Top 10 reference

| Code | Risk |
|---|---|
| LLM01 | Prompt injection |
| LLM02 | Insecure output handling |
| LLM03 | Training data poisoning |
| LLM04 | Model denial of service |
| LLM05 | Supply chain vulnerabilities |
| LLM06 | Sensitive information disclosure |
| LLM07 | Insecure plugin design |
| LLM08 | Excessive agency |
| LLM09 | Overreliance |
| LLM10 | Model theft |

## Risk row schema

```yaml
risk_id: RISK-NNN
system_id: AI-NNN
owasp_codes: [LLM01, LLM06, ...]
description: what could go wrong, plain language
likelihood: low | medium | high
impact: low | medium | high
mitigations:
  - control: reference to a Dealix doc or runtime control
  - control: ...
residual: low | medium | high
review_date: YYYY-MM-DD
owner: role
```

## Dealix priority risks (illustrative pattern, fill per system)

| Risk | OWASP | Primary mitigations |
|---|---|---|
| Prompt injection from untrusted input | LLM01 | input boundary per [docs/agentic_operations/AGENT_TOOL_BOUNDARY.md](../agentic_operations/AGENT_TOOL_BOUNDARY.md); never treat external content as instructions |
| Hallucinated claim in client-facing draft | LLM09 | mandatory human review per [AI_HUMAN_OVERSIGHT.md](./AI_HUMAN_OVERSIGHT.md); claim-safety check per [docs/05_governance_os/CLAIM_SAFETY.md](../05_governance_os/CLAIM_SAFETY.md) |
| PII leakage via prompt | LLM06 | redaction per [docs/06_llm_gateway/REDACTION_POLICY.md](../06_llm_gateway/REDACTION_POLICY.md) |
| Excessive agency in agent action | LLM08 | autonomy capped at A2/A3 per [docs/agents/AGENT_PERMISSIONS.md](../agents/AGENT_PERMISSIONS.md) |
| Insecure handling of model output rendered to user | LLM02 | schema validation per [docs/06_llm_gateway/SCHEMA_VALIDATION.md](../06_llm_gateway/SCHEMA_VALIDATION.md) |
| Supplier outage or change | LLM05 | supplier policy per [AI_SUPPLIER_POLICY.md](./AI_SUPPLIER_POLICY.md); fallback model routing per [docs/06_llm_gateway/MODEL_ROUTING.md](../06_llm_gateway/MODEL_ROUTING.md) |

## Operations

1. New AI system in inventory triggers at least one risk row per applicable OWASP code.
2. High residual risks reviewed weekly until reduced.
3. Mitigation changes follow [AI_CHANGE_MANAGEMENT.md](./AI_CHANGE_MANAGEMENT.md).
4. Incidents update the register with lessons learned.

## Evidence

- Register file: `dealix-ops-private/ai_management/risk_register.yaml`.
- Mitigation links resolve to dated control documents.

## Owner & cadence

- AI Governance Lead owns the register.
- Reviewed monthly; high residuals weekly.

## AR — ملخّص

سجل المخاطر يربط كل نظام AI بمخاطره الواقعية وفق تصنيف OWASP LLM Top 10، يحدّد الاحتمال والأثر والضوابط والمخاطر المتبقية. حقن التوجيه، التهلوس، تسرّب PII، الوكالة الزائدة، فشل المزوّد — كلها لها ضوابط موثّقة. القيمة التقديرية ليست قيمة مُتحقَّقة.
