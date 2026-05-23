# War Room — Postgres migration design (post-JSON stabilization)

**Status:** design only — implement after War Room JSON MVP is stable for 2+ weeks.

## Target tables

| Table | Purpose |
|-------|---------|
| `war_room_targets` | One row per funnel lead / target; mirrors `FunnelLeadRecord` war-room columns |
| `war_room_status_history` | Optional audit of `war_room_status` transitions |

## Event bridge

Append `EvidenceEvent` payloads to `revenue_events` via existing [isolated_pg_event_store.py](../../auto_client_acquisition/revenue_memory/isolated_pg_event_store.py):

- `event_type` = `war_room_*` from [war_room.py](../../dealix/revenue_ops_autopilot/war_room.py) `CRITICAL_OUTREACH_EVENTS`
- `entity_id` = `lead_id`

## Migration steps

1. Alembic revision: `war_room_targets` with FK optional to `commercial_engagements` when wired.
2. Backfill script: read `var/revenue_ops_autopilot.json` → upsert rows.
3. Feature flag `DEALIX_WAR_ROOM_STORE=postgres|json` in [store.py](../../dealix/revenue_ops_autopilot/store.py).
4. Dual-write period; compare counts weekly; cut over when diff = 0.

## Non-goals (v1 DB)

- No automated external send columns.
- No invented CRM revenue fields — KPI still from `kpi_founder_commercial_import.yaml`.

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
