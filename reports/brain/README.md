# Company Brain OS — Reports

This directory holds generated reports from the Company Brain OS engine.

## What the Brain produces

| Report | Script | Cadence |
|--------|--------|--------|
| Brain Day Summary | `scripts/brain/run_brain_day.py` | Daily |
| Weekly Board Memo | `scripts/brain/generate_weekly_board_memo.py` | Weekly |
| 30-Day Action Plan | `scripts/brain/generate_30_day_action_plan.py` | Rolling |
| Future Radar | `scripts/brain/generate_future_radar.py` | On demand |

## Guardrails

The Company Brain OS is governed by four non-negotiable principles:

1. **No deterministic future predictions.** Every forward-looking statement is
   expressed as a *scenario* (base / upside / downside).
2. **Every scenario carries an explicit confidence level** (low / medium /
   high). Confidence reflects the strength of evidence, not a probability
   guarantee.
3. **No guaranteed ROI.** The brain never claims a specific return is
   guaranteed.
4. **No automatic external action.** The brain only recommends; humans act.

## Decision schema

Every decision in `ledgers/decisions_log.csv` must include these fields:

- `decision` — what is being decided
- `why_now` — why this decision is time-sensitive
- `assumption` — the key assumption underpinning the decision
- `confidence` — low / medium / high
- `owner` — accountable person
- `next_action` — the immediate next step
- `success_metric` — how the outcome will be measured
- `review_date` — when the decision will be revisited
- `risk_if_delayed` — what happens if no action is taken

## Running a brain day

```bash
python -m scripts.brain.run_brain_day
```

This builds the brain map, detects bottlenecks, generates a decision, writes the
weekly memo and 30-day plan, and drops a summary report in this directory.

## Seeding demo data

```bash
python -m scripts.brain.seed_demo_brain_data
```

Populates all six ledgers with a small set of demo rows for testing.

## Ledgers

| Ledger | Path | Purpose |
|--------|------|---------|
| Company Signals | `ledgers/company_signals.csv` | Observed signals (revenue, churn, etc.) |
| Decisions Log | `ledgers/decisions_log.csv` | Every decision with required fields |
| Assumptions Log | `ledgers/assumptions_log.csv` | Key assumptions and their evidence |
| Experiments Log | `ledgers/experiments_log.csv` | Hypotheses being tested |
| Risk Register | `ledgers/risk_register.csv` | Identified risks and mitigations |
| Opportunity Register | `ledgers/opportunity_register.csv` | Opportunities with scenarios |