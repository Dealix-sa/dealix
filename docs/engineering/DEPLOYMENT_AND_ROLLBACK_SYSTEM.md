# Deployment and Rollback System

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Focused on Results.

This document is the canonical deploy and rollback playbook for the
Dealix application. It complements the existing operations runbooks
(`docs/DEPLOYMENT.md`, `docs/ops/DEPLOY_RUNBOOK.md`,
`docs/ops/ROLLBACK_RUNBOOK.md`) with a single, opinionated reference
that ties deploys to the trust posture, the eval gate, and the
private ops runtime.

## Deploy principles

1. **Small changes, often.** One change per deploy. Compound changes
   amplify failure modes.
2. **Reversible by default.** Every change must be revertable in one
   step. Schema changes ship with down-migrations or feature flags.
3. **Branch protection enforced.** Required checks must pass; see
   `BRANCH_PROTECTION_REQUIRED_CHECKS.md`.
4. **No deploy bypasses trust.** Deploys do not touch the audit
   ledger, the suppression list, or the policy file in production.
5. **Founder is informed of every deploy.** Deploys are recorded in
   the founder brief.

## Pipeline stages

```
local → PR → CI checks → review → merge → staging → production
```

### Stage 1: Local

- Run unit tests and the relevant verifier scripts before pushing.
- Run `pre-commit` (see `docs/PRE_COMMIT_SETUP.md`).
- Confirm no `policies/dealix_control_policy.yaml`,
  `registries/agent_registry.yaml`, or
  `evals/gates/dealix_agent_eval_gate.yaml` changes are unintended.

### Stage 2: PR

- PR includes a one-line summary of the change.
- PR carries a checkbox affirming "no trust-plane file changed
  unintentionally."
- Reviewer is required.

### Stage 3: CI checks

The four required workflows are listed in
`BRANCH_PROTECTION_REQUIRED_CHECKS.md`. They include trust-plane
verifiers, schema verifiers, and the test suite.

### Stage 4: Review

- One human reviewer minimum.
- Changes to trust-plane files require two reviewers, one of whom is
  the Trust Guardian's named human counterpart.
- Changes to the audit writer require security review.

### Stage 5: Merge

- Merges to `main` go through the protected branch.
- Squash-merge preferred; commit message references the audit
  context for any trust-relevant change.

### Stage 6: Staging

- Staging environment runs the same build as production.
- Staging private ops runtime is a separate path (e.g.,
  `/opt/dealix-ops-private-staging`).
- Staging soak time is at least 10 minutes for high-risk changes.

### Stage 7: Production

- Production deploys are time-boxed (avoid Thursday-Friday for
  trust-plane changes).
- Production deploy emits an audit row tagged
  `action: deploy_complete`, `risk: low`.

## Pre-deploy checklist

| Item                                                       | Verified by                                |
| ---------------------------------------------------------- | ------------------------------------------ |
| All CI checks green                                        | Engineering                                |
| No unintended trust-plane changes                           | PR reviewer                                |
| `DEALIX_INTERNAL_TOKEN` is set in production                | Environment audit                          |
| `PRIVATE_OPS` path mounted and writable                     | Environment audit                          |
| Recent Postgres backup available                            | `BACKUP_AND_RESTORE_OS.md`                 |
| Recent private ops snapshot available                       | `BACKUP_AND_RESTORE_OS.md`                 |
| Founder informed                                            | Founder brief                              |
| Rollback plan documented in PR                              | PR template                                |

## Post-deploy checklist

| Item                                                           | Verified by                |
| -------------------------------------------------------------- | -------------------------- |
| Smoke tests pass against the deployed environment              | Engineering                |
| Founder Console returns `auth_mode: "enforced"` in production  | Engineering                |
| Policy adapter loads (`/control/policies` returns rules)        | Engineering                |
| Worker orchestrator is running (`/workers/health` returns data) | Engineering                |
| Eval gate is green (`/evals/status` no blocking failures)       | Engineering                |
| No new trust flags at `severity >= high`                        | Trust Guardian             |

## Rollback playbook

Rollback is a normal operation, not an exception. We ship in a way
that makes rollback the fast path.

### When to roll back

| Signal                                                        | Action                  |
| ------------------------------------------------------------- | ----------------------- |
| 5xx rate above baseline by 2x for >5 minutes                  | Roll back.              |
| Founder Console returning `dev_unprotected` in production     | Roll back immediately. |
| Policy adapter denial spike on `no_a3_auto`                    | Investigate first; roll back if drift is in code. |
| Audit ledger write failures                                    | Roll back immediately. |
| Trust flag at `severity: critical` related to the deploy        | Roll back. Open incident. |
| Worker mass failure                                            | Roll back. Investigate. |

### How to roll back

1. Revert the merge commit on `main`. Do not amend or force-push.
2. Trigger a deploy of the previous artifact (CI tag-based deploy).
3. Verify the post-deploy checklist on the rolled-back version.
4. Record the rollback in the audit ledger via
   `action: deploy_rollback`, `risk: high`.
5. Open an incident in `trust/incidents.csv` with the deploy id.
6. Schedule a post-mortem within 48 hours.

### What rollback does not undo

- Audit ledger rows. Those are immutable.
- Suppression list rows. Those are immutable.
- Customer data committed during the broken deploy. Those follow the
  data export / restore path in `BACKUP_AND_RESTORE_OS.md`.

## Schema changes

| Change type                       | Rollback path                                          |
| --------------------------------- | ------------------------------------------------------ |
| Additive Postgres migration       | Down-migration via Alembic. Backward compatible.       |
| Destructive Postgres migration    | Disallowed in the same deploy as code that depends on the change. Phased: deploy code that tolerates both shapes, then migrate, then clean up. |
| Additive CSV column                | Append on the right; readers tolerate.                  |
| Destructive CSV column             | Disallowed without a deprecation cycle.                |
| Policy rule change                 | New version of the policy file; old rules stay until removed in a separate deploy. |
| Agent registry change              | Same as policy: versioned, audited.                    |

## Feature flags

Feature flags are encouraged for any change that could affect the
trust plane. Flags are documented in the PR. Flag toggles in
production are audit-recorded (`action: feature_flag_toggle`,
`risk: medium`).

## Incident hook

A deploy that triggers an incident enters the incident response
flow (`INCIDENT_RESPONSE_OS.md`). The deploy id, the incident id,
and the rollback id are linked in the post-mortem.

## Verifier coverage

The following verifiers must pass on every deploy:

- `scripts/verify_ultimate_operating_layer.py`
- `scripts/verify_sovereign_operating_stack.py`
- `scripts/verify_market_entry_stack.py`
- `scripts/verify_policy_as_code.py`
- `scripts/verify_eval_gate.py`
- `scripts/verify_agent_registry.py`
- `scripts/verify_governance.py`

The four GitHub workflows that run these are listed in
`BRANCH_PROTECTION_REQUIRED_CHECKS.md`.

## Discipline

1. Small changes, often.
2. Reversible by default.
3. Required checks are real, not theatre.
4. The trust plane is the constraint; deploy practice is the means.
5. Rollback is normal. Incidents are not.
