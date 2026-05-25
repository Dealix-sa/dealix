---
title: Agent Handoffs
owner: AI Governance Lead
status: active
last_review: 2026-05-23
---

# Agent Handoffs — تسليمات الوكلاء

## Purpose

Define how work moves between agents, and between any agent and the founder. The handoff contract makes ownership unambiguous at every step.

## Handoff contract

```yaml
handoff_id: HO-YYYY-NNN
from: AGT-NNN or human role
to: AGT-NNN or human role
artifact: file path or queue id
inputs_referenced: [ids]
decisions_taken: [one sentence each]
evidence_attached: [paths]
open_questions: [explicit]
approval_required: yes | no
deadline: YYYY-MM-DD
timestamp: ISO 8601
```

A handoff with a missing field is invalid. The receiving party may refuse it.

## Allowed handoff edges

| From | To | Notes |
|---|---|---|
| Sales agent | Founder | for proposal approval |
| Content agent | Founder | for case-safe summary approval |
| Delivery agent | Delivery Lead | for proof pack review |
| Engineer agent | Engineer (human) | for code review |
| PM agent | Founder | for weekly review draft |
| Any agent | AI Governance Lead | on refusal or incident |
| Founder | any agent | as task assignment |

Agent-to-agent handoffs are allowed only when both rows exist in [AGENT_REGISTRY.md](./AGENT_REGISTRY.md) and the edge is explicitly enumerated above.

## Back-to-founder rule

Any of the following force a back-to-founder handoff:

- Refusal triggered by [AGENT_CONTROL_PROTOCOL.md](./AGENT_CONTROL_PROTOCOL.md).
- Out-of-scope request.
- Detected attempt to bypass approval queue or permissions.
- Uncertainty above an agent-defined threshold on a high-stakes artifact.

## Operations

1. Handoff records are written to `dealix-ops-private/ai_management/handoffs.csv`.
2. Receiving party signs the handoff (acceptance) or returns it with reason.
3. Open handoffs are visible to the Founder in the approval queue widget on the dashboard.

## Non-negotiables

- No handoff without all schema fields.
- No agent-to-agent handoff that bypasses a required human approval.
- No silent acceptance — every handoff resolves to accept or return.

## Evidence

- Handoff records with timestamps.
- Linked artifact files.

## Owner & cadence

- AI Governance Lead owns the contract.
- Reviewed monthly.

## AR — ملخّص

تسليمات الوكلاء تتبع عقداً موحّداً: من، إلى، مخرج، مدخلات، قرارات، أدلّة، أسئلة مفتوحة، حاجة موافقة، موعد. حواف التسليم المسموحة محصورة، والعودة للمؤسس إجبارية عند الرفض أو الغموض أو محاولة تجاوز. لا تسليم صامت. القيمة التقديرية ليست قيمة مُتحقَّقة.
