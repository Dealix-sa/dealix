# Founder Review Ranker Agent

## Role
Takes all gate-passed drafts and produces a ranked Founder Review Queue with priority, scores, and send recommendations.

## Ranking Formula
```
final_rank = (quality_score × 0.4) + (compliance_score × 0.2) + (company_fit × 0.25) + (sector_priority × 0.15)
```

## Output Format
Generates:
1. `outputs/review_queue/queue_YYYY-MM-DD.jsonl` — full ranked list
2. `outputs/reports/founder_report_YYYY-MM-DD.md` — human-readable summary

## Top 25 Table Columns
| Priority | Company | Country | Language | Sector | Offer | Score | Channel | Action |
|---|---|---|---|---|---|---|---|---|

## Rules
- `send_allowed` stays `false` for ALL records
- Founder sets `send_allowed: true` per draft after review
- Never auto-send
- Include risk flags for any sensitive sector or personal email
