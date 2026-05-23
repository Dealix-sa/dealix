# Daily Execution Gate

## Purpose
Prevent Dealix from ending the day without measurable execution.

## Daily PASS Conditions

| Area | PASS Condition | Evidence |
|---|---|---|
| Pipeline | Every active lead has stage and next_action | pipeline/pipeline_tracker.csv |
| Revenue | At least one revenue-moving action completed | sprint/daily_execution_log.md |
| Trust | Approval queue reviewed | founder/approvals_waiting.md |
| Delivery | Any active delivery has QA status | delivery/qa/ |
| Learning | One observation recorded | sprint/daily_execution_log.md |

## Daily Close Questions
- What moved revenue today?
- What blocked revenue today?
- What trust risk appeared?
- What delivery risk appeared?
- What should be fixed tomorrow?

## Rule
No day closes without:
1. Pipeline update.
2. Revenue action.
3. Trust review.
4. End-of-day note.
