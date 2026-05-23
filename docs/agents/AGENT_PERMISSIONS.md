---
title: Agent Permissions
owner: AI Governance Lead
status: active
last_review: 2026-05-23
---

# Agent Permissions — صلاحيات الوكلاء

## Purpose

Declare what each agent can read, write, and execute, and map those capabilities to autonomy bands. The default for every permission is deny. Explicit allow rows are the only way capability is granted.

## Permission shape

```yaml
agent_id: AGT-NNN
read:
  - data_class: e.g. client_briefs, internal_docs, public_corpus
    scope: e.g. own-client only, all
write:
  - artifact: e.g. proposal_draft, sample_summary_draft
    destination: e.g. dealix-ops-private/drafts/
execute:
  - tool_id: e.g. schema_validator, file_writer
    constraints: e.g. max_calls_per_run, max_tokens
external_send: false  # MVP rule
data_export: false    # MVP rule
notes:
  - "Permissions follow Agent Control Protocol clauses 1–5."
```

## Autonomy band mapping

| Band | Read | Write | Execute | External |
|---|---|---|---|---|
| A1 | yes (scoped) | drafts to private path | safe utilities | no |
| A2 | yes (scoped) | drafts queued for approval | tools required for drafting | no |
| A3 | yes (scoped) | execute approved internal artifact | approved tools only, post-action audit | no |
| A4+ | n/a | n/a | n/a | forbidden in MVP |

## Standard restrictions (apply to every agent)

- No reading of unredacted PII; redaction per [docs/06_llm_gateway/REDACTION_POLICY.md](../06_llm_gateway/REDACTION_POLICY.md).
- No writing to public repositories; output paths are private until approval.
- No executing shell commands beyond an allow list.
- No invoking another agent without an explicit handoff row per [AGENT_HANDOFFS.md](./AGENT_HANDOFFS.md).
- No widening of permissions at runtime.

## Operations

1. Permission rows live in `dealix-ops-private/ai_management/agent_permissions.yaml`.
2. Any widening (read, write, execute) requires a PR and gate per [docs/ai_management/AI_AGENT_RELEASE_GATE.md](../ai_management/AI_AGENT_RELEASE_GATE.md).
3. Quarterly review: each owner re-attests the permissions match purpose.
4. A permission breach attempt is logged and triggers an audit per [AGENT_LOGGING.md](./AGENT_LOGGING.md) and [docs/ai_management/AI_INCIDENT_RESPONSE.md](../ai_management/AI_INCIDENT_RESPONSE.md).

## Non-negotiables

- `external_send: true` is impossible in MVP — enforced at the gateway, not just by policy.
- `data_export: true` is impossible without founder approval and a contract clause permitting it.
- No agent inherits permissions from another implicitly.

## Evidence

- Permissions file under version control.
- Audit log for any widening or breach attempt.

## Owner & cadence

- AI Governance Lead owns the file.
- Quarterly re-attestation; per-PR on changes.

## AR — ملخّص

الصلاحيات تُعلَن صراحة (قراءة، كتابة، تنفيذ)، والافتراضي هو المنع. كل وكيل في MVP بنطاق A1–A3، بلا إرسال خارجي ولا تصدير بيانات، مع تطبيق على مستوى البوّابة لا السياسة فقط. أي توسيع يحتاج PR وبوّابة إطلاق. القيمة التقديرية ليست قيمة مُتحقَّقة.
