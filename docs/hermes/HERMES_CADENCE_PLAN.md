# Hermes Cadence Plan

Hermes starts in review-only mode. The purpose is to create useful founder-visible artifacts on a predictable schedule before any live automation is considered.

## Recommended rhythm

| Rhythm | Owner | Output |
| --- | --- | --- |
| Hourly review | Revenue Scout | Opportunity watchlist |
| Every 6 hours | Ops Guardian | Readiness and risk notes |
| Daily 08:00 Asia/Riyadh | Hermes Supervisor | Founder digest inputs |
| Daily 17:00 Asia/Riyadh | Market and Finance agents | Market, pricing, and cost notes |
| Pull request review | Product QA and Security Sentinel | Quality and security notes |
| Weekly Sunday 09:00 | Hermes Supervisor | Strategic priority queue |

## Artifact locations

Suggested local paths:

- `data/hermes/revenue_watchlist.jsonl`
- `data/hermes/ops_health.jsonl`
- `data/hermes/founder_digest.md`
- `data/hermes/market_finance_digest.md`
- `data/hermes/pr_reviews.jsonl`
- `data/hermes/weekly_strategy.md`

These paths are recommendations for future implementation. This PR does not create live scheduled jobs.

## Founder review loop

1. Agent prepares an artifact.
2. Hermes Supervisor summarizes the artifact.
3. Founder reviews the recommendation.
4. Approved items become normal GitHub issues, PRs, or manual work items.
5. Unclear or risky items are held for review.

## Initial rollout

1. Keep Hermes in review-only mode.
2. Run the local AI gateway from the AI workflow foundation.
3. Generate artifacts locally first.
4. Add CI or scheduled jobs only after the artifacts are useful and safe.
