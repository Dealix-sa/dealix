# Pipeline Tracker Schema

The canonical CSV schema used by `dealix-ops-private/pipeline/pipeline_tracker.csv`.

## Purpose
Lock the column set for the private pipeline tracker so every verifier and every agent reads the same shape.

## Owner
Sami (Founder, Revenue OS).

## Review Cadence
Quarterly, or when a new stage/field is added to the pipeline.

## Inputs
- The pipeline stages defined in `docs/revenue/PIPELINE_STAGES.md`.
- The offer ladder in `docs/revenue/OFFER_LADDER.md`.

## Outputs
- The CSV schema below.
- The expected first row (header) of the private pipeline tracker.

## Rules
- All columns are required.
- Stage values must be one of the seven canonical stages.
- Priority values must be `A`, `B`, or `C`.
- `last_touch` is an ISO-8601 date.

---

## Columns

| Column | Type | Notes |
|---|---|---|
| `company` | text | Customer company name. |
| `sector` | text | ERP, retail, healthcare, etc. |
| `contact` | text | Decision-maker name + role. |
| `stage` | enum | New / Contacted / Replied / Proposal Sent / Paid / Delivered / Retainer. |
| `priority` | enum | A (this week), B (this month), C (this quarter). |
| `next_action` | text | The single next move. |
| `last_touch` | date | ISO-8601 date of the last outbound or inbound contact. |
| `notes` | text | Free text. |

## Example Row

```csv
company,sector,contact,stage,priority,next_action,last_touch,notes
Example Co,ERP,CEO,New,A,Send founder DM,,Good B2B fit
```

## Metrics
- Number of rows per stage.
- Number of `A` priority leads with `last_touch` older than 7 days (target: zero).

## Evidence
- The header row of `dealix-ops-private/pipeline/pipeline_tracker.csv` matches this schema.

## Last Reviewed
2026-05-23
