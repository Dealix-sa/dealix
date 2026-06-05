# Governance OS

> **Status:** `BETA` · **Plane:** Trust · **Owner:** Founder · **Last reviewed:** 2026-06-05
>
> This protects Dealix from becoming "random AI." Governance is a trust feature,
> not a side document.

---

## Purpose

Ensure Dealix is approval-first, auditable, and safe — so customers trust it with
their business.

## Functions

- Human approval
- No auto-send
- No fake proof
- No scraping
- No overclaim
- Audit trail
- Access control
- Data retention
- Incident log

## Approval classes

| Class | Needs approval? |
|---|---|
| A0 Internal draft | No |
| A1 Internal analysis | No |
| A2 Customer-facing draft | Yes, before sending |
| A3 External action | Yes, always |
| A4 Financial / legal / security | Yes + log |
| A5 Destructive action | Forbidden unless explicitly authorized |

See `docs/03_governance/HUMAN_APPROVAL_POLICY.md` for the full policy.

## Forbidden actions

- Automatic WhatsApp sending
- Bulk email sending
- Scraping
- Pricing changes without documentation
- Publishing a case study without approval
- Deleting data without a record

## Regulatory posture

Governance OS is built as a **trust feature**. NCA publishes an official set of
cybersecurity controls and guidelines (social-media accounts, remote work,
critical systems, e-commerce, and more). Dealix builds **NCA-aligned controls** —
we say "aligned," never "certified," unless we hold an actual certification.

## Inside the Command Sprint

Governance OS produces the **Approval Register** — what in the customer's flow
needs human approval and who the approver is.

## Deeper references

- `docs/03_governance/` (this branch's canonical governance docs)
- `docs/07_governance/`, `dealix/trust/`, `dealix/registers/`
