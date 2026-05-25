# Lead Table Schema — مخطط جدول الفرص

## Purpose
Define the canonical CSV schema for every lead table Dealix ships. The schema is enforced at G3 (Pack Built). A table that fails validation cannot ship.

## Owner
Head of Delivery (schema). Data lead (validator script).

## Inputs
- Raw research rows from Day 2.
- Scoring outputs from Day 3.
- Intake constraints (geo, exclusions, channels).

## Outputs
- `lead_table.csv` validated against this schema.
- `lead_table_validation.log` with row-level pass/fail.

## Rules (numbered)
1. Schema version is pinned in the file header (`# schema_version: vX.Y`).
2. No PII columns. No personal phone, no personal email, no national ID.
3. Every row carries `source_url` and `source_captured_at`.
4. Every row carries `score_fit`, `score_signal`, `score_reach` integers 0–5.
5. Empty mandatory fields fail the row.
6. Any row with `excluded=true` is shipped in a separate `excluded.csv` for auditability.
7. Schema changes follow `docs/delivery/CHANGE_REQUEST_PROCESS.md` and bump the version.

## Metrics
- Validation pass rate on first run: target ≥ 95%.
- Rows with full evidence URL: 100%.
- Schema drift incidents per quarter: target 0.

## Cadence
Per sprint at G3. Schema reviewed quarterly.

## Evidence (paths)
- `docs/audit/sprints/SPRINT_<ID>/lead_table.csv`
- `docs/audit/sprints/SPRINT_<ID>/lead_table_validation.log`

## Verifier
Data lead runs the validator. Head of Delivery signs the validation log.

## Runtime Command
`make sprint.leads.validate SPRINT=<ID>` — runs schema validation and writes the log.

## Columns

| column | type | required | description |
|---|---|---|---|
| `lead_id` | string | yes | Sprint-scoped unique ID, format `SPRINT-<ID>-NNNN`. |
| `company_legal_name` | string | yes | Legal entity name as published. |
| `company_trading_name` | string | no | Trade name if different. |
| `country` | ISO-2 | yes | Buyer country code. |
| `region` | string | no | Region or city. |
| `sector_code` | string | yes | Sector code from intake list. |
| `sub_sector` | string | no | Sub-sector if applicable. |
| `employee_band` | enum | yes | 1-10, 11-50, 51-200, 201-500, 501-1000, 1000+. |
| `revenue_band_sar` | enum | no | Estimated band; mark `estimated=true`. |
| `buying_center_role` | string | yes | Role title we target (no personal name). |
| `signal_type` | enum | yes | tender, hiring, expansion, news, filing, registry. |
| `signal_summary` | string | yes | One-line description of the buying signal. |
| `signal_date` | date | yes | When the signal was observed. |
| `source_url` | url | yes | Public source URL. |
| `source_captured_at` | datetime | yes | ISO 8601 timestamp when the row was captured. |
| `score_fit` | int 0-5 | yes | Fit to ICP. |
| `score_signal` | int 0-5 | yes | Signal strength. |
| `score_reach` | int 0-5 | yes | Reachability via in-scope channels. |
| `score_total` | int 0-15 | yes | Sum of the three. |
| `recommended_channel` | enum | yes | email, form, association, tender_portal, in_person. |
| `excluded` | bool | yes | true if excluded; row moves to `excluded.csv`. |
| `exclusion_reason` | string | conditional | Required if `excluded=true`. |
| `notes` | string | no | Operator notes, no PII. |

## Operating substance
The schema is intentionally short. Every column has a clear purpose at QA or at the client's audit. We do not collect personal contact data; the client owns their own contact policy. We do not invent revenue figures; estimated bands are flagged so the client can decide how much weight to give them.

Validation runs as a CI step before the gate can close. A row that fails any required-field check is written to the validation log with the failure reason. The builder fixes the row or drops it. We do not "soft-pass" rows.

The schema version is pinned per sprint, so a client can re-validate the file months later against the same rules. This is part of how Dealix earns audit trust.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
