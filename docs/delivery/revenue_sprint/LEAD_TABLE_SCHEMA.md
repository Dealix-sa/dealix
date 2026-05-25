---
title: Lead Table Schema
owner: Delivery Lead
status: active
last_review: 2026-05-23
---

# Lead Table Schema — مخطط جدول الفرص

## Purpose

The exact schema of the lead table delivered to buyers. One schema across all sprints. Schema drift is treated as a control failure.

## Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `row_id` | string | yes | Stable per sprint; format `<sprint_id>-NNN`. |
| `company_name` | string | yes | Legal or trade name as it appears publicly. |
| `sector` | string | yes | Must match intake sector. |
| `sub_segment` | string | yes | From intake's sub-segment list. |
| `region` | string | yes | KSA region. |
| `city` | string | yes | Saudi city or "multiple". |
| `role` | string | yes | Named buyer role; not personal name unless explicit add-on. |
| `signal` | string | yes | Single sentence: why this company, this quarter. |
| `score` | integer | yes | 0–100 per [SCORING_RULES.md](./SCORING_RULES.md). |
| `priority` | enum | yes | `top` (≥ 70) / `secondary` (40–69) / `monitor` (< 40). |
| `source_url` | URL | yes | Public source URL. |
| `source_type` | enum | yes | `company_site` / `registry` / `news` / `industry_report` / `directory`. |
| `retrieved_at` | ISO-8601 timestamp | yes | UTC; when source was last read. |
| `notes` | string | optional | Reviewer notes; never personal data. |

## Schema example

```json
{
  "row_id": "RSP-2026-05-22-014",
  "company_name": "Example Holding (anonymized for docs)",
  "sector": "Logistics services",
  "sub_segment": "Last-mile B2B",
  "region": "Riyadh Region",
  "city": "Riyadh",
  "role": "Head of Commercial",
  "signal": "Public tender win for inter-city distribution announced 2026-04-12.",
  "score": 82,
  "priority": "top",
  "source_url": "https://example-registry.sa/notice/...",
  "source_type": "registry",
  "retrieved_at": "2026-05-22T08:14:00Z",
  "notes": "Two warehouses publicly listed; expansion language in 2025 annual."
}
```

## Forbidden fields

- Personal name (unless the decision-maker mapping add-on is purchased AND the contact is publicly documented in that role).
- Personal phone or personal email.
- National ID or any government identifier of an individual.
- Inferred or fabricated data.

## Validation

- Schema validated automatically before the QA gate (control D-07).
- Any row missing a required field or carrying a forbidden field is rejected; sprint cannot ship until cleared.

## Delivery formats

- `lead_table.xlsx` — formatted for buyer reading.
- `lead_table.csv` — clean import-friendly version.

## Cross-links

- [SCORING_RULES.md](./SCORING_RULES.md)
- [DELIVERY_CONTROL_SYSTEM.md](./DELIVERY_CONTROL_SYSTEM.md) — D-02, D-07.
- [docs/04_data_os/DATA_PROVENANCE.md](../../04_data_os/DATA_PROVENANCE.md)
- [docs/04_data_os/PII_CLASSIFICATION.md](../../04_data_os/PII_CLASSIFICATION.md)

## Owner & cadence

- Delivery Lead. Schema reviewed quarterly; changes require a migration note.

## AR — ملخّص

مخطط ثابت لجدول الفرص: معرّف الصف، اسم الشركة، القطاع، القطاع الفرعي، المنطقة، المدينة، الدور (لا الشخص)، الإشارة، النتيجة، الأولوية، رابط المصدر، نوع المصدر، توقيت السحب. حقول محظورة: الأسماء الشخصية، الجوّال الشخصي، البريد الشخصي، الهوية الوطنية، أي بيانات مُستنتجة. التحقّق آلي قبل بوّابة الجودة. القيمة التقديرية ليست قيمة مُتحقَّقة.
