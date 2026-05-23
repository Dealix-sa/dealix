---
title: AI Incident Response
owner: Founder
status: active
last_review: 2026-05-23
---

# AI Incident Response — الاستجابة لحوادث الذكاء الاصطناعي

## Purpose

Define what counts as an AI incident, who is on the response team, the timelines, and the post-incident output. Complements the general [docs/trust/INCIDENT_RESPONSE.md](../trust/INCIDENT_RESPONSE.md) where it exists.

## AI-specific incident types

| Type | Description |
|---|---|
| Jailbreak | a prompt successfully bypassed system policy |
| Prompt injection | external content was treated as instructions |
| Hallucinated claim | an output stated a non-verified claim as fact |
| Data leakage | client data appeared in an output it should not |
| Unauthorized external send | an external message left the system without approval |
| Excessive agency | an agent took an action outside its permission scope |
| Supplier outage / change | upstream model provider failed or changed silently |

## Severity ladder

| Severity | Trigger | Response time |
|---|---|---|
| SEV-1 | client harm or data exposure | response start < 1 hour, written update < 4 hours |
| SEV-2 | external send without approval, hallucinated claim shipped | response start < 4 hours, written update < 24 hours |
| SEV-3 | internal-only incident, contained | response start < 24 hours, written update < 72 hours |

## Response steps

1. **Contain** — pause the affected system or agent.
2. **Preserve** — snapshot inputs, outputs, prompts, model versions, run ledger entries.
3. **Notify** — Founder for any SEV-1 or SEV-2; client notification follows [docs/05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md) and contract terms.
4. **Mitigate** — apply rollback per [AI_CHANGE_MANAGEMENT.md](./AI_CHANGE_MANAGEMENT.md) or temporary policy.
5. **Investigate** — root cause within the severity timeline.
6. **Document** — incident file: `dealix-ops-private/incidents/AI-YYYY-NNN.md`.
7. **Update register** — add or update rows in [AI_RISK_REGISTER.md](./AI_RISK_REGISTER.md).
8. **Close** — closure requires founder sign-off and a written lesson.

## Non-negotiables

- No incident is closed without a written root cause and a control update.
- No incident is hidden from a client whose data was affected.
- No SEV-1 response is delegated.

## Evidence

- Incident files in private ops repo.
- Cross-link to the run ledger entries and eval results.
- Monthly aggregate count on the CEO dashboard trust row.

## Owner & cadence

- Founder owns SEV-1 and SEV-2 response.
- AI Governance Lead owns SEV-3 and the post-incident registry update.
- Reviewed monthly; trend analysis quarterly.

## AR — ملخّص

الاستجابة لحوادث الذكاء الاصطناعي تحدّد سبعة أنواع (jailbreak، حقن، تهلوس، تسرّب، إرسال خارجي غير مصرّح به، وكالة زائدة، فشل مزوّد) وثلاثة مستويات للخطورة بزمن استجابة محدّد. الخطوات: احتواء، حفظ، إبلاغ، تخفيف، تحقيق، توثيق، تحديث السجل، إغلاق بدرس. القيمة التقديرية ليست قيمة مُتحقَّقة.
