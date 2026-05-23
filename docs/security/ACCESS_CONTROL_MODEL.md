# Access Control Model

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

The Access Control Model is the discipline by which humans, agents,
and workers are granted exactly the scope they need to do their work,
and no more. The model is intentionally narrow: a small number of
roles, explicit scopes, and an audit trail for every grant and
revocation.

## Principles

1. **Least privilege.** Every role gets the minimum necessary access.
2. **Explicit scope.** Implicit access is not access.
3. **Audited grants.** Every grant and revocation produces an audit
   row.
4. **Separation of concerns.** Operating roles and security roles
   are distinct.
5. **Single mutation surface.** The Founder Console is the only path
   for state-changing operations on the trust plane.

## Actors

| Actor                          | Type     | Notes                                                          |
| ------------------------------ | -------- | -------------------------------------------------------------- |
| Founder                         | Human    | Final approver for trust-plane actions.                         |
| Engineering                     | Human    | Code, infrastructure, deploys.                                 |
| Customer Success / Delivery     | Human    | Sprint execution, customer relationships.                      |
| Legal                           | Human    | Contracts, DPAs, compliance.                                   |
| Agents                          | Software | A1 (read-only / single write target) or A2 (assist).            |
| Workers                         | Software | Instances of agents running on a schedule.                     |
| Customers                       | Human    | Customer-facing application access only.                       |
| Partners                        | Human    | Limited access if any; per partner agreement.                  |
| Auditors                        | Human    | Time-boxed read access to specific artifacts.                  |

## Roles and scopes

### Founder

| Scope                                   | Notes                                                       |
| --------------------------------------- | ----------------------------------------------------------- |
| Full Founder Console access              | The console enforces the trust plane.                       |
| Repository merge to `main`               | Subject to required checks.                                 |
| Secrets store                            | Holds production secrets; rotates per policy.               |
| Audit ledger                             | Reads; writes happen via the console.                       |
| External communications                  | Sole final approver.                                        |

### Engineering

| Scope                                   | Notes                                                       |
| --------------------------------------- | ----------------------------------------------------------- |
| Repository write (PRs only)              | No direct push to `main`.                                   |
| Staging environment                       | Full access.                                                |
| Production environment                    | Deploys via CI; no manual SSH.                               |
| Logs and metrics                          | Read access.                                                |
| Postgres                                  | Read access for debugging; writes via application only.     |
| Private ops runtime                       | Read access; writes only through workers and the console.   |
| Secrets store                              | Limited; rotation of operational tokens.                     |

### Customer Success / Delivery

| Scope                                   | Notes                                                       |
| --------------------------------------- | ----------------------------------------------------------- |
| Founder Console (delivery-specific endpoints) | Read; queue drafts. No external sending.               |
| Customer artifacts                         | Per engagement scope.                                       |
| Customer Success CSVs                      | Read; writes via Customer Success agents.                  |

### Legal

| Scope                                   | Notes                                                       |
| --------------------------------------- | ----------------------------------------------------------- |
| Contract repository                      | Read/write within legal review process.                     |
| Audit ledger                              | Read for compliance review.                                  |
| DPA storage                                | Read/write.                                                  |

### Agents

Agents are software actors declared in
`registries/agent_registry.yaml`. Each agent has:

| Field                            | Notes                                                          |
| -------------------------------- | -------------------------------------------------------------- |
| `approval_class_max`             | `A1` or `A2`. A3 is banned.                                    |
| `tools`                          | A whitelist of tool ids.                                        |
| `external_action_allowed`         | Must be `false`.                                                |
| `allowed_write_targets`            | Directory paths in the private ops runtime.                    |
| `kill_switch`                     | Must be `true`.                                                 |
| `enabled`                          | The current state; can be flipped from the console.             |

Agents do not have direct database access. Agents do not have
external network access except through the application.

### Workers

Workers inherit the agent's scope and run under the orchestrator.
The orchestrator enforces `allowed_write_targets` at the file system
level. Any write outside the declared targets is refused and audit-
recorded.

### Customers

Customer access is via the customer-facing application. Customers
do not see the Founder Console.

### Partners

Partners do not have system access by default. Partner programs
that involve any access carry a specific addendum and a time-boxed
scope.

### Auditors

External auditors receive time-boxed, read-only access to specific
artifacts. The grant is recorded as an audit row
(`action: auditor_grant`, `risk: medium`) and revoked at the end of
the window.

## Grant and revocation

| Action                            | Audit action                  | Risk     | Approver             |
| --------------------------------- | ----------------------------- | -------- | -------------------- |
| Grant human role                  | `role_grant`                  | medium   | Founder.             |
| Revoke human role                  | `role_revoke`                 | medium   | Founder.             |
| Enable an agent                    | `agent_enable`                | medium   | Founder.             |
| Disable an agent                   | `agent_disable`               | high     | Founder.             |
| Grant a tool to an agent           | `agent_tool_grant`            | medium   | Founder.             |
| Revoke a tool from an agent        | `agent_tool_revoke`           | medium   | Founder.             |
| Issue auditor grant                 | `auditor_grant`               | medium   | Founder.             |
| Revoke auditor grant                | `auditor_revoke`              | medium   | Founder.             |
| Rotate token                       | `token_rotation`              | medium   | Founder.             |

## Authentication

| Surface                              | Mechanism                                                     |
| ------------------------------------ | ------------------------------------------------------------- |
| Founder Console                      | `x-dealix-internal-token` (see `INTERNAL_API_AUTH_GATE.md`).   |
| Customer application                  | Standard authentication (per application).                     |
| Postgres                              | Per-environment credentials.                                   |
| Object storage                         | IAM roles.                                                    |
| Repository                             | GitHub identity + 2FA.                                          |
| Secrets store                          | MFA-protected.                                                  |

MFA is required for all human access.

## Authorization

Authorization is enforced at three layers:

1. **Surface.** The Founder Console requires the internal token.
2. **Policy.** The policy adapter refuses guarded actions per the
   policy file.
3. **Runtime.** The worker orchestrator refuses writes outside the
   `allowed_write_targets`.

A request must clear all three layers to take effect.

## Customer data access

| Aspect                              | Practice                                                       |
| ----------------------------------- | -------------------------------------------------------------- |
| Storage                              | Postgres (business) + object storage (artifacts).              |
| Worker access                         | Through the application API only.                              |
| Direct database access                 | Read-only for debugging; no production write outside the app. |
| Cross-tenant                           | Disallowed without a documented arrangement.                  |
| Export                                 | Policy-gated (`data_export_requires_escalation`).             |

## Revocation drill

Quarterly drill:

1. Pick a sample human role and an agent.
2. Revoke and re-grant.
3. Confirm the audit row is present.
4. Confirm the access change took effect.
5. Record the drill in the audit ledger.

## Anti-patterns

| Anti-pattern                                          | Why                                                                |
| ----------------------------------------------------- | ------------------------------------------------------------------ |
| Shared accounts                                        | Audit becomes ambiguous.                                            |
| Implicit access                                        | Implicit is not auditable.                                          |
| Long-lived agent tool grants beyond scope               | Agents should have only the tools they currently need.              |
| Customer data in the private ops runtime                | Boundary violation.                                                 |
| Auditor access without time-boxing                      | Drift.                                                              |
| MFA disabled for any human account                      | Critical posture failure.                                            |

## Discipline

1. Least privilege, always.
2. Explicit scopes, always.
3. Audited grants, always.
4. MFA for humans, always.
5. The Founder Console is the only mutation surface for the trust
   plane.

## Cross-references

- `ULTIMATE_SECURITY_GOVERNANCE.md` for the broader model.
- `INTERNAL_API_AUTH_GATE.md` for the Founder Console gate.
- `AUDIT_EVENT_MODEL.md` for the audit row schema.
- `ULTIMATE_TRUST_PLANE.md` for the trust plane.
