# Dealix Master Stable Company OS

## Purpose
A stable daily business operating layer for Dealix.

It prepares:
- lead queue
- prospect scoring
- approval queue
- CRM rows
- CEO report
- weekly board report
- next founder actions

## It does not
- run Docker
- run heavy frontend build
- auto-send WhatsApp
- auto-send email
- issue invoices
- sign contracts
- merge PRs
- commit generated daily outputs

## Daily founder workflow
1. Run `./scripts/dealix_master_stable_day.sh`
2. Open the CEO report
3. Open the approval queue
4. Approve/send top 20 manually
5. Update CRM statuses
6. Push paid Diagnostic Sprint for warm leads
