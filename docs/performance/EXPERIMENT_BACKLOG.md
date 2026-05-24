# Experiment Backlog

> Hypotheses, ranked.

## 1. Format

```yaml
experiment_id: exp_xxxx
hypothesis: <one sentence>
metric: <one metric>
duration_days: <int>
expected_lift: <signed number, with rationale>
risk: low | medium | high
required_approvals: founder | brand_guardian | trust_guardian
owner: <name>
status: backlog | running | completed | dropped
result: <one paragraph, after completion>
audit_link: <id>
```

## 2. Ranking heuristics

- Cash impact × Probability ÷ Risk.
- Favour reversible experiments.
- Stop running experiments if KPI hygiene degrades.

## 3. File

`performance/experiment_backlog.csv` columns:

```
experiment_id, hypothesis, metric, duration_days, expected_lift, risk, required_approvals, owner, status, result_summary, source
```

## 4. Cadence

- Sunday: re-rank backlog.
- Monday: ≤ 3 experiments enter `running`.
- Friday: completed experiments produce learnings.

## 5. Trust

No experiment touches a live customer without explicit consent and an audit entry.
