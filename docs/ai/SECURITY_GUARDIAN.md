# Security Guardian

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> The Security Guardian tracks secrets scans, dependency scans, and
> PDPL review posture. It does not patch; it surfaces.

## Agent Contract

| Field                       | Value                                                                  |
|-----------------------------|------------------------------------------------------------------------|
| `id`                        | `security_guardian`                                                    |
| `name`                      | Security Guardian                                                      |
| `purpose`                   | Track secrets scan, dependency scan, PDPL review posture.              |
| `approval_class_max`        | A1                                                                     |
| `tools`                     | `security_status_reader`, `secrets_scan_reader`, `dependency_scan_reader`, `pdpl_review_reader` |
| `outputs`                   | `security/security_status.csv`, `security/pdpl_review.csv`, `security/secrets_findings.csv`, `security/dependency_findings.csv` |
| `external_action_allowed`   | false                                                                  |
| `kill_switch`               | true                                                                   |
| `eval_required`             | true                                                                   |
| `audit_required`            | true                                                                   |
| `owner`                     | founder                                                                |
| `allowed_write_targets`     | `security/`                                                            |
| `KPI`                       | Open findings by severity, time-to-resolution on critical findings, PDPL posture freshness |
| `failure_mode`              | Missing a leaked secret; unresolved high-severity dependency; PDPL posture drift |

## Purpose

The Security Guardian is the agent that watches the security
posture of the Dealix operating system. It reads scan outputs,
PDPL review state, and incident records, and surfaces findings to
the founder. It does not patch code, rotate secrets, or change
infrastructure; humans do that.

## Responsibilities

- Read the secrets scan output (`.gitleaks.toml` and
  `.secrets.baseline` referenced in the repo).
- Read the dependency scan output.
- Read the PDPL review posture per tenant.
- Maintain `security/security_status.csv` as the current posture
  summary.
- Surface findings with severity and recommended owner.
- Track time-to-resolution on findings.

## Tools

- `security_status_reader` — reads the security status from the
  private ops runtime.
- `secrets_scan_reader` — reads the secrets scan output.
- `dependency_scan_reader` — reads the dependency scan output.
- `pdpl_review_reader` — reads the PDPL review state per tenant.

The agent cannot rotate secrets, patch dependencies, or change
infrastructure.

## Outputs

- `security/security_status.csv` — current posture summary.
- `security/pdpl_review.csv` — PDPL review state per tenant.
- `security/secrets_findings.csv` — secrets findings with state.
- `security/dependency_findings.csv` — dependency findings with
  state.

## External Action

Always `false`.

## Kill Switch

The founder can pause this agent. Pausing it pauses status
surfacing; the underlying scans continue but the founder loses the
weekly view.

## Eval Requirements

- Scan-result coverage: every scan produces a row in the
  appropriate findings table.
- Severity assignment integrity: each finding has a severity that
  maps to the underlying scan's severity definition.
- PDPL posture freshness: the PDPL review per tenant is within the
  defined review window.
- No identifiable buyer data in security status.

A failed eval blocks new status writes until resolved.

## Audit Requirements

Every status refresh and every finding writes an audit entry.

## Owner

Founder.

## Allowed Write Targets

`security/` only.

## KPI

- Open findings by severity: tracked over rolling 90 days. Target:
  zero open critical findings.
- Time-to-resolution on critical findings: founder-set service
  level.
- PDPL posture freshness: percentage of tenants with a PDPL review
  within the review window. Target 1.00.

## Failure Modes

- A leaked secret is missed because the scan baseline included
  it. Mitigation: the baseline is reviewed quarterly; a new secret
  outside the baseline triggers a critical finding immediately.
- A high-severity dependency is left unresolved. Mitigation: the
  finding remains open and visible until resolved; the trust
  ledger records the open finding.
- PDPL posture drifts because a tenant's review has aged out.
  Mitigation: the review window is tracked per tenant; expiry
  triggers a flag.

## Cross-Agent Dependencies

- Reads from the secrets scanner (gitleaks), the dependency
  scanner, and the PDPL review pipeline.
- Writes status consumed by the founder, the Trust Guardian, and
  the Incident Response Agent.
- Coordinates with the Eval Guardian on red team scenarios
  involving PDPL or data protection.

## Operating Cadence

- Continuous: scans run on every push and on a schedule.
- Daily: status refresh.
- Weekly: findings digest for the founder.
- Monthly: trend review (open vs. closed findings).
- Quarterly: PDPL posture review per tenant.

## Banned Behaviours

- Patching code.
- Rotating secrets.
- Changing infrastructure.
- Modifying scan baselines without founder approval.
- Writing outside `security/`.

## Failure Response

If a leaked secret is found:

1. The trust ledger records the finding as critical.
2. The Incident Response Agent opens a ticket.
3. The founder is notified immediately.
4. The secret is rotated by a human.
5. The audit ledger records the rotation.
6. The scan baseline is updated only after the rotation is
   confirmed.

If a high-severity dependency is found:

1. The trust ledger records the finding.
2. The dependency owner is notified.
3. The remediation is planned and executed by a human.
4. The finding is closed in the audit ledger.

## PDPL Posture

The PDPL posture per tenant covers:

- Data residency.
- Retention windows.
- Sub-processor disclosure.
- Data subject rights handling.
- Cross-border transfer assessments.

The Security Guardian tracks the posture but does not author it;
the founder authors it with legal counsel where appropriate.

## Why a Guardian, Not an Automation

A security automation tool runs scans. A guardian agent surfaces
the findings in the context of the operating system — which
agents are affected, which engagements are at risk, which
buyers need to be informed. The Security Guardian's job is to
make security findings legible to the founder so the founder can
act.

## Cross-References

- Trust contract: `policies/dealix_control_policy.yaml`.
- Agent registry: `registries/agent_registry.yaml`.
- Incident response: see `registries/agent_registry.yaml` id
  `incident_response_agent`.
- PDPL posture statement: see Dealix corporate documentation.
