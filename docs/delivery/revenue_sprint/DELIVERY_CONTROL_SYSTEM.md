---
title: Delivery Control System
owner: Delivery Lead
status: active
last_review: 2026-05-23
---

# Delivery Control System — نظام ضوابط التسليم

## Purpose

The controls that guard the sprint deliverable. Each control has a trigger, an action, and evidence. A deliverable that has not passed every control does not ship.

## Controls

| ID | Control | Trigger | Action | Evidence |
|---|---|---|---|---|
| D-01 | Scope match | Intake to deliverable comparison | Every output mapped to a scope item; out-of-scope items flagged | `qa_log.scope_check` |
| D-02 | Lead evidence | Every row in the lead table | Public source URL + retrieval timestamp present | `lead_table.source_url`, `lead_table.retrieved_at` |
| D-03 | PII filter | Any text in deliverable | No personal phone, personal email, or national ID | `claim_filter.log` |
| D-04 | QA gate | Pre-handover | [QA_CHECKLIST.md](./QA_CHECKLIST.md) signed off | `qa_log.qa_passed` |
| D-05 | No-overclaim | Any narrative text | Run against [docs/trust/NO_OVERCLAIM_POLICY.md](../../trust/NO_OVERCLAIM_POLICY.md) | `claim_filter.log` |
| D-06 | Approval log | Pre-handover send | A1 approval recorded | `approvals/AYYYY-NNN.md` |
| D-07 | Schema validation | Lead table | Matches [LEAD_TABLE_SCHEMA.md](./LEAD_TABLE_SCHEMA.md) | `schema_validation.log` |
| D-08 | Source diversity | Lead table | No single source > 50% of rows; flag if so | `qa_log.source_diversity` |
| D-09 | Language pass | All text | Arabic + English present and parallel | `qa_log.bilingual` |
| D-10 | Estimated-value disclaimer | Report | "Estimated value is not Verified value" line present | `qa_log.disclaimer_present` |

## Operational steps

1. Controls run in order during stages 6–7 of the factory.
2. Any control failure routes to rework, not exception.
3. Three consecutive sprints failing the same control trigger a structural fix in the playbook.

## Bypass policy

- D-01 through D-10 may not be bypassed.
- Time pressure is not a valid reason; an SLA slip is preferable to a control failure.

## Cross-links

- [REVENUE_SPRINT_FACTORY.md](./REVENUE_SPRINT_FACTORY.md)
- [QA_CHECKLIST.md](./QA_CHECKLIST.md)
- [docs/trust/TRUST_CONTROL_SYSTEM.md](../../trust/TRUST_CONTROL_SYSTEM.md)
- [docs/trust/EVIDENCE_SYSTEM.md](../../trust/EVIDENCE_SYSTEM.md)

## Owner & cadence

- Delivery Lead. Reviewed monthly with the sprint cohort.

## AR — ملخّص

نظام ضوابط التسليم عشرة ضوابط تحرس المنتج: مطابقة النطاق، إسناد المصدر، فلتر بيانات شخصية، بوّابة جودة، عدم مبالغة، سجل موافقات، تحقّق مخطط، تنوّع مصادر، توازي اللغتين، وجود إقرار القيمة التقديرية. أي إخفاق يُحال إلى إعادة عمل لا إلى استثناء، وضغط الوقت ليس عذرًا. القيمة التقديرية ليست قيمة مُتحقَّقة.
