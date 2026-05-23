# Policy-as-Code v1

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

This document is the authoritative reference for Dealix's policy-as-code
implementation. The actual policy lives in
`policies/dealix_control_policy.yaml`. The evaluator that consumes it
lives in `api/internal/policy_adapter.py`. The Founder Console wires the
evaluator into every state-changing endpoint exposed by
`api/routers/founder_console_internal.py`. Nothing in this stack is
permitted to bypass policy-as-code.

## Why policy-as-code exists

Dealix is a Saudi B2B Revenue Operating System. Every agent output that
touches a prospect, a customer, a contract, a payment, or a public proof
asset must be auditable, refusable, and reversible. Writing policy as
prose makes that impossible at scale; writing policy as code makes it a
build-time constraint. The rules below are how we encode the
non-negotiables that the founder, the trust guardian, and the security
guardian are all responsible for upholding.

The core non-negotiables encoded in the rules:

- A3 (autonomous external action) is banned. Agents may draft, queue,
  and recommend, but never act externally without explicit founder
  approval recorded in the audit ledger.
- No external sending, proof publication, pricing/contract/payment
  commitments without explicit founder approval recorded in
  `trust/approval_decisions.csv`.
- No guaranteed revenue, sales, or meeting claims appear in any draft.
- The private ops runtime is the only sanctioned storage for
  operational state (approvals, suppression, audit), and it lives
  outside the repository.

## Rule structure

Each rule in `policies/dealix_control_policy.yaml` carries the
following fields:

| Field         | Purpose                                                                                  |
| ------------- | ---------------------------------------------------------------------------------------- |
| `id`          | Stable identifier; emitted with every audit event that refers to the rule.               |
| `description` | One-line plain-English explanation surfaced in the Founder Console policies panel.       |
| `severity`    | `info`, `low`, `medium`, `high`, or `critical`. Maps to alerting and rollout decisions.   |
| `applies_to`  | List of action keys this rule guards. Wildcard `*` is supported but reserved.            |
| `deny_when`   | Keyed match against the action context. The rule denies only when all key/values match.  |
| `reason`      | Machine-stable reason string returned to the caller; mirrored in the audit row.          |
| `owner`       | Accountable role. The role appears in the registry and the on-call rotation.             |

The evaluator iterates rules in declaration order. The first matching
deny short-circuits the evaluation. An empty `deny_when` block makes a
rule informational. Special handling exists for `no_a3_auto` on
`external_send` actions: any external send without an explicit
`approval_class` in the context is rejected, even if no `deny_when`
keys match.

## The 11 rules

The list below is canonical for v1. Any change here must ship as a
versioned bump (`version: 2`) and a documented migration.

### 1. `no_a3_auto`

- Severity: `critical`
- Applies to: `external_send`, `outreach_send`, `post_publish`,
  `contract_sign`
- Denies when: `approval_class == A3`
- Owner: `founder`

A3 is the autonomous external action class. It is banned at the policy
layer, registered as banned in `registries/agent_registry.yaml`
(`banned_approval_classes: [A3]`), and asserted in the eval gate. If a
caller hands an `A3` approval class to the evaluator we reject with
`A3_disabled_in_dealix`.

### 2. `no_suppressed_outreach`

- Severity: `high`
- Applies to: `outreach_draft`, `outreach_send`
- Denies when: `target_suppressed == true`
- Owner: `trust_guardian`

The Distribution Operator agent is required to call the suppression
check before queueing any draft. The check sets
`target_suppressed: true|false` in the action context; this rule
finishes the job by refusing the queue write. See `SUPPRESSION_SYSTEM.md`
for the suppression contract.

### 3. `high_risk_requires_evidence`

- Severity: `high`
- Applies to: `approval_approve`
- Denies when: `risk == high && evidence_present == false`
- Owner: `trust_guardian`

High-risk approvals (data exports, payment-term changes, contract
amendments, expansion commitments) must carry evidence references. The
Founder Console surfaces an evidence field whenever the approval row
is tagged `risk: high`.

### 4. `no_guaranteed_revenue_claims`

- Severity: `critical`
- Applies to: `outreach_draft`, `proposal_draft`,
  `marketing_copy_draft`, `sample_draft`
- Denies when: `contains_guaranteed_claim == true`
- Owner: `brand_guardian`

This rule mirrors the `no_guaranteed_claims` eval suite. The eval
runner pattern-matches drafts for banned phrasing (`guaranteed
revenue`, `100% conversions`, `we promise sales`); the policy rule
ensures that even if a draft slips past the eval gate, the queueing
step refuses it. See `NO_OVERCLAIM_POLICY.md` for the phrasing matrix.

### 5. `approved_a2_can_request_execution`

- Severity: `medium`
- Applies to: `external_send`
- Denies when: `approval_class == A2 && approved == false`
- Owner: `founder`

A2 (assist) outputs may request external execution only after a
founder approval is recorded. This is the rule that prevents an
auto-replay of a queued draft from acquiring agency.

### 6. `public_proof_requires_approval`

- Severity: `critical`
- Applies to: `proof_publish`
- Denies when: `approval_state == draft`
- Owner: `proof_safety_agent`

Case studies, public screenshots, customer logos, and named proof
artifacts must carry an `approved` state in the proof library. The
Proof Safety Agent is the only path to flip the state, and it requires
a redaction lint pass plus a customer-consent flag.

### 7. `pricing_commit_requires_approval`

- Severity: `critical`
- Applies to: `pricing_commit`, `discount_commit`, `contract_commit`,
  `refund_commit`, `payment_terms_commit`
- Denies when: `approved == false`
- Owner: `founder`

External pricing, discount, contract, refund, and payment-term
commitments require explicit founder approval. The Finance Copilot may
prepare proposals but cannot commit. This rule is the policy
counterpart to the `pricing_safety`, `contract_safety`, and
`payment_terms_safety` eval suites.

### 8. `data_export_requires_escalation`

- Severity: `critical`
- Applies to: `data_export`
- Denies when: `escalation_recorded == false`
- Owner: `security_guardian`

Customer data exports require an escalation record. The Security
Guardian raises a trust flag, the founder reviews, and the escalation
is recorded in `trust/approval_decisions.csv` with `risk: high` before
the export can proceed.

### 9. `payment_terms_require_escalation`

- Severity: `high`
- Applies to: `payment_terms_change`
- Denies when: `escalation_recorded == false`
- Owner: `finance_copilot`

A change to payment terms (net 30 to net 60, milestone restructuring,
currency switch) cannot be applied without an escalation record. The
Finance Copilot raises the request; the founder approves.

### 10. `contract_change_requires_escalation`

- Severity: `high`
- Applies to: `contract_change`
- Denies when: `escalation_recorded == false`
- Owner: `founder`

Contract changes (scope, term, SLA, data residency) must be escalated
to the founder. This rule plus rule 7 form a two-step lock around any
change to a customer contract.

### 11. `destructive_operation_requires_escalation`

- Severity: `critical`
- Applies to: `destructive_op`
- Denies when: `escalation_recorded == false`
- Owner: `security_guardian`

Destructive operations (mass delete, drop, force-push, mass-update)
require escalation. This is the policy-layer guard for the Incident
Response Agent and any automation that touches production state.

## How the evaluator integrates with the API

`evaluate_action()` is imported in the founder console internal router
(`api/routers/founder_console_internal.py`). Every state-changing
endpoint calls it. When the call returns `allowed=False`, the endpoint
raises HTTP 409 with `{"rule": ..., "reason": ...}` as the detail
payload. The Founder Console UI surfaces the rule and the reason to
the founder verbatim. The reason strings are stable across versions
and are mirrored in the audit row.

The evaluator is cached via `functools.lru_cache` so policy reads do
not hit disk per request. To force a reload (after editing
`policies/dealix_control_policy.yaml`), restart the worker or clear
the cache.

## Versioning and change control

Policy is versioned at the file level. A change to the rule set
requires:

1. A bump of the `version` field in
   `policies/dealix_control_policy.yaml`.
2. A migration note in this document.
3. A green run of `scripts/verify_policy_as_code.py`.
4. A founder approval recorded in `trust/approval_decisions.csv`
   under the `policy_change` action.

The eval gate (`evals/gates/dealix_agent_eval_gate.yaml`) and the
agent registry (`registries/agent_registry.yaml`) follow the same
discipline. The four documents together form the trust plane;
changing one in isolation is never appropriate.
