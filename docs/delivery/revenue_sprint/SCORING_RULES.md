---
title: Revenue Sprint Lead Scoring Rules
owner: Revenue Lead
status: active
cadence: review-monthly
last_review: 2026-05-23
---

# Revenue Sprint Lead Scoring Rules

A lead must score above the qualification threshold to enter the Reached stage of the pipeline. The scoring rules are deliberately simple. They do not predict revenue; they filter out work that should not be done.

## Scoring rubric

| Signal | Points | How it's checked |
|---|---|---|
| Named decision-maker (role + name) | 2 | Public link in `pipeline_tracker.csv` |
| Sector code matches an active focus sector | 2 | Sector field present |
| Public statement of a relevant bottleneck | 2 | Quote captured |
| Buyer is reachable via a compliant channel | 1 | Channel logged; cold WhatsApp is forbidden |
| Buyer's organisation is the right size | 1 | Headcount band recorded |
| No PDPL red flag on the public profile | 1 | Trust Lead sanity-check |

Threshold: **6 points or higher** to advance past Sourced.

## Disqualification rules

- The lead is on a closed platform that prohibits scraping. Disqualified.
- The lead is a regulator, journalist, or competitor probing. Disqualified.
- The lead has previously asked not to be contacted. Permanently disqualified.

## How the score is recorded

- Score lives in the `pipeline_tracker.csv` row for the lead.
- The score timestamp is logged in the AI Run Ledger.
- Re-scores are allowed weekly; older scores are overwritten with the new value and the prior value is in the ledger.

## Owner

Revenue Lead. Reviewed monthly with the Trust Lead.
