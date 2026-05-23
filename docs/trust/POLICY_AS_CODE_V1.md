# Policy as Code v1

Dealix policy is not a PDF in a folder. It is a YAML file in `policies/dealix_control_policy.yaml` that the runtime reads on every action and enforces without exception.

**Source of truth:** `policies/dealix_control_policy.yaml`
**Owner:** Founder + Engineering Lead
**Trust gate:** A2 — policy file changes require founder approval; PR must be signed.

## Why policy as code

A policy that humans read but software does not enforce is a policy that drifts. Policy as code means:

- Every action checks the policy.
- Every policy change is reviewable in source control.
- Every enforcement is logged.
- Every exception is named and time-boxed.

This is the foundation of the NIST AI RMF "Govern" function: organisational policy mechanised into runtime.

## File structure

```yaml
version: 1.0.0
last_reviewed_by: founder
last_reviewed_at: 2026-04-01T08:00:00Z

approval_classes:
  A0: read_only_internal
  A1: drafts_for_internal_review
  A2: founder_approved_external_or_financial
  A3: prohibited

protected_decisions:
  - proof_publishing
  - pricing_change
  - contract_execution
  - refund_issuance
  - payment_term_change
  - data_export
  - agent_activation
  - policy_change

forbidden_actions:
  - cold_whatsapp_automation
  - scraped_list_outreach
  - linkedin_automated_invite
  - bulk_outreach_without_consent
  - guaranteed_revenue_claim
  - external_send_without_founder_approval
  - autonomous_a3_action

guardrails:
  per_run_cost_cap_sar: 5.00
  per_agent_monthly_cost_cap_sar: 5000
  per_client_daily_cost_cap_sar: 200
  inference_outage_fail_count: 3
  eval_pass_threshold: 0.95
  red_team_defence_threshold: 1.00
```

## Enforcement points

| Layer | Enforcement |
|-------|-------------|
| Agent dispatch | Trust Guardian (`docs/ai/TRUST_GUARDIAN_AGENT.md`) |
| External send | Runtime contract (`docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md`) |
| Pricing changes | Pricing engine (`docs/product/PRICING_GUARDRAILS.md`) |
| Publish surfaces | Proof Approval OS (`docs/proof/PROOF_APPROVAL_OS.md`) |
| Data access | Data Trust (`docs/trust/DATA_TRUST_ARCHITECTURE.md`) |

## Change process

1. Engineer or founder proposes change in PR.
2. PR triggers full eval suite + red-team suite.
3. Engineering Lead reviews.
4. Founder signs the change (A2).
5. Merge triggers runtime re-load with version bump.

A policy change without an eval suite pass cannot merge.

## Exceptions

| Exception type | Authority |
|----------------|-----------|
| Per-engagement guardrail relaxation | Founder, time-boxed, logged |
| Per-agent kill-switch override | Founder + Engineering Lead |
| Per-client data-handling deviation | Founder + Legal |

Every exception is written to `$PRIVATE_OPS/policy_exceptions.csv` with `expires_at`. No open-ended exception is permitted.

## Failure modes

- **Policy / runtime drift:** runtime version differs from policy version. Detection: nightly check. Recovery: pause new actions; reload; root cause filed.
- **Silent bypass:** an enforcement point fails to check policy. Detection: red-team. Recovery: fix runtime; expand red-team suite.
- **Exception sprawl:** more than 10 active exceptions. Detection: weekly review. Recovery: founder review; expirations enforced.

## Recovery path

If the policy file is invalid (parse error, version mismatch), the runtime fails closed. No actions dispatch until a valid policy is restored.

## Metrics

- Policy version in production.
- Active exceptions count and aged.
- Enforcement denials per day (by reason).
- Bypass incidents (target: 0).

## Disclaimer

Policy as code is a control surface. It does not replace human judgement; it makes human judgement enforceable. Estimated value is not Verified value.
