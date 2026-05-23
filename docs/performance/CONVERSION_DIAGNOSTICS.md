# Conversion Diagnostics

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Closing Deals.

Conversion diagnostics is the disciplined practice of finding the
single biggest leak in the revenue motion and writing a focused
hypothesis to plug it. The diagnostic walks the KPI tree
(`REVENUE_KPI_TREE.md`) top-down and produces ranked candidate
hypotheses for the experiment backlog (`EXPERIMENT_BACKLOG.md`).

## The diagnostic question set

For every conversion drop, ask the four-question set in this order:

1. **Is the measurement honest?** Is the CSV current? Are there
   import errors? Is the eval gate failing on these draft types?
2. **Is the target right?** Is the sector or ICP segment producing
   the engagement we want? Or are we engaging the wrong accounts?
3. **Is the message right?** Is the hook landing? Are replies signal
   or noise? Is the brand voice on point?
4. **Is the offer right?** Is the sample sprint scoped correctly?
   Is the price band aligned with the segment?

A diagnostic that skips a step is a diagnostic that wastes an
experiment slot.

## Stage-by-stage diagnostic moves

### Sector targets → Accounts in ICP

| Drop signal                                      | Diagnostic moves                                                          |
| ------------------------------------------------ | ------------------------------------------------------------------------- |
| ICP shrinks unexpectedly                         | Inspect `account_scoring_model` outputs; check sector taxonomy drift.     |
| ICP grows but quality drops                       | Tighten the ICP threshold; review the sector ranking weights.             |

### Accounts in ICP → Targets Reached

| Drop signal                                      | Diagnostic moves                                                          |
| ------------------------------------------------ | ------------------------------------------------------------------------- |
| High in-ICP, low reach                           | Inspect channel mix; check campaign capacity; review suppression hits.    |
| High reach, low ICP fit                          | Targeting is loose; tighten ICP and re-run.                               |

### Targets Reached → Drafts Queued

| Drop signal                                      | Diagnostic moves                                                          |
| ------------------------------------------------ | ------------------------------------------------------------------------- |
| Reach high, drafts low                            | Eval gate rejecting drafts; review `evals/eval_status.csv` failure modes.|
| Drafts high, reach low                            | Distribution Operator is over-targeting; review account list quality.    |

### Drafts Queued → Drafts Sent After Approval

| Drop signal                                      | Diagnostic moves                                                          |
| ------------------------------------------------ | ------------------------------------------------------------------------- |
| Queue grows, approvals lag                       | Founder bandwidth; sharpen draft quality; reduce volume in favor of fit. |
| Approvals high but drafts dropping               | Eval gate failure; review most common eval failure modes.                |

### Drafts Sent → Replies

| Drop signal                                      | Diagnostic moves                                                          |
| ------------------------------------------------ | ------------------------------------------------------------------------- |
| Sent volume up, reply rate flat                  | Hook fatigue; rotate hooks; refresh proof points.                         |
| Sent volume flat, reply rate down                | Sector saturation; rebalance the portfolio.                               |
| Reply rate up, qualification down                | Wrong replies arriving; reverse-engineer the hook.                        |

### Replies → Engaged Conversations

| Drop signal                                      | Diagnostic moves                                                          |
| ------------------------------------------------ | ------------------------------------------------------------------------- |
| Many replies, few engaged                        | Reply routing failure; review `outreach/reply_routing_queue.csv`.         |
| Engaged conversations stall                      | Sales motion clarity; review qualification questions.                    |

### Engaged → Qualified

| Drop signal                                      | Diagnostic moves                                                          |
| ------------------------------------------------ | ------------------------------------------------------------------------- |
| Qualification rate drops                         | Tighten or loosen criteria; check the proof relevance.                    |
| Time to qualified rises                          | Schedule pressure; check the founder review cadence.                     |

### Qualified → Proposal Sent

| Drop signal                                      | Diagnostic moves                                                          |
| ------------------------------------------------ | ------------------------------------------------------------------------- |
| Qualified stalls before proposal                 | Proposal Factory throughput; review the proposal queue.                   |
| Proposal sent rises, win rate falls              | Proposal quality drop; review proof attachments.                          |

### Proposal Sent → Won

| Drop signal                                      | Diagnostic moves                                                          |
| ------------------------------------------------ | ------------------------------------------------------------------------- |
| Win rate flat, deal size shrinks                 | Pricing erosion; review the offer ladder.                                 |
| Win rate falls, deal size flat                   | Objection pattern shift; consult `OBJECTION_ANALYTICS.md`.                |
| Both fall                                        | Segment fit is wrong; consult sector and ICP scoring.                     |

### Won → Cash Collected

| Drop signal                                      | Diagnostic moves                                                          |
| ------------------------------------------------ | ------------------------------------------------------------------------- |
| Cash conversion days rises                       | Payment process drift; review payment capture queue.                      |
| Invoiced revenue drops                           | Billing failure; consult `REVENUE_RECOGNITION_NOTES.md`.                  |

## Diagnostic outputs

Every diagnostic produces:

1. A one-line statement of the leak: "Drafts queued is healthy; sent
   after approval is half of last month's pace."
2. A short list of candidate hypotheses ranked by expected impact and
   cost.
3. A primary recommendation that becomes an experiment draft (see
   `EXPERIMENT_BACKLOG.md`).
4. A risk note: what could go wrong if we run the experiment.

## Anti-patterns

| Anti-pattern                                          | Why to avoid                                                                       |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Reacting to a one-day spike                            | Variance is not signal. Trend over at least the diagnostic cadence.                |
| Diagnosing the message before the targeting           | Messaging tweaks rarely fix targeting drift.                                       |
| Diagnosing the offer before the message              | A wrong offer drafted in the right voice still loses; but a right offer in the wrong voice loses faster. |
| Skipping the "is measurement honest" question         | A KPI that moved because the CSV is broken does not need an experiment.            |
| Running parallel experiments on the same node         | Confounded results, no learning. Sequence experiments deliberately.                |

## How diagnostics integrate with the Founder Console

- `/api/v1/internal/sales/funnel` provides the stage counts.
- `/api/v1/internal/distribution/summary` provides the channel and
  sector breakdowns.
- `/api/v1/internal/experiments/backlog` shows live experiments.
- `/api/v1/internal/control/scorecard` is the four-pillar summary.

The Performance Analyst runs the diagnostic weekly and surfaces the
top three candidate hypotheses in the founder brief.

## Discipline

- One diagnostic per cadence (weekly is the default).
- One primary recommendation per diagnostic.
- One experiment at a time on a given KPI node.
- The diagnostic is recorded in the audit ledger
  (`action: diagnostic_run`, risk: low) and the lesson is recorded at
  the close of the experiment.
