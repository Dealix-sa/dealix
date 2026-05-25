# Delivery Analyst Scorecard

> 90-day evaluation. Quality is the metric.

## Period
- Start date: yyyy-mm-dd
- End date: yyyy-mm-dd (90 days later)
- Reviewer: founder

## Core Metrics

| Metric | Target (90d) | Actual |
|--------|--------------|--------|
| Sprints supported (research → memo draft) | 9–12 | |
| Founder edits per memo (lower = better) | ≤ 5 substantive | |
| QA pass rate of drafts on first review | ≥ 80% | |
| Time-to-draft per Sprint | ≤ 5 working days | |
| Hallucination incidents | 0 | |
| Evidence-link completeness | 100% | |
| Founder hours saved per week | ≥ 12 | |

## Quality Checks (audit each Sprint)

- Every A-priority account has linked evidence.
- No overclaim language in drafts.
- Bilingual quality acceptable (or honestly flagged when not).
- Memo passes the QA checklist on second pass.

## Outcomes Map

| 90-day result | Decision |
|---------------|----------|
| Metrics ≥ 90% + 0 hallucination incidents | Extend 6 months |
| Metrics 70–89% + 0 incidents | Extend 90 days with named focus area |
| Metrics < 70% or any hallucination incident | End amicably |

## Documentation

- `dealix-ops-private/people/scorecards/delivery_analyst/<name>/<period>.md`
- Includes: per-Sprint quality scores, hallucination audit, founder
  observations.

## Anti-Patterns

- Counting "Sprints touched" instead of Sprints passed QA.
- Allowing hallucination incidents to be "almost not customer-facing".
- Extending past 90 days without a written decision.
