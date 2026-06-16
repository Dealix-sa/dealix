# Approval Log Schema

The canonical CSV schema used by `dealix-ops-private/trust/approval_log.csv`.

## Purpose
Lock the column set for the private approval log so the Trust Loop produces auditable evidence.

## Owner
Sami (Founder, Trust OS).

## Review Cadence
Quarterly, or after any incident.

## Inputs
- The approval matrix defined in `docs/trust/APPROVAL_MATRIX.md`.
- The autonomy policy in `docs/trust/AUTONOMY_POLICY.md`.

## Outputs
- The CSV schema below.
- The expected header row of the private approval log.

## Rules
- One row per approval event (approved or rejected).
- `risk_level` is `A0`, `A1`, `A2`, `A3`, or `Never`.
- `decision` is `approved` or `rejected`.
- `evidence` references a file path, URL, or message ID.

---

## Columns

| Column | Type | Notes |
|---|---|---|
| `date` | date | ISO-8601 timestamp of the decision. |
| `item` | text | Short description (e.g., outbound DM to Company X). |
| `type` | text | outreach / proposal / report / pricing / autonomy / other. |
| `risk_level` | enum | A0 / A1 / A2 / A3 / Never. |
| `decision` | enum | approved / rejected. |
| `approved_by` | text | Person who signed off. |
| `evidence` | text | File path, link, or reference. |

## Example Row

```csv
date,item,type,risk_level,decision,approved_by,evidence
2026-05-23T08:30:00+03:00,DM to Example Co,outreach,A2,approved,Sami,clients/example_co/outreach_pack.md
```

## Metrics
- Number of approvals per week per type.
- Rejection rate per type (signal of AI prep quality).

## Evidence
- The header row of `dealix-ops-private/trust/approval_log.csv` matches this schema.

## Last Reviewed
2026-05-23
