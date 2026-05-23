# مقاييس المؤسس الأسبوعية (مصادر حقيقية فقط)

**الغرض:** ربط الأسبوع بـ KPI من CRM + Truth Matrix + أحداث الإثبات — بدون اختراع أرقام.

---

## مصادر الحقيقة

| المصدر | الملف | قاعدة |
|--------|-------|--------|
| KPI تجاري | `kpi_founder_commercial_import.yaml` | من CRM فقط — gitignored |
| سجل KPI | `kpi_founder_commercial_registry.yaml` | بعد `apply_kpi_founder_commercial.py` |
| تكاملات | `founder_integration_truth.yaml` | green/yellow/red يدوياً |
| إثبات أسبوعي | `evidence_events_tracker.csv` | أحداث حقيقية فقط |

---

## أمر واحد

```bash
python scripts/founder_weekly_metrics_bundle.py --write
python scripts/apply_kpi_founder_commercial.py --status
```

**مخرج:** `data/founder_weekly/metrics_{ISO_WEEK}.yaml`

**حكم:** `FOUNDER_WEEKLY_METRICS_VERDICT=READY|BLOCKED`

---

## ضمن الحلقة الأسبوعية

```bash
bash scripts/founder_weekly_loop.sh
```

يشمل الآن حزمة المقاييس قبل أقوى خطة.

---

## مراجع

- [`AGENT_DAILY_WORK_PACKETS_AR.md`](AGENT_DAILY_WORK_PACKETS_AR.md) — حزمة `weekly_metrics_bundle`
- [`FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md`](FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md)

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
