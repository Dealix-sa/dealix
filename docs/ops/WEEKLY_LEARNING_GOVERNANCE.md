# Weekly Learning Governance

## Purpose
Force each week to end with a recorded learning decision and one durable system update.

## Cadence
Once per week, at the end of the sprint week.

## Inputs
- `dealix-ops-private/sprint/sprint_scorecard.csv`
- `dealix-ops-private/sprint/daily_execution_log.md`
- `dealix-ops-private/founder/daily_brief.md`
- `dealix-ops-private/founder/decision_queue.md`
- `dealix-ops-private/pipeline/pipeline_tracker.csv`
- `dealix-ops-private/revenue/revenue_action_log.csv`

## Output
- `dealix-ops-private/learning/weekly_intelligence_review.md` (this week's entry).
- One commit on the public repo that updates a playbook, control system, or template.

## Review Format

### 1. What moved revenue this week?
- Leads added, DMs sent, replies, samples, proposals, payments.

### 2. What blocked revenue this week?
- Specific objections, channels, ICP misfits, scope drift.

### 3. What did we learn about ICP / message / offer?
- Evidence over hypothesis.

### 4. One learning decision
- A single sentence describing the change to make.

### 5. One system update
- The file or playbook updated to reflect the learning.
- Linked commit hash.

## Governance Rules
- No week ends without a learning decision.
- No week ends without one committed system update or an explicit "no change, here is why".
- Verifiers (`scripts/verify_priority_operating_layer.py`, `scripts/verify_priority_execution_sprint.py`) pass before close.

## Trust Note
Weekly learning never includes guaranteed forecasts. It records evidence and decisions, not promises.

## Last Reviewed
2026-05-23
