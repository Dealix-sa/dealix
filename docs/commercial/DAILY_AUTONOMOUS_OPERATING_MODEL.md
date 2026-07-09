# Dealix Daily Autonomous Operating Model

## What runs every day

After this workflow is merged into the default branch, GitHub Actions runs the Dealix Full Company OS daily at:

```text
05:17 UTC
08:17 Asia/Riyadh
```

The workflow is intentionally not scheduled exactly at the top of the hour to reduce delay/drop risk during high GitHub Actions load periods.

## Important GitHub Actions rule

Scheduled workflows run only when the workflow file exists on the repository default branch.

That means:

- While this work is still in PR #881, it can be reviewed and manually tested.
- After merge to `main`, the daily schedule becomes active.

## Daily loop

```text
GitHub Actions schedule
-> checkout repo
-> run Full Company OS draft-only cycle
-> verify Full Company OS guardrails
-> run First Paid Client path
-> verify revenue/payment guardrails
-> render GitHub issue body
-> create or update today's Dealix Daily Command issue
-> upload artifacts
```

## What the issue contains

Each daily issue includes:

- generated timestamp,
- opportunities scored,
- drafts pending founder review,
- approval queue items,
- proof events,
- self-improvement items,
- first paid client path status,
- revenue eligibility status,
- founder checklist.

## What it can do without founder intervention

- Run daily.
- Score safe seed/founder-provided targets.
- Generate draft messages.
- Generate approval queue.
- Generate proof log.
- Generate self-improvement recommendations.
- Generate first paid client path status.
- Create or update an internal GitHub issue.
- Upload internal artifacts.

## What it must not do without founder intervention

- Send WhatsApp, email, SMS, or LinkedIn messages.
- Publish posts.
- Charge customers.
- Mark revenue received without payment evidence.
- Mark closed-won without proof pack delivery.
- Merge PRs.
- Deploy or mutate production.
- Print secrets.
- Scrape prohibited sources.

## Why this is the right autonomy level

This gives Dealix daily operating leverage without creating legal, compliance, or brand risk.

The system does the thinking, scoring, drafting, reporting, and queueing.
The founder keeps approval over external actions.

## Commands run by CI

```bash
python scripts/commercial/run_full_company_os.py --client dealix --mode draft-only --limit 10 --json
python scripts/commercial/verify_full_company_os.py
python scripts/commercial/run_first_paid_client_path.py
python scripts/commercial/verify_first_paid_client_path.py
python scripts/commercial/render_full_company_os_issue.py --output reports/full_company_os/daily_issue.md
```

## Issue behavior

The workflow searches for an open issue titled:

```text
Dealix Daily Command - YYYY-MM-DD
```

If it exists, the workflow updates it.
If it does not exist, the workflow creates it.

Labels:

```text
daily-command
dealix-os
safe-draft
```

## Activation checklist

1. Review PR #881.
2. Let CI run.
3. Merge into `main` only if checks are green.
4. Confirm GitHub Actions is enabled in repository settings.
5. Confirm Actions token has issue write permission or repository Actions settings allow `GITHUB_TOKEN` to create issues.
6. Check the next daily issue after 08:17 Riyadh.

## Scaling later

Future PRs can add controlled integrations in this order:

1. Airtable/Sheets import for safe target cards.
2. Gmail draft creation only.
3. Slack internal report only.
4. CRM read-only enrichment.
5. CRM draft task creation.
6. Controlled live outbound only after explicit policy, opt-out, rate limits, audit log, and kill switch.
