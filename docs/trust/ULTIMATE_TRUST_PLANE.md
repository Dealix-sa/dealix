# Ultimate Trust Plane

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

The trust plane is the meta-architecture that makes every Dealix
output safe enough to ship. It is not a single component; it is a
discipline expressed across four artifact families plus an audit
ledger. Every agent, every Founder Console action, and every worker
pass through it. There are no side doors.

## The four artifact families

| Family       | Path                                       | Purpose                                                            |
| ------------ | ------------------------------------------ | ------------------------------------------------------------------ |
| Policy       | `policies/dealix_control_policy.yaml`      | Declarative rules; what is denied, by whom, under what context.    |
| Registry     | `registries/agent_registry.yaml`           | What each agent is allowed to do; the kill switches and the bans.  |
| Eval gate    | `evals/gates/dealix_agent_eval_gate.yaml`  | Pre-output checks that block regressions before drafts surface.    |
| Audit        | `trust/approval_decisions.csv` (private)   | Append-only ledger of every approval, rejection, and escalation.   |

These four files are the only sanctioned source of trust truth. If a
fifth file claims to override any of them, that file is wrong. The
Founder Console (`api/routers/founder_console_internal.py`) is the
only sanctioned surface that operates on them.

## Layered enforcement

The trust plane stacks four enforcement layers. A draft must clear all
four before it can become an externally observable action.

1. **Brand and content layer.** The Brand Guardian and Content
   Strategist agents validate phrasing, voice, and proof claims. The
   `no_guaranteed_claims` eval suite runs at this layer.
2. **Eval gate layer.** The Eval Guardian agent runs the full 15-suite
   gate before any draft can land in the approvals queue. Blocking
   suites must show zero failures.
3. **Policy layer.** Every Founder Console endpoint that mutates state
   calls `evaluate_action()` from `api/internal/policy_adapter.py`.
   The 11 policy rules can refuse a request even after eval passes.
4. **Founder layer.** The founder is the final approver for every A2
   output, every pricing commit, every proof publication, every data
   export, every contract change. There is no auto-approve.

Each layer logs to the audit ledger when it makes a decision. The
audit row carries `actor`, `action`, `target`, `risk`, and the JSON
payload. The schema is documented in `AUDIT_EVENT_MODEL.md`.

## Banned classes and banned paths

The trust plane explicitly bans:

- **A3 (autonomous external action).** Encoded in
  `registries/agent_registry.yaml` as `banned_approval_classes: [A3]`.
  Reinforced by policy rule `no_a3_auto` and eval suite
  `A3_escalation`.
- **External sending without approval.** Policy rule
  `approved_a2_can_request_execution` plus the eval suite
  `approval_bypass`.
- **Proof publication without approval.** Policy rule
  `public_proof_requires_approval` plus the eval suite `proof_safety`.
- **Guaranteed revenue, sales, or meeting claims.** Policy rule
  `no_guaranteed_revenue_claims` plus the eval suite
  `no_guaranteed_claims`.
- **Pricing, discount, contract, refund, or payment-term commitments
  without founder approval.** Policy rule
  `pricing_commit_requires_approval` plus eval suites `pricing_safety`,
  `contract_safety`, `payment_terms_safety`, `proposal_safety`.
- **Customer data export without escalation.** Policy rule
  `data_export_requires_escalation` plus eval suite
  `data_export_safety`.
- **Destructive operations without escalation.** Policy rule
  `destructive_operation_requires_escalation`.

There is no override switch. To remove a ban, the founder must change
the source file, bump its version, and re-record approval in the audit
ledger.

## The approval queue contract

Every action that resembles external agency flows through the
approval queue. The queue is the file
`approvals/approval_queue.csv` in the private ops runtime. The
Founder Console reads it via
`/api/v1/internal/approvals` and writes decisions via
`/api/v1/internal/approvals/{id}/approve`, `/reject`,
`/request-edit`, `/escalate`. Each decision is policy-evaluated before
being committed.

The queue schema is documented in `PRIVATE_OPS_RUNTIME_CONTRACT.md`.
The lifecycle is:

1. An agent drafts an action and writes a row with `status: open`.
2. The Trust Guardian raises any flags as separate rows in
   `trust/trust_flags.csv`.
3. The founder reviews the row in the Founder Console.
4. The founder approves, rejects, requests-edit, or escalates.
5. The decision is recorded in `trust/approval_decisions.csv`.
6. The downstream worker reads the audit row and acts.

The worker never reads the queue without checking the audit ledger
first. This is the rule that prevents a stale `approved` flag from
being honored after a revoke.

## Suppression as a first-class trust object

Suppression is not a list of email addresses; it is a contract. See
`SUPPRESSION_SYSTEM.md` for the match-types, lifecycle, and the audit
trail. The trust plane treats suppression as an enforcement
mechanism on par with the policy file: a missed suppression check is
a critical incident, not a near miss.

## Kill switches

Every agent declared in the registry carries `kill_switch: true`. The
Founder Console exposes `agent_disable` and `agent_enable` endpoints
that record an audit row with `risk: high` (disable) or
`risk: medium` (enable). The worker orchestrator checks the registry
state before starting any worker pass; a disabled agent does not run.

In incident conditions, the Incident Response Agent can flip kill
switches via the same console path. The audit row carries the
incident id in the payload.

## How the trust plane defends against drift

Three mechanisms protect against drift:

1. **Verifier scripts.** `scripts/verify_policy_as_code.py`,
   `scripts/verify_eval_gate.py`, `scripts/verify_agent_registry.py`,
   and `scripts/verify_governance.py` run in CI. They block merges
   that desynchronize the four artifact families.
2. **Append-only audit.** The audit CSV is append-only by convention,
   and the storage path is outside the repo. Rotating or pruning the
   audit is itself an action that must be recorded.
3. **Founder Console as single origin.** The internal API is the only
   sanctioned mutation path. It is protected by
   `DEALIX_INTERNAL_TOKEN` and surfaces `auth_mode` in every
   response, so a dev-unprotected deployment is impossible to miss.

## What the trust plane is not

The trust plane is not a compliance veneer. It is not aspirational
language about safety. It is not a single agent or a single file. It
is the union of four files, one append-only ledger, and a strict
discipline that no agent, no script, and no person bypasses the
Founder Console for state-changing operations.

The next document, `FOUNDER_CONSOLE_TRUST_GATE.md`, walks through how
the console enforces this discipline at the API surface.
