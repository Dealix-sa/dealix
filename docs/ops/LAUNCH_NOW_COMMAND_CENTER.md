# Dealix Launch Command Center

This runbook gives Dealix one controlled launch surface across backend, frontend, data intelligence, revenue, command room, and Railway checks.

## Purpose

Dealix has many useful operating scripts. Launch Command Center reduces launch risk by running the important gates in one ordered flow and writing a clear verdict to `reports/launch/latest.md`.

## Operating doctrine

- Internal launch can proceed only when required gates pass.
- Public launch waits for frontend, Railway, and Docker build gates.
- Riyadh targeting is review-first.
- Data Intelligence results must be reviewed before they move to the canonical prospects ledger.
- No automatic external action is enabled by this runbook.

## Commands

Internal launch gate:

```bash
python scripts/launch/run_launch_now.py
```

Full product launch gate:

```bash
python scripts/launch/run_launch_now.py --include-frontend --include-docker
```

Data Intelligence only:

```bash
python scripts/intelligence/run_data_intelligence_day.py
```

Revenue and command room after founder review:

```bash
make revenue-daily
make command-room
```

## Verdicts

`GO_INTERNAL_MANUAL` means the system is ready for internal Riyadh research, manual review, and founder-reviewed daily operations.

`BLOCKED` means at least one required gate failed and must be fixed before launch.

## Expected outputs

- `reports/launch/latest.md`
- `reports/launch/latest.json`
- `reports/intelligence/latest.md`
- `reports/intelligence/latest.json`
- `ledgers/riyadh_exa_prospects.csv`

## Launch sequence

1. Pull latest `main`.
2. Add secrets only to Railway/GitHub/local env.
3. Run Launch Command Center.
4. Review Riyadh intelligence rows.
5. Move approved rows into `ledgers/prospects.csv`.
6. Run `make revenue-daily`.
7. Run `make command-room`.
8. Use drafts manually only after founder approval.

## Do not do

- Do not commit real keys.
- Do not bypass failed required gates.
- Do not treat dry-run rows as verified leads.
- Do not activate external channels from this flow.
- Do not merge stale PRs just because they are old.
