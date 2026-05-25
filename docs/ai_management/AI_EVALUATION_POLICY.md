# AI Evaluation Policy

> No release without measurement.

## Why evals

- Catch regressions on model bumps.
- Catch prompt-engineering regressions.
- Set objective release thresholds.
- Defend against "but the demo looked good".

## Eval Structure

`evals/<agent_id>/` contains:

- `golden/` — known inputs with expected outputs (or expected properties).
- `adversarial/` — prompt-injection, edge-case, hostile-input examples.
- `edge/` — boundary inputs (empty, very long, multilingual).
- `harness.py` — runs the set, returns a structured score.
- `thresholds.yaml` — release-gate pass thresholds per metric.

## Metrics (per agent)

- **Format correctness** — output parses, contains required fields.
- **Faithfulness** — claims in output appear in inputs (not invented).
- **Safety** — no forbidden phrases (`NO_OVERCLAIM_POLICY.md`).
- **Refusal** — adversarial prompts are refused or treated as data.
- **PII boundary** — private data not echoed.
- **Cost** — average cost per call below cap.
- **Latency** — p50, p95 within budget.

## Pass Thresholds (typical)

| Metric | Pass threshold |
|--------|----------------|
| Format correctness | 100% |
| Faithfulness | ≥ 95% |
| Safety (forbidden phrases) | 0 hits |
| Adversarial refusal | 100% |
| PII boundary | 100% |
| Cost (per call) | ≤ cap |
| Latency p95 | ≤ budget |

Any metric below threshold blocks release.

## Cadence

- Pre-release: full eval suite run.
- Weekly: regression smoke (subset).
- Monthly: full suite re-run + threshold review.
- On any model version bump: full suite re-run (release gate).

## Eval data hygiene

- Eval sets versioned in git.
- No real customer PII in eval sets (synthesise or anonymise).
- Adversarial sets reviewed by founder to ensure they reflect realistic
  attacks.

## Reporting

`evals/_reports/<yyyy-mm-dd>-<agent_id>.md` — one report per run, with:

- Run timestamp
- Model + version
- Per-metric score
- Pass/fail vs thresholds
- Regressions flagged
- Action taken
