# Offer Packaging

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> How a Dealix sprint, retainer, pilot, or console is packaged into
> a coherent commercial artefact.

A Dealix offer is not a slide. It is a packaged artefact — a scope
letter, a charter, an SLA, an acceptance, or an agreement — that
states the contract between Dealix and the buyer. This document
defines the packaging system: structure, required components,
evidence requirements, and approval markers.

## Packaging Principles

- One offer, one document. There is no "verbal scope".
- Every offer document carries a refusal list — the things Dealix
  will not do on this engagement — alongside the scope.
- No outcome metric in an offer document is allowed to read like a
  guarantee. Targets are described as targets; commitments are
  described as commitments.
- Pricing in offer documents is final only after founder approval.
  Until that approval, pricing is marked `PENDING_APPROVAL`.
- Every offer document references the Dealix trust contract: the
  policy-as-code rules, the eval gate, and the audit ledger.

## Universal Offer Skeleton

Every Dealix offer document — Sprint Scope, Pilot Charter, Retainer
SLA, Console Acceptance, Enterprise Master Agreement, Partner
Agreement — uses the same skeleton.

1. **Header** — buyer name, Dealix counterpart, rung, version, date,
   approval state.
2. **Why this offer** — one paragraph naming the buyer's revenue
   posture in plain terms.
3. **What we will do** — bulleted, specific, written as deliverables
   not adjectives.
4. **What we will not do** — explicit refusal list, including the
   universal refusals and any engagement-specific refusals.
5. **Evidence we will produce** — list of artefacts written to the
   private ops runtime.
6. **How we will review** — cadence (weekly / monthly / quarterly),
   participants, and decision rights.
7. **Trust gate** — eval gate posture, suppression list contract,
   approval flow.
8. **Pricing** — band, instalment schedule, payment terms.
9. **Term, renewal, exit** — start, end, renewal logic, exit terms.
10. **Approval markers** — buyer signature block; Dealix founder
    approval marker; trust ledger record id.

## Rung-Specific Packaging

### R1 — Diagnostic Engagement Note

Lightweight, single page. Carries:

- The scope of the Diagnostic.
- The explicit "no PII beyond what you choose to share" clause.
- The "we will publish nothing about you" clause.
- The refusal list (no guaranteed pipeline, no proof publication,
  no data export).

No pricing block; this rung is free. There is still an approval
marker so the buyer's request is recorded.

### R2 — Sprint Scope Letter

3–5 pages. Adds to the skeleton:

- Named deliverables with file paths (`sprint/<account>/...`).
- Sprint window dates.
- A short "what we need from you" section — buyer responsibilities
  on data access and review time.
- The instalment schedule (50/50).
- A `PENDING_APPROVAL` marker on pricing until the founder signs.

### R3 — Pilot Charter

6–10 pages. Adds to the skeleton:

- The pilot slice (which accounts, which sectors, which channels).
- The eval gate posture at week 0 and the review threshold for each
  weekly review.
- Mid-point decision rights — either party can pause without
  penalty if the eval gate regresses.
- Kill conditions, written as numbered items, not narrative.
- A 40/40/20 instalment schedule with the mid-point payment
  conditional on a green eval gate and a clean trust posture.

### R4 — Retainer SLA

8–12 pages. Adds to the skeleton:

- The data scope agreement (what Dealix may read; what Dealix may
  write; what Dealix may never touch).
- The monthly cadence and the agendas for the monthly executive
  review and the quarterly trust audit.
- 30-day cancellation notice.
- A renewal memo template that is filed 60 days before each
  renewal.

### R5 — Console Acceptance

5–8 pages. Adds to the skeleton:

- Seat list with role-scoped permissions.
- PDPL posture summary for the tenant.
- Tenant policy mirror — which rules from
  `policies/dealix_control_policy.yaml` are mirrored, which are
  overridden, and what the overrides are.
- Kill switch ownership — who can pause an agent at the tenant
  level.
- An explicit "A3 cannot be enabled" clause.

### R6 — Enterprise Master Agreement and Data Processing Agreement

20+ pages, plus addenda. Adds to the skeleton:

- Tenant isolation specification.
- Data residency and retention windows.
- Sub-processor disclosure list.
- Security review acceptance criteria.
- Sector overlay scoping, with each overlay capable of being
  enabled or disabled separately.
- Audit export specification.

### R7 — Partner Agreement

Bespoke. Adds to the skeleton:

- Brand carve-out — exactly how the partner brand may be used and
  what must remain attributed to Dealix.
- Eval gate certification process for partner-side agents.
- Revenue share schedule and reporting cadence.
- Termination terms covering trust violations.

## Evidence Requirements

A Dealix offer document is not finished until the evidence is
linked. Each deliverable line in the "Evidence we will produce"
section must reference a file path in the private ops runtime — the
file does not need to exist yet, but the path and schema do.

For example, a Sprint Scope Letter referencing `outreach/queue.csv`
must include a one-line schema reference so the buyer knows what
will be written. A Pilot Charter referencing
`evals/eval_status.csv` must reference the eval gate that applies.

## Approval Flow

1. Drafter (Offer Architect or founder) prepares the document with
   pricing marked `PENDING_APPROVAL`.
2. Brand Guardian reviews the document for claims discipline and
   brand voice.
3. Trust Guardian reviews the document for refusal-list completeness,
   policy mirror, and proof contract.
4. Finance Copilot reviews the pricing block against the pricing
   guardrails (`docs/product/PRICING_GUARDRAILS.md`).
5. Founder approves or returns. Pricing becomes `APPROVED` only after
   founder approval is recorded in the trust ledger.
6. Document is sent to the buyer. Buyer signature returns; signed
   document is filed in `proposals/<account>/<rung>/`.

## Refusal Marker Library

Each offer document pulls from a shared refusal marker library so
language is consistent.

- `R-001 — no_guaranteed_outcomes` (universal)
- `R-002 — no_external_send_automation` (universal)
- `R-003 — no_proof_publication_without_approval` (universal)
- `R-004 — no_pricing_change_without_founder_approval` (universal)
- `R-005 — no_data_export_without_escalation` (universal)
- `R-006 — no_a3_autonomous_execution` (universal)
- `R-101 — no_external_send_during_pilot_pause` (R3)
- `R-102 — no_console_seat_without_policy_mirror` (R5)
- `R-103 — no_enterprise_overlay_without_security_review` (R6)
- `R-104 — no_partner_brand_use_outside_carve_out` (R7)

The Brand Guardian eval includes a refusal-marker presence test;
documents missing the relevant markers are flagged before approval.

## Versioning

Every offer document is versioned (`v1`, `v1.1`, `v2`). Material
changes between versions are summarised at the top of the document.
A signed document is immutable; a follow-up change is a new version
or a written amendment.

## Storage

Drafts live in the private ops runtime under
`proposals/<account>/<rung>/drafts/`. Approved and signed documents
live under `proposals/<account>/<rung>/approved/`. Nothing about a
buyer is stored in this repository.

## Packaging Anti-Patterns

- Verbal scope — the offer is not real until it is written.
- "Up to" deliverables — every line must be deterministic, not
  aspirational.
- Marketing language inside an offer document — adjectives like
  "world-class", "best-in-class", "guaranteed" are stripped by the
  Brand Guardian.
- Refusal list omitted to make the document feel friendlier.
- Pricing block missing the instalment schedule.
- Pricing block missing the `PENDING_APPROVAL` or `APPROVED`
  marker.
- Renewal memo missing the trust-audit reference.

## Audit and Eval

Every offer document, every version, and every approval is logged
in the audit ledger. The Performance Analyst tracks:

- Time from draft to approval.
- Time from approval to buyer signature.
- Win rate by rung.
- Refusal rate by rung (offers Dealix declined).

These metrics are read internally; they are never published as
benchmarks.

## Why Packaging Matters

Most B2B vendors lose the buyer's trust in the offer document — by
vague scope, surprise pricing, or unstated commitments. Dealix
treats the offer document as the first delivery of the engagement.
A clean offer document is itself evidence that the operating system
works.
