# الخطة الرئيسية للتدشين التجاري — Dealix

> **الحالة الحاكمة الحالية — Current governing state (2026-05-18):** المشروع
> تحت **تجميد تجاري نشط** ([`ops/COMMERCIAL_FREEZE.md`](ops/COMMERCIAL_FREEZE.md)).
> المنصة جاهزة؛ القيد هو البيع بقيادة المؤسس وتفعيل الدفع، لا الكود. **المسار
> الحرج الوحيد** الآن = أول Pilot مدفوع مُسلَّم + Proof Pack موافق عليه (L3+)،
> والعائق #1 هو تفعيل Moyasar ([`ops/MOYASAR_KYC_CHECKLIST.md`](ops/MOYASAR_KYC_CHECKLIST.md)).
> المراحل التسعة أدناه تبقى مرجعاً؛ لا تُستأنف الدرجات 2–5 إلا بعد الخروج من
> التجميد، وعندها يحكم [`90_DAY_BUSINESS_EXECUTION_PLAN.md`](90_DAY_BUSINESS_EXECUTION_PLAN.md).
> The 9 phases below remain a reference — the freeze and the first-paid-pilot
> critical path take precedence until the freeze exits.

**خطة إكمال شاملة (عربي — دمج + CI + نشر + Level 1 + أول إيراد):** [COMPREHENSIVE_COMPLETION_PLAN_AR.md](COMPREHENSIVE_COMPLETION_PLAN_AR.md)

## المراحل

1. **Post-merge verification** — [`POST_MERGE_VERIFICATION.md`](POST_MERGE_VERIFICATION.md)
2. **Staging** — [`STAGING_DEPLOYMENT.md`](STAGING_DEPLOYMENT.md) + `scripts/smoke_staging.py`
3. **Compliance baseline** — [`DATA_MAP.md`](DATA_MAP.md)، [`PRIVACY_PDPL_READINESS.md`](PRIVACY_PDPL_READINESS.md)، DPA pilot
4. **Observability + evals** — [`OBSERVABILITY_ENV.md`](OBSERVABILITY_ENV.md)، [`EVALS_RUNBOOK.md`](EVALS_RUNBOOK.md)
5. **WhatsApp beta** — [`WHATSAPP_OPERATOR_FLOW.md`](WHATSAPP_OPERATOR_FLOW.md)، [`WHATSAPP_PRODUCTION_CUTOVER.md`](WHATSAPP_PRODUCTION_CUTOVER.md)
6. **Billing** — [`BILLING_RUNBOOK.md`](BILLING_RUNBOOK.md)
7. **Private beta** — [`PRIVATE_BETA_RUNBOOK.md`](PRIVATE_BETA_RUNBOOK.md)
8. **Paid beta metrics** — [`PAID_BETA_SCORECARD.md`](PAID_BETA_SCORECARD.md)
9. **Go / No-Go عام** — [`PUBLIC_LAUNCH_GO_NO_GO.md`](PUBLIC_LAUNCH_GO_NO_GO.md)

## حزم RevOps + AI (تسعير ونطاق)

مصدر الحقيقة للعروض التجارية (أسعار، ما يشمل، ربط بالمنتج): [`commercial/DEALIX_REVOPS_PACKAGES_AR.md`](commercial/DEALIX_REVOPS_PACKAGES_AR.md).

## قاعدة التسمية

حتى تتحقق مدفوعات واستقرار وتشغيل: الإطلاق هو **Paid Private Beta** أو **Launch Candidate** وليس “Public Launch” كاملاً.
