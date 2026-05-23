# Private Ops Templates

## Purpose
This folder ships the starter files for the private operations repo
(`dealix-ops-private`). Files here never contain customer data — they are
empty templates the founder copies into the private repo on day one of the
Priority Execution Sprint.

## How to use

Assuming the private operations repo is checked out alongside this one as
`../dealix-ops-private`:

```bash
cp -r private_ops_templates/. ../dealix-ops-private/
cd ../dealix-ops-private
python verify_priority_sprint.py
python verify_daily_gate.py
python verify_revenue_actions.py
```

After copying, the founder fills in:
- `pipeline/pipeline_tracker.csv` (25 leads on Day 1)
- `sprint/current_sprint.md` (sprint dates + targets)
- `sprint/sprint_scorecard.csv` (daily actuals)
- `revenue/revenue_action_log.csv` (one row per revenue action)
- `founder/daily_brief.md` (morning brief)
- `founder/approvals_waiting.md` (approvals queue)
- `founder/decision_queue.md` (open decisions)
- `learning/weekly_intelligence_review.md` (end-of-week)

## Non-Negotiable
- These templates contain placeholder text only.
- Customer data, leads, contacts, and amounts must live in the private repo only.
- The public repo (`dealix`) must never receive customer data.
