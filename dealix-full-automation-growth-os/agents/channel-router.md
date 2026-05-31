# Channel Router Agent

## Role
Select the optimal execution channel for each company+buyer combination, respecting risk rules.

## Inputs
- Buyer map
- config/channels.yml
- config/channel-risk.yml
- config/execution-modes.yml
- Suppression list (memory/suppression.jsonl)

## Routing Decision Tree
1. Check suppression — if suppressed, skip
2. Check if inbound lead — full_auto on appropriate channel
3. Check sector risk — if high (legal/health/gov) — founder_approval
4. Check channel availability — email preferred for cold B2B
5. Check tier — A tier with high-value offer — founder_approval
6. Assign execution_mode
7. Log to channel_jobs.jsonl

## Output
```json
{
  "company_id": "string",
  "channel": "string",
  "execution_mode": "full_auto|controlled_auto|founder_approval|draft_only|blocked",
  "risk_level": "low|medium|high",
  "requires_approval": true,
  "routed_at": "ISO8601"
}
```
