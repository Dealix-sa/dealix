# Policy-as-Code System

> Make Dealix trust decisions explicit, testable, and
> version-controlled.

## Purpose

Trust policies stop being prose in a wiki and become YAML files in the
repo. Every change goes through PR, CI, and the founder's approval —
not a tribal decision that nobody can later audit.

This lets `/approvals`, `/trust`, and the workers all evaluate the
**same** rules, in the same way, with the same outcome.

## Position in the Operating Layer

Policy-as-Code is the deterministic half of the Trust Plane. Trust
Guardian is the judgment half. They run in sequence; stricter wins.

```
Agent / Frontend / Approval Request
       │
       ▼
Policy Evaluator (this system)
       │
       ▼  (allow / require_review / deny)
Trust Guardian
       │
       ▼
Approval Queue / Audit / Worker
```

## Policy Files

| File | Scope |
|------|-------|
| `policies/founder_console_policy.yaml` | Approval-class rules, A3 lockout, evidence requirements, suppression enforcement, A2 promotion conditions |
| `policies/outreach_policy.yaml` (later) | Outreach-specific: sector cadence, language, evidence, banned phrasing |
| `policies/proposal_policy.yaml` (later) | Proposal-specific: pricing matrix bounds, discounts, contract template requirement |
| `policies/proof_policy.yaml` (later) | Public proof: signoff requirement, redaction, attribution |
| `policies/data_export_policy.yaml` (later) | Who may export which classes of data, with which destination |

v1 ships the first one. The others are added when the corresponding
surface (outreach, proposal, proof, export) is moved into the trust
plane.

## Rule Schema

Each rule is a YAML object with:

```yaml
- id: stable_snake_case_id
  description: One short sentence in English.
  if:
    # any combination of these match keys
    approval_class: A1 | A2 | A3
    risk_level: Low | Medium | High | Critical | [list]
    suppressed: true | false
    evidence_required: true | false
    evidence_exists: true | false
    decision: Pending | Approved | Rejected | Escalated
  then:
    result: ALLOW | ALLOW_AFTER_APPROVAL | REQUIRE_EVIDENCE | DENY | ESCALATE
    external_action_allowed: true | false
```

`if` keys are AND-ed. List values mean "any of". The evaluator runs all
rules; if any rule yields a stricter outcome (DENY > ESCALATE >
REQUIRE_EVIDENCE > ALLOW_AFTER_APPROVAL > ALLOW), that outcome wins.

## Output

The evaluator returns:

```json
{
  "result": "ALLOW | ALLOW_AFTER_APPROVAL | REQUIRE_EVIDENCE | DENY | ESCALATE",
  "external_action_allowed": true,
  "fired_rules": ["no_a3_auto", "..."],
  "policy_version": "string (file hash + commit)",
  "evaluated_at": "ISO-8601"
}
```

Every evaluation writes a `policy.evaluation` audit event with the
inputs (hashed), outputs, and policy version.

## CI Wiring

Every PR that touches a `policies/*.yaml` file must:

1. Validate the YAML against the schema.
2. Run the policy unit tests in `tests/policies/`.
3. Run a diff report showing rule changes in human-readable form.
4. Require founder approval before merge.

## Versioning

- Policy version = git commit hash of the policies directory.
- Surfaces show the active policy version (`/approvals`, `/trust`).
- A drift between the version in the running process and the version
  on disk causes the Trust Plane to fail closed until reconciled.

## Rule

> Trust policy changes go through PR, CI, and approval. No live edits.

A "live policy edit" means typing into the production server. We do not
do that. If the founder needs to change a policy now, the change goes
through a PR-and-merge flow that takes minutes, not seconds — and that
is the point.

## Failure Modes

| Mode | Detection | Response |
|------|-----------|----------|
| YAML schema invalid | CI validation | Block merge |
| Stricter rule introduced silently | Diff report in PR | Founder review required |
| Evaluator unreachable | Health check | Trust Plane fails closed |
| Policy version drift | Process vs disk hash | Block external actions until aligned |
| Policy bypass attempted | Audit shows action without `policy.evaluation` | Open incident, freeze writer |

## See Also

- [`DEALIX_OPERATING_LAYER_V1`](../ops/DEALIX_OPERATING_LAYER_V1.md)
- [`TRUST_GUARDIAN_AGENT`](../ai/TRUST_GUARDIAN_AGENT.md)
- [`AI_NATIVE_COMPANY_ARCHITECTURE`](../architecture/AI_NATIVE_COMPANY_ARCHITECTURE.md)
- `policies/founder_console_policy.yaml`
