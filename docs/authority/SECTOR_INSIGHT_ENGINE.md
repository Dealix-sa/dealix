# Sector Insight Engine

> Insights are the raw material for authority. Every insight is a
> specific, evidenced statement about a Saudi B2B sector.

## CSV schema

`<PRIVATE_OPS>/authority/sector_insights.csv`

```
insight_id,sector,insight,evidence,source,status,
approved_for_public,next_action
```

- `insight` — one sentence; not a take, a finding.
- `evidence` — pointer (file path, link, internal id) to the data
  behind the insight.
- `source` — `internal_ledger`, `customer_interview`, `partner`,
  `public_report`, `regulatory_filing`.
- `status` — `draft`, `validated`, `archived`.
- `approved_for_public` — `yes` / `no` / `governance_review`.

## Validation rule

An insight cannot have `approved_for_public=yes` while
`evidence` is empty. The verifier enforces this.

## Sourcing

We do not extrapolate from one customer. An insight that says "Saudi
construction firms…" must be supported by ≥ 3 distinct data points
(deals, interviews, public reports).
