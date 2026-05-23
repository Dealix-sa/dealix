---
title: CEO Dashboard Data Model
owner: Founder / Data Lead
status: active
last_review: 2026-05-23
---

# CEO Dashboard Data Model — نموذج بيانات لوحة الرئيس التنفيذي

## Purpose

Define the single schema that powers the CEO dashboard. Every widget in [CEO_DASHBOARD_V2.md](./CEO_DASHBOARD_V2.md) reads from this schema. One shape, one source of truth.

## File

`dealix-ops-private/dashboard/company_metrics.json` — committed weekly, regenerated from authoritative sources, never edited by hand.

## Schema

```json
{
  "as_of": "YYYY-MM-DD",
  "period": "YYYY-WW",
  "pipeline": {
    "leads_new": 0,
    "leads_qualified": 0,
    "dms_queued": 0,
    "dms_sent_with_consent": 0,
    "samples_sent": 0,
    "proposals_out": 0,
    "proposals_signed": 0,
    "estimated_acv_open_sar": 0,
    "by_sector": [
      { "sector": "code", "open_count": 0, "estimated_acv_sar": 0, "signed_last_180d": 0 }
    ]
  },
  "revenue": {
    "booked_mtd_sar": 0,
    "booked_qtd_sar": 0,
    "booked_ytd_sar": 0,
    "estimated_value_open_sar": 0,
    "observed_value_open_sar": 0,
    "verified_value_closed_sar": 0,
    "note": "Estimated, Observed, Verified per docs/08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md"
  },
  "delivery": {
    "sprints_in_flight": 0,
    "sprints_on_track": 0,
    "sprints_at_risk": 0,
    "evidence_complete_rate": 0.0,
    "proof_packs_shipped_mtd": 0
  },
  "learning": {
    "experiments_active": 0,
    "experiments_decided_mtd": 0,
    "router_promotions_mtd": 0,
    "case_safe_summaries_total": 0
  },
  "trust": {
    "incidents_open": 0,
    "incidents_closed_mtd": 0,
    "approval_queue_depth": 0,
    "ai_evals_passed_mtd": 0,
    "ai_evals_failed_mtd": 0,
    "audit_findings_open": 0
  }
}
```

## Field rules

- All SAR amounts are integers. No fractions.
- `estimated_acv_open_sar` is labeled estimated wherever displayed.
- `verified_value_closed_sar` only counts amounts that pass [docs/08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md](../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md) verification.
- `by_sector.sector` uses codes from [docs/02_saudi_positioning/SAUDI_SECTOR_TAXONOMY.md](../02_saudi_positioning/SAUDI_SECTOR_TAXONOMY.md).
- Trust fields cross-reference [docs/14_trust_os/](../14_trust_os/) and [docs/ai_management/AI_COMMAND_CENTER.md](../ai_management/AI_COMMAND_CENTER.md).

## Operations

1. The JSON is regenerated every Sunday before the weekly review.
2. Source-of-truth links are documented per field in `dealix-ops-private/dashboard/sources.md`.
3. Any field that cannot be sourced is omitted, not invented.

## Evidence

- Each weekly snapshot is committed and kept for 24 months.
- Diffs across weeks are how trajectory is read.

## Owner & cadence

- Founder owns the schema definition. Data Lead owns the weekly regeneration.
- Schema changes follow a PR with an entry in [docs/learning/COMPANY_MEMORY.md](../learning/COMPANY_MEMORY.md).

## AR — ملخّص

نموذج بيانات اللوحة هو مصدر حقيقة واحد لكل widget. ملف JSON أسبوعي مولّد من المصادر الرسمية، يفصل بين القيمة التقديرية والملاحظة والمتحقّقة، يستعمل رموز قطاعات معتمدة، ولا يخترع حقولاً غير قابلة للمصدر. القيمة التقديرية ليست قيمة مُتحقَّقة.
