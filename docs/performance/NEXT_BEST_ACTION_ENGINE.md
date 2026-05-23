# Next Best Action Engine

The Next Best Action Engine takes the current state of the Revenue Factory, the Health Score distribution, the Experiment Backlog, and the Learning Loop, and proposes the single action that would most move the system forward today.

**Source of truth:** `$PRIVATE_OPS/nba_proposals.csv`
**Owner:** Founder + Performance Analyst (`docs/ai/PERFORMANCE_ANALYST_AGENT.md`)
**Trust gate:** A1 for proposing; A2 for any action the founder elects to take that affects external surfaces.

## What it does

1. Reads the KPI Tree (`docs/performance/REVENUE_KPI_TREE.md`).
2. Reads open diagnostics (`docs/performance/CONVERSION_DIAGNOSTICS.md`).
3. Reads the Experiment Backlog (`docs/performance/EXPERIMENT_BACKLOG.md`).
4. Reads confirmed learnings (`docs/performance/LEARNING_LOOP.md`).
5. Reads the Client Health Score distribution (`docs/customer_success/CLIENT_HEALTH_SCORE_SYSTEM.md`).
6. Proposes one or two actions with: expected effect, evidence, prerequisite, owner.

## Action menu (illustrative)

| Action | When triggered |
|--------|----------------|
| Approve highest-ranked experiment | Backlog stale; recent reads stable |
| Re-prioritise sample queue | Sample queue aging; pipeline thin |
| Pause an underperforming channel | Channel cost / lead exceeds floor |
| Run a Client Success outreach to At-Risk clients | Health Score band shift |
| Re-price a sponge package | Margin breach repeated |
| Refresh a stale sector report | Inbound from sector report dropped |
| Pause an agent | Eval drift |

The Engine is intentionally conservative: it surfaces one or two actions, not ten.

## What it does not do

- It does not execute.
- It does not approve.
- It does not change pricing.
- It does not contact a client.
- It does not push a publish.

Every recommended action carries a clearly named human owner and the approval class required.

## OWASP / NIST posture

- **Excessive agency (LLM08).** The Engine writes to one CSV. It does not act.
- **Overreliance (LLM09).** Recommendations carry confidence and evidence; the founder is shown the source data.
- **Govern / Map / Measure / Manage.** Same loop as Performance Analyst.

## Failure modes

- **Action bias:** the Engine always recommends an experiment. Detection: action-mix audit. Recovery: prompt re-anchored to action menu breadth.
- **Stale input:** the Engine runs on yesterday's data. Detection: freshness check. Recovery: refresh.
- **Confidence inflation:** the Engine reports high confidence on weak evidence. Detection: eval. Recovery: prompt re-anchored to calibration.

## Recovery path

If the Engine's recommendations are consistently rejected by the founder, the agent is paused and the founder runs the loop manually.

## Metrics

- Recommendations per week.
- Founder acceptance rate.
- Recommended-action attribution to KPI movement (estimated).
- Action-mix breadth.

## Disclaimer

Recommendations are analytical proposals. The founder decides. Dealix does not guarantee that any recommendation succeeds. Estimated value is not Verified value.
