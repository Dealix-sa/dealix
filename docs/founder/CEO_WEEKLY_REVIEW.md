# CEO Weekly Review

Friday afternoon, 90 minutes. The single most important ritual in the
[CEO_OPERATING_SYSTEM](CEO_OPERATING_SYSTEM.md). Source of truth for the
question set and scorecard rubric:
[`dealix/execution_assurance/registry.yaml`](../../dealix/execution_assurance/registry.yaml).

## Inputs

| Input | Source |
|---|---|
| Weekly scorecard | `scripts/founder_weekly_scorecard.py` → `data/founder_briefs/weekly_scorecard_<date>.md` |
| KPI snapshot | `kpis_targets` in [`dealix/execution_assurance/registry.yaml`](../../dealix/execution_assurance/registry.yaml) |
| Decisions made this week | PRIVATE_OPS `ceo/decisions.jsonl` (filtered to last 7 days) |
| Bottlenecks resolved this week | `scripts/dealix_bottleneck_radar.py` output |
| Sector signals | [../strategy/BEACHHEAD_SECTOR_SCORECARD](../strategy/BEACHHEAD_SECTOR_SCORECARD.md) |

## Agenda (90 min)

### 1. Scorecard walkthrough — 20 min

Grade each machine on the 0–5 rubric in `scorecard_rubric_en`. Capture the
grades inline; commit them with the review note.

### 2. Question set — 30 min

Walk every question in `weekly_ceo_review_questions_en`. For each: write a
one-sentence answer + the decision (if any) it implies. Decisions go into
PRIVATE_OPS `ceo/decisions.jsonl` via
[`scripts/founder_decision_log_append.py`](../../scripts/founder_decision_log_append.py).

### 3. Capital adjustments — 15 min

Open [../finance/CAPITAL_ALLOCATION_SYSTEM](../finance/CAPITAL_ALLOCATION_SYSTEM.md).
For each bucket: keep / increase / decrease / kill. Append to PRIVATE_OPS
`ceo/capital_allocations.csv`.

### 4. Assumptions re-grade — 15 min

Re-grade the top 5 entries in
[STRATEGIC_ASSUMPTIONS_REGISTER](STRATEGIC_ASSUMPTIONS_REGISTER.md). For each:
`still valid`, `weakening`, or `falsified` — kill anything falsified.

### 5. Scale / Fix / Kill — 10 min

Pick one initiative for each verb. Append the call to the decision log with
a one-line "why".

## Outputs

- `data/founder_briefs/ceo_weekly_review_<week_end>.md` (committed weekly via workflow)
- N new entries in PRIVATE_OPS `ceo/decisions.jsonl`
- Updated PRIVATE_OPS `ceo/strategic_assumptions.csv` (`last_reviewed` bumped, `status` adjusted)
- Updated PRIVATE_OPS `ceo/capital_allocations.csv` (if any bucket changed)

## Cadence

- Friday 14:00 KSA (manual)
- Workflow trigger: weekly Monday 06:00 KSA via [`founder_ceo_hypergrowth.yml`](../../.github/workflows/founder_ceo_hypergrowth.yml) — generates the *next* week's pre-filled template

## Failure mode

If you miss a Friday: the next-Monday workflow still drops a pre-filled
template. Run the review on Monday morning before the daily brief. Two
missed Fridays in a row triggers a `WARN` in the verifier.

## Non-negotiables

No external messages are sent as part of the review. No payment terms are
committed. See [DO_NOT_SAY](DO_NOT_SAY.md).
