---
title: CEO Dashboard v2
owner: Founder
status: active
last_review: 2026-05-23
---

# CEO Dashboard v2 — لوحة الرئيس التنفيذي

## Purpose

The single screen the founder opens every weekday morning and every Sunday review. It answers five questions in five rows: are we pulling pipeline, are we converting, are we delivering, are we learning, are we safe.

## Layout (top to bottom)

| Row | Widget | Reads from | Refresh |
|---|---|---|---|
| 1 | Targets vs actuals (weekly) | `company_metrics.pipeline` + [CEO_TARGETS.md](./CEO_TARGETS.md) | weekly |
| 2 | Pipeline funnel by sector | `company_metrics.pipeline.by_sector` | weekly |
| 3 | Revenue split (Estimated / Observed / Verified) | `company_metrics.revenue` | weekly |
| 4 | Delivery health | `company_metrics.delivery` | weekly |
| 5 | Learning flow | `company_metrics.learning` | weekly |
| 6 | Trust + AI governance | `company_metrics.trust` | weekly |

## Widget specs

### Row 1 — Targets vs actuals
Shows for the current week: 25 leads / 25 DMs / 3 samples / 1 proposal. Green if at or above, amber within 80%, red below. No vanity targets.

### Row 2 — Pipeline funnel by sector
Bar per sector with open count and estimated ACV. Labeled "Estimated". Click-through links to the sector verdict file in [docs/learning/SECTOR_PERFORMANCE.md](../learning/SECTOR_PERFORMANCE.md).

### Row 3 — Revenue split
Three columns: Estimated, Observed, Verified, per [docs/08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md](../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md). The verified column is the only one that travels into external materials.

### Row 4 — Delivery health
Sprints in flight, sprints at risk, evidence-completeness rate, proof packs shipped MTD. At-risk sprints surface owner and unblock action.

### Row 5 — Learning flow
Active experiments, decided MTD, router promotions MTD, case-safe summaries total. Promotions counter is the leading indicator of capital growth.

### Row 6 — Trust + AI governance
Open incidents, approval queue depth, AI evals passed/failed MTD, open audit findings. Any non-zero open incident or failed eval is highlighted until closed.

## Data source

All widgets read from [`CEO_DASHBOARD_DATA_MODEL.md`](./CEO_DASHBOARD_DATA_MODEL.md). No widget pulls from a side spreadsheet. If a needed field is missing, the schema is extended via PR, not bypassed.

## Operations

1. Data Lead regenerates the JSON every Sunday before 18:00 KSA.
2. Founder reads the dashboard at the start of each weekly review.
3. Any red or amber widget triggers a one-line action in the weekly note.

## Non-negotiables

- No projected metric is shown without an estimated/observed/verified label.
- No client-identifying data appears on a shared screen; only sector codes and aggregates.
- No widget computes ROI as a single headline. ROI claims follow [docs/08_value_os/ROI_DISCIPLINE.md](../08_value_os/ROI_DISCIPLINE.md).

## Evidence

- Weekly JSON snapshots in the private ops repo.
- Dashboard screenshots are not shared externally.

## Owner & cadence

- Founder owns the layout.
- Data Lead owns the refresh.
- Layout changes follow a PR and are logged in [docs/learning/COMPANY_MEMORY.md](../learning/COMPANY_MEMORY.md).

## AR — ملخّص

لوحة v2 تجيب على خمسة أسئلة في خمسة صفوف: نسحب أنبوب؟ نحوّل؟ نسلّم؟ نتعلّم؟ نحن آمنون؟ كل widget يقرأ من JSON واحد، يفصل بين القيمة التقديرية والملاحظة والمتحقّقة، ولا يعرض ROI كرقم وحيد. القيمة التقديرية ليست قيمة مُتحقَّقة.
