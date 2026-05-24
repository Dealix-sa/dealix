# Strategic Assumptions Register

The list of falsifiable bets the company is currently making. Every bet has
an owner, a kill-trigger, and a `last_reviewed` date. Anything older than
30 days without re-grading is flagged stale by
[`scripts/strategic_assumptions_check.py`](../../scripts/strategic_assumptions_check.py).

Stored at `$DEALIX_OPS_PRIVATE/ceo/strategic_assumptions.csv`.

## CSV schema

| Column | Notes |
|---|---|
| `id` | Stable handle, e.g. `a-erp-icp-001` |
| `assumption` | One sentence, falsifiable, present tense |
| `owner` | `ceo`, contractor handle, or team |
| `kill_trigger` | The observable that invalidates it, with a date |
| `status` | `valid` / `weakening` / `falsified` |
| `last_reviewed` | ISO date — bumped at the weekly review |
| `notes` | Free text — supporting links or data |

## How an assumption is born

1. A decision in [DECISION_LOG_SYSTEM](DECISION_LOG_SYSTEM.md) implies one or more bets
2. The CEO writes each bet as a falsifiable sentence
3. Each bet gets a kill-trigger ("If X by date D, this is falsified")
4. The CSV is updated via PRIVATE_OPS write

## Examples

| id | assumption | kill_trigger |
|---|---|---|
| `a-erp-icp-001` | ERP implementers are our highest-yield beachhead sector | < 2 paid samples from ERP firms by 2026-07-31 |
| `a-li-conv-001` | LinkedIn outbound converts at ≥ 4% positive reply on Saudi B2B | 4-week rolling positive-reply rate < 2% |
| `a-sample-throughput-001` | Sample factory can produce 10 samples/week with one contractor | < 5 samples/week for two consecutive weeks |

## Weekly cadence

Top 5 assumptions are re-graded during [CEO_WEEKLY_REVIEW](CEO_WEEKLY_REVIEW.md).
Stale assumptions (>30 days) auto-surface in the daily brief.

## API surface

- `GET /api/v1/founder/ceo-os/assumptions` — full register, redacted if PRIVATE_OPS off

## Cross-references

- [DECISION_LOG_SYSTEM](DECISION_LOG_SYSTEM.md) — every assumption ties back to a decision
- [../strategy/BEACHHEAD_SECTOR_SCORECARD](../strategy/BEACHHEAD_SECTOR_SCORECARD.md) — sector bets are assumptions
- [../strategy/NORTH_STAR_METRIC](../strategy/NORTH_STAR_METRIC.md) — the NSM rests on assumptions; revisit when they shift

## Non-negotiables

Assumptions are tested with real signal, not opinion. Tests are run via the
existing operational systems with their own human approvals. See
[DO_NOT_SAY](DO_NOT_SAY.md).
