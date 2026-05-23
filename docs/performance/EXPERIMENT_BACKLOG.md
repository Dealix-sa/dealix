# Experiment Backlog

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Driven by Growth.

The experiment backlog is the only sanctioned place to record a
proposed change to the revenue motion. Every change starts as a
written hypothesis. Every hypothesis ends with a measured outcome
and a lesson. The backlog is durable: the file is
`distribution/experiment_log.csv` in the private ops runtime.

## Schema

The columns are defined in
`scripts/bootstrap_private_ops_runtime.py`:

| Column        | Type        | Notes                                                                  |
| ------------- | ----------- | ---------------------------------------------------------------------- |
| `id`          | string      | Experiment id (e.g., `exp_2026_05_18`).                                |
| `hypothesis`  | string      | One-sentence statement: "If we do X, then Y will move by Z."           |
| `channel`     | string      | Which channel or motion the experiment touches.                        |
| `started_at`  | ISO ts      | When the experiment started.                                           |
| `ended_at`    | ISO ts      | When the experiment ended.                                             |
| `result`      | string      | `win`, `flat`, or `loss`.                                              |
| `status`      | enum        | `draft`, `running`, `closed`.                                          |
| `owner`       | string      | Accountable agent or founder.                                          |

The Founder Console exposes the backlog at
`/api/v1/internal/experiments/backlog` and accepts new drafts at
`/api/v1/internal/experiments/backlog/draft`. Drafts record an audit
row with `action: experiment_draft`, `risk: low`.

## Lifecycle

```
draft -> running -> closed
              \-> aborted
```

| State    | Meaning                                                       |
| -------- | ------------------------------------------------------------- |
| draft    | Hypothesis is written. Not yet started.                       |
| running  | Experiment is live. Outcomes are being measured.              |
| closed   | Experiment ended. Result is `win`, `flat`, or `loss`.         |
| aborted  | Experiment ended early. Reason is recorded in the audit ledger.|

Transitions are recorded in the audit ledger. An aborted experiment
must carry a reason; flatness is acceptable as a result but not as a
cause for abort.

## Hypothesis discipline

A well-formed hypothesis has four parts:

1. **The change**: a specific, observable change in the motion.
2. **The target KPI node**: the node from the KPI tree we expect to
   move.
3. **The expected direction and magnitude**: e.g., "reply rate up by
   3 percentage points."
4. **The measurement window**: "over a 14-day window with at least
   100 drafts."

Examples:

| Bad                                                | Good                                                                                                  |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Try a new email hook.                              | If we switch the opening hook for the F&B sector from "process pain" to "trust gap" we will see reply rate rise by 3 pp over 14 days with at least 100 drafts. |
| See if proposals work better.                      | If we cap the proposal at 4 pages we will see proposal-sent → won win rate rise from 18% to 25% over 30 days.                                                   |
| Run a LinkedIn campaign.                            | If we add LinkedIn DM as a parallel channel to email for tier-1 ICP we will see qualified opportunities rise by 20% with no rise in suppression hits.           |

## Constraints

Hypotheses are constrained by the trust plane:

| Constraint                                     | Notes                                                                  |
| ---------------------------------------------- | ---------------------------------------------------------------------- |
| No external action without approval            | Every draft still queues; only the founder approves the send.          |
| No banned phrasing                             | Hypotheses cannot pretend to test guaranteed claims.                   |
| No proof publication outside the proof gate    | Experiments that touch proof must coordinate with the Proof Safety Agent. |
| No pricing or contract commitments             | Pricing experiments require approval at the policy layer.              |
| Single KPI target per experiment               | Compound experiments produce confounded results.                       |

## Priority ranking

The Next Best Action engine (`NEXT_BEST_ACTION_ENGINE.md`) ranks
backlog items by:

- Expected impact on the KPI tree node.
- Cost (founder time, AI cost, delivery cost).
- Risk class (trust risk, brand risk, customer risk).
- Time to outcome.

The ranking is recomputed weekly and surfaced in the founder brief.

## Cohorts and segmentation

Experiments must declare the cohort: sector, channel, ICP segment,
or offer rung. Cross-cohort experiments are explicitly flagged. The
Performance Analyst tags each experiment row with the cohort. Where
necessary, a control cohort is held out (no change), recorded in the
audit ledger, and reviewed in the close report.

## Close report

Every closed experiment produces a one-page close report. The report
contains:

- The hypothesis as written.
- The cohort and the control.
- The measured delta on the target KPI node.
- The result band.
- The lesson, in one sentence.
- A pointer to the next experiment, if any.

The close report is reviewed in the weekly performance meeting and
the lesson is appended to the Learning Loop record
(`LEARNING_LOOP.md`).

## Anti-patterns

| Anti-pattern                                       | Why                                                                  |
| -------------------------------------------------- | -------------------------------------------------------------------- |
| Running an experiment without writing a hypothesis | The whole point of the backlog is to force the discipline.            |
| Running an experiment without a target KPI node    | Without a node, there is no measurement, no lesson.                  |
| Closing an experiment without a result band        | "Inconclusive" is `flat`. Other outcomes require evidence.            |
| Running multiple experiments on one node           | Confounded results, no learning.                                     |
| Reopening a closed experiment                       | If the conditions changed, draft a new experiment.                   |

## Cadence

- Draft additions: daily, from the diagnostic.
- Backlog grooming: weekly, by the Performance Analyst and the founder.
- Closures: as they end.
- Backlog audit: monthly. Stale drafts are aborted with reason
  `stale_no_owner`.

## Founder Console exposure

| Endpoint                                | Purpose                                  |
| --------------------------------------- | ---------------------------------------- |
| `GET /experiments/backlog`              | List backlog items.                      |
| `POST /experiments/backlog/draft`       | Draft a new hypothesis. Audit recorded.  |

## Discipline summary

1. Every change is a written hypothesis.
2. Every hypothesis names one KPI node.
3. Every experiment has a measurement window.
4. Every closure produces a lesson.
5. Every lesson reaches the Learning Loop.
