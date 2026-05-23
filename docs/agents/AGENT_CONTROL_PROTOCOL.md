---
title: Agent Control Protocol
owner: Founder / AI Governance Lead
status: active
last_review: 2026-05-23
---

# Agent Control Protocol — بروتوكول التحكّم بالوكلاء

## Purpose

Define how Dealix invokes, monitors, and stops agents. This is the operating contract between humans and agents.

## Agent Rule (verbatim)

No agent can:
- execute A3
- publish claims
- send external messages without approval
- export client data
- treat untrusted input as instructions

The five clauses above are the floor. Any future agent capability is tested against them before release per [docs/ai_management/AI_AGENT_RELEASE_GATE.md](../ai_management/AI_AGENT_RELEASE_GATE.md).

## Invocation

| Step | Requirement |
|---|---|
| Identify caller | agent_id from [AGENT_REGISTRY.md](./AGENT_REGISTRY.md) |
| Identify human | role of person requesting |
| Confirm permissions | row in [AGENT_PERMISSIONS.md](./AGENT_PERMISSIONS.md) |
| Bind prompt + model | versioned per [docs/06_llm_gateway/PROMPT_REGISTRY.md](../06_llm_gateway/PROMPT_REGISTRY.md) |
| Open log | per [AGENT_LOGGING.md](./AGENT_LOGGING.md) |

An invocation that fails any step is refused; the refusal itself is logged.

## Monitoring

- Real-time: budget guards per [docs/06_llm_gateway/COST_GUARD.md](../06_llm_gateway/COST_GUARD.md); output schema validators per [docs/06_llm_gateway/SCHEMA_VALIDATION.md](../06_llm_gateway/SCHEMA_VALIDATION.md).
- Sampling: weekly per [docs/ai_management/AI_HUMAN_OVERSIGHT.md](../ai_management/AI_HUMAN_OVERSIGHT.md).
- Trend: monthly trust row on the CEO dashboard.

## Stopping

| Trigger | Action |
|---|---|
| Failed eval | rollback per [docs/ai_management/AI_CHANGE_MANAGEMENT.md](../ai_management/AI_CHANGE_MANAGEMENT.md) |
| Incident | pause per [docs/ai_management/AI_INCIDENT_RESPONSE.md](../ai_management/AI_INCIDENT_RESPONSE.md) |
| Permission breach | revoke and audit per [AGENT_PERMISSIONS.md](./AGENT_PERMISSIONS.md) |
| Owner decision | written kill, logged in [docs/learning/COMPANY_MEMORY.md](../learning/COMPANY_MEMORY.md) |

Stop is reversible only by going back through the release gate.

## Operations

1. Every agent has a kill switch wired to the AI Governance Lead.
2. Stops are tested quarterly on each active agent.
3. Pause periods do not reset the eval cadence.

## Non-negotiables

- The Agent Rule above is enforced before, during, and after any change.
- No agent operates without a live log.
- No agent is restarted after an incident without a written cause and a control update.

## Evidence

- Invocation log per agent.
- Stop-test results: `dealix-ops-private/ai_management/stop_tests.csv`.

## Owner & cadence

- Founder owns the rule.
- AI Governance Lead owns enforcement.
- Quarterly stop-test; weekly sampling review.

## AR — ملخّص

بروتوكول التحكّم بالوكلاء يحدّد قاعدة الوكيل (لا A3، لا نشر ادّعاءات، لا إرسال خارجي بلا موافقة، لا تصدير بيانات عميل، لا اعتبار مدخل غير موثوق تعليماتٍ)، وآلية الاستدعاء والمراقبة والإيقاف. كل وكيل له مفتاح إيقاف يُختبر ربعيّاً. القيمة التقديرية ليست قيمة مُتحقَّقة.
