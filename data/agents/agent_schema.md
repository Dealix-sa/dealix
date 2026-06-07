# Agent Data Schema

## task_queue.json fields
- id
- created_at
- role
- priority
- input
- status: queued|running|needs_approval|done|rejected
- output_path

## agent_runs.jsonl fields
- run_id
- task_id
- role
- started_at
- finished_at
- status
- output_summary
- risk_level
- approval_required

## approvals.jsonl fields
- approval_id
- task_id
- approver
- decision
- notes
- timestamp
