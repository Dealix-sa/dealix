# Ultimate Security Governance

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

Security governance at Dealix is the discipline of keeping the
trust plane, the application, and the operating data safe enough
that customers can rely on us. This document is the top-level
reference for the security model, its owners, its surfaces, and its
practices.

## Owners

| Concern                            | Owner                                                          |
| ---------------------------------- | -------------------------------------------------------------- |
| Application security                | Engineering.                                                   |
| Trust plane                         | Trust Guardian + Founder.                                       |
| Secrets management                  | Engineering + Founder.                                          |
| Identity and access                  | Founder (gates), Engineering (mechanisms).                     |
| Incident response                   | Incident Response Agent + Engineering + Founder.                |
| PDPL alignment                      | Founder + Legal.                                                |
| Sovereign data residency            | Founder + Engineering.                                          |
| Backups and restore                  | Engineering.                                                   |

## Surfaces

| Surface                                  | Document                                          |
| ---------------------------------------- | ------------------------------------------------- |
| Application security gate                 | `PRODUCTION_SECURITY_GATE.md`.                    |
| Internal API auth                          | `INTERNAL_API_AUTH_GATE.md`.                      |
| Branch protection                          | `BRANCH_PROTECTION_REQUIRED_CHECKS.md`.           |
| Incident response                          | `INCIDENT_RESPONSE_OS.md`.                        |
| Backup and restore                          | `BACKUP_AND_RESTORE_OS.md`.                        |
| Access control                             | `ACCESS_CONTROL_MODEL.md`.                        |
| Trust plane                                 | `docs/trust/ULTIMATE_TRUST_PLANE.md`.              |

## Security principles

1. **Least privilege.** Every actor (human, agent, worker) has the
   minimum necessary scope.
2. **Defense in depth.** No single control is sufficient; controls
   stack.
3. **Audit everything that matters.** The audit ledger is the proof
   of discipline.
4. **Fail closed.** When in doubt, refuse the action.
5. **No silent fallback.** Dev modes are surfaced visibly (e.g.,
   `auth_mode: "dev_unprotected"`).
6. **Recovery before perfection.** Backups, restore drills, and
   incident response receive priority over hardening exotics.

## Threat model

The threats Dealix prioritizes:

| Threat                                                        | Primary control                                                       |
| ------------------------------------------------------------- | --------------------------------------------------------------------- |
| Token leakage                                                 | Token rotation, redaction in logs, `INTERNAL_API_AUTH_GATE.md`.       |
| Prompt injection                                              | `prompt_injection` eval suite; ingest sanitization.                    |
| Data exfiltration via worker                                  | `allowed_write_targets`, `data_export_safety` policy rule.            |
| Unauthorized state mutation                                    | Founder Console as single mutation surface; policy adapter.            |
| Drift in policy or registry                                   | Verifier scripts in CI; required checks.                              |
| Backup loss                                                   | Daily backups + restore drills.                                       |
| PDPL violation                                                | DPA in place; data retention policy; cross-border addendum.            |
| Stolen credentials                                            | MFA on accounts; key rotation; access control model.                  |
| Supply chain                                                  | Dependency scanning; minimal third-party surface.                     |
| Insider misuse                                                 | Audit ledger; single mutation surface; least privilege.               |

## Controls overview

### Application layer

- HTTPS everywhere.
- Strict CORS (see `docs/security/CORS_POLICY.md`).
- Rate limits on public endpoints (see
  `docs/security/RATE_LIMITS.md`).
- Secrets only via environment variables; never committed.
- Pre-commit hooks for secret detection (see
  `.pre-commit-config.yaml`).

### Internal API layer

- `DEALIX_INTERNAL_TOKEN` required in production.
- Token is rotated on a defined cadence (see
  `INTERNAL_API_AUTH_GATE.md`).
- Token is never logged.
- Token is never returned in responses.

### Worker layer

- `allowed_write_targets` enforced by the orchestrator.
- Kill switches per agent.
- Eval gate as a precondition to draft writes.

### Data layer

- Postgres backups daily (see `BACKUP_AND_RESTORE_OS.md`).
- Private ops runtime backups daily.
- Restore drills quarterly.
- Audit ledger is append-only; pruning is policy-gated.

### Identity layer

- Founder Console requires the internal token.
- Customer-facing application uses standard authentication.
- Service accounts have scoped permissions.

## Compliance posture

| Concern                  | Posture                                                              |
| ------------------------ | -------------------------------------------------------------------- |
| Saudi PDPL                | Aligned via DPA, retention policy, cross-border addendum.            |
| Saudi data residency      | Postgres in Saudi region (per deployment configuration).             |
| ZATCA invoicing          | Compliant per `docs/INVOICING_ZATCA_READINESS.md`.                    |
| GDPR (where applicable)   | Mirrored controls; not the primary alignment.                        |

## Required CI checks

The four GitHub workflows enforced as required checks are listed in
`BRANCH_PROTECTION_REQUIRED_CHECKS.md`. They cover:

- Test suite.
- Policy-as-code verifier.
- Trust plane verifiers (eval gate, agent registry, governance).
- Operating layer verifiers.

## Incident response

Incidents follow `INCIDENT_RESPONSE_OS.md`. Briefly:

1. The Incident Response Agent opens a row in
   `trust/incidents.csv`.
2. The founder is notified.
3. A short-form action plan is recorded.
4. The incident is closed only when the action plan is complete.
5. A post-mortem is filed within 48 hours of close.

## Backups and restore

Daily Postgres and private ops runtime backups. Restore drills
quarterly. See `BACKUP_AND_RESTORE_OS.md`.

## Discipline

1. Every external surface has a documented gate.
2. Every gate has an owner.
3. Every gate has a verifier in CI.
4. Every breach scenario has a documented response.
5. The trust plane and the security plane reinforce each other.

## Cross-references

- `PRODUCTION_SECURITY_GATE.md` for the production posture check.
- `INTERNAL_API_AUTH_GATE.md` for the Founder Console auth.
- `BRANCH_PROTECTION_REQUIRED_CHECKS.md` for CI gates.
- `INCIDENT_RESPONSE_OS.md` for incident handling.
- `BACKUP_AND_RESTORE_OS.md` for data resilience.
- `ACCESS_CONTROL_MODEL.md` for the identity model.
