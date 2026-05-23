---
title: Agent Logging
owner: AI Governance Lead
status: active
last_review: 2026-05-23
---

# Agent Logging — تسجيلات الوكلاء

## Purpose

Define what every agent must log on every run, where the logs live, and how long they are kept. Without logs, there is no audit, no eval, no incident response. Logging is not optional.

## Mandatory log fields

```yaml
run_id: ULID
agent_id: AGT-NNN
agent_version: vX
prompt_version: PRM-NNN-vX
model_id: provider/model@version
caller: human role or upstream agent_id
inputs:
  - input_id: file or message reference
  - inputs_redacted: true
tools_called:
  - tool_id: ...
    args_hash: sha256
    result_hash: sha256
outputs:
  - output_id: artifact id
    schema_validated: true | false
decisions:
  - one sentence each, with rationale
evidence_links: [paths]
approvals:
  - approver: role
    timestamp: ISO 8601
    artifact: output_id
refusals:
  - reason: code
cost:
  tokens_in: n
  tokens_out: n
  estimated_sar: amount
duration_ms: n
timestamp_start: ISO 8601
timestamp_end: ISO 8601
```

## Where logs live

- Runtime: structured JSON lines to the LLM gateway sink — see [docs/06_llm_gateway/AI_RUN_LEDGER.md](../06_llm_gateway/AI_RUN_LEDGER.md).
- Long-term: aggregated daily into `dealix-ops-private/ai_management/run_logs/YYYY-MM-DD.jsonl`.
- Retention: 24 months minimum; permanent for any run linked to a client artifact, an incident, or a release gate.

## Redaction discipline

- PII is redacted before logging per [docs/06_llm_gateway/REDACTION_POLICY.md](../06_llm_gateway/REDACTION_POLICY.md).
- Hashes are stored for tool args and results so equivalence can be checked without storing payloads.
- Sensitive client content is referenced by ID, not embedded.

## What must always appear

- Inputs and outputs, even when empty (record the empty).
- Tool calls and refusals.
- Approvals attached to the run that produced the approved artifact.
- The decision sentence(s) the agent made — explicit, not implicit.

## Operations

1. Logging failure is a SEV-2 incident per [docs/ai_management/AI_INCIDENT_RESPONSE.md](../ai_management/AI_INCIDENT_RESPONSE.md). The agent is paused until logs resume.
2. Weekly sampling reads logs, not summaries.
3. Logs feed evals via captured task examples.

## Non-negotiables

- No agent runs without logging on.
- No log line carries unredacted PII.
- No retroactive log editing — corrections are appended.

## Evidence

- Daily aggregated log files.
- Linked from incident files, release gates, and eval results.

## Owner & cadence

- AI Governance Lead owns the schema.
- Reviewed quarterly; on every gateway change.

## AR — ملخّص

تسجيلات الوكلاء إلزامية على كل تشغيل: هوية الوكيل، نسخة الموجّه، النموذج، المدخلات (منقّحة)، استدعاءات الأدوات، المخرجات، القرارات، الموافقات، الرفض، التكلفة. الاحتفاظ 24 شهراً أو دائم عند ارتباط بعمل عميل أو حادث. أي خلل تسجيلي يوقف الوكيل. القيمة التقديرية ليست قيمة مُتحقَّقة.
