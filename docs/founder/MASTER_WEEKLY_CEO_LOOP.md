# Master Weekly CEO Loop

## Purpose
A 60-minute Sunday-evening loop that closes the week, scores the company, and chooses the next bet.

## Step 1 — Refresh business score (10 min)
```
make business-score
```
Writes `business_audit/ceo_business_score.md` and appends to `business_audit/score_history.csv`.

## Step 2 — Refresh execution assurance (10 min)
```
make assurance
```
Writes `evidence/execution_assurance_report.md`. Flags any non-compliance with the daily loop.

## Step 3 — Run the weekly close (10 min)
```
make weekly-close
```
Appends to `metrics_history/weekly_metrics.csv`.

## Step 4 — Win/Loss review (10 min)
- Read `pipeline/win_loss_log.md`.
- Add one entry per won, lost, or stalled deal this week.
- Tag each entry with a learning.

## Step 5 — Choose next week's bet (15 min)
- Decide one bet for the week.
- Write it at the top of `founder/ceo_action_queue.md`.
- Add an experiment row to `experiments/market_experiments.csv` if applicable.

## Step 6 — One system improvement (5 min)
- Identify one friction in the system.
- File it (commit) as a doc, schema, or verifier update to the public repo.
- Or queue it in `productization/automation_backlog.md`.

## Output of the loop
A scored, learned, decided week. Everything else is noise.
