# Dealix Daily Self Runner

The Daily Self Runner makes Dealix operate by itself on a safe schedule. It runs inside GitHub Actions every morning and can also be started manually.

## What it does automatically

- chooses the best available free/low-cost LLM provider stack for coding, Arabic, batch drafting, and sensitive work boundaries;
- runs the Dealix Daily Operator;
- refreshes lead scoring, draft queues, follow-ups, prospect packs, proposal material, CEO brief, and pipeline report when the underlying scripts are available;
- runs draft quality checks and distribution metrics when available;
- writes reports under `reports/autopilot/` and uploads artifacts from GitHub Actions.

## What it does not do automatically

- it does not send customer-facing messages;
- it does not approve outreach;
- it does not commit pricing, contracts, legal statements, or regulated claims;
- it does not put private customer data into free providers by default;
- it does not store provider secrets in the repository.

## GitHub Actions schedule

Workflow:

```text
.github/workflows/dealix-daily-self-runner.yml
```

Schedule:

```text
07:15 Asia/Riyadh daily
```

Manual run:

1. Open GitHub Actions.
2. Select **Dealix Daily Self Runner**.
3. Click **Run workflow**.
4. Download the generated artifact after the run completes.

## Local run

```bash
python scripts/ops/dealix_daily_self_runner.py
```

## Daily founder review

After the workflow runs:

1. Open the latest artifact.
2. Review `reports/autopilot/daily-self-runner-YYYY-MM-DD.md`.
3. Review generated outreach queues and proposal material.
4. Approve only accurate, safe, non-overclaiming commercial actions.
5. Send through the approved Dealix path only.

## Why this is the right autonomy level

The system is autonomous for research, planning, drafts, checks, and report generation. It stops before actions that can create legal, commercial, privacy, or reputation risk. This keeps Dealix fast while preserving the approval-first operating model.
