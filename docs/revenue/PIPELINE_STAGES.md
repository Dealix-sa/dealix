# Pipeline Stages

> 11 stages. Each is a verb. Each has an exit criterion.

## The Stages

| # | Stage | Verb | Exit criterion to next stage |
|---|-------|------|-------------------------------|
| 1 | New | Identified | Lead enters CRM with name, role, company, sector |
| 2 | Qualified | Scored | Lead scores ≥ 14/25 on ICP rubric |
| 3 | Contacted | Reached | DM or email sent with personalised hook |
| 4 | Replied | Engaged | Lead has replied at least once |
| 5 | Sample Sent | Sampled | Personalised sample delivered |
| 6 | Call Booked | Scheduled | Calendar invite confirmed |
| 7 | Proposal Sent | Proposed | Proposal delivered with price + scope |
| 8 | Paid | Closed | Payment received OR PO + signed scope |
| 9 | Delivered | Shipped | Proof Pack handed off + signed off |
| 10 | Retainer | Retained | Monthly Revenue Desk active |
| 11 | Lost | Closed-Lost | Disqualified, with documented reason |

## Stage Time Limits

If a deal stays in a stage longer than the time limit without movement,
it is auto-flagged for review:

| Stage | Time limit |
|-------|-----------|
| New | 3 days |
| Qualified | 7 days |
| Contacted | 7 days |
| Replied | 5 days |
| Sample Sent | 5 days |
| Call Booked | 7 days |
| Proposal Sent | 14 days |
| Paid | 7 days (to start delivery) |
| Delivered | 7 days (to retainer ask) |
| Retainer | rolling monthly |

After the time limit, the deal is either advanced, moved to Lost, or
escalated to the founder with an explicit reason.

## Loss Reasons (controlled vocabulary)

- `out_of_icp`
- `no_budget`
- `no_authority`
- `wrong_timing`
- `chose_competitor`
- `chose_internal`
- `price_objection`
- `trust_concern`
- `unresponsive`
- `policy_decline` (we declined them)

Loss reasons are entered into the Friction Log monthly.

## Win Sub-Categorisation

When a deal moves to Paid, also tag with a Revenue Quality Tier (A/B/C/D)
from `REVENUE_MODEL.md`.

## Anti-Patterns

- Skipping stages "because we already know them".
- Marking a deal Paid before money is in the bank.
- Marking a deal Lost without a controlled-vocabulary loss reason.
- Re-opening Lost deals more than once without new evidence.
