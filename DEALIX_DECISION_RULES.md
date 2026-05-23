# Dealix Decision Rules

> Owner: Founder. Approval level: Founder. Verify: `scripts/verify_company_os.py`.
> Companion module: `dealix/trust/approval_matrix.py`.

This document encodes who decides what, on what timeline, with what
evidence. It is the single source of truth for the approval matrix.

---

## 1. Approval Classes

Each action carries an **approval class**. Classes are defined in
`dealix/registers/approval_classes.yaml` and consumed by
`dealix/trust/approval_matrix.py`.

| Class | Meaning | Default approver |
|-------|---------|------------------|
| `auto` | Agent may execute without human review (internal-only effects) | n/a |
| `founder` | Requires founder approval before effect | Founder |
| `founder_24h` | Founder approval required within 24h or action expires | Founder |
| `ops_manager` | Ops manager may approve; founder may override | Ops Manager |
| `founder_capital` | Founder approval + recorded in capital allocation review | Founder |
| `blocked` | Action is policy-prohibited until doctrine is amended | n/a |

---

## 2. Action -> Class Matrix

| Action | Class | Notes |
|--------|-------|-------|
| Outbound message to external party | `founder` | Always queued, never auto-sent |
| Pricing change | `founder` | Logged in `revenue/pricing_experiments.md` |
| New offer | `founder` | Requires offer ladder update |
| Public claim (case study, metric, logo) | `founder` | Must match `public_claims.yaml` |
| Refund or credit | `founder` | Logged in `trust/approval_log.csv` |
| Suppression-list addition | `auto` | Add-only is auto; removal is `founder` |
| Suppression-list removal | `founder` | Reversal requires reason |
| Data export with client identifiers | `founder` | Logged in `trust/export_log.csv` |
| Lead scoring threshold change | `ops_manager` | Founder veto window: 7 days |
| Internal SOP update | `ops_manager` | Founder may revert |
| Capital deployment > 5,000 SAR | `founder_capital` | Logged in `finance/capital_allocation_review.md` |
| Hiring offer | `founder` | Founder signs |
| Vendor / supplier addition | `founder` | Added to `docs/ai_management/AI_SUPPLIER_POLICY.md` |
| Policy override / risk exception | `founder` | Logged in `trust/risk_exceptions.md` |
| Auto-execute outbound | `blocked` | Permanently blocked by doctrine |

---

## 3. Approval Flow

1. Agent or workflow proposes an action and tags an approval class.
2. `dealix/trust/approval_matrix.py` writes a pending entry to the
   approval queue (`founder/approvals_waiting.md` in the private repo).
3. Founder resolves to `approved` or `rejected` with a one-line reason.
4. `dealix/trust/audit.py` writes an immutable audit record.
5. The original workflow polls the queue; on `approved`, it executes;
   on `rejected`, it records the rejection and stops.

---

## 4. Escalation

Documented in `docs/ops/ESCALATION_MATRIX.md`. Severity tiers map to
SLAs:

| Tier | Definition | SLA |
|------|------------|-----|
| P0 | Data exposure, payment failure, public-trust risk | < 1h founder review |
| P1 | Customer-impacting (delivery slip, missed renewal) | < 24h |
| P2 | Internal blocker | < 72h |
| P3 | Improvement / learning | Weekly review |

---

## 5. Audit & Evidence

Every approval is paired with:

- An entry in `trust/approval_log.csv` (private repo).
- A pointer to the originating workflow ID.
- A pointer to the resulting effect (message ID, invoice ID, etc.).

Auditability is asserted by `tests/trust/test_approval_matrix.py`.
