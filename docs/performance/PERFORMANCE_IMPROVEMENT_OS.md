# Performance Improvement OS

How Dealix continuously diagnoses, experiments, learns, and scales — without breaking trust gates or doctrine.

## 1. The loop

```
Observe → Diagnose → Prioritise → Experiment → Measure → Decide → Scale | Kill | Fix → Document learning
```

Each step is a named artefact, not a vibe.

## 2. Observe

Inputs:

- The KPI tree (`REVENUE_KPI_TREE.md`).
- The friction log.
- The approval queue patterns.
- Founder + customer interviews.

Cadence: weekly.

Owner: Performance Analyst agent + founder.

## 3. Diagnose

Output: a one-page diagnosis identifying **the smallest leak** in the funnel — the one place where a fix would unblock the most.

Doctrine: we always work on the bottleneck. We never work on a metric that isn't the bottleneck.

See: `CONVERSION_DIAGNOSTICS.md`.

## 4. Prioritise

Output: the experiment backlog (`EXPERIMENT_BACKLOG.md`) sorted by (impact × confidence ÷ effort).

Constraint: no more than 2 experiments running simultaneously.

## 5. Experiment

Each experiment carries:

- Hypothesis (one sentence).
- Owner (one person).
- Time-box (typically 14 days).
- Success metric.
- Kill criterion (when to stop early).
- Rollback plan.

## 6. Measure

We measure both **the metric** and **side effects** (approval queue load, brand drift, customer complaints).

## 7. Decide

After the time-box:

- **Scale** — succeeded; rollout to all relevant accounts.
- **Kill** — failed; document why; remove the experiment.
- **Fix** — partial success; adjust hypothesis and re-run.

Decisions are documented in `EXPERIMENT_BACKLOG.md`.

## 8. Document learning

Every experiment ends with a learning note in `LEARNING_LOOP.md`. The note answers:

- What was the hypothesis?
- Was it supported?
- What surprised us?
- What changes about how we operate now?

The note exists even if the experiment failed.

## 9. Cadence

- **Daily:** 10-minute founder check on active experiments.
- **Weekly:** diagnose + decide cycle (≤ 60 minutes).
- **Monthly:** scaled experiments review.
- **Quarterly:** learning roll-up.

## 10. Doctrine

- We do not "always be testing" everything. We test the bottleneck only.
- We do not run an experiment without a kill criterion.
- We do not scale without documented learning.
