# المرحلة ج — الإنتاج الكامل (بعد Soft Launch)

**متى:** بعد 3–5 اجتماعات مبيعات ناجحة من Soft Launch ومسار حزمة عميل مكرّر.

## بوابة واحدة

```bash
bash scripts/official_launch_verify.sh
# Windows:
powershell -File scripts/official_launch_verify.ps1
```

مع API حي (اختياري):

```bash
export DEALIX_API_BASE=https://your-api.example
export DEALIX_ADMIN_API_KEY=your-key
bash scripts/official_launch_verify.sh --api-base "$DEALIX_API_BASE" --admin-key "$DEALIX_ADMIN_API_KEY"
```

## قبل التشغيل

1. راجع [LAUNCH_GATES.md](../LAUNCH_GATES.md) — Moyasar live، DPA، PDPL.
2. Bootstrap إنتاج (مرة): `bash scripts/railway_prod_bootstrap.sh`
3. انسخ [DEPLOYMENT.md](../../DEPLOYMENT.md) — `APP_SECRET_KEY`، `DATABASE_URL`، `ENVIRONMENT=production`.

## ما يبقى يدوياً بعد المرحلة ج

- لا واتساب بارد · لا LinkedIn آلي · لا Gmail خارجي بدون موافقة.
- KPI من `kpi_founder_commercial_import.yaml` فقط (لا أرقام مخترعة).

## مراجع

- [DEALIX_COMPANY_READY_MASTER_AR.md](../company/DEALIX_COMPANY_READY_MASTER_AR.md)
- [COMMERCIAL_LAUNCH_CHECKLIST_AR.md](../commercial/COMMERCIAL_LAUNCH_CHECKLIST_AR.md)

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
