# Dealix Claims Register

**Purpose:** Every customer-facing claim Dealix makes must be either (a) provable
from the customer's own data, or (b) a clearly-scoped description of what the
product does. This register is the single place where each claim is recorded
with its status and its evidence basis. If a claim is not in this register with
status `approved`, it must not appear on the public surface, in a proposal, or
in a Proof Pack.

**Owner:** Founder (CEO). **Last updated:** 2026-06-06.

## Claim status legend

| Status | Meaning |
|--------|---------|
| `approved` | Cleared for use. Evidence basis recorded below. |
| `review` | Pending founder decision — do **not** use yet. |
| `forbidden` | Permanently banned (guaranteed-outcome / cold-outreach / scraping). |

## Forbidden claim classes (never allowed)

These are blocked by automated guardrails (`tests/test_landing_forbidden_claims.py`,
`scripts/verify_dealix_positioning.py`) and may only appear in an explicit
negation/disclaimer context ("لا scraping", "no cold outreach", "صفر تواصل بارد").

| Class | Examples | Status |
|-------|----------|--------|
| Guaranteed revenue / ROI | "نضمن مبيعات", "guaranteed ROI" | `forbidden` |
| Guaranteed ranking | "نضمن المركز الأول" | `forbidden` |
| Cold outreach automation | "cold WhatsApp blast", "cold email sequences" | `forbidden` |
| Data scraping | "scrape leads", "scraping behind login" | `forbidden` |
| Fake proof / fabricated metrics | invented case-study numbers | `forbidden` |

## Approved positioning claims

| # | Claim | Basis | Status |
|---|-------|-------|--------|
| 1 | "Dealix is an AI Business Operating System for Saudi companies." | Product category statement. | `approved` |
| 2 | "Not a CRM, not a chatbot." | Differentiation statement (descriptive). | `approved` |
| 3 | "Command Sprint is a 7-day, founder-led engagement." | Delivery model (`data/launch/module_status.json`). | `approved` |
| 4 | "Outputs: Revenue Map, Proof Register, Executive Command Brief, Next Action Board, Approval Register." | Defined deliverables, produced from the customer's own data. | `approved` |
| 5 | "Every external action requires human approval." | Enforced by Approval Register + Human Approval Policy. | `approved` |
| 6 | "PDPL-aware." | Descriptive of data-handling posture, not a certification claim. | `approved` |
| 7 | "Manual payment; full refund within 7 days if not satisfied." | Operational policy (founder-honored). | `approved` |

## Per-customer proof claims

Any number quoted in a Proof Pack must trace to a row in that customer's
`05_proof_register.md`, which in turn cites the source data the customer
provided. Proof claims are **per-engagement** and are not added to this global
register. The rule: *no number without a traceable source*.

## Change log

- 2026-06-06 — Register created for Wave 7 private launch. Positioning + Command
  Sprint claims approved; forbidden classes enumerated.
