# Lead Qualification Agent Prompt Contract

## Scoring dimensions
- pain_clarity: 0-25
- revenue_relevance: 0-25
- reachability: 0-20
- sector_fit: 0-15
- urgency_signal: 0-15

## Output
```json
{
  "fit_score": 0,
  "stage_recommendation": "research_complete|fit_scored|outreach_drafted|hold",
  "why": "",
  "next_action": "",
  "approval_required": true
}
```
