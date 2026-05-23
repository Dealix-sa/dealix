# DEALIX Proposal Template Guide

**Owner:** Founder
**Source of truth:** `docs/brand/DEALIX_MARKETING_ASSET_GUIDE.md` + `docs/03_commercial_mvp/`

## Purpose

A Dealix proposal is a founder-signed contract scaffold. It commits scope, pricing, timeline, gates, and exclusions. It is not a sales pitch. The pitch is in the discovery call.

## Structure (eight sections)

1. Cover
2. Executive summary
3. Scope (what is in)
4. Out of scope (what is not in)
5. Timeline
6. Pricing — with guardrail
7. Approval gates and operating commitments
8. Appendix — disclosures, definitions, references

Every proposal has exactly these eight sections in this order. No extras, no skips.

## Cover

- Full-bleed Pipeline gradient background.
- Lockup top-left.
- Customer name top-right (matches official trade name).
- Document title centered: "Sprint Proposal — [Sprint Type] — [Sector]".
- Document number bottom-left (format `DLX-PROP-YYYY-NNNN`).
- Date bottom-right.
- Version stamp bottom-center (`vX-draft` or `vX-final`).

## Executive summary

Length: 120-180 words. Structure:

- Sentence 1 — Customer's stated problem (in their words).
- Sentence 2 — Dealix sprint that addresses it (by name).
- Sentence 3-5 — What the customer will hold in their hand at the end of the sprint (named deliverables).
- Sentence 6 — Cost and timeline in one line.
- Sentence 7 — Approval gate.

No marketing adjectives. No "we are excited to partner with you."

## Scope

Bulleted list of named deliverables. Each bullet has:

- Deliverable name (proper noun, capitalized).
- One-line description.
- Owner (Dealix or Customer).
- Acceptance criterion ("Accepted when X is true").

Example:

- **Account Map (40)** — A scored list of 40 candidate accounts in the target sector. Owner: Dealix. Accepted when Customer signs off the scoring rubric.

## Out of scope

Bulleted list. Each bullet is one line. This section is mandatory. It exists to prevent scope drift.

Common exclusions:

- External outreach send (queued only, not sent).
- WhatsApp messaging.
- Cold scraping of third-party platforms.
- Paid media spend.
- CRM platform license.

## Timeline

Table with three columns: Week, Milestone, Owner.

Example:

| Week | Milestone | Owner |
|---|---|---|
| 1 | Discovery + Account Map draft | Dealix |
| 2 | Account Map sign-off + Draft outreach pack | Dealix + Customer |

## Pricing — with guardrail

Table with line items, unit price, quantity, subtotal. Below the table:

- Total in SAR, bold.
- Payment schedule (e.g., 50 percent upfront, 50 percent on acceptance).
- VAT line (15 percent KSA).
- **Guardrail clause**: "If by the acceptance milestone the deliverable is not in the Customer's hand, Dealix issues a credit equal to [X percent] of the affected line item, applied to the next sprint. No cash refunds. This clause is the entire remedy."

This guardrail replaces guarantees.

## Approval gates and operating commitments

Named gates with named approvers:

- Proof publication — Founder.
- External send — Customer + Founder.
- Pricing change — Founder.
- Contract amendment — Founder.
- Refund or credit — Founder.

Plus operating commitments:

- "Dealix prepares; the Customer approves; Dealix sends only with written approval."
- "Dealix does not scrape, does not auto-send cold messages, does not bypass platform terms."
- "PDPL and CITC frameworks govern data handling."

## Appendix

- Definitions (Sprint, Proof Pack, Approval Gate, Verified Value, Estimated Value).
- References (linked Dealix docs, dated).
- Disclosure block.

## Disclosure block (mandatory footer on the appendix page)

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
> Dealix does not guarantee revenue, meetings, or conversion outcomes. All forecasts are estimated and bound by the trust gates above.

## Jinja2 template

A machine-fillable version lives at `templates/PROPOSAL_SPRINT.md.j2` (created separately). Variables:

- `customer_name`
- `sprint_type`
- `sector`
- `total_sar`
- `start_date`
- `end_date`
- `account_count`

## Failure mode

- Proposal sent as `vX-draft`.
- Out-of-scope section missing.
- Guarantee phrase ("we guarantee") inside the pricing section.
- Disclosure block missing on the appendix page.

## Recovery path

1. Pull the proposal.
2. Restore missing sections from the latest `vX-final` template.
3. Re-issue with a new document number and a note: "Replaces [prior number]."

## Disclaimer

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
