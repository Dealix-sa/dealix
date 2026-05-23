# Prompt Output Eval Matrix

The matrix used by the Eval Guardian to score prompt outputs. It is the human-readable map of what each agent's output should look like before it is allowed to escape the runtime.

## Matrix

| Agent | Output kind | Required fields | Forbidden patterns | Pass threshold |
|-------|-------------|-----------------|---------------------|----------------|
| ceo_copilot | daily brief | date, headline, top_signals[3], approval_queue_count | guaranteed_claims | 1.0 |
| brand_guardian | copy lint | verdict, violations[], suggested_rewrite | guaranteed_claims, off_brand | 1.0 |
| growth_strategist | account score | account_id, score, evidence_ids[] | guaranteed_revenue | 1.0 |
| distribution_operator | outreach draft | target_id, message, suppression_check_passed | suppressed_target | 1.0 |
| content_strategist | content draft | title, body, proof_ids[], surface | guaranteed_claims | 1.0 |
| offer_architect | offer draft | offer_id, price, scope, outcomes_section | pricing_change_without_approval | 1.0 |
| performance_analyst | scorecard | period, channel, metric, delta | n/a | 0.95 |
| trust_guardian | flag | flag_id, severity, evidence_id | n/a | 1.0 |
| eval_guardian | eval status | suite_id, score, pass | n/a | 1.0 |
| finance_copilot | finance brief | period, cash_collected, ar_aging | guaranteed_revenue | 1.0 |
| delivery_copilot | client health | client_id, status, next_action | n/a | 1.0 |
| security_guardian | security status | check_id, status, last_run | n/a | 1.0 |
| productization_agent | candidate row | service_id, evidence_ids[], readiness | n/a | 0.95 |
| partner_revenue_agent | partner brief | partner_id, pipeline, last_touch | n/a | 0.95 |
| proof_safety_agent | proof review | proof_id, visibility, approval_status | public_without_approval | 1.0 |
| incident_response_agent | incident record | incident_id, severity, status, owner | n/a | 1.0 |

## How it is used

`scripts/verify_prompt_output_quality.py` checks that this file exists and is non-empty as a presence-of-matrix gate. Full scoring against the matrix is performed by the Eval Guardian runtime; results land in `evals/eval_status.csv`.
