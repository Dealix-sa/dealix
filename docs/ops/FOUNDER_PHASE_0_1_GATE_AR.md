# بوابة المرحلة 0–1 — أول Diagnostic مدفوع + Proof Pack

**الغرض:** صمام أمان قبل توسيع المنتج أو الفريق — يتماشى مع [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md).

---

## متى تُفتح البوابة (PASS)

| شرط | مصدر |
|-----|------|
| `payment_received` حقيقي (شركة حقيقية) | [evidence_events_tracker.csv](../commercial/operations/evidence_events_tracker.csv) |
| `proof_pack_delivered` حقيقي | نفس السجل |
| KPI غير placeholder | `dealix/transformation/kpi_founder_commercial_import.yaml` |

**تحقق:**

```bash
py -3 scripts/founder_comprehensive_plan_status.py --section phase
py -3 scripts/verify_first_paid_diagnostic_tracker.py
```

---

## عند BLOCKED

1. أغلق مسار إغلاق واحد — [EVIDENCE_EVENTS_CLOSE_PATH_AR.md](../commercial/operations/EVIDENCE_EVENTS_CLOSE_PATH_AR.md)
2. DoD تسليم — [FIRST_PAID_DIAGNOSTIC_DOD_AR.md](../commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md)
3. دفع يدوي — [MANUAL_PAYMENT_SOP.md](MANUAL_PAYMENT_SOP.md)

**ممنوع حتى PASS:** بناء ميزات جديدة · توظيف مبيعات تقليدية · ادعاء «إيراد live» في التسويق.

---

*آخر تحديث: 2026-05-18*

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
