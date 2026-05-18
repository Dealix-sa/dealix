# Soft Launch vs Paid Launch

| البُعد | Soft (الآن) | Paid (لاحقاً) |
|--------|-------------|---------------|
| الدفع | يدوي / تحويل | Moyasar live |
| CRM KPI | `kpi_founder_commercial_import.yaml` | HubSpot + نفس الملف |
| التحقق | `verify_commercial_launch_ready.py` | `verify_paid_launch_readiness.py` |
| المرحلة | `py -3 scripts/verify_launch_phase.py` | `DEALIX_LAUNCH_PHASE=PAID_*` |

**أول إيراد:** `payment_received` + `proof_pack_delivered` في evidence CSV — [FIRST_PAID_DIAGNOSTIC_DOD_AR.md](operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md).
