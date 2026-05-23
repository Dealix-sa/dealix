# ICP Operating System

## Purpose
Define the Ideal Customer Profile (ICP) and how to apply it to every commercial decision.

## Primary ICP
Saudi mid-market companies (revenue 10M–500M SAR/year) in:
- Insurance brokerage & claims
- Retail (regional chains, not enterprise)
- Healthcare clinics & medical groups
- Real estate developers & brokerages
- B2B services (legal, accounting, recruiting)

Common traits:
- Already digital but operating off spreadsheets and ad-hoc tools.
- A revenue or operations leader who personally feels the pain.
- Willing to start small (under 5,000 SAR) to prove value.

## Secondary ICP (opportunistic)
- Saudi family offices using B2B data.
- KSA-based regional consulting firms needing data packs.

## Anti-ICP (avoid)
- Pre-revenue startups.
- Companies looking only for translation or generic content.
- Buyers who demand free pilots > 2 weeks of effort.
- Buyers who refuse to disclose their KPI baseline.

## ICP scorecard
Columns in `icp/icp_scorecard.csv`:
`sector, lead_count, dms, replies, samples, proposals, paid, fit_score, decision, next_action`

Update weekly. A sector with low fit_score and zero paid after 30 days is paused.

## How to use ICP in daily work
- Before adding a lead: confirm sector ∈ Primary ICP.
- Before drafting a proposal: confirm the buyer matches a Primary ICP role.
- Before promising a custom build: confirm the deal is rung 4 or 5 of the ladder.

## When to revise ICP
- After 25 paying customers, revisit the segmentation.
- If a non-ICP customer pays for 2 retainer renewals, that segment moves to Primary.
