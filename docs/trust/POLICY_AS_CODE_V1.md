# Policy-as-Code v1

`policies/dealix_control_policy.yaml` is the authoritative source of
truth for which AI/worker actions are allowed, and under what controls.

## Approval classes

| Class | Label                 | Approval | Evidence | Escalation | Examples                                 |
|-------|-----------------------|----------|----------|------------|------------------------------------------|
| A0    | safe_internal         | no       | no       | no         | read summary, render scorecard           |
| A1    | internal_with_audit   | no       | no       | no         | retry worker, classify reply             |
| A2    | founder_approval      | yes      | no       | no         | queue outreach draft for send            |
| A3    | founder_plus_evidence | yes      | yes      | yes        | publish proof, commit pricing, data export |

## Rules

The YAML declares the rules below; the adapter (`api/internal/policy_adapter.py`)
exposes them as plain dicts for downstream gates. See the YAML for the
authoritative list:

- `no_a3_auto`
- `no_suppressed_outreach`
- `high_risk_requires_evidence`
- `no_guaranteed_revenue_claims`
- `approved_a2_can_request_execution`
- `public_proof_requires_approval`
- `pricing_commit_requires_approval`
- `data_export_requires_escalation`

## Verifier

```
make policy-check
```

This runs `scripts/verify_policy_as_code.py`, which fails the build if
any required class or rule is missing.
