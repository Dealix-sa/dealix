# Pipeline Stages

Canonical pipeline. Every prospect lives in exactly one stage at a time.

| # | Stage | Definition | Exit criterion |
|---|---|---|---|
| 1 | New | Identified, not contacted | Enrichment + ICP score complete |
| 2 | Qualified | Passes ICP filter | Approved for outreach |
| 3 | Contacted | First message sent | Acknowledged or follow-up due |
| 4 | Replied | Prospect responded | Sample or call discussion opened |
| 5 | Sample Sent | Free / 199 signal sample delivered | Sample reviewed by prospect |
| 6 | Call Booked | Discovery call scheduled | Call held |
| 7 | Proposal Sent | Written proposal sent | Accept / reject / negotiation |
| 8 | Paid | Invoice paid | Delivery kicked off |
| 9 | Delivered | Engagement closed | Feedback collected |
| 10 | Retainer | Recurring contract active | Renewal review |
| 11 | Lost | Closed lost | Reason logged, suppression check |

## Movement rules
- A prospect cannot skip from stage 1 to stage 7. Each stage has an exit criterion.
- A prospect can move to Lost from any stage. The reason must be logged.
- Stage 8 (Paid) is the only trigger for full delivery work.
- Stage 10 (Retainer) is the north star. Every Sprint is designed to make this stage reachable.

## Reporting
- Weekly: count and value per stage.
- Weekly: conversion rate between adjacent stages.
- Monthly: aging report — prospects stuck > 14 days in any stage.
