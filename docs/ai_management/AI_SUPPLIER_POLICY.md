---
title: AI Supplier Policy
owner: Founder
status: active
last_review: 2026-05-23
---

# AI Supplier Policy — سياسة موردّي الذكاء الاصطناعي

## Purpose

Define the criteria a third-party AI vendor must meet before Dealix sends any data, the review cadence, and the exit plan. Maps to NIST AI RMF "Govern" and OWASP LLM05 (supply chain).

## Vetting criteria

| Criterion | Requirement |
|---|---|
| Data handling | contractual no-training on customer data; deletion on request |
| Data residency | preference for KSA / GCC region; non-GCC requires documented justification and customer notice |
| Sub-processors | full list disclosed; changes notified in advance |
| Security posture | SOC 2 Type II or equivalent; recent third-party assessment |
| Encryption | in transit and at rest; key handling documented |
| Logging | tenant-isolated logs accessible to Dealix |
| Incident SLA | written response and notification times |
| Model lineage | versioning, deprecation notice windows |
| Pricing transparency | per-call or per-token; published rate card |
| Exit plan | data export, model output portability, off-boarding window |

## Risk-tier mapping

| Use of supplier | Required criteria met |
|---|---|
| T1 (internal drafting only, redacted inputs) | data handling, encryption, logging |
| T2 (touches client data) | all T1 + sub-processors, incident SLA, exit plan |
| T3 (influences client decision) | all T2 + residency, security posture, model lineage; Founder approval required |

## Operations

1. New supplier proposal filed by AI Governance Lead with a checklist of criteria evidence.
2. Founder approves T2 and T3 supplier adoption.
3. Annual review per supplier; reassessment triggered by any incident or material change.
4. Exit plan is rehearsed at least once per supplier per year — confirm export works, confirm a fallback model is in [docs/06_llm_gateway/MODEL_ROUTING.md](../06_llm_gateway/MODEL_ROUTING.md).

## Non-negotiables

- No client data goes to a supplier that has not been vetted at the appropriate tier.
- No "free tier" use for any T2 or T3 workflow.
- No supplier change is silent. Notice within 30 days of any sub-processor or material policy change.

## Evidence

- Supplier register: `dealix-ops-private/ai_management/suppliers.yaml`.
- Vetting evidence files attached per supplier.
- Annual review notes.

## Owner & cadence

- Founder owns supplier approval.
- AI Governance Lead maintains the register.
- Annual review; ad hoc on any change.

## AR — ملخّص

سياسة موردّي الذكاء الاصطناعي تشترط: معالجة بيانات بلا تدريب، إقامة بيانات مفضّلة في الخليج، إفصاح المعالجين الفرعيين، تشفير، تسجيلات معزولة، SLA حوادث، شفافية تسعير، وخطّة خروج. T3 تحتاج موافقة المؤسس ومراجعة سنوية وتدريب على الخروج. القيمة التقديرية ليست قيمة مُتحقَّقة.
