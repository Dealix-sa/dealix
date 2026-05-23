# Growth Strategist Agent

| Field | Value |
|---|---|
| Agent ID | `growth_strategist` |
| Scope | Maintain sector ranking, ICP segmentation, account scoring, trigger feed, buyer personas |
| Tools | Read: market intel sources, internal events. Write: growth CSVs, recommendations |
| Approval class | Internal; recommendations only |
| Eval suite | Scoring stability, ranking explainability, false-positive trigger detection |
| Kill switch | Per-machine |
| Audit | Every score change and recommendation logged |
| Owner | Founder + Distribution Operator |
| Allowed write targets | `growth/sector_targets.csv`, `growth/account_scores.csv`, `growth/target_segments.csv`, `growth/trigger_events.csv`, audit log |
| Never-auto actions | Engagement decisions, external sends |

## Responsibilities

1. Daily recompute of account scores and trigger events.
2. Weekly recompute of sector ranking and segments.
3. Surface significant changes in the daily brief.
4. Recommend sector promotions / exits.
5. Maintain buyer persona documents.

## Why this matters

The Growth Strategist is the eyes of the operating system. If it goes blind, distribution shoots into the dark.
