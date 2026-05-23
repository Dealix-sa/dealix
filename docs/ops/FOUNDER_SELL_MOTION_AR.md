# آلة البيع — أيام 1–3 (مؤسس فقط)

## ديمو 12 دقيقة

1. شغّل `bash scripts/run_business_now.sh`
2. افتح `/ar/business-now#strategy`
3. simulate (قطاع / مدينة / ميزانية)
4. اعرض **focus** بصدق (غالباً kpi_hygiene حتى تعبئة CRM)
5. GTM أول 10 · Sales Script · Proof demo
6. اختم: **Governed Revenue Ops Diagnostic** — لا المنصة كاملة

مرجع: [dealix_ops_runbook_ar.md](../commercial/ops_client_pack/dealix_ops_runbook_ar.md)

## 5 جهات دافئة (يوم 2–3)

- قائمة من [WARM_LIST_WORKFLOW.md](../sales-kit/WARM_LIST_WORKFLOW.md)
- قبل أي مسودة: `POST /api/v1/revenue-os/anti-waste/check`
- إرسال **يدوي فقط** بعد `founder_confirmed=true`

## تصنيف الردود

| التصنيف | الإجراء |
| --- | --- |
| interested | أرسل Diagnostic Scope + موعد |
| objection | سجّل الاعتراض — استخدم dealix-sales لمسودة رد |
| wrong_segment | أرشف — لا متابعة |
| referral | شكر + طلب warm intro |
| silence | متابعة واحدة بعد 5 أيام — لا spam |

## قواعد عدم الهزل

- لا revenue قبل `invoice_paid`
- لا واتساب بارد / لا LinkedIn تلقائي
- أي score تجريبي: `is_estimate: true`

## وكيل Cursor

استخدم **dealix-sales** مع القالب في [FOUNDER_AGENT_PLAYBOOK_AR.md](FOUNDER_AGENT_PLAYBOOK_AR.md)

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
