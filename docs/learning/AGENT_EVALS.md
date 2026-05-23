# Agent Evaluations

> Quantitative evaluation of each agent in `docs/agents/AGENT_REGISTRY.md`.

## Format

| Agent | Eval Date | Accuracy | Useful Rate | Hallucination Rate | Risk Recall | Approval Correctness | Decision |
|---|---|---:|---:|---:|---:|---:|---|

## Eval Suites

Each agent has a versioned eval suite under `evals/`. The suite is:
- Held out from training-style updates.
- Reviewed quarterly.
- Expanded when a Trust incident exposes a gap.

## Thresholds

| Metric | Floor |
|---|---:|
| Accuracy | 90% |
| Useful Rate (1–5 scale) | ≥ 4.0 |
| Hallucination Rate | ≤ 2% |
| Risk Recall (Trust Guard) | ≥ 95% |
| Approval Correctness | 100% |

Falling below floor triggers a demotion per `docs/trust/WORKFLOW_RISK_CLASSIFICATION.md`.

## Cadence

- Run monthly per agent.
- Reviewed in the Weekly CEO Review when any threshold is missed.
