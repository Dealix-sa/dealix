# Lead Table Schema — Revenue Sprint

The canonical columns for every delivered lead table.

| Column | Type | Notes |
|---|---|---|
| lead_id | string | Stable id within the sprint |
| company_name | string | Legal or trading name |
| sector | enum | From the sector taxonomy |
| sub_sector | string | Free text |
| city | string | Saudi cities preferred form |
| size_band | enum | micro / small / mid / large |
| website | url | Public |
| public_contact_name | string | If publicly listed |
| public_contact_role | string | If publicly listed |
| public_contact_email | string | If publicly listed |
| public_contact_phone | string | If publicly listed |
| source_url | url | Required |
| icp_score | int | 0–100, from `ICP_SCORING_MODEL.md` |
| score_reason | string | One sentence |
| recommended_message_angle | string | One sentence |
| risk_flag | enum | none / review / exclude |
| risk_reason | string | If flagged |

## Required
- Every row has `source_url`, `icp_score`, and `score_reason`.
- Rows flagged `exclude` are kept for audit but marked.

## Format
- CSV inside the client folder.
- A rendered, readable view inside the report.

## Rule
A row without a source is removed before delivery.
