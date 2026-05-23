# Performance Improvement OS

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Driven by Growth · Focused on Results.

The Performance Improvement OS is the discipline by which Dealix
turns operating data into deliberate changes to the revenue motion.
It is not a dashboard. It is a closed loop that runs continuously
across measurement, diagnosis, intervention, and learning. The loop
is wired into the Founder Console, the agent registry, and the
private ops runtime.

## The loop

```
  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
  │ 1. Measure       │ -> │ 2. Diagnose      │ -> │ 3. Intervene     │ -> │ 4. Learn         │
  │ scorecards,      │    │ funnel + cohort  │    │ experiment +     │    │ outcomes file    │
  │ KPIs, drift      │    │ analysis         │    │ next-best action │    │ updates          │
  └──────────────────┘    └──────────────────┘    └──────────────────┘    └──────────────────┘
            ^                                                                       │
            └───────────────────────────────────────────────────────────────────────┘
```

Each step has an owner agent, a runtime CSV, and a Founder Console
surface. The loop runs on three cadences: daily, weekly, and monthly.

## Cadences

| Cadence | What happens                                                                        | Lead agent             |
| ------- | ----------------------------------------------------------------------------------- | ---------------------- |
| Daily   | Refresh funnel snapshot, surface blockers in the founder brief, retry failed workers.| performance_analyst    |
| Weekly  | Refresh the operating scorecard, review experiments, close the loop on hypotheses.   | ceo_copilot            |
| Monthly | KPI tree review, sector portfolio rebalance, win/loss analysis.                      | growth_strategist      |

The cadences correspond to the Founder Console scorecard refresh
action (`/control/scorecard/refresh`) and to the four-pillar
scorecard documented in `founder/operating_scorecard.md`.

## Four pillars (the scorecard)

The scorecard is a four-pillar view of the operating system.

| Pillar    | What it tracks                                                       | Source CSVs                                                  |
| --------- | -------------------------------------------------------------------- | ------------------------------------------------------------ |
| Revenue   | Pipeline, qualified, won, cash collected; AI unit economics.         | `finance/cash_collected.csv`, `finance/ai_unit_economics.csv`|
| Trust     | Open trust flags, audit volume, eval gate pass rate, incident count. | `trust/trust_flags.csv`, `evals/eval_status.csv`, `trust/incidents.csv` |
| Delivery  | Sample queue health, proposal queue health, on-time delivery.        | `sales/sample_queue.csv`, `sales/proposal_queue.csv`         |
| Growth    | Sector scoring, account scoring, channel scorecard, experiments.     | `growth/sector_targets.csv`, `distribution/channel_scorecard.csv`, `distribution/experiment_log.csv` |

The scorecard endpoint is `/api/v1/internal/control/scorecard`.

## Step 1: Measure

Measurement is the responsibility of the Performance Analyst agent
(approval class A1, read-only). It assembles:

- The four-pillar scorecard.
- The funnel snapshot via the conversation log
  (`outreach/conversation_log.csv`).
- The channel and sector scorecards.
- The experiment log status counts.

The agent never makes an external claim from this data. The numbers
are surfaced inside the Founder Console only.

## Step 2: Diagnose

Diagnosis is a structured walk through the KPI tree (see
`REVENUE_KPI_TREE.md`). The Conversion Diagnostics doc
(`CONVERSION_DIAGNOSTICS.md`) defines the diagnostic moves. The
output is a list of candidate hypotheses, each tagged with:

- the KPI node affected
- the expected delta
- the cost of the intervention
- the risk class

Hypotheses become rows in `distribution/experiment_log.csv` via the
`/experiments/backlog/draft` endpoint.

## Step 3: Intervene

Interventions are not auto-executed. They become drafts in the
distribution machine and the offer ladder, and they queue for founder
approval. The Next Best Action engine (see
`NEXT_BEST_ACTION_ENGINE.md`) ranks them.

Interventions fall into four families:

| Family       | Examples                                                          |
| ------------ | ----------------------------------------------------------------- |
| Targeting    | Reweight sector priority; change ICP segment filters.             |
| Messaging    | Rewrite a hook; switch the opening proof point.                    |
| Offer        | Add a rung; change a sample sprint scope.                          |
| Delivery     | Change the handoff template; add a QA gate.                        |

## Step 4: Learn

Learning is the explicit step that closes the loop. The Learning Loop
doc (`LEARNING_LOOP.md`) defines the artifacts. The experiment log
row is updated with:

- the result band (`win`, `flat`, `loss`)
- the delta on the targeted KPI node
- a one-sentence lesson
- a link to the next experiment, if any

The Win/Loss Analysis doc (`WIN_LOSS_ANALYSIS.md`) consumes the
result band counts.

## Roles and accountability

| Agent                    | Role in the loop                                                  |
| ------------------------ | ----------------------------------------------------------------- |
| performance_analyst      | Measurement, funnel snapshot.                                      |
| growth_strategist        | Sector and account reweighting; targeting interventions.           |
| distribution_operator    | Messaging interventions (always queued, never sent).               |
| offer_architect          | Offer interventions.                                               |
| delivery_copilot         | Delivery interventions.                                            |
| eval_guardian            | Confirms that any intervention draft clears the eval gate.         |
| trust_guardian           | Confirms that interventions do not violate trust policy.           |
| founder                  | Approves every intervention; reads the scorecard.                  |

## What the OS will not do

- It will not approve interventions itself. Every intervention is a
  founder decision.
- It will not change pricing, contract, or payment terms as part of
  an experiment. Those are policy-gated.
- It will not run unbounded experiments. Each experiment has a start,
  an end, and a measured outcome.
- It will not chase a metric without proof. Numbers that move without
  a hypothesis are flagged, not celebrated.

## How performance is exposed in the API

| Endpoint                                   | Purpose                                    |
| ------------------------------------------ | ------------------------------------------ |
| `GET /control/scorecard`                   | Read the four-pillar scorecard.            |
| `POST /control/scorecard/refresh`          | Trigger a recompute (audit row recorded).  |
| `GET /sales/funnel`                        | Funnel stage counts.                       |
| `GET /distribution/summary`                | Channel and sector scorecards.             |
| `GET /experiments/backlog`                 | Open and closed experiments.               |
| `POST /experiments/backlog/draft`          | Draft a new experiment hypothesis.         |

## Operating principles

1. **One scorecard.** The four-pillar scorecard is the only operating
   view of the system. No private dashboards.
2. **Hypothesis first.** No intervention runs without a written
   hypothesis in the experiment log.
3. **Measured outcomes.** No experiment is closed without a numeric
   outcome on the targeted KPI node.
4. **Audit every change.** Every intervention draft has an audit row.
5. **Founder is the bottleneck on purpose.** The bottleneck enforces
   discipline; throughput is improved by sharpening drafts, not by
   removing the bottleneck.

The next documents in this section unpack each step of the loop in
detail.
