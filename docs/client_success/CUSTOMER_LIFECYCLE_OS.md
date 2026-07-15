# Customer Lifecycle OS

## Doctrine Anchor
- Non-negotiables touched: #1 (approval before external action), #2 (no value claim without evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: approval-first for external action.

## Purpose

Manage every customer from first contact through retention, proof, referral, and expansion as a single lifecycle. No stage exists without a defined next action; no stage closes without a recorded outcome.

## Lifecycle Stages

| # | Stage | Definition | Exit criterion |
|---|-------|------------|----------------|
| 1 | Discovered | Account found in market intelligence | Enriched record exists |
| 2 | Qualified | Account passes ICP and scoring threshold | Scoring record present |
| 3 | Contacted | Approved outreach sent | Send logged |
| 4 | Replied | Any reply received | Reply classified |
| 5 | Sample | Sample artifact prepared and sent | Sample acknowledged |
| 6 | Proposal | Proposal drafted, approved, sent | Proposal received by buyer |
| 7 | Payment / PO | Payment captured or written PO received | Revenue event recorded |
| 8 | Delivery | Work in progress against delivery lifecycle | Delivery milestones logged |
| 9 | Feedback | Client feedback collected post-delivery | Feedback recorded |
| 10 | Retainer | Ongoing scope agreed | Retainer terms signed |
| 11 | Proof | Public or private proof asset prepared | Client approval recorded |
| 12 | Referral | Referral asked and received | Referral logged |
| 13 | Expansion | Additional scope sold | Expansion revenue event |

## Core Rules

- No customer stage exists without `next_action`, `owner`, and `due_date`.
- A stage transition writes to the revenue event store with a `causation_id`.
- A regression (e.g. stage 6 → stage 5) is allowed and recorded; we do not hide regressions.
- "Proof" never publishes without client written approval recorded as a source-evidence link.
- "Referral" never names a client publicly without the same.
- A delivery milestone missed by SLA appears in the war room.

## Per-Stage Hand-offs

| From → To | Trigger | Approval needed |
|-----------|---------|-----------------|
| 1 → 2 | Scoring pass | None |
| 2 → 3 | Approved outreach batch | Approval Center |
| 3 → 4 | Reply received | None (router classifies) |
| 4 → 5 | Positive reply classification | Founder approves sample |
| 5 → 6 | Sample acknowledged + interest signal | Founder approves proposal |
| 6 → 7 | Proposal accepted | Payment / PO is external event |
| 7 → 8 | Payment or PO recorded | Delivery start condition met |
| 8 → 9 | Delivery completed | Feedback request approved |
| 9 → 10 | Strong feedback + scope clarity | Founder approves retainer ask |
| 10 → 11 | Retainer signed | Client approves proof |
| 11 → 12 | Proof public + relationship intact | None for ask; founder asks |
| 12 → 13 | Referral or expansion signal | Founder approves new scope |

## Runtime Wiring

- Delivery lifecycle (existing cross-link): `docs/delivery/DELIVERY_LIFECYCLE.md`.
- Agent lifecycle (existing cross-link): `docs/agentic_operations/AGENT_LIFECYCLE.md`.
- Lead inbox (stage 1 source): `auto_client_acquisition/lead_inbox.py`.
- Scoring (stage 2): `auto_client_acquisition/crm_v10/lead_scoring.py`.
- Outreach queue (stage 3): `db/models.py::OutreachQueueRecord`.
- Reply router (stage 4): currently partial (`docs/runtime/REVENUE_FACTORY_RUNTIME.md` worker #10).
- Revenue event store (stage transitions and 7+): `auto_client_acquisition/revenue_memory/event_store.py`.
- Payments (stage 7): `db/migrations/versions/20260512_005_payments_table.py`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Records with missing `next_action` | 0 in any active stage | derived |
| Median time in each stage | tracked, optimized | event store |
| Stage 4 → 5 conversion (positive reply → sample) | tracked, experimented against | event store |
| Stage 6 → 7 conversion (proposal → payment / PO) | tracked, experimented against | event store |
| Retainer conversion (stage 9 → 10) | tracked | event store |
| Referrals received per active client | tracked | event store |

## Cross-Links

- `docs/runtime/REVENUE_FACTORY_RUNTIME.md`
- `docs/delivery/DELIVERY_LIFECYCLE.md`
- `docs/agentic_operations/AGENT_LIFECYCLE.md`
- `docs/client_success/SUPPORT_SUCCESS_OS.md`
- `docs/finance/BILLING_RECEIVABLES_OS.md`
- `docs/control_plane/APPROVAL_CENTER_V2.md`

## Open Items

- Stages 9–13 (Feedback through Expansion) are spec'd here but lack first-class tables in the database; today they live across notes and Streamlit pages.
- Reply router (stage 4) is partial; positive-reply classification is a stub the lifecycle depends on.
- Proof workflow (stage 11) lacks a dedicated approval queue type in the Approval Center.
- Referral tracking (stage 12) is informal; partners doc carries a partial referral ledger.
