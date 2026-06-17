# Billing & Receivables OS

## Doctrine Anchor
- Non-negotiables touched: #1 (approval before external action — payments and refunds), #2 (no value claim without evidence — every revenue number tied to an event), #5 (no proof-level overclaiming).
- Frozen decisions touched: approval-first for external and irreversible actions.

## Purpose

Make sure every proposal converts to paid work or a clear written PO, and every paid record produces a recoverable, auditable trail from quote → invoice → payment link → receipt → revenue recognition.

## Objects (today)

| Object | Storage | Source |
|--------|---------|--------|
| Quote / proposal | proposal worker outputs | partial today |
| Invoice | payments table | `db/migrations/versions/20260512_005_payments_table.py` |
| Payment link | Moyasar payment URL | `docs/BILLING_MOYASAR_RUNBOOK.md` |
| Receipt | webhook event + database row | Moyasar webhook handler |
| Webhook event | append-only event log | `auto_client_acquisition/revenue_memory/event_store.py` |
| Payment status | derived from event log | revenue projections |
| Refund request | approval queue item | Approval Center |
| Revenue recognition note | revenue event | event store |

## Core Rules

- Every proposal has a payment path (Moyasar link, written PO, or signed agreement). A proposal with no payment path is a draft, not a proposal.
- Every payment has a status traceable to a webhook event or a manually recorded source-evidence link.
- Webhook failures alert; silent webhook failures are treated as incidents.
- A refund is A3 (irreversible) — founder approval is required and a written reason is recorded.
- Delivery does not start without a documented start condition (payment captured, PO received, or signed letter of intent with cash schedule).
- No revenue is recognized that does not have a corresponding cash or written commitment event.

## Operating Cadence

| Cadence | What happens |
|---------|--------------|
| Daily | Payment capture queue surfaces in the cockpit; founder follows up on overdue items |
| Weekly | Receivables review: aging, dunning, write-offs |
| Monthly | Revenue recognition close: cash collected, MRR, deferred revenue |

## Approval Gates

- **Payment link issuance**: per proposal, founder approves.
- **Refund**: per request, founder approves with written reason.
- **Write-off**: per case, founder approves; recorded in event store.
- **Pricing exception below floor**: per case, founder approves (see `docs/finance/PRICING_YIELD_MANAGEMENT.md`).
- **Custom payment terms**: per case, founder approves; legal review for >30 days.

## Runtime Wiring

- Payments table: `db/migrations/versions/20260512_005_payments_table.py`.
- Moyasar integration runbook: `docs/BILLING_MOYASAR_RUNBOOK.md`.
- General billing runbook: `docs/BILLING_RUNBOOK.md`.
- Checkout endpoint: `/api/v1/checkout` (see `api/routers/`).
- Moyasar webhook (HMAC-verified): see security setup in repo root and `docs/security/`.
- Revenue event store: `auto_client_acquisition/revenue_memory/event_store.py`.
- Audit log: `db/models.py::AuditLogRecord`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Proposals with a payment path attached | 100% | proposal worker + payments |
| Average days from proposal sent to payment captured | tracked, < 14 target | revenue events |
| Webhook failure rate | < 0.5% | webhook handler logs |
| Refund rate | tracked, investigated if rising | refund event |
| Receivables aging > 30 days | minimized; weekly review | derived |
| Revenue recognized without source event | 0 | reconciliation |

## Cross-Links

- `docs/BILLING_MOYASAR_RUNBOOK.md`
- `docs/BILLING_RUNBOOK.md`
- `docs/finance/PRICING_YIELD_MANAGEMENT.md`
- `docs/finance/AI_UNIT_ECONOMICS.md`
- `docs/founder/BOARD_LEVEL_KPI_STACK.md`
- `docs/control_plane/APPROVAL_CENTER_V2.md`
- `docs/transformation/01_doctrine_lock.md`

## Open Items

- A unified receivables aging view does not yet exist as a single cockpit panel.
- Dunning automation (gentle, approval-gated reminders for overdue payments) is not wired.
- The write-off workflow lacks a dedicated approval queue type.
- Revenue recognition is correct in principle (event-sourced) but lacks a monthly reconciliation script.
