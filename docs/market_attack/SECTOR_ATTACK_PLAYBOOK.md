# Sector Attack Playbook

> The repeatable 90-day playbook to attack a locked beachhead sector.

## Day 0 — lock the beachhead

- Top sector from `beachhead_sector_scorecard.csv` → priority `P0`.
- Founder writes a one-line **sector thesis** into
  `MARKET_LEARNING_MEMORY.md`: *"Why this sector, this offer, this
  90-day window."*

## Days 1-14 — proof-safe authority

- Authority engine emits 6-8 founder posts scoped to the sector.
- Each post pulls from `authority/sector_insights.csv`. No claim posts
  without `evidence` populated.
- Sector one-pager and proof-safe sample asset are drafted (status:
  `draft` → `approval_required`).

## Days 15-30 — warm motion

- Strategic Account List filtered to the sector → top 25 accounts.
- Each account receives an approved outreach draft routed through the
  campaign queue (`approval_class = founder_review`).
- Partner pipeline filtered for the sector; 5 partner conversations
  opened.

## Days 31-60 — paid offers

- First 5 paid Managed Pilot proposals sent.
- Conversion Command Room (`make campaign-command`) reviewed weekly.
- Objection intelligence runs after every lost deal.

## Days 61-90 — scale or pivot

- Re-score the beachhead.
- Decide: `scale`, `expand to adjacent sector`, or `pivot`.
- Postmortem the campaigns and roll learnings into
  `MARKET_LEARNING_MEMORY.md`.

## Hard rules

- No automation sends without founder approval.
- No proof published without proof-pack validation.
- No discount or contract terms outside the offer ladder.
- No claim like "guaranteed leads", "guaranteed revenue", "we will get
  you customers" — replaced by *"we run the system, the system produces
  signals, the signals are reviewed and acted on with you"*.
