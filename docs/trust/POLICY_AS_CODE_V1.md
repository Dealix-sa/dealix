# Policy-as-Code v1

Single source of truth: [`policies/dealix_control_policy.yaml`](../../policies/dealix_control_policy.yaml).

## Approval classes

| Class | Meaning | Auto? |
|---|---|---|
| A0 | Internal read | yes |
| A1 | Internal draft / prep | yes |
| A2 | External impact (send, propose, invoice) | only after recorded founder approval |
| A3 | High-risk (pricing, contract, refund, public proof, data export, destructive ops) | **never automatic** |

## Required rules

The verifier (`scripts/verify_policy_as_code.py`) requires every rule
listed in `policies/dealix_control_policy.yaml`. Removing any rule
fails CI.

## Runtime adapter

`api/internal/policy_adapter.py` loads the YAML and exposes
`evaluate(action, external_impact=..., suppressed=...)`. The router
calls it before recording any approval decision.

## How to add a rule

1. Add the rule under `rules:` in the YAML with name, description, severity, applies_to.
2. Reference the rule from the adapter if it should block at runtime.
3. Add a row in `docs/evals/PROMPT_OUTPUT_EVAL_MATRIX.md` if the rule
   has an output-text dimension.
4. Run `make policy-check`.
