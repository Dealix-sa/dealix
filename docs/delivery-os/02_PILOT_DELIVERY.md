# Pilot Delivery — تسليم التجربة الموجّهة

The Pilot tier (SAR 5,000–25,000). A time-boxed, scoped engagement that turns one diagnostic finding into a working, governed draft pipeline the client can see operating. The Pilot proves the motion on real client data inside one workflow.

التجربة الموجّهة عرض محدد المدة والنطاق، يحوّل أحد نتائج التشخيص إلى مسار عملي مُحوكَم يراه العميل وهو يعمل.

## Inputs — المدخلات

- A signed Pilot scope referencing a specific diagnostic finding.
- The single workflow to be piloted (e.g., inbound lead triage, draft generation for one outreach segment).
- Client-owned data for that workflow, with a completed Source Passport.
- A named client-side owner who will review drafts.

## Outputs — المخرجات

- A governed draft pipeline: AI drafts and ranks; the client owner and founder review.
- A run ledger showing every draft, its rank, and its approval state. See [06_llm_gateway/AI_RUN_LEDGER.md](../06_llm_gateway/AI_RUN_LEDGER.md).
- An evidenced-results summary at Pilot close, labeled Estimated/Observed.
- A Department OS or Retainer proposal sized to observed Pilot patterns.

## Timeline — الجدول الزمني

- Standard Pilot: 2–4 weeks.
- Week 1: setup, Source Passport, first drafts.
- Weeks 2–3: review loop and tuning.
- Final week: results summary and handover.

## Acceptance criteria — معايير القبول

Delivered only when: the draft pipeline produced reviewed output for the agreed workflow; the run ledger is complete; the results summary is approved and sent; and the engagement is set to `pilot_delivered`.

## Human approval boundary — حدود الموافقة البشرية

Every draft is reviewed before any external use. The system never sends to the client's prospects or customers. If the Pilot involves outreach drafts, the client sends them manually after their own approval — Dealix does not send on their behalf.

## Security boundary — حدود الأمان

Data is scoped to the piloted workflow only. PII is classified and minimized per [04_data_os/PII_CLASSIFICATION.md](../04_data_os/PII_CLASSIFICATION.md). Retention and deletion follow the signed scope and [04_data_os/DATA_RETENTION_POLICY.md](../04_data_os/DATA_RETENTION_POLICY.md).

## Handover — التسليم

Bilingual results summary, the run ledger export, the tuned configuration for the workflow, and explicit limitations. Template: [06_HANDOVER_TEMPLATE.md](06_HANDOVER_TEMPLATE.md).

## Upsell path — مسار الترقية

Pilot → Department OS (productionize the workflow at department scale) or Pilot → Retainer (keep operating the piloted workflow monthly). The choice depends on whether the client wants a built system or an operated one. See [07_EXPANSION_PLAYBOOK.md](07_EXPANSION_PLAYBOOK.md).

## Retainer trigger — مُحفِّز الاشتراك الشهري

A Pilot triggers a Retainer conversation when: the workflow is recurring, the client lacks internal capacity to run the review loop, and observed Pilot value justifies a monthly fee. The trigger is a documented recommendation, not an automatic enrollment.

## Client success metrics — مقاييس نجاح العميل

- Drafts generated vs. drafts approved (review yield).
- Cycle time from intake to approved draft.
- Observed value on the piloted workflow (Estimated → Observed labeling).
- Pilot-to-next-tier conversion (tracked, never promised).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
