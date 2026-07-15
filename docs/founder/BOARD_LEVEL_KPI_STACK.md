# Board-Level KPI Stack

## Doctrine Anchor
- Non-negotiables touched: #2 (no measured value claim without source evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: control-plane verification scripts as release blockers.

## Purpose

Define the KPI hierarchy that Dealix reports against — from a single north star down through input, conversion, delivery, financial, trust, and product metrics. Every KPI has a source, an owner, and a review cadence.

## North Star

**Cash collected from qualified Saudi B2B revenue operations.**

Cash, not pipeline. Collected, not invoiced. Qualified, not anyone. Saudi B2B, not generic. Operations, not promises.

## KPI Layers

### Input KPIs (what we control)

- Leads discovered
- Leads enriched
- A-tier leads identified
- Approved outreach batches
- Content published
- Referrals requested

### Conversion KPIs (what the market responds to)

- Reply rate
- Positive reply rate
- Sample-request rate
- Proposal rate
- Payment / PO conversion rate

### Delivery KPIs (whether we keep what we win)

- Delivery cycle time
- QA pass rate
- Feedback received
- Retainer asks made
- Retainer conversions

### Financial KPIs

- Cash collected (north star)
- Monthly recurring revenue (where applicable)
- Pipeline value (with confidence band — never a guaranteed number)
- Gross margin
- AI / tool cost per outcome
- Runway

### Trust KPIs

- Approval SLA breach rate
- Trust incidents (any unapproved external action attempt)
- Overclaim violations caught by evals
- Suppression compliance (drafts attempted against suppressed records — target 0)

### Product KPIs

- Repeated workflows used by clients
- Automation hours saved (measured, not estimated)
- Feature usage
- Active clients

## Cadence

| Layer | Review cadence | Owner |
|-------|---------------|-------|
| Input | Daily | Founder |
| Conversion | Weekly | Founder + commercial |
| Delivery | Weekly | Delivery lead |
| Financial | Weekly + monthly | Founder |
| Trust | Daily review of breaches; weekly aggregate | Trust owner |
| Product | Monthly | Product lead |

## Core Rules

- Every KPI has one source. If two sources disagree, the source-of-record wins and the discrepancy becomes a ticket.
- No KPI is reported without a link to the underlying records.
- No KPI is reported as a forward commitment (e.g. "we will hit X next month") without a confidence band and the assumptions that produce it.
- Trust KPIs have hard thresholds (e.g. suppression breaches must be 0); a breach is escalated, not averaged away.
- Pipeline value is always reported with the confidence band; a single number with no band is not allowed in board reporting.

## Runtime Wiring

- Daily digest: `.github/workflows/daily_digest.yml`, `make v5-digest`.
- Daily JSON snapshot: `.github/workflows/daily_snapshot.yml`, `make v5-snapshot`.
- 22-point production verifier: `make v5-verify`.
- KPI registry (mentioned in doctrine): `kpi_registry.yaml` (location maintained per repo conventions).
- Revenue event store (source of cash and conversion data): `auto_client_acquisition/revenue_memory/event_store.py`.
- Audit log (source of trust data): `db/models.py::AuditLogRecord`.

## Cross-Links

- `docs/founder/REVENUE_WAR_ROOM_OS.md`
- `docs/control_plane/SALES_COCKPIT_SYSTEM.md`
- `docs/finance/AI_UNIT_ECONOMICS.md`
- `docs/finance/PRICING_YIELD_MANAGEMENT.md`
- `docs/UNIT_ECONOMICS_AND_MARGIN.md`
- `docs/company/UNIT_ECONOMICS.md`
- `docs/SLO.md`
- `docs/transformation/01_doctrine_lock.md`

## Open Items

- The KPI registry referenced by the doctrine lock does not yet have a one-file source-of-truth; metrics live across `make v5-status`, dashboard pages, and several markdown files.
- Confidence bands on pipeline value are not yet calculated by a documented method; they are stated qualitatively.
- Some trust KPIs (overclaim violations) depend on evals that are not yet running on every PR; see `docs/evals/AI_EVAL_RED_TEAM_SYSTEM.md`.
