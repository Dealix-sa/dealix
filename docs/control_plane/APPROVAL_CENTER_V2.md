# Approval Center v2

## Doctrine Anchor
- Non-negotiables touched: #1 (no external high-risk action without approval), #2 (no measured value claim without source evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: approval-first is mandatory for external and irreversible actions.

## Purpose

Give the founder a single place to approve, reject, edit, or escalate every high-leverage Dealix decision. The Approval Center is the gate between automation and the outside world.

## Status

The Approval Center exists as a working module (`auto_client_acquisition/approval_center/`) with a policy engine, founder rules, and REST endpoints (`api/routers/approval_center.py`). Today it is in-memory (Redis-swappable). v2 is the **operating specification** for how the founder uses it daily and weekly, and the rules the policy engine must enforce.

## Queues

| Queue | Source | Approval cadence |
|-------|--------|------------------|
| Outreach Queue | Outreach draft worker | Daily batch |
| Follow-Up Queue | Follow-up worker | Daily batch |
| Proposal Queue | Proposal worker | Same-day |
| Pricing Exception Queue | Sales motion | Same-day |
| Delivery Report Queue | Delivery worker | Per artifact |
| Proof / Case Study Queue | Proof worker | Per artifact |
| Trust Escalation Queue | Policy engine when a rule is uncertain | Before external action |
| Agent Action Queue | Any agent attempting an external side effect | Before external action |
| Refund / Contract Queue | Finance / Legal | Per request |

## Actions on a Queue Item

- **Approve** — pass through to executor.
- **Reject** — drop with reason recorded.
- **Needs Edit** — return with notes; worker re-drafts.
- **Escalate** — route to trust review or co-founder review.
- **Defer** — snooze with a follow-up date.

Every action writes to `AuditLogRecord`.

## SLA (operating targets)

- Outreach approvals: daily review window.
- Follow-up approvals: daily review window.
- Proposal approvals: same business day.
- Payment / PO follow-ups: same business day.
- Trust escalations: before any external action executes.
- Refund / contract / legal: 48-hour review window.

A queue item that exceeds its SLA appears in the daily founder digest with a red flag.

## Policy Engine Rules (anchored to existing code)

The policy engine in `auto_client_acquisition/approval_center/approval_policy.py` enforces:

- **WhatsApp** outreach requires founder approval.
- **LinkedIn** outreach requires founder approval.
- **Email** outreach may be auto-approvable only when **all** of these hold: lead is not in `SuppressionRecord`, deliverability checks pass, the draft is in the warmup volume budget, and the draft contains no overclaim language.
- Any action with payment, refund, or contract impact requires founder approval and a second signal (written PO, signed agreement, or recorded conversation).
- Any action that publishes a public claim requires founder approval and a source-evidence link.

Founder-defined rules live in `auto_client_acquisition/approval_center/founder_rules.py` and can tighten the defaults but never loosen them below the doctrine line.

## Core Rules

- No external A2 (committed) or A3 (irreversible) action leaves Dealix without an approval record.
- "Auto-approved" is not "approved without record"; it is "approved by a rule, with the rule version logged."
- A reject reason is mandatory.
- An approval that touches money, contracts, or public claims requires the founder; it cannot be delegated to a rule alone.
- Every approval references the source evidence used to make the decision.

## Runtime Wiring

- Policy engine: `auto_client_acquisition/approval_center/approval_policy.py`.
- Founder rules: `auto_client_acquisition/approval_center/founder_rules.py`.
- Approval REST endpoints: `api/routers/approval_center.py` (`pending`, `create`, `approve`, `reject`, `edit`, `history`).
- Audit log: `db/models.py::AuditLogRecord`.
- Outreach queue surface: `db/models.py::OutreachQueueRecord`.
- Daily founder digest surface: `.github/workflows/daily_digest.yml` and `make v5-digest`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| SLA breach rate per queue | < 5% | `AuditLogRecord` |
| Reject rate by queue | tracked weekly, drives draft quality fixes | `AuditLogRecord` |
| Items approved without source evidence | 0 | policy engine |
| Items approved that should have escalated | 0 | weekly review |

## Cross-Links

- `docs/runtime/REVENUE_FACTORY_RUNTIME.md`
- `docs/control_plane/SALES_COCKPIT_SYSTEM.md`
- `docs/trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md`
- `docs/evals/AI_EVAL_RED_TEAM_SYSTEM.md`
- `docs/transformation/01_doctrine_lock.md`

## Open Items

- The Approval Center is in-memory today; persistence is on the roadmap (Redis or Postgres-backed queue).
- A single unified "Approval Inbox" UI page across all queues is not yet built in `apps/web/` or in the Streamlit dashboard.
- Proof / case study queue logic is partially specified; the proof worker is not end-to-end.
- Pricing exception queue is conceptual; the pricing yield system needs to write into it (see `docs/finance/PRICING_YIELD_MANAGEMENT.md`).
