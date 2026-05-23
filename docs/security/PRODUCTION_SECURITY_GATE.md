# Production Security Gate

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

The Production Security Gate is the set of checks that must pass
before any environment is considered "production." It is a posture
check, not a one-time event. The gate is re-run after every
deployment and reviewed weekly.

## Scope

| Concern                              | In scope                  |
| ------------------------------------ | ------------------------- |
| Internal API auth                     | Yes.                      |
| Public application surface            | Yes.                      |
| Worker orchestrator                   | Yes.                      |
| Database posture                      | Yes.                      |
| Private ops runtime mount             | Yes.                      |
| CI required checks                    | Yes (gate dependency).    |
| Customer data                         | Yes.                      |
| Secrets management                    | Yes.                      |

## Gate checks

### 1. Internal API auth in enforced mode

| Check                                                       | Pass criterion                                          |
| ----------------------------------------------------------- | ------------------------------------------------------- |
| `DEALIX_INTERNAL_TOKEN` is set.                              | Environment variable present and non-trivial.            |
| Founder Console responses return `auth_mode: "enforced"`.    | Test endpoint returns the expected mode.                 |
| 401 response when token is missing or wrong.                 | Smoke-test request returns 401.                          |

### 2. HTTPS everywhere

| Check                                                       | Pass criterion                                          |
| ----------------------------------------------------------- | ------------------------------------------------------- |
| All public endpoints respond on HTTPS.                       | Plain-HTTP requests redirect or refuse.                  |
| HSTS header set with reasonable max-age.                      | Header inspection.                                        |

### 3. CORS posture

| Check                                                       | Pass criterion                                          |
| ----------------------------------------------------------- | ------------------------------------------------------- |
| Allowed origins match the documented list.                  | See `docs/security/CORS_POLICY.md`.                      |
| Wildcard origins disallowed in production.                  | Configuration audit.                                    |

### 4. Rate limits

| Check                                                       | Pass criterion                                          |
| ----------------------------------------------------------- | ------------------------------------------------------- |
| Public endpoints have rate limits.                           | See `docs/security/RATE_LIMITS.md`.                       |
| Limits are non-zero and tested.                              | Smoke test with controlled burst.                        |

### 5. Secrets

| Check                                                       | Pass criterion                                          |
| ----------------------------------------------------------- | ------------------------------------------------------- |
| No secrets in the repository.                                | Gitleaks pass; secrets baseline current.                 |
| Pre-commit hooks active.                                     | `.pre-commit-config.yaml` matches required hooks.        |
| Secrets-scan log shows recent green pass.                    | `security/security_status.csv` latest row.               |

### 6. Database posture

| Check                                                       | Pass criterion                                          |
| ----------------------------------------------------------- | ------------------------------------------------------- |
| Postgres connection requires TLS.                            | Connection string asserts SSL.                           |
| Backups taken in the last 24 hours.                          | Backup log inspected.                                    |
| Restore drill completed in the last quarter.                  | Drill log inspected.                                    |

### 7. Private ops runtime

| Check                                                       | Pass criterion                                          |
| ----------------------------------------------------------- | ------------------------------------------------------- |
| `PRIVATE_OPS` is set and the path exists.                    | Environment audit.                                       |
| Directory is writable by the application process.            | File-system check.                                       |
| Recent backup of the runtime exists.                          | Backup log inspected.                                    |
| Bootstrap files present.                                     | All canonical CSVs present (per bootstrap script).       |

### 8. Worker orchestrator

| Check                                                       | Pass criterion                                          |
| ----------------------------------------------------------- | ------------------------------------------------------- |
| Orchestrator is running.                                      | Health endpoint or process check.                        |
| `runtime/worker_state.csv` was updated in the last hour.      | File inspection.                                         |
| No worker has been `failed` for >24h.                          | File inspection.                                         |

### 9. CI required checks

| Check                                                       | Pass criterion                                          |
| ----------------------------------------------------------- | ------------------------------------------------------- |
| Branch protection enforces the four required workflows.      | See `BRANCH_PROTECTION_REQUIRED_CHECKS.md`.              |
| Last main-branch run is green.                                | CI dashboard inspection.                                  |

### 10. Eval and trust posture

| Check                                                       | Pass criterion                                          |
| ----------------------------------------------------------- | ------------------------------------------------------- |
| Latest eval gate pass shows no blocking failures.            | `evals/eval_status.csv` latest row.                      |
| No open trust flag at `severity: critical`.                   | `trust/trust_flags.csv`.                                |
| No open incident at `severity: critical`.                     | `trust/incidents.csv`.                                  |
| Audit ledger writes are succeeding.                           | Latest audit row recent.                                 |

### 11. Customer data posture

| Check                                                       | Pass criterion                                          |
| ----------------------------------------------------------- | ------------------------------------------------------- |
| Customer data does not reside in the private ops runtime.    | Audit of runtime files.                                  |
| Data export endpoints require approval.                       | Manual verification.                                     |
| PDPL retention policy is enforced.                            | See `docs/DATA_RETENTION_POLICY.md`.                      |

## Failure handling

A failed gate check means the environment is not production. The
posture is downgraded and the gate must be re-passed. The Incident
Response Agent opens an incident if any critical-severity check
fails.

## Gate run cadence

| Trigger                          | Frequency                            |
| -------------------------------- | ------------------------------------ |
| After every deploy                | Always.                              |
| Weekly posture review              | Always.                              |
| Before a major release             | Always.                              |
| After an incident                  | After resolution.                    |

## Roles

| Role                            | Responsibility                                                   |
| ------------------------------- | ---------------------------------------------------------------- |
| Engineering                      | Runs the technical checks.                                       |
| Founder                          | Reviews the gate at the weekly posture meeting.                  |
| Trust Guardian                   | Confirms the trust posture checks.                               |
| Incident Response Agent          | Triggers incidents on critical failures.                         |

## Verifiers

Existing verifier scripts that contribute to the gate:

- `scripts/verify_dealix_ready.py`
- `scripts/verify_governance.py`
- `scripts/verify_policy_as_code.py`
- `scripts/verify_eval_gate.py`
- `scripts/verify_ultimate_operating_layer.py`
- `scripts/verify_sovereign_operating_stack.py`
- `scripts/verify_market_entry_stack.py`
- `scripts/verify_railway_production_config.py`

## What the gate will not do

- Auto-remediate failures.
- Approve a deploy without all checks green.
- Lower the bar to ship faster.

## Discipline

1. The gate is a posture, not a one-shot event.
2. Every check has a documented pass criterion.
3. Critical failures open incidents.
4. The weekly posture meeting reviews the latest gate result.
5. The trust posture is part of the security posture.

## Cross-references

- `ULTIMATE_SECURITY_GOVERNANCE.md` for the broader model.
- `INTERNAL_API_AUTH_GATE.md` for the internal auth detail.
- `BRANCH_PROTECTION_REQUIRED_CHECKS.md` for the CI side.
- `INCIDENT_RESPONSE_OS.md` for what happens on failure.
