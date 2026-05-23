# Objection Intelligence System

> Every objection encountered in a Saudi B2B sales motion is data.
> The Objection Library converts objections into assets, training,
> and product roadmap inputs.

## CSV schema

`<PRIVATE_OPS>/market_attack/objection_library.csv`

```
objection_id,sector,stage,objection,frequency,response_angle,
asset_needed,owner,status,next_action
```

- `stage` ∈ {`cold`, `discovery`, `sample`, `proposal`, `negotiation`, `post_sale`}.
- `frequency` integer, count of times seen.
- `response_angle` short one-liner of the current best response.
- `asset_needed` ∈ {`none`, `one_pager`, `proof_link`, `sample`,
  `proposal_template`, `case_study`, `compliance_doc`, `pricing_table`}.
- `status` ∈ {`open`, `response_drafted`, `asset_in_progress`,
  `resolved`, `recurring`}.

## Loop

1. Sales call ends → objection captured into the library
   (frequency += 1).
2. Top 3 objections in a sector each week become an `asset_needed`
   ticket in `sales_asset_registry.csv`.
3. Assets shipped → linked back in the objection row's `next_action`.
4. Objection frequency drops in subsequent weeks → mark `resolved`.

## Refusals

- We do **not** rewrite objections to make ourselves look good. The
  raw customer wording is preserved in `objection` so the team
  hears the customer voice.
