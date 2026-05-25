# Sales Cockpit System

## Doctrine Anchor
- Non-negotiables touched: #1 (approval before external action), #2 (no value claim without evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: approval-first for external action.

## Purpose

Give the founder one operating view for all commercial execution. The cockpit surfaces the decisions of the day — not raw data, not historical analytics — so the founder closes today's loops before opening new ones.

## Cockpit Panels

| Panel | What it shows | Source |
|-------|---------------|--------|
| Lead Intelligence | Newly discovered + enriched + scored accounts pending review | `LeadRecord`, `LeadScoreRecord` |
| Outreach Approval | Drafts pending founder approval | `OutreachQueueRecord` |
| Follow-Ups Due | Sequenced follow-ups due today | follow-up worker |
| Positive Replies | Replies routed to sample / proposal queue | reply router |
| Sample Queue | Positive replies awaiting a sample artifact | sample factory |
| Proposal Queue | Active proposals awaiting drafting or send | proposal worker |
| Payment Capture | Proposals awaiting payment / PO follow-up | revenue events |
| Delivery Trigger | Paid or PO'd work to start delivery | delivery worker |
| Retention Queue | Delivered clients due for feedback / retainer ask | retention worker |
| Trust Risks | Policy escalations, SLA breaches, opt-out spikes | approval center + suppression |

## Founder Actions on the Cockpit

- Approve a batch of outreach.
- Reject a lead that is misqualified.
- Approve a proposal for send.
- Request a sample.
- Push a payment follow-up.
- Start delivery on a paid record.
- Schedule a retainer ask.
- Escalate a trust risk.

Each action writes to `AuditLogRecord`.

## Core Rules

- The cockpit surfaces **decisions**, not dashboards. Each panel renders the next action a human can take.
- The founder should not be searching CSV files or jumping across modules to find the day's work.
- No panel renders a metric without a source-evidence link to the record(s) that produced it.
- SLA breaches in any panel are highlighted at the top of the daily digest.
- The cockpit never executes external actions on its own — it is a control surface, not an autopilot.

## Runtime Wiring

- Streamlit dashboard (current operational view): `dashboard/app.py` with pages in `dashboard/pages/` (Overview, Leads, Approvals, Evidence, Costs, Audit).
- Command Center HTTP surface: `api/routers/command_center.py`.
- Real-time business snapshot: `api/routers/business_now.py`.
- Founder command center docs (cross-link): `docs/company/FOUNDER_COMMAND_CENTER.md`, `docs/company/CEO_OPERATING_SYSTEM.md`.
- Daily digest: `.github/workflows/daily_digest.yml`, `make v5-digest`.
- Local snapshot: `make v5-status`, `make v5-snapshot`.
- Frontend (future Next.js consumer): `frontend/src/`.

## Metrics (what the cockpit itself is judged on)

| Metric | Target | Source |
|--------|--------|--------|
| Items closed per day from the cockpit | trending up | `AuditLogRecord` |
| Items aging past their SLA in any panel | < 5% | per-panel SLA timers |
| Time from positive reply to sample queue entry | < 1 business day | reply router → sample queue |
| Time from sample shown to proposal | < 5 business days | proposal worker timestamps |
| Time from proposal sent to payment captured or written PO | < 14 business days | revenue events |

## Cross-Links

- `docs/control_plane/APPROVAL_CENTER_V2.md`
- `docs/runtime/REVENUE_FACTORY_RUNTIME.md`
- `docs/founder/REVENUE_WAR_ROOM_OS.md`
- `docs/founder/BOARD_LEVEL_KPI_STACK.md`
- `docs/company/FOUNDER_COMMAND_CENTER.md`
- `docs/product/COMMAND_CENTER_PRODUCT_SPEC.md`

## Open Items

- The Streamlit dashboard pages cover Overview / Leads / Approvals / Evidence / Costs / Audit but do not yet cover Sample Queue, Proposal Queue, Payment Capture, Retention Queue as first-class panels.
- A unified frontend cockpit in `frontend/src/` is stub-only today.
- Cross-panel SLA timers are conceptual; per-panel age computation needs a small library.
- The "Trust Risks" panel needs the policy engine to emit a structured event stream the cockpit can subscribe to.
