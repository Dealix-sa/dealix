# Sales Funnel

> Every stage a lead passes through, what triggers a stage move, what kills the lead.

## The Funnel

```
Lead → Qualified → Contacted → Replied → Sample Sent → Call Booked
                                                            │
                                                            ▼
                              Proposal Sent → Paid → Delivered → Retainer
```

## Stage Definitions + Triggers

| Stage | Definition | Move-in trigger | Move-out trigger | Kill trigger |
|---|---|---|---|---|
| **Lead** | Identified prospect, not contacted | Source agent adds row | Fit score ≥ 60 | Fit score < 40 → suppression |
| **Qualified** | Passes ICP + fit score | Score ≥ 60 + enriched | First outreach drafted | Disqualifier hit |
| **Contacted** | First message sent | Founder-approved send | Reply OR 7 days silence | 3 messages no reply → nurture |
| **Replied** | Prospect engaged | Reply logged | Sample/call requested | Negative reply → suppression |
| **Sample Sent** | Sanitized sample artifact shared | Founder approves sample | Call booked | 14 days silence → nurture |
| **Call Booked** | Calendar slot held | Calendar event created | Proposal sent | No-show twice → suppression |
| **Proposal Sent** | Productized proposal delivered | Founder signs proposal | Paid invoice | 21 days no decision → ask, then close-lost |
| **Paid** | Invoice cleared | Payment confirmation | Delivery starts | Refund inside policy window |
| **Delivered** | Sprint complete, evidence pack handed off | Handoff doc signed | Retainer convo opens OR closed-won-final | n/a |
| **Retainer** | Recurring contract signed | First retainer invoice paid | Renewal OR churn | Churn → close-lost with reason |

## Conversion Targets (per stage transition)

| Transition | Target rate |
|---|---|
| Lead → Qualified | 50% |
| Qualified → Contacted | 90% |
| Contacted → Replied | 15% |
| Replied → Sample Sent | 60% |
| Sample → Call | 40% |
| Call → Proposal | 70% |
| Proposal → Paid | 35% |
| Paid → Delivered | 100% |
| Delivered → Retainer | 30% |

Compound conversion Lead → Retainer target this quarter: ~0.6%. That means **170 quality leads to land 1 retainer**. Plan accordingly.

## Funnel Hygiene Rules

1. Every lead has exactly one stage at any time
2. Every stage move gets logged in `pipeline/pipeline_tracker.csv` (private)
3. No lead sits in any stage > 30 days without a logged action — auto-flagged for review
4. No lead skips stages (no jumping straight from Lead → Proposal)
5. Closed-lost / suppressed leads stay in the ledger forever (no deletion)

## Anti-Patterns (forbidden)

- "Updating stages in bulk" — every change is a logged action
- Pushing leads to later stages to inflate pipeline
- Marking dead leads as "nurture" indefinitely → use suppression
- Re-engaging suppressed leads without a fresh consent signal

## Funnel Review Cadence

- Daily: stage moves (Daily Brief section 2)
- Weekly: conversion rates per transition (Weekly Review GTM section)
- Monthly: funnel shape analysis — where do leads stall the most?

## When A Stage Conversion Misses Target

Diagnosis order:
1. Check the input quality (was the prior stage's leads actually qualified?)
2. Check the artifact quality (message, sample, proposal — what does the prospect see?)
3. Check the timing (is the follow-up cadence right?)
4. Check the offer (is the rung priced right for the segment?)
5. If still missing → escalate to Weekly CEO Review with hypothesis

Don't add stages. Don't add features. Diagnose first.
