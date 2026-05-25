# Delivery QA Score

## Purpose
Score every Revenue Sprint delivery before handoff.

## Score Areas
| Area | Points |
|---|---:|
| ICP fit | 20 |
| Evidence quality | 20 |
| Lead relevance | 20 |
| Outreach usefulness | 15 |
| Executive summary clarity | 10 |
| Trust safety | 10 |
| Next action clarity | 5 |

## Score Meaning
- 90–100 = excellent, can deliver.
- 75–89 = acceptable, fix minor issues.
- 60–74 = fix before delivery.
- below 60 = blocked.

## Automatic Blockers
- guaranteed revenue claim
- client data leak
- no evidence for A-priority leads
- wrong ICP
- unclear scope
- no next action

## Rule
No client delivery below 75.

## Log
Every QA pass is recorded in:
- delivery/qa_score_log.csv

## CSV Header (canonical)
```
date,client,icp_fit,evidence_quality,lead_relevance,outreach_usefulness,summary_clarity,trust_safety,next_action_clarity,total_score,status,notes
```

## Status Values
PASS / FIX / BLOCKED

## Trust Safety Sub-Checks
- no guaranteed revenue language
- no fabricated metrics
- no public data of private contacts
- no compliance promises Dealix does not own
- no client names used outside their approval
