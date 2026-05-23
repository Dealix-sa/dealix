# Ultimate Data Platform

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

The Dealix data platform is intentionally lean. We deliberately do
not run a generic data warehouse, a data lake, or a wide event bus.
We have a primary OLTP store (Postgres), an operational CSV tier
(private ops runtime), a small set of derived snapshots, and a clear
set of rules for what may live where. The point is to keep the data
surface small enough to govern and large enough to operate.

## Layers

```
┌────────────────────────────────────────────────────────────────┐
│ Layer 1 · Sources                                              │
│   - Application (user actions, deals, invoices)                │
│   - Worker outputs (scorecards, queues, snapshots)             │
│   - External APIs (when invoked manually)                      │
└──────────────────┬─────────────────────────────────────────────┘
                   │
┌──────────────────▼─────────────────────────────────────────────┐
│ Layer 2 · Stores                                               │
│   - Postgres (system of record for business data)              │
│   - Private ops CSVs (operating tier, outside repo)            │
│   - Object storage (large blobs)                               │
└──────────────────┬─────────────────────────────────────────────┘
                   │
┌──────────────────▼─────────────────────────────────────────────┐
│ Layer 3 · Derived snapshots                                    │
│   - Channel scorecard, sector scorecard, KPI tree snapshots    │
│   - AI unit economics                                          │
│   - Win/loss + objection tables                                │
└──────────────────┬─────────────────────────────────────────────┘
                   │
┌──────────────────▼─────────────────────────────────────────────┐
│ Layer 4 · Surfaces                                             │
│   - Founder Console internal API                               │
│   - Verifier scripts                                           │
│   - Founder brief                                              │
└────────────────────────────────────────────────────────────────┘
```

## Layer 1: Sources

| Source                | Notes                                                                  |
| --------------------- | ---------------------------------------------------------------------- |
| Application           | User actions, deals, invoices, payments. Goes to Postgres.             |
| Worker outputs        | Queues, scorecards, snapshots, AI unit economics. Goes to CSV tier.   |
| External APIs         | Used through the application only. Never auto-invoked.                |

External data ingestion is policy-gated. Bulk imports are
`data_export_safety`-class actions and require escalation.

## Layer 2: Stores

| Store              | Primary use                                                              | Trust boundary             |
| ------------------ | ------------------------------------------------------------------------ | -------------------------- |
| Postgres           | Business-critical state, transactions, identity.                         | Application boundary.       |
| Private ops CSVs   | Audit, suppression, approvals, queues, scorecards, worker state.         | Outside the repo and app.   |
| Object storage     | Large blobs (proof assets, exports).                                     | Encrypted at rest, access-controlled. |

The Postgres-primary model is detailed in `POSTGRES_PRIMARY_MODE.md`.
The CSV tier contract is detailed in
`docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md`.

## Layer 3: Derived snapshots

Derived snapshots are read-only outputs of analytical workers.

| Snapshot                              | File                                              | Reader                                          |
| ------------------------------------- | ------------------------------------------------- | ----------------------------------------------- |
| Four-pillar scorecard                  | `founder/operating_scorecard.md`                  | Founder Console `/control/scorecard`.            |
| Channel scorecard                      | `distribution/channel_scorecard.csv`              | `/distribution/summary`.                         |
| Sector scorecard                       | `distribution/sector_scorecard.csv`               | `/distribution/summary`.                         |
| AI unit economics                       | `finance/ai_unit_economics.csv`                   | `/finance/summary`, `/finance-ops/summary`.      |
| Eval status                            | `evals/eval_status.csv`                           | `/evals/status`.                                 |
| Sovereign readiness                    | `founder/sovereign_readiness.md`                  | `/sovereign/readiness`.                          |

Each snapshot is produced by a single worker. The worker is named in
`registries/agent_registry.yaml` and writes only to its
`allowed_write_targets`.

## Layer 4: Surfaces

The only sanctioned surfaces are:

| Surface                            | Audience                                                   |
| ---------------------------------- | ---------------------------------------------------------- |
| Founder Console internal API       | The founder (and the console UI).                          |
| Founder brief                      | The founder.                                               |
| Verifier scripts                   | CI and engineering.                                        |
| Customer-facing application API    | Customers (Postgres-backed, not CSV-backed).                |

No public dashboard, no public BI surface. The trust plane is the
only consumer of operating data.

## Identifier discipline

| Object             | Identifier shape          | Notes                                                  |
| ------------------ | ------------------------- | ------------------------------------------------------ |
| Deal               | `deal_xxxx`               | Postgres-issued.                                       |
| Invoice            | `inv_xxxx`                | Postgres-issued.                                       |
| Approval           | `apr_xxxx`                | CSV-issued, monotonic.                                 |
| Audit event        | UUID v4                   | CSV-issued.                                            |
| Lead               | `lead_xxxx`               | CSV-issued.                                            |
| Worker             | `worker_xxxx`             | CSV-issued.                                            |
| Sector             | Short code (e.g., `gov`)  | Registered in `growth/sector_targets.csv`.             |

Identifiers are stable across joins. The Founder Console responses
always carry the id type prefix so downstream consumers can route.

## Data quality

DQ is owned by the Data Quality System (see
`DATA_QUALITY_SYSTEM.md`). DQ is a property of the snapshot layer:
we check that scorecards refresh, that distinct ids are unique, that
CSV schemas match the bootstrap declaration, and that the audit
ledger is monotonic.

## Retention

| Tier               | Retention                                              | Mechanism                  |
| ------------------ | ------------------------------------------------------ | -------------------------- |
| Postgres business  | Per the PDPL data retention policy (`docs/DATA_RETENTION_POLICY.md`). | Application-level deletes. |
| Private ops CSVs   | Indefinite. Audit and suppression must not be pruned.   | File-level.                |
| Object storage     | Per asset class (proof, exports).                       | Lifecycle rules.           |

Pruning the audit ledger or the suppression list is a destructive
operation and requires the policy rule
`destructive_operation_requires_escalation`.

## Privacy and residency

- Data residency posture is Saudi-aligned. See
  `docs/DPA_DEALIX_FULL.md` and the sovereign readiness doc.
- The PDPL alignment is documented in
  `docs/PRIVACY_PDPL_READINESS.md`.
- The cross-border transfer addendum lives at
  `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.

## Failure isolation

The data platform is designed so that a failure in any one layer
does not cascade:

- Postgres outage: the Founder Console business endpoints return
  errors; the operating endpoints (CSV-backed) continue to function.
- Private ops runtime outage: the operating endpoints return
  `data_source: "no-runtime"`; business endpoints continue.
- Worker outage: the snapshots become stale; the founder sees the
  `last_run` field go stale and can take action.

## Discipline

1. The data surface is intentionally small.
2. Postgres is the business store; CSVs are the operating store.
3. Derived snapshots are read-only outputs of named workers.
4. Surfaces are the Founder Console, the founder brief, and the
   verifiers.
5. Retention follows the PDPL policy; audit and suppression never
   prune.
6. Every write path traces to an `allowed_write_targets` declaration.
