# Customer Success Agent Prompt Contract

## Health score
- usage: 0-30
- outcome: 0-30
- relationship: 0-20
- risk: -20 to 0

## Output
```json
{
  "health_score": 0,
  "status": "green|yellow|red",
  "risks": [],
  "expansion_opportunities": [],
  "next_customer_action": ""
}
```
