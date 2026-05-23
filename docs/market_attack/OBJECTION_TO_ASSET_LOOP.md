# Objection → Asset Loop

> The mechanical pipeline from "we heard the same objection 3 times"
> to "we have an approved, proof-safe asset that handles it".

## Trigger

`objection_library.csv` row reaches `frequency >= 3` within a single
`sector` and `stage` → an `asset_needed` is auto-set.

## Routing

| Stage           | Default asset type             |
| --------------- | ------------------------------ |
| cold            | sector_one_pager               |
| discovery       | sample                         |
| sample          | proof_link or case_study       |
| proposal        | proposal_template              |
| negotiation     | pricing_table / compliance_doc |
| post_sale       | onboarding doc                 |

## SLA

- Within 14 days, the corresponding row in `sales_asset_registry.csv`
  must transition from `draft` → `approval_required` → `approved`.
- If not, the objection row's `status` is forced to `recurring` and
  flagged in the weekly Conversion Command Room.

## Verifier check

`scripts/verify_market_attack_system.py` warns (does not fail) when:

- ≥ 3 objections at `frequency >= 3` lack a linked `sales_asset_registry`
  row.
- ≥ 1 objection has been in `recurring` for more than 30 days.
