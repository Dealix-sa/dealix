# يوم 0 — خط الأساس (مؤسس فقط)

> مرجع: خطة Sell Verify Train · لا أرقام CRM مخترعة.

## 1) لقطة الأعمال

```powershell
# Windows
.\scripts\run_business_now.ps1
```

```bash
# Linux / macOS / Git Bash
bash scripts/run_business_now.sh
```

**مخرجات:** `dealix/transformation/business_now_cache.yaml` · `docs/business/evidence/business_now_snapshot.md`

## 2) KPIs التجارية (إلزامي قبل ادّعاء إيراد)

1. انسخ [`dealix/transformation/kpi_founder_commercial_import.example.yaml`](../../dealix/transformation/kpi_founder_commercial_import.example.yaml) → `kpi_founder_commercial_import.yaml`
2. املأ من CRM الحقيقي فقط
3. `python3 scripts/apply_kpi_founder_commercial.py`
4. تحقق: `python3 scripts/apply_kpi_founder_commercial.py --status`

## 3) ديمو + Deck

| أصل | مسار |
| --- | --- |
| واجهة | `/ar/business-now#strategy` (API `:8000`) |
| Runbook | [`docs/commercial/ops_client_pack/dealix_ops_runbook_ar.md`](../commercial/ops_client_pack/dealix_ops_runbook_ar.md) |
| Deck | `docs/commercial/ops_client_pack/dealix_ops_sales_kit_ar.pptx` |

**Screenshots (3):** focus · simulate · proof demo

## 4) تحقق سريع

```bash
bash scripts/founder_go_live_verify.sh
```

## 5) سلم البيع (ماذا تبيع بصدق)

1. **Diagnostic (Ops)** — 4,999–15,000 SAR — مدخل المحادثة
2. **Sprint 499** أو **Data Pack 1500** — بعد القبول
3. **Growth 2999** — بعد Proof Pack فقط

مرجع الربط: [COMMERCIAL_WIRING_MAP.md](../COMMERCIAL_WIRING_MAP.md) · [FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md](FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md)

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
