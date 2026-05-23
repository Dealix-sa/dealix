# Agent Evaluation

## Metrics

Each agent in `AGENT_REGISTRY.md` is graded on:

| Metric | Definition |
|---|---|
| Accuracy | Agent output matches a held-out reference answer |
| Usefulness | Founder rates output on a 1–5 scale at point of use |
| Risk Detection | Trust Guard catches risky outputs before send |
| Hallucination Rate | Outputs that contain unsupported claims |
| Evidence Quality | Outputs cite verifiable sources where required |
| Approval Correctness | Agent correctly routes to A1 / A2 / A3 |

## Eval Suite Structure

```
evals/
  founder_brief/
  lead_finder/
  scoring/
  message/
  proposal/
  trust_guard/
  learning/
  delivery_qa/
```

Each subfolder holds:
- `cases.jsonl` — input + reference output.
- `rubric.md` — how each case is graded.
- `runs/` — dated run outputs with scores.

## Cadence

- Monthly run for every active agent.
- Quarterly review of the suite itself (add cases for new failure modes).

## Promotion / Demotion

- An agent below floor on any metric is demoted per
  `docs/trust/WORKFLOW_RISK_CLASSIFICATION.md`.
- Three consecutive months at or above floor allow promotion of one level
  in automation, subject to A2 approval.
