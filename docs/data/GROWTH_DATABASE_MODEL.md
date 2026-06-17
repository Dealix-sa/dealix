# Growth Database Model

## Doctrine Anchor
- Non-negotiables touched: #2 (no measured value claim without source evidence), #3 (no cross-tenant operational access), #5 (no proof-level overclaiming).
- Frozen decisions touched: approval-first for external action, control-plane verification scripts as release blockers.

## Purpose

Define the canonical data layout that powers the Revenue Factory. The "pipeline" is **not** the database. The pipeline is only the active commercial subset of a larger market universe that Dealix continuously discovers, enriches, suppresses, routes, and retains.

## Conceptual Layers

1. **Market Universe** — every discoverable Saudi B2B account, even if unqualified.
2. **Lead Intelligence Base** — researched and scored accounts.
3. **Pipeline** — active commercial engagement (contacted → replied → sample → proposal).
4. **Outreach Queue** — drafts approved or pending approval.
5. **Conversation Log** — every reply and the routing decision it triggered.
6. **Opportunity Queue** — samples, proposals, payment capture in motion.
7. **Client Queue** — delivery, retention, proof, referral, expansion.

A record can occupy multiple layers over its lifetime, but every layer transition is logged.

## Tables and Files (existing today)

| Layer | Storage | Path |
|-------|---------|------|
| Lead Intelligence Base | `LeadRecord` | `db/models.py` |
| Scoring | `LeadScoreRecord` | `db/models.py` |
| Outreach Queue | `OutreachQueueRecord`, `GmailDraftRecord`, `LinkedInDraftRecord` | `db/models.py` |
| Suppression | `SuppressionRecord` | `db/models.py` |
| Approval audit | `AuditLogRecord` | `db/models.py` |
| Revenue events (append-only) | `RevenueEventRecord` | `db/models_revenue_events.py` |
| Background jobs | `BackgroundJobRecord` | `db/models.py` |
| Tenancy + RBAC | `TenantRecord`, `UserRecord`, `RoleRecord` | `db/models.py` |
| Payments | payments table | `db/migrations/versions/20260512_005_payments_table.py` |
| Sector reports | sector reports tables | `db/migrations/versions/20260513_008_sector_reports.py` |
| Operational streams | value ledger + operational streams | `db/migrations/versions/20260515_012_value_ledger_and_operational_streams.py` |
| Enterprise control plane | governance tables | `db/migrations/versions/20260515_011_enterprise_control_plane.py` |
| Landing-form leads | JSONL | `auto_client_acquisition/lead_inbox.py` |
| Revenue memory | event store + projections | `auto_client_acquisition/revenue_memory/` |

## Conceptual Tables (to be wired or formalized)

| Conceptual Table | Status | Notes |
|-----------------|--------|-------|
| `market_accounts` | Partial — discovered accounts live across enrichment outputs | Should consolidate into a discovered-accounts view |
| `conversation_log` | Partial — replies not yet centrally stored | Reply router writes here once wired |
| `sample_queue` | Not yet a table | Founder approval surface required first |
| `proposal_queue` | Partial — proposal generation not yet end-to-end | Backs the proposal worker |
| `payment_capture_queue` | Not yet a queue — payments table tracks final state, not capture motion | Daily founder follow-up surface |
| `client_delivery_queue` | Tracked across delivery docs; not a single table | Backs delivery trigger worker |
| `retention_queue` | Not yet a table | Backs retention worker |

## Core Rules

- The pipeline view is a **derived** view over the intelligence base, not its own source of truth.
- No outreach record may be created for a record present in `SuppressionRecord`.
- Every external-action record (drafts that became sends, payments, public proof) carries an `AuditLogRecord` reference.
- Cross-tenant joins are forbidden at the ORM and policy layer; tenant scope is enforced in every router.
- Append-only event streams (`RevenueEventRecord`) are the system of record for everything that already happened externally; mutable tables are only for current state.

## Runtime Wiring

- ORM and async session: `db/models.py`, `db/session.py`.
- Migrations: `db/migrations/versions/`.
- Revenue event store: `auto_client_acquisition/revenue_memory/event_store.py`.
- Projections: `auto_client_acquisition/revenue_memory/projections.py`.
- Agent-facing semantic memory: `core/memory/revenue_memory.py`.
- Lead inbox (file-backed staging): `auto_client_acquisition/lead_inbox.py`.

## Metrics

- Records in `LeadRecord` over time (intelligence base growth).
- Records in `SuppressionRecord` by reason (compliance signal).
- Active vs total `OutreachQueueRecord` per day (approval backlog).
- `RevenueEventRecord` cardinality per event type per week (factory throughput).
- Cross-tenant access denials in `AuditLogRecord` (must remain zero).

## Cross-Links

- `docs/runtime/REVENUE_FACTORY_RUNTIME.md`
- `docs/trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md`
- `docs/control_plane/APPROVAL_CENTER_V2.md`
- `docs/engineering/OBSERVABILITY_SLO_SYSTEM.md`
- `docs/transformation/01_doctrine_lock.md`

## Open Items

- Several conceptual tables (`market_accounts`, `conversation_log`, `sample_queue`, `retention_queue`) are not yet first-class tables; data is scattered across files and modules. Consolidating them is a follow-up RFC.
- A formal data dictionary mapping every column in `db/models.py` to its conceptual layer does not yet exist.
- The relationship between `auto_client_acquisition/lead_inbox.py` (JSONL) and `LeadRecord` (database) should be unified.
