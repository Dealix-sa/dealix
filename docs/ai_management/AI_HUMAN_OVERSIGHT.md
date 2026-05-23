---
title: AI Human Oversight
owner: Founder
status: active
last_review: 2026-05-23
---

# AI Human Oversight — الإشراف البشري على الذكاء الاصطناعي

## Purpose

Define where a human must approve, where a human samples, and where an AI may act without per-instance review. Maps to NIST AI RMF "Manage" function and the agent autonomy levels in [docs/agentic_operations/AGENT_OPERATING_LEVELS.md](../agentic_operations/AGENT_OPERATING_LEVELS.md).

## Autonomy bands (Dealix mapping)

| Band | Description | Oversight |
|---|---|---|
| A1 | Drafting / analysis only, internal | 10% sampling, weekly review |
| A2 | Recommendation queued for approval | per-instance approval before action |
| A3 | Internal execution after approval | per-instance approval + post-action audit |
| A4+ | External action / autonomous external | forbidden in MVP |

A4+ is listed for completeness; see [docs/agents/AGENT_PERMISSIONS.md](../agents/AGENT_PERMISSIONS.md) for the enforcement rule.

## Where a human must approve

| Action | Required approver | Reference |
|---|---|---|
| Sending any external message | Founder | [docs/05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md), [docs/05_governance_os/CHANNEL_POLICY.md](../05_governance_os/CHANNEL_POLICY.md) |
| Publishing any external claim | Founder | [docs/05_governance_os/CLAIM_SAFETY.md](../05_governance_os/CLAIM_SAFETY.md) |
| Releasing a new or changed agent | Founder | [AI_AGENT_RELEASE_GATE.md](./AI_AGENT_RELEASE_GATE.md) |
| Adopting a new AI supplier | Founder | [AI_SUPPLIER_POLICY.md](./AI_SUPPLIER_POLICY.md) |
| Exporting client data into an AI tool | Founder | [docs/04_data_os/ALLOWED_USE_POLICY.md](../04_data_os/ALLOWED_USE_POLICY.md) |

## Sampling for A1

- 10% of A1 outputs are human-reviewed weekly.
- Sampling is random across systems and not weighted to easy cases.
- Findings feed [AI_RISK_REGISTER.md](./AI_RISK_REGISTER.md) when novel.

## Operations

1. A2/A3 actions sit in a visible approval queue; queue depth is on the dashboard.
2. Approval includes the approver name, timestamp, and the artifact reviewed.
3. Post-action audit on A3 happens within 7 days of action.
4. Approval cannot be delegated to an AI.

## Non-negotiables

- No external action by any AI system without explicit human approval.
- No bulk approval. One artifact per approval entry.
- No silent override of a refusal by an AI system.

## Evidence

- Approval queue: `dealix-ops-private/ai_management/approvals.csv`.
- Sampling log: `dealix-ops-private/ai_management/sampling.csv`.

## Owner & cadence

- Founder owns approvals.
- AI Governance Lead owns the sampling discipline.
- Reviewed weekly at the trust ritual.

## AR — ملخّص

الإشراف البشري يحدّد ثلاث نطاقات: A1 مع عيّنات 10%، A2 موافقة لكل توصية، A3 موافقة قبل وتدقيق بعد. أي إجراء خارجي يحتاج موافقة المؤسس، ولا تفويض لذكاء اصطناعي. لا موافقة جماعية. القيمة التقديرية ليست قيمة مُتحقَّقة.
