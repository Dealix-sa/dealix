# Dealix Company Operating System

## What it is

The company operating system combines:
- Strategy and measurement
- Sales and revenue
- Delivery and service
- Compliance and trust
- Learning and improvement

## Daily rhythm

### Morning (30 min)
1. Run `make company-day`.
2. Review `reports/command_room/index.html`.
3. Review drafts in `outbox/YYYY-MM-DD/`.

### During the day
4. Manually send approved drafts.
5. Update `ledgers/outreach_log.csv` after each send.
6. Log replies in `ledgers/reply_log.csv`.

### Evening (15 min)
7. Update `ledgers/deals_pipeline.csv`.
8. Review `reports/revenue/YYYY-MM-DD/daily_ceo_report.md`.

## Source files

- `ledgers/prospects.csv` — opportunities
- `ledgers/deals_pipeline.csv` — pipeline
- `ledgers/outreach_log.csv` — sends
- `ledgers/reply_log.csv` — replies
- `data/outreach/saudi_icp_segments.json` — ICP segments
- `scripts/revenue/run_daily_revenue_machine.py` — daily machine

## Outputs

- `outbox/YYYY-MM-DD/*.md` — drafts
- `reports/revenue/YYYY-MM-DD/` — reports
- `reports/command_room/index.html` — command dashboard

## How we sell

1. Identify operational pain.
2. Offer Diagnostic Sprint SAR 4,999.
3. Offer one-month Pilot SAR 14,999.
4. Move to monthly subscription after Pilot success.

## How we deliver

- Week 1: Discovery + data.
- Week 2: Build the small system.
- Week 3: Test + adjust.
- Week 4: Success report.

## How we measure proof

- baseline before Pilot.
- after after Pilot.
- Clear documented delta.

## Mistakes to avoid

- No guaranteed percentages.
- No sensitive data collection.
- No automatic external sending.
