# Policy-as-Code v1

Source of truth: `policies/dealix_control_policy.yaml`.
Adapter: `api/internal/policy_adapter.py`.
Verifier: `scripts/verify_policy_as_code.py`.

## Approval classes

- **A0** — info / read-only. External action may be allowed.
- **A1** — internal draft / recommendation. No external action.
- **A2** — external action after explicit human approval + evidence.
- **A3** — banned automated. Founder-only, never agent-initiated.

## Rules

1. `no_a3_auto` — agents may not initiate A3 actions.
2. `no_suppressed_outreach` — recipients on the suppression list are refused.
3. `high_risk_requires_evidence` — high/critical risk requires evidence.
4. `no_guaranteed_revenue_claims` — banned phrases (guaranteed revenue,
   guaranteed sales, guaranteed meetings, guaranteed replies, fully
   compliant, no-risk, zero risk, sent automatically without approval).
5. `approved_a2_can_request_execution` — only approved A2 actions with
   evidence and a non-suppressed recipient may request execution.

## Decision contract

`policy_adapter.evaluate(...)` returns `{decision, external_action_allowed,
reason, rule_id}`. Default-deny: anything that does not match a rule is
rejected with `default_deny`.

## Where decisions are recorded

Every approval write through the internal API appends a row to
`${DEALIX_PRIVATE_OPS}/trust/approval_decisions.csv`. The row carries the
policy rule id so audits can re-evaluate any past decision.
