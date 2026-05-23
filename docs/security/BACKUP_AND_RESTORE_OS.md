# Backup and Restore OS

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

The Backup and Restore OS is the discipline that makes Dealix
recoverable. Daily backups, quarterly restore drills, and explicit
recovery procedures keep data and operating state safe from
hardware, software, and human failure.

## Scope

| Asset                                | Backup target                                                        |
| ------------------------------------ | -------------------------------------------------------------------- |
| Postgres business database            | Off-host encrypted snapshot.                                          |
| Private ops runtime (CSVs)            | Off-host encrypted snapshot.                                          |
| Customer-supplied artifacts (objects) | Object storage versioning + lifecycle.                                |
| Configuration and secrets             | Secrets store (separate from backups).                               |
| Application code                      | Git repository (no backup; reproducible from main).                   |

The repo itself is not backed up here; it is in source control. The
config and secrets are not in this backup system; they are in the
secrets store with its own backup and recovery.

## Backup policy

| Asset                           | Cadence       | Retention                                                  |
| ------------------------------- | ------------- | ---------------------------------------------------------- |
| Postgres                         | Daily         | 30 days of daily; 12 months of monthly; 7 years of yearly.  |
| Private ops runtime              | Daily         | 30 days of daily; 12 months of monthly.                    |
| Customer artifacts (objects)      | Continuous (versioning) | Per asset class; minimum 90 days for recent versions. |
| Audit ledger                     | Daily (with runtime) | 12 months minimum; legal hold may extend.              |
| Suppression list                  | Daily (with runtime) | Indefinite.                                            |

Daily backups run during a low-traffic window (UTC overnight Saudi
local). Backup completion is recorded in
`security/security_status.csv` for the day.

## Backup integrity

| Check                              | Cadence       |
| ---------------------------------- | ------------- |
| Backup completion notification     | Daily         |
| Backup size sanity check           | Daily         |
| Random-row sample restore           | Weekly        |
| Full restore drill                  | Quarterly     |

A missing or undersized backup is a `severity: high` trust flag.
Three consecutive failures escalate to `severity: critical` and open
an incident.

## Recovery time objectives

| Scenario                            | RTO target           | RPO target          |
| ----------------------------------- | -------------------- | ------------------- |
| Postgres point-in-time recovery      | 4 hours               | 5 minutes            |
| Postgres full restore                 | 8 hours               | 24 hours             |
| Private ops runtime restore           | 1 hour                | 24 hours             |
| Object storage restore (version)       | 30 minutes (per object) | 0 (versioning)     |

The RTOs reflect a small-team operating posture, not an "elite" SaaS
posture. The RPOs reflect the criticality of each asset.

## Restore procedures

### Postgres point-in-time recovery

1. Identify the desired recovery target time.
2. Provision a new Postgres instance from the latest base backup.
3. Apply WAL up to the target time.
4. Run schema and application smoke tests.
5. Switch the application connection string.
6. Record the recovery in the audit ledger
   (`action: restore_executed`, `risk: high`).
7. Open an incident if customer data was affected.

### Postgres full restore

1. Choose the most recent valid daily backup.
2. Provision a new Postgres instance.
3. Restore the dump.
4. Apply Alembic migrations as needed to match the application code.
5. Run smoke tests.
6. Switch the application connection string.
7. Record the restore in the audit ledger.

### Private ops runtime restore

1. Choose the most recent valid daily snapshot.
2. Mount the runtime path or restore to `/opt/dealix-ops-private`.
3. Verify the file list against the bootstrap script.
4. Restart the worker orchestrator.
5. Run the eval gate to confirm.
6. Record the restore in the audit ledger.

### Object storage restore (single object)

1. Identify the object id and the desired version.
2. Use the object store's versioning to restore.
3. Notify the customer if the object is customer data.
4. Record the restore.

## Restore drills

Quarterly drills exercise the full procedure end-to-end:

| Drill type                              | Quarter       |
| --------------------------------------- | ------------- |
| Postgres point-in-time recovery          | Q1            |
| Private ops runtime restore               | Q2            |
| Postgres full restore                    | Q3            |
| Object storage restore                   | Q4            |

Each drill produces a one-page log in `docs/ops/RESTORE_DRILL_LOG.md`.
Drills that miss their RTO trigger an action item.

## Backup posture in the Founder Console

The latest backup status is read from `security/security_status.csv`
and surfaced in the security status endpoint
(`/api/v1/internal/security/status`):

```json
{
  "secrets_scan": "...",
  "dependency_scan": "...",
  "pdpl_review": "...",
  "incident_open": 0
}
```

Backup-specific surfacing is a planned addition.

## Encryption and access

| Aspect                            | Practice                                                       |
| --------------------------------- | -------------------------------------------------------------- |
| In transit                         | TLS to the backup target.                                      |
| At rest                            | AES-256 server-side encryption.                                |
| Key management                     | Managed by the cloud provider; rotated per provider policy.    |
| Access control                      | Least-privilege role for backup writes; separate role for restores. |
| Audit                              | Every restore audited.                                          |

## Cross-border and residency

- Backups are stored in Saudi-region storage by default.
- Cross-border replication is policy-gated (see
  `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`).
- Customer-requested deletions are honored at the backup layer per
  the data retention policy.

## Anti-patterns

| Anti-pattern                                          | Why                                                                  |
| ----------------------------------------------------- | -------------------------------------------------------------------- |
| Treating backup completion as success                  | Restore tested is success. Backup taken is hypothesis.               |
| Skipping the quarterly drill                            | Without drills, RTOs are aspirational.                                |
| Storing backups on the primary host                    | Hardware failure takes both.                                          |
| Storing the secrets in the backup                       | Conflates two control planes.                                         |
| Long retention windows without legal review             | Storage cost and privacy posture.                                     |

## Discipline

1. Daily backups. No exceptions.
2. Quarterly drills. No exceptions.
3. Restore is audited.
4. RTOs and RPOs are tracked.
5. The audit ledger and suppression list never lose history.

## Cross-references

- `ULTIMATE_SECURITY_GOVERNANCE.md` for the security model.
- `INCIDENT_RESPONSE_OS.md` for recovery playbooks.
- `docs/DATA_RETENTION_POLICY.md` for the retention frame.
- `POSTGRES_PRIMARY_MODE.md` for the data model.
