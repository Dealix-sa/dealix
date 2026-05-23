# Next Best Action Engine

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Closing Deals.

The Next Best Action engine ranks candidate moves and surfaces the
top recommendation in the founder brief. It is a ranking layer over
the experiment backlog, the account scoring model, the operating
scorecard, and the lesson register. It does not act. It recommends.
The founder approves; the agents draft.

## Inputs

The engine consumes:

| Input                                       | Source                                                                  |
| ------------------------------------------- | ----------------------------------------------------------------------- |
| Open experiments                            | `distribution/experiment_log.csv`                                       |
| Account scores                              | `growth/account_scores.csv`                                             |
| Sector scores                               | `growth/sector_targets.csv`                                             |
| Channel scorecard                            | `distribution/channel_scorecard.csv`                                    |
| Open approvals                               | `approvals/approval_queue.csv`                                          |
| Trust flags                                  | `trust/trust_flags.csv`                                                 |
| Eval status                                  | `evals/eval_status.csv`                                                 |
| Lesson register                              | `performance/lessons.csv` (private ops, see `LEARNING_LOOP.md`)         |
| AI unit economics                            | `finance/ai_unit_economics.csv`                                         |
| Cash and finance                             | `finance/cash_collected.csv`, `finance/payment_capture_queue.csv`       |

## Action types

The engine recommends from a controlled vocabulary:

| Action type                            | Description                                                          |
| -------------------------------------- | -------------------------------------------------------------------- |
| `approve_pending_drafts`               | Clear a backlog in the approvals queue (top N by score).             |
| `rebalance_sector_portfolio`           | Move attention between sectors based on score deltas.                |
| `tighten_or_loosen_icp`                | Adjust the ICP threshold; rescore accounts.                          |
| `rotate_outreach_hook`                 | Switch the active hook for a sector or channel.                      |
| `adjust_sample_sprint_scope`           | Add or remove a deliverable in a sample sprint.                      |
| `add_offer_ladder_rung`                | Add a productized rung.                                              |
| `update_handoff_template`              | Modify the handoff template for a sprint type.                        |
| `escalate_incident`                    | Open or escalate an incident.                                        |
| `pause_an_agent`                       | Flip a kill switch on an agent (requires founder approval).           |
| `accept_a_risk`                        | Record a risk acceptance with justification.                         |

Each action maps to an existing Founder Console endpoint and to an
agent owner.

## Ranking function

The ranking score is a linear combination:

```
score = w_impact * impact_score
      + w_evidence * evidence_score
      - w_cost * cost_score
      - w_risk * risk_score
      + w_lesson * lesson_alignment_score
      - w_blockers * blocker_penalty
```

| Term                       | Meaning                                                                  |
| -------------------------- | ------------------------------------------------------------------------ |
| `impact_score`             | Expected delta on the targeted KPI node, normalized 0..1.                |
| `evidence_score`           | Strength of evidence behind the action: lesson confidence + proof links. |
| `cost_score`               | Founder time + AI cost + delivery cost, normalized 0..1.                 |
| `risk_score`               | Combined trust, brand, customer risk class, normalized 0..1.             |
| `lesson_alignment_score`   | +1 if a `high`-confidence lesson supports the move, 0 otherwise.         |
| `blocker_penalty`          | +1 if an open trust flag or incident contradicts the move.               |

The weights are static defaults today; they are tunable per cadence by
the Growth Strategist via an audit-recorded change.

## Why this is not autopilot

The engine is read-only. It writes nothing externally and writes
nothing to the approvals queue without an approval. Its only outputs
are:

1. A ranked list surfaced in the founder brief.
2. A weekly written recommendation in the scorecard refresh.
3. A trust flag at `severity: medium` if it detects a blocker that
   should be cleared before any action can proceed.

The founder is the only actor that can move a recommendation into the
queue. The agents are the only actors that can draft the underlying
work. The engine is a recommendation layer; A3 remains banned.

## Worked example

Inputs at a snapshot:

| Signal                                                   | Value                                |
| -------------------------------------------------------- | ------------------------------------ |
| F&B sector reply rate                                    | 1.8% (down from 2.6%)                 |
| Government sector reply rate                              | 4.1% (up from 3.2%)                   |
| F&B account scores                                       | mean 0.62                            |
| Government account scores                                | mean 0.71                            |
| Open trust flags                                          | none material                        |
| High-confidence lesson aligned                            | "Government sector responds to procurement-relevance hooks." |
| Open approvals queue                                      | 14 (Gov: 6, F&B: 8)                   |

The top recommendation: rebalance the portfolio toward Government for
two cadences and rotate the Government hook to the procurement-relevance
variant. The recommendation lands in the founder brief, the founder
approves, the Growth Strategist drafts a new sector target row, the
Distribution Operator drafts the hook switch, and both queue.

## Cohort hygiene

The engine respects cohort definitions from the experiment backlog.
It does not recommend an action that confounds a running experiment
in the same cohort. The Performance Analyst is responsible for
flagging cohort conflicts at ranking time.

## Refresh cadence

| Activity                       | Cadence  |
| ------------------------------ | -------- |
| Inputs refresh                 | Daily    |
| Score recompute                 | Daily    |
| Recommendation surfaced        | Daily (in the founder brief) |
| Weight review                   | Monthly  |
| Action vocabulary review        | Quarterly|

## Failure modes

| Failure                                          | Behavior                                                              |
| ------------------------------------------------ | --------------------------------------------------------------------- |
| Missing input CSV                                | Engine skips that signal and notes the gap in the recommendation.    |
| Conflicting experiments                          | Recommendation declines to act on the conflicting cohort.            |
| Recommendation against a banned action           | Suppressed; trust flag opened.                                       |
| Recommendation against a paused agent             | Suppressed; the engine recommends unpausing as a separate action.    |

## Discipline

1. The engine recommends; the founder decides.
2. Every recommendation cites the inputs that drove it.
3. Every recommendation traces to a KPI node and to a lesson where
   one exists.
4. Recommendations against trust posture are not surfaced.
5. The engine's outputs are auditable: every recommendation has a
   timestamp, a snapshot of inputs, and a stable id.

## Cross-references

- `EXPERIMENT_BACKLOG.md` for hypothesis discipline.
- `LEARNING_LOOP.md` for the lessons that influence the score.
- `REVENUE_KPI_TREE.md` for the target node taxonomy.
- `CONVERSION_DIAGNOSTICS.md` for the upstream diagnosis.
- `OBJECTION_ANALYTICS.md` and `WIN_LOSS_ANALYSIS.md` for late-funnel
  signals.
