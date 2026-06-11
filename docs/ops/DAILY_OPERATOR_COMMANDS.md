# Daily Operator Commands

## Quick Start
```bash
# Demo mode (no external APIs needed)
python3 scripts/dealix_daily_operator.py --mode demo

# Production mode (requires leads CSV)
python3 scripts/dealix_daily_operator.py --mode production --leads data/imports/leads.csv
```

## What It Does
1. Scans for secrets
2. Verifies core files exist
3. Imports/scores leads
4. Generates outreach drafts (pending review)
5. Queues follow-ups
6. Builds prospect pack
7. Generates proposal for top account
8. Writes CEO brief
9. Writes pipeline report
10. Outputs operator summary

## Outputs
- `reports/operator/dealix-daily-operator-YYYY-MM-DD.md`
- `business/reports/exports/dealix-daily-ceo-brief-YYYY-MM-DD.txt`
- `business/crm/exports/`
- `business/persuasion/exports/`
- `business/sales-machine/exports/`
- `business/proposals/generated/`

## Safety
- No auto-send
- All drafts pending_review
- Demo mode clearly labeled
