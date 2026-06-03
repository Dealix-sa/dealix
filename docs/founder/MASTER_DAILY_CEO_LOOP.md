# Master Daily CEO Loop

## Purpose
A 15-minute morning loop that aligns the founder with the operating system before any other work.

## Step 1 — Refresh control tower (3 min)
```
make control-tower
```
Reads inputs, writes `founder/control_tower_brief.md`.

## Step 2 — Refresh action queue (3 min)
```
make ceo-action-queue
```
Reads inputs, writes `founder/ceo_action_queue.md`.

## Step 3 — Refresh mission control (3 min)
```
make mission-control
```
Reads inputs, writes `founder/mission_control.md`.

## Step 4 — Choose ONE top action (1 min)
Open `founder/ceo_action_queue.md` and circle the top item. Do not start anything else until it's moved.

## Step 5 — Move money or learning (rest of the morning)
Spend the next 2–3 uninterrupted hours on the top action. Track effort in `experiments/market_experiments.csv` if it is a market move.

## Daily evening close (5 min)
- Log every action taken in `revenue/revenue_action_log.csv`.
- Log any evidence in `evidence/execution_evidence_ledger.csv`.
- Note tomorrow's intended top action in `founder/ceo_action_queue.md` (top of file).

## What this loop is NOT
- Not a planning meeting.
- Not a place for new ideas (those go to `content/content_ideas.md`).
- Not optional.

## Failure mode
If the loop is skipped for 2 days in a row, the next weekly close adds a `loop_skip` event to `evidence/execution_evidence_ledger.csv` and asks for a written reason.
