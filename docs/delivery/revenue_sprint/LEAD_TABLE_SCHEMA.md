# Lead Table Schema

> The canonical structure of every Sprint deliverable spreadsheet.

## Columns

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| account_id | string | yes | Stable per Sprint |
| legal_name | string | yes | Customer's legal entity, Arabic + English where applicable |
| website | url | yes | |
| sector | string | yes | Controlled vocabulary |
| size_employees | int | yes | Use bands if exact unknown |
| size_revenue_band | string | no | Public ranges only |
| geo | string | yes | KSA city or "Multi-KSA" |
| decision_maker_name | string | yes | |
| decision_maker_role | string | yes | |
| decision_maker_email | string | conditional | When safely sourced |
| decision_maker_phone | string | conditional | Only when consented |
| linkedin_url | url | yes | |
| trigger_signal | string | yes | The specific signal triggering this account |
| trigger_signal_evidence_url | url | yes | Link to the source of the signal |
| icp_fit_score | int 0-5 | yes | |
| pain_score | int 0-5 | yes | |
| authority_score | int 0-5 | yes | |
| budget_score | int 0-5 | yes | |
| timing_score | int 0-5 | yes | |
| total_score | int 0-25 | yes | Sum of the above |
| priority | A / B / C / D | yes | Per `SCORING_RULES.md` |
| dm_draft_ar | text | for A,B | Arabic DM |
| dm_draft_en | text | for A,B | English DM |
| email_draft_ar | text | for A,B | Arabic email |
| email_draft_en | text | for A,B | English email |
| evidence_links | text | yes | Per claim |
| notes | text | no | |

## Data quality rules

- No account without a `trigger_signal_evidence_url`.
- Score columns must sum to `total_score`.
- `priority` derived from score, not entered manually.
- No two accounts with the same legal entity.
- No accounts on the customer's "do not contact" list.

## File format

- Delivered as Excel (xlsx) and CSV.
- Encoding: UTF-8.
- Arabic text right-to-left aware where displayed in the Excel file.

## PDPL Note

- Decision-maker personal data only included when it was lawfully obtained
  (public business profile, prior consent, or shared by the customer).
- Personal data lives only in the customer's workspace; not committed
  to any public surface.
