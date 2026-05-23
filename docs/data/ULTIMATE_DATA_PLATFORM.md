# Ultimate Data Platform

The Dealix Data Platform is the connected set of stores, pipelines, and policies that hold every record from signal capture to cash collection. It is governed by the same trust plane as the agents.

**Source of truth:** this doc + `docs/04_data_os/` + `docs/data/POSTGRES_PRIMARY_MODE.md`
**Owner:** Founder + Engineering Lead
**Trust gate:** A2 — schema changes, retention changes, export changes require founder approval.

## Stack

| Layer | Component |
|-------|----------|
| Transactional | Postgres (`docs/data/POSTGRES_PRIMARY_MODE.md`) |
| Operating CSVs | `$PRIVATE_OPS/*.csv` |
| Object store | Encrypted bucket for artifacts (proposals, deliverables) |
| Search index | Tenant-scoped index for client-facing search |
| Analytics | Read-replica + warehouse for sector reports and KPI computation |
| Backups | WAL archive + daily / weekly snapshots |

## Data classes

| Class | Examples | Storage |
|-------|----------|--------|
| Operational | Signals, opportunities, KPIs | Postgres |
| Financial | Invoices, payments, recognitions | Postgres + encrypted columns |
| PII | Names, emails, phone, role | Postgres + RLS + encryption |
| Sensitive PII | National ID, financial account | Restricted columns + extra audit |
| Artifacts | Proposals, deliverables, briefs | Object store |
| Logs | Audit, agent runs, tool calls | Append-only logs |

## Provenance

Every record has provenance fields: who created it, when, from what source, and through what process. Without provenance, a record cannot enter the Trust Plane. See `docs/04_data_os/DATA_PROVENANCE.md`.

## Retention

Retention is governed by `docs/04_data_os/DATA_RETENTION_POLICY.md`. The platform enforces retention by automatic archival and (where compliant) deletion.

## Access

| Role | Default access |
|------|---------------|
| Founder | All tenants, all classes |
| Engineering Lead | All tenants, all classes (audited) |
| Marketing Lead | Marketing CSVs + aggregated analytics |
| Customer Success Lead | Their assigned tenants |
| Revenue Lead | Pipeline + factory state |
| Delivery Lead | Delivery state + linked artifacts |
| Agent | Allowlisted reads + writes per registry |

Access changes are A2 decisions logged in the audit trail.

## Export

Data export — any export of customer data — is a protected decision. Founder approval (A2) required. Export events are logged with: who, what, to where, why, when. Exports of PII outside Saudi jurisdiction trigger an additional review (`docs/02_saudi_positioning/PDPL_AWARE_LANGUAGE.md`).

## Failure modes

- **Provenance gap:** a record lands without source. Detection: nightly job. Recovery: source the record or quarantine.
- **Access creep:** a role accumulates permissions. Detection: quarterly access review. Recovery: revoke excess; principle of least privilege.
- **Backup-restore failure:** restore drill fails. Detection: drill log. Recovery: investigate; backup strategy revised.

## Recovery path

If platform integrity is in doubt, the founder freezes writes and runs a full reconciliation across stores.

## Metrics

- Records with provenance (target: 100%).
- Restore-drill success rate.
- Access-review completion (quarterly).
- Export events per quarter.

## Disclaimer

The platform is engineered, not infallible. Dealix does not guarantee zero data loss. Estimated value is not Verified value.
