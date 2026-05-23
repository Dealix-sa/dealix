# Eval Gate v1

Source: [`evals/gates/dealix_agent_eval_gate.yaml`](../../evals/gates/dealix_agent_eval_gate.yaml).

## 15 mandatory suites

| Suite | What it blocks |
|---|---|
| `no_guaranteed_claims` | absolute revenue/sales/meetings/replies claims |
| `approval_bypass` | language that asks for skipping approval |
| `prompt_injection` | acting on hostile inputs in researched data |
| `sensitive_data_leakage` | secrets / PII / financial leakage |
| `suppression_compliance` | outreach to suppressed accounts |
| `evidence_required` | A2 drafts without an evidence reference |
| `arabic_business_quality` | machine-translation artefacts in Arabic |
| `proposal_safety` | proposals missing scope/price/acceptance |
| `tool_misuse` | calling tools outside the declared set |
| `A3_escalation` | A3 candidates that produce a draft instead of an escalation |
| `proof_safety` | unsafe public-proof content |
| `pricing_safety` | drafts that commit a price |
| `data_export_safety` | export requests producing data instead of an escalation |
| `contract_safety` | contracts missing the legal-review clause |
| `payment_terms_safety` | payment-terms drafts missing the founder approval block |

## How CI runs the gate

`make eval-gate` invokes `scripts/verify_eval_gate.py`. The agent run
itself is performed by the Eval Guardian outside CI; CI only verifies
that every required suite is declared and well-formed.
