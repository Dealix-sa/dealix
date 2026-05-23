# Eval Gate v1

Source: `evals/gates/dealix_agent_eval_gate.yaml`.

Required suites:

- `no_guaranteed_claims`
- `approval_bypass`
- `prompt_injection`
- `sensitive_data_leakage`
- `suppression_compliance`
- `evidence_required`
- `arabic_business_quality`
- `proposal_safety`
- `tool_misuse`
- `A3_escalation`
- `proof_safety`
- `pricing_safety`

Verifier:

```
make eval-gate
```
