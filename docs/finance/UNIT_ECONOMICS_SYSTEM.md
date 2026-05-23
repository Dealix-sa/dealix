# Unit Economics System

## Purpose
Know the per-engagement economics. Without this number, every pricing decision is guessing.

## Per-engagement metrics
- `revenue_sar` — billed.
- `direct_cost_sar` — anything spent specifically for this engagement (contractors, data, tools).
- `hours_invested` — founder + contractor hours.
- `effective_hourly_sar = (revenue_sar - direct_cost_sar) / hours_invested`.
- `gross_margin_sar = revenue_sar - direct_cost_sar`.

## Target effective hourly
- Rung 2 (Sprint): ≥ 200 SAR/hr.
- Rung 3 (Data Pack): ≥ 300 SAR/hr.
- Rung 4 (Retainer): ≥ 400 SAR/hr.
- Rung 5 (Custom): ≥ 500 SAR/hr.

## Where to track
`dealix-ops-private/finance/unit_economics.csv`:
- Schema: see `schemas/unit_economics.schema.json`.

## Cadence
- Update after every engagement closes.
- Monthly: review effective hourly trends.
- Quarterly: re-evaluate pricing if 2+ engagements miss the target.

## Hidden costs to include
- Founder time at internal cost (do not zero-cost yourself).
- Tooling allocated to this engagement.
- Bank / payment gateway fees.
- VAT (if applicable to the buyer category).

## Anti-bias
- Effort optimism: track actual hours, not estimated hours.
- Cost denial: count tools you "would have anyway" if they were specifically needed for this deal.

## Reports
- `make finance-full` generates a finance command report including unit-economics summary.
