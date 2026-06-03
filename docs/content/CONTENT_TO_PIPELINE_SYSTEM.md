# Content → Pipeline System

## Purpose
Tie content effort to revenue. If content doesn't influence pipeline, it's a hobby.

## Tracking
For every published asset:
- Row in `content/published_log.csv`.
- After every conversation it influences, append to `content/content_pipeline_influence.csv`:
  - `date, asset, channel, leads_influenced, proposals_influenced, paid_influenced, notes`.

## Influence definition
- **Leads influenced** — a prospect who cites the asset in their outreach or in a conversation.
- **Proposals influenced** — a deal that progresses to proposal because of the asset.
- **Paid influenced** — a closed-won deal where the asset was a stated factor.

## Cadence
- Weekly: founder spends 10 min logging influence.
- Monthly: review which asset drove the most pipeline.

## Decision rules
- An asset with zero influence after 90 days is retired or rewritten.
- A high-influence asset is repurposed into a sector report, deck slide, or proposal language.

## Anti-patterns
- Vanity metrics (likes / impressions) used as the only signal.
- "Brand awareness" without a defined conversion path.
- Spending more than 20% of founder weekly time on content while pipeline < 25 leads.

## Outputs
- A weekly note in the CEO action queue if content yielded ≥ 1 proposal-influenced row.
- A quarterly retrospective of content ROI.
