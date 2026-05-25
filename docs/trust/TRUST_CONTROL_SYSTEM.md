---
title: Trust Control System
owner: Trust Lead
status: active
last_review: 2026-05-23
---

# Trust Control System — نظام ضوابط الثقة

## Purpose

The actual controls that prevent unsafe behavior. Each control has a name, a trigger, an action, and an evidence artifact. If a control is not listed here, it does not exist.

## Control inventory

| ID | Control | Trigger | Action | Evidence |
|---|---|---|---|---|
| C-01 | PII redaction | Any text entering LLM gateway | Strip name, phone, email, national ID | `ai_run_ledger.redaction_log` |
| C-02 | Approval gate A1 | Outbound proposal, refund < 1,500 SAR | Founder click-approve in queue | `approvals/AYYYY-NNN.md` |
| C-03 | Approval gate A2 | Contract signature, refund 1,500–10,000 SAR, public claim | Founder written approval + counter-sign | `approvals/AYYYY-NNN.md` |
| C-04 | Approval gate A3 | Regulator comms, data export, legal filing, revenue claim | Founder + Trust Lead, never auto-executed | `approvals/AYYYY-NNN.md` |
| C-05 | Audit log | Every agent action | Append to `ai_run_ledger` (immutable) | `ai_run_ledger.jsonl` |
| C-06 | Kill switch | Any agent fails schema 3× in 10 min | Halt agent, page founder | `incidents/INC-NNN.md` |
| C-07 | Claim filter | Any draft containing banned phrase | Block, route to rewrite | `claim_filter.log` |
| C-08 | Scope gate | Delivery item outside signed scope | Reject, route to change request | `delivery/scope_rejections/` |
| C-09 | Public commit scan | Pre-commit hook on public repo | Scan for client names, secrets, PII | `pre_commit.log` |
| C-10 | Source provenance | Every lead in deliverable | Must have URL + retrieval timestamp | `lead_table.source_url` |

## Operational steps

1. Every new agent or workflow must map to at least one control before it ships.
2. Controls are tested monthly via [AUDIT_POLICY.md](./AUDIT_POLICY.md).
3. A control without recent evidence is treated as broken until proven otherwise.

## Cross-links

- [APPROVAL_MATRIX.md](./APPROVAL_MATRIX.md) — A0/A1/A2/A3 levels in detail.
- [AUTONOMY_POLICY.md](./AUTONOMY_POLICY.md) — what agents may run alone.
- [EVIDENCE_SYSTEM.md](./EVIDENCE_SYSTEM.md) — what counts as evidence.
- [docs/06_llm_gateway/REDACTION_POLICY.md](../06_llm_gateway/REDACTION_POLICY.md) — redaction implementation.

## Owner & cadence

- Trust Lead owns the inventory.
- Reviewed monthly; every control gets one live test per quarter.

## AR — ملخّص

نظام الضوابط يسرد كل ضابط أمان فعلي مع المُحفّز والإجراء والدليل. أي سلوك لا يربط بضابط لا يُسمح بإطلاقه. تُختبر الضوابط شهريًا، والضابط بلا دليل حديث يُعتبر معطّلًا حتى يُثبت العكس. القيمة التقديرية ليست قيمة مُتحقَّقة.
