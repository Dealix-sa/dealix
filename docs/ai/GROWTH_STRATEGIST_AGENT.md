# Growth Strategist Agent

The Growth Strategist agent produces structured growth analyses: where the funnel is leaking, which experiments to run, which channels to invest in. It does not act; it recommends.

**Source of truth:** `registries/agent_registry.yaml` entry `growth_strategist`
**Owner:** Founder + Marketing Lead
**Trust gate:** A1 — recommendations; founder selects which to act on (A2 for any change to channel mix or spend).

## Spec

| Field | Value |
|-------|-------|
| `id` | `growth_strategist` |
| `name` | Growth Strategist |
| `purpose` | Analyse the revenue funnel and recommend prioritised experiments |
| `approval_class_max` | A1 |
| `tools` | `read_factory_state`, `read_attribution`, `read_experiment_log`, `write_recommendation` |
| `outputs` | `growth_analysis`, `experiment_proposal` |
| `external_action_allowed` | false |
| `kill_switch` | true |
| `eval_required` | true |
| `audit_required` | true |
| `owner` | marketing_lead |
| `allowed_write_targets` | `$PRIVATE_OPS/growth_recommendations.csv`, `$PRIVATE_OPS/experiment_proposals.csv` |

## Inputs

| Input | Source |
|-------|--------|
| Revenue Factory state | `$PRIVATE_OPS/revenue_factory_state.csv` |
| Attribution | `$PRIVATE_OPS/attribution_log.csv` |
| Experiment history | `$PRIVATE_OPS/experiment_log.csv` |
| Content calendar | `$PRIVATE_OPS/content_calendar.csv` |
| Health Score distribution | `$PRIVATE_OPS/client_health_score.csv` |

## Outputs

For each weekly cycle:

1. A funnel snapshot with stage-by-stage conversion (estimated).
2. A leak ranking: which stage is most costly to leave broken.
3. A prioritised list of three experiments with hypotheses, sample sizes, and stop rules.
4. A risk note: what could go wrong if the recommendations are acted on.

Recommendations are framed as "evidence suggests" and "based on current pattern" — never as "you will see X% lift".

## OWASP LLM Top 10 posture

- **Excessive agency (LLM08).** The agent cannot launch experiments; it can only propose them. Launching requires founder approval (A2) and creates a row in the Experiment Backlog (`docs/performance/EXPERIMENT_BACKLOG.md`).
- **Insecure output handling (LLM02).** Outputs are markdown and CSV rows. They are not executed.
- **Training data poisoning (LLM03).** The agent reads operational data; it does not write back to the data it reads from.

## NIST AI RMF posture

- **Govern.** The agent's purpose, scope, and approval class are registered.
- **Map.** The agent identifies its inputs and the engagements affected.
- **Measure.** The eval suite scores recommendation quality against historical outcomes.
- **Manage.** The kill switch and audit log are active.

## Eval

The agent is evaluated against:

- Historical funnels with known leaks (the agent should rank the known leak in the top three).
- Recommendation quality against a panel of human-graded recommendations.
- Hype-and-guarantee lint (no banned language).

## Failure modes

- **Hype creep:** recommendations contain guarantee language. Detection: lint. Recovery: kill switch + rewrite.
- **Over-confident ranking:** the agent ranks a leak without evidentiary support. Detection: eval check. Recovery: rule tuning, reduced confidence.
- **Stale data:** agent runs on yesterday's data; recommendations are obsolete. Detection: freshness check. Recovery: refresh, re-run.

## Recovery path

If the agent's recommendations are repeatedly off-pattern, the founder kills it and growth analysis runs manually until the agent is re-certified.

## Metrics

- Recommendations per week.
- Recommendations adopted (estimated).
- Adopted recommendations leading to measured improvement (estimated).
- Eval pass-rate.

## Disclaimer

Recommendations are analysis, not guarantees. Dealix does not guarantee that any experiment will succeed. Estimated value is not Verified value.
