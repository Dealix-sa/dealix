# Incident Response OS

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

The Incident Response OS is how Dealix detects, contains, recovers
from, and learns from operational and security incidents. It is owned
by the Incident Response Agent (A1 max), with the founder as the
final authority. The audit ledger is the spine.

## Source files

| File                              | Purpose                                                          |
| --------------------------------- | ---------------------------------------------------------------- |
| `trust/incidents.csv`              | Open and closed incidents.                                        |
| `trust/trust_flags.csv`            | Trust flags that may escalate to incidents.                       |
| `trust/approval_decisions.csv`     | Every incident-related decision is audit-recorded.                |

The Founder Console exposes incidents indirectly via the CEO summary
and the trust flags feed.

## Incident severity

| Severity   | Examples                                                                 |
| ---------- | ------------------------------------------------------------------------ |
| `critical` | Token leakage; customer data export without approval; eval gate bypass.   |
| `high`     | Worker mass failure; suppression list missing; backup failure.            |
| `medium`   | Single agent persistent failure; DQ score in alert band; failed handoff.  |
| `low`      | Single transient failure; minor configuration drift.                      |

Only `medium` and above open formal incidents. `low` items are logged
as trust flags.

## The five phases

```
Detect → Triage → Contain → Recover → Learn
```

### 1. Detect

Detection sources:

| Source                              | Trigger                                                       |
| ----------------------------------- | ------------------------------------------------------------- |
| Application logs / metrics           | 5xx spike, alert rule, log pattern.                            |
| Eval gate                            | Sustained blocking failure.                                    |
| Worker orchestrator                   | Worker failure threshold.                                     |
| Trust flags                          | Severity high or critical.                                    |
| Customer report                      | Reported via support; the founder is the on-call ear.          |
| Verifier failure                     | A required check fails in CI on main.                          |

### 2. Triage

Within 15 minutes of detection (best effort):

- The Incident Response Agent writes a row in
  `trust/incidents.csv` with `status: open`, `severity`, `summary`,
  `owner`, `opened_at`.
- The founder is notified.
- An initial action plan is drafted (one sentence per planned step).

### 3. Contain

| Action type                          | Examples                                                              |
| ------------------------------------ | --------------------------------------------------------------------- |
| Pause an agent                       | Flip kill switch via Founder Console.                                 |
| Rotate a token                       | Per `INTERNAL_API_AUTH_GATE.md`.                                       |
| Roll back a deploy                   | Per `DEPLOYMENT_AND_ROLLBACK_SYSTEM.md`.                                |
| Block a worker write                 | Refuse via orchestrator's `allowed_write_targets`.                    |
| Suppress an outreach target          | Append to suppression list.                                            |

Containment is the immediate-stop phase. Speed matters more than
elegance.

### 4. Recover

| Action                                                           | Owner            |
| ---------------------------------------------------------------- | ---------------- |
| Restore service from a known-good state.                          | Engineering.     |
| Re-enable agents after fix.                                       | Founder.         |
| Reconcile any data drift (rare; audit and suppression never drift). | Engineering + Trust Guardian. |
| Customer communication (if affected).                              | Founder.        |
| Update the incident row with `status: recovering` then `closed`.   | Incident Response Agent. |

### 5. Learn

Within 48 hours of close, a one-page post-mortem:

| Section                          | Content                                                            |
| -------------------------------- | ------------------------------------------------------------------ |
| Summary                          | What happened.                                                     |
| Timeline                         | Key timestamps from logs and the audit ledger.                     |
| Root cause                       | What broke and why.                                                |
| Contributing factors             | Process or system factors.                                         |
| Impact                           | Customers affected, data impacted, hours of degradation.            |
| What worked                      | Containment that succeeded.                                        |
| What didn't                      | Containment that failed.                                            |
| Action items                     | Concrete changes, with owners and due dates.                       |

The post-mortem is reviewed in the next weekly engineering meeting.

## Audit events

| Action                       | Risk      | Notes                                              |
| ---------------------------- | --------- | -------------------------------------------------- |
| `incident_open`              | matches incident severity | Row written.                          |
| `incident_close`             | low       | Row closed.                                       |
| `incident_action`            | matches severity | A specific contain/recover step.            |
| `post_mortem_filed`          | low       | The doc is on file.                              |

## Roles

| Role                          | Responsibility                                                   |
| ----------------------------- | ---------------------------------------------------------------- |
| Incident Response Agent        | Opens and closes incidents; writes audit rows.                   |
| Founder                        | Approves containment actions; communicates with customers.       |
| Engineering                    | Executes technical containment and recovery.                     |
| Trust Guardian                  | Confirms trust-plane impact.                                     |
| Security Guardian               | Confirms security-plane impact.                                   |

## On-call

On-call rotation and paging are defined in `docs/ops/ON_CALL.md` and
`docs/ops/ON_CALL_ROTATION.md`. The founder is always the
last-resort escalation.

## Communication

| Audience            | When                                  | How                                                  |
| ------------------- | ------------------------------------- | ---------------------------------------------------- |
| Founder             | Always.                                | Founder brief; direct ping.                          |
| Engineering          | During the incident.                  | Internal channels; incident doc.                     |
| Customers           | If they are materially affected.       | Founder-approved message; per the SOP.               |
| Public               | Only in exceptional cases.              | Founder-approved statement; rare.                    |

## Post-mortem culture

Post-mortems are blameless and concrete. The format is consistent so
patterns surface across incidents. Action items must be specific and
have due dates; vague items are treated as not-yet-done.

## Anti-patterns

| Anti-pattern                                          | Why                                                                  |
| ----------------------------------------------------- | -------------------------------------------------------------------- |
| Closing without a post-mortem                          | Loses the learning compound.                                          |
| Vague action items                                    | "Improve monitoring" is not an action item.                          |
| Skipping the audit row                                 | The audit ledger is the spine.                                       |
| Quiet incident handling                                | The team loses context for future incidents.                          |
| Customer communication without founder approval        | Brand and trust risk.                                                |

## Cadence

| Activity                       | Cadence                              |
| ------------------------------ | ------------------------------------ |
| Active triage                  | Within 15 minutes of detection.       |
| Containment                    | As fast as safe.                      |
| Recovery                        | As soon as containment holds.          |
| Post-mortem                     | Within 48 hours of close.            |
| Action item review              | In the next weekly engineering meeting. |
| Incident metrics                 | Monthly in the founder brief.         |

## Verifier and metrics

- `trust/incidents.csv` is part of the DQ checks.
- Mean time to restore is a DORA metric (see
  `ULTIMATE_OBSERVABILITY_DORA.md`).
- Open incident count is in the four-pillar scorecard.

## Discipline

1. Detect, triage, contain, recover, learn.
2. Every incident has an audit row.
3. Every incident has a post-mortem within 48 hours.
4. Action items are specific and owned.
5. The founder is informed of every incident.

## Cross-references

- `ULTIMATE_SECURITY_GOVERNANCE.md` for the broader model.
- `BACKUP_AND_RESTORE_OS.md` for the recovery paths.
- `INTERNAL_API_AUTH_GATE.md` for token rotation.
- `DEPLOYMENT_AND_ROLLBACK_SYSTEM.md` for rollbacks.
