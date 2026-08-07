# Dealix Deal Desk Rules

## Purpose
The deal desk is the founder-operated gate between a qualified opportunity and a signed SOW.

## When the deal desk runs
- Any opportunity above 5,000 SAR setup or 2,000 SAR/mo MRR.
- Any custom scope outside the published 17 offerings.
- Any discount request below the floor in `PRICING_DISCOUNT_POLICY.md`.
- Any acceptance-criteria deviation.

## Inputs
- `business/_data/scored_leads.json` — qualified account.
- `business/_data/quotes.index.json` — pending quote.
- A friction log + workflow review notes.

## Outputs
- An approved quote (status=approved).
- A draft SOW from `business/contracts/STATEMENT_OF_WORK_TEMPLATE_*.md`.
- A line in `business/_data/deals.ledger.json` once the deal is won/lost.

## Approval matrix
- Setup ≤ 10,000 SAR + scope on-catalog: founder unilateral approval.
- Setup 10,001–25,000 SAR or custom scope: founder + commercial owner from the customer side must both sign.
- Above 25,000 SAR or multi-tenant: founder + customer commercial + customer legal.

## Forbidden actions
- No verbal commitments without a written quote backing them.
- No discount > 30% off the listed price without documented strategic rationale.
- No payment terms more lenient than net-30 unless on enterprise SOW.

## Cadence
Weekly review of all open quotes during the founder operating review on Sunday.
