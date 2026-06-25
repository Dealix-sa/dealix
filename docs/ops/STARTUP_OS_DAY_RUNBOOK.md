# Dealix Startup OS Day Runbook

## Purpose

Startup OS Day is the daily operating workflow for Dealix as a founder-led Saudi B2B AI Operating Systems company.

It turns account pipeline data into:

- prioritized commercial queue
- Sales Agent and Company Brain packs
- founder review actions
- startup command center
- founder daily brief
- proof pack
- frontend snapshots

## Command

```bash
python scripts/commercial/run_startup_os_day.py
```

## Inputs

- `data/commercial/lead_pipeline.csv`
- `data/commercial/startup_os_product_matrix.json`
- `data/commercial/startup_os_operating_config.json`

## Generated reports

- `reports/commercial/sales_agent_company_brain/latest.md`
- `reports/commercial/review_actions/latest.md`
- `reports/startup_command_center/latest.md`
- `reports/founder_daily_brief/latest.md`
- `reports/startup_proof_pack/latest.md`

## Frontend snapshots

- `apps/web/lib/commercial-command-snapshot.ts`
- `apps/web/lib/startup-command-snapshot.ts`
- `apps/web/lib/founder-daily-brief-snapshot.ts`

## Frontend pages

- `/app/command-room`
- `/app/startup-command`
- `/app/founder-brief`

Actual route prefix depends on the Next.js app route grouping and deployment configuration.

## Daily founder rhythm

1. Run Startup OS Day.
2. Open Startup Command Center.
3. Review top P1 accounts.
4. Prepare three discovery notes.
5. Create one scoped diagnostic proposal only after qualification.
6. Update HubSpot or local ledgers after every founder action.
7. Generate proof notes after every paid sprint.

## Safety rules

- No fake ROI.
- No fake testimonials.
- No guaranteed revenue claims.
- No live outbound by default.
- No WhatsApp live send by default.
- No SMS by default.
- `source_url` is required.
- Pain statements remain hypotheses until verified.
- Owner review is required before sensitive external action.

## Validation

```bash
python scripts/commercial/run_startup_os_day.py
python -m pytest -q tests/saas/test_startup_command_center_assets.py tests/saas/test_startup_os_day_assets.py
npm --prefix apps/web run verify || true
```

## Done criteria

- Startup command report generated.
- Founder daily brief generated.
- Proof pack generated.
- Frontend snapshots generated.
- Safe defaults remain present.
- No external system was changed by the workflow.
