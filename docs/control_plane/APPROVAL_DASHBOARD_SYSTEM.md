# Approval Dashboard System

## Purpose

Let Sami approve or reject batches quickly instead of reviewing raw CSV
files.

## Dashboard Panels

1. Leads pending approval.
2. Outreach messages pending approval.
3. Follow-ups pending approval.
4. Proposals pending approval.
5. Trust risks.
6. Today's top action.

## Actions

- Approve lead.
- Reject lead.
- Request edit.
- Approve message.
- Send to draft queue.
- Block risky action.

## Rule

Dashboard can approve internal status only.
External sending still requires explicit confirmed action.

## Phasing

- Phase A: Markdown queue files in private ops.
- Phase B: Local SQLite-backed dashboard.
- Phase C: Web dashboard (founder-only auth).
- Phase D: Multi-user hosted product (only after delivered proof).
