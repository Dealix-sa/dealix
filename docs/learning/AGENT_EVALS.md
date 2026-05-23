# Agent Evaluations

> How we evaluate every agent before, during, and after deployment.
> Aligned to NIST AI RMF "Measure" function + OpenAI agent governance.

## Eval Sets Per Agent

Every agent has three eval sets:

1. **Golden** — known-good inputs with expected outputs (regression baseline)
2. **Red-team** — adversarial / prompt-injection / edge case inputs
3. **Regression** — every past failure becomes a permanent eval case

Stored in `evals/datasets/{agent_name}/`.

## Eval Rubrics

Per `evals/rubrics/{agent_name}.md`. Common dimensions:

- **Accuracy** — output matches expected (where deterministic) or passes rubric (where generative)
- **Cite-ability** — every claim has source
- **Trust-gate compliance** — output respects approval matrix, claim_guard, suppression
- **Refusal correctness** — agent refuses what it should (per `AI_GOVERNANCE.md`)
- **Latency** — within SLA
- **Format conformance** — output matches schema

## Eval Cadence

| Trigger | Run |
|---|---|
| Pre-deploy (any agent change) | All three eval sets |
| Weekly (production agents) | Golden + regression |
| Monthly (production agents) | All three + drift analysis |
| Post-incident | Add incident to regression set + re-run all |

## Eval Results

Stored in `evals/results/{agent_name}/{date}.json`:

```json
{
  "agent": "lead_scoring_agent",
  "agent_version": "v1.3.0",
  "run_at": "2026-05-23T09:00:00Z",
  "eval_set": "golden",
  "total_cases": 50,
  "pass": 49,
  "fail": 1,
  "pass_rate": 0.98,
  "failures": [
    {
      "case_id": "G-042",
      "expected": "...",
      "actual": "...",
      "category": "fit_score_misclassification"
    }
  ]
}
```

## Pass Thresholds

| Eval set | Pass threshold |
|---|---|
| Golden | ≥ 95% |
| Red-team | 100% (must refuse / handle every adversarial case) |
| Regression | 100% (no regressions, ever) |

If any threshold misses → block deploy + log in `learning/AGENT_EVALS.md` rollup.

## What An Agent Card Must Include

Per `AI_GOVERNANCE.md`, each agent has:
- Purpose
- Inputs (typed)
- Outputs (typed)
- Risk level
- Approval tier
- Evaluation rubric reference
- Logging location
- Owner

If any of these are missing → agent doesn't run in production.

## Agents Currently Tracked

| Agent | Risk | Approval tier | Eval status |
|---|---|---|---|
| lead_finder_agent | low | A0 | pending eval set |
| enrichment_agent | low | A0 | pending eval set |
| scoring_agent | low | A0 | pending eval set |
| pain_hypothesis_agent | medium | A0 (internal only) | pending eval set |
| message_agent | medium | A1 (founder approves output) | pending eval set |
| proposal_agent | medium | A1 (founder approves output) | pending eval set |
| qa_agent | medium | A0 (assists founder QA) | pending eval set |
| trust_guard_agent | high (operates trust gates) | n/a (it IS the gate) | high-priority eval set |
| content_agent | medium | A3 (founder + claim_guard) | pending eval set |
| learning_agent | low | A0 | pending eval set |
| finance_watch_agent | medium | A1 (alerts founder) | pending eval set |
| client_success_agent | medium | A1 (founder owns client) | pending eval set |
| founder_brief_agent | low | A0 (founder reads) | pending eval set |
| strategy_review_agent | low | A0 (founder reviews) | pending eval set |
| delivery_report_agent | medium | A1 (founder approves before client) | pending eval set |

## Anti-Patterns

- Deploying an agent without an eval set
- Lowering pass thresholds to ship
- Removing failures from regression set
- Eval set that mirrors training data exactly (overfitting)
- "Vibes" evaluation in place of rubric

## What This Refuses

- Untested agent in production
- Agent operating outside its documented purpose
- Agent making A3/A4 decisions
- Agent without an owner
- Hiding eval failures
