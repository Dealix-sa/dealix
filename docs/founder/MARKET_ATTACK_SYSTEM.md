# Market Attack System

The beachhead, the ICP, and the offensive GTM motion. This is the answer
to "why this customer, this week, instead of that customer next month?"

## Purpose

Concentrate the company's limited founder-hours on a single segment we
can dominate, then expand only after the beachhead is owned.

## Owner

Founder. Re-evaluated quarterly.

## Cadence

- Daily: top 3 attack moves surfaced at /ops/founder.
- Weekly: pipeline vs. beachhead alignment check.
- Quarterly: beachhead re-evaluation.

## Source of Truth

- Beachhead definition: section "Beachhead" below.
- ICP definition: section "ICP" below.
- Account list: `docs/commercial/operations/targeting/agency_accounts_seed.csv`

## Beachhead

| Field | Value |
| --- | --- |
| Sector | Saudi mid-market services / agencies / boutique consultancies |
| Geo | Riyadh + Jeddah |
| Company size | 20 – 200 staff |
| Buying trigger | Vision 2030 reporting + customer-data fragmentation |
| Why us | Bilingual data ops + governance proof, not just AI hype |

## ICP

- Decision maker: founder, COO, or head of revenue
- Has internal data (CRM, ERP, WhatsApp business) but no glue layer
- Has paid for at least one consulting engagement in the last 12 months
- Believes "AI matters" but does not have an in-house AI team

## Inputs

- Sector signals (filings, public news, hiring posts)
- Inbound interest delta
- Referral graph

## Outputs

- Updated beachhead definition (this doc)
- Weekly "top 5 to attack" list at /ops/founder
- A monthly "expand to next sector?" decision

## KPI

- ≥ 60% of pipeline value inside the beachhead
- < 20% time spent outside ICP
- Beachhead win rate ≥ 2x out-of-beachhead

## Trust Boundary

This doc never leaves the company in raw form. Any external version is a
sanitized derivative reviewed under `claim_policy.yaml`.

## Failure Mode

- Beachhead drifts (pipeline majority outside it) → weekly review flags.
- Expansion attempted before beachhead is owned → counted as a decision
  that must be logged in the decision log.

## Recovery Path

1. Pull pipeline by sector.
2. If < 60% inside beachhead, refocus this week's drafts.
3. If still drifting after 4 weeks, re-evaluate beachhead at the next
   monthly capital review.

## Verification

```bash
make business-os
python scripts/verify_everything.py --layer market_attack
```

## Next Action

Look at this week's outreach drafts. Drop anything outside the beachhead
unless there's a logged decision saying otherwise.
