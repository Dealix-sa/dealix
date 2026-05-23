---
title: Delivery Playbook
owner: Delivery Lead
status: active
last_review: 2026-05-23
---

# Delivery Playbook — كتيب التسليم

## Purpose

A step-by-step playbook the Delivery Lead follows for one sprint, from paid invoice to evidence-pack archive. Read top to bottom. Skip nothing.

## Day 0 — Paid invoice received

1. Confirm payment in bank ([docs/revenue/CASH_RULES.md](../../revenue/CASH_RULES.md)).
2. Open the sprint folder: `dealix-ops-private/sprints/<sprint_id>/`.
3. Send the intake form via approved email template.
4. Book the handover review slot 5–7 business days out.

## Day 1 — Intake and source plan

1. Confirm intake completeness ([CLIENT_INTAKE.md](./CLIENT_INTAKE.md)).
2. If decision-maker is absent or ICP is vague, request a 20-min clarification call before proceeding.
3. Draft the source plan: which public sources, which queries.
4. Save plan to sprint folder.

## Day 2–3 — Lead surfacing and scoring

1. Run lead surfacing agent against the source plan.
2. Capture raw output to sprint folder.
3. Validate the lead table against [LEAD_TABLE_SCHEMA.md](./LEAD_TABLE_SCHEMA.md).
4. Score each row per [SCORING_RULES.md](./SCORING_RULES.md).
5. Mark the top 5–10 prioritized.

## Day 3–4 — Next-step pack

1. Pull templates from [OUTREACH_PACK_TEMPLATE.md](./OUTREACH_PACK_TEMPLATE.md).
2. Tailor to the buyer's sector and ICP.
3. Produce both Arabic and English versions.

## Day 4–5 — QA and report assembly

1. Run [QA_CHECKLIST.md](./QA_CHECKLIST.md).
2. Address any rework items.
3. Assemble the report per [REPORT_TEMPLATE.md](./REPORT_TEMPLATE.md).
4. Submit A1 approval request to founder.

## Day 5–6 — Handover

1. On A1 approval, send pre-read 24 hours before the call.
2. Conduct 30-minute handover review.
3. Capture written feedback during or immediately after.
4. Use [HANDOFF_TEMPLATE.md](./HANDOFF_TEMPLATE.md).

## Day 6–7 — Evidence pack and case capture

1. Archive the evidence pack ([docs/trust/EVIDENCE_SYSTEM.md](../../trust/EVIDENCE_SYSTEM.md)).
2. Request consent for case-safe capture per [CASE_STUDY_CAPTURE.md](./CASE_STUDY_CAPTURE.md).
3. Update the revenue log row.
4. Schedule the retainer conversation if buyer expressed continued need.

## What to do if something breaks

- Stage SLA slip: log, notify founder by EoD.
- Control failure (D-01 to D-10): rework, do not ship.
- Data exposure or PII leak: open an incident per [docs/trust/INCIDENT_RESPONSE.md](../../trust/INCIDENT_RESPONSE.md).

## Cross-links

- [REVENUE_SPRINT_FACTORY.md](./REVENUE_SPRINT_FACTORY.md)
- [DELIVERY_CONTROL_SYSTEM.md](./DELIVERY_CONTROL_SYSTEM.md)
- [CLIENT_INTAKE.md](./CLIENT_INTAKE.md)
- [docs/delivery/DELIVERY_LIFECYCLE.md](../DELIVERY_LIFECYCLE.md)

## Owner & cadence

- Delivery Lead. Updated whenever the factory changes.

## AR — ملخّص

كتيب يومي للمرحلة الواحدة: يوم الفاتورة تأكيد الدفع وإرسال نموذج الاستلام، يوم 1 خطّة مصادر، يومان 2–3 استكشاف وتسجيل، يومان 3–4 حزمة الخطوة التالية، يومان 4–5 جودة وتجميع التقرير وموافقة A1، يومان 5–6 مراجعة التسليم 30 دقيقة، يومان 6–7 حزمة الأدلة والتقاط القصة. الانزلاق يُبلَّغ، وإخفاق الضابط يُعاد العمل، وتسرّب البيانات يفتح حادثة. القيمة التقديرية ليست قيمة مُتحقَّقة.
