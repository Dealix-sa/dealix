# Dealix Machines

## Purpose

Define internal workers that run the 24/7 Dealix Growth Factory.

## Machines

- market_intelligence
- lead_discovery
- enrichment
- scoring
- outreach_drafting
- approval_queue
- send_queue
- followup
- reply_router
- sample_factory
- proposal_factory
- finance_followup
- delivery_trigger
- content_proof
- ceo_reporting

## Rule

Machines may prepare and route.
Machines may not make A2/A3 external commitments automatically.

## Layout

Each machine is a thin module under `machines/` that wraps existing scripts
in `scripts/` or `dealix_cli`. The orchestration entry points live in:

- `scripts/run_growth_hourly.py`
- `scripts/run_growth_4h.py`
- `scripts/run_growth_daily.py`

These are scheduled on the server via `deploy/cron/dealix_crontab.example`.
