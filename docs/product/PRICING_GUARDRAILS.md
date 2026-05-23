# Pricing Guardrails

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> Pricing bands, discount limits, and the approval flow that governs
> any deviation. Pricing in Dealix is never improvised.

This document defines the pricing guardrails for the Dealix product
ladder. The guardrails are deliberately conservative: pricing
discipline is part of the trust contract. The Finance Copilot reads
this file; so does the Founder Console; so does the policy adapter.

## Operating Principles

- All pricing is denominated in SAR for Saudi-domiciled buyers and
  USD-equivalent for non-Saudi buyers, with conversion fixed at the
  date of the offer document.
- Pricing on any offer document is marked `PENDING_APPROVAL` until
  the founder approves. After approval, it becomes `APPROVED` and
  the approval is recorded in the trust ledger.
- No commercial term — price, discount, payment schedule, refund
  clause, contract change — may be communicated externally without
  founder approval.
- The Founder Console is the only sanctioned origin for pricing
  approvals. Off-system commitments are not enforceable inside the
  Dealix operating system and will be flagged by the Finance
  Copilot.
- The policy adapter denies any action of type `pricing_commit`,
  `discount_commit`, `contract_commit`, `refund_commit`, or
  `payment_terms_commit` when `approved: false`.

## Reference Bands

The bands below are operating guidance for sales conversations. They
are not published externally.

| Rung | Offer                              | Floor (SAR) | Reference (SAR)  | Ceiling (SAR) | Billing default     |
|------|------------------------------------|-------------|------------------|---------------|---------------------|
| R1   | Free Sample / Diagnostic           | 0           | 0                | 0             | None                |
| R2   | Revenue Sprint                     | 18,000      | 25,000           | 35,000        | 50/50               |
| R3   | Managed Pilot                      | 45,000      | 65,000           | 90,000        | 40/40/20            |
| R4   | Revenue Desk Retainer (per month)  | 25,000      | 40,000           | 55,000        | Monthly, NET-15     |
| R5   | Founder Console (per year)         | 60,000      | 120,000          | 180,000       | Annual, prepay      |
| R6   | Enterprise Revenue Intelligence OS | 250,000     | 600,000          | 1,200,000     | Annual + milestones |
| R7   | Partner / White-label Revenue OS   | Bespoke     | Bespoke + revshare | Bespoke     | Bespoke             |

The reference column is the conversational anchor; the band exists
to absorb scope variation. Below the floor and above the ceiling,
the founder must approve and a written rationale must be recorded.

## Discount Limits

| Discount | Authority required        | Recorded as                          |
|----------|---------------------------|--------------------------------------|
| 0–5%     | Offer Architect (operator)| Note in offer document               |
| 5–15%    | Founder approval          | Trust ledger entry + offer document  |
| 15–25%   | Founder approval + reason | Trust ledger entry + reason memo     |
| > 25%    | Hard stop; not allowed unless paired with reduced scope. The Finance Copilot raises a flag. |

Discounts are tracked by reason code so we can see whether discounts
are driven by scope reduction, by competitive pressure, by sector
constraint, or by buyer relationship.

## Discount Reason Codes

- `D-001` — scope reduction, written in the offer document.
- `D-002` — multi-rung commitment (e.g. R2 + R4 booked together).
- `D-003` — sector partnership or sector body referral.
- `D-004` — anchor account (early evidence partner). Requires
  founder rationale.
- `D-005` — multi-year prepay (R5 / R6 only).
- `D-006` — buyer-side data-quality commitment that reduces
  Dealix's lift.

A discount without a reason code is invalid. The Finance Copilot
audits the offer ledger weekly for discounts missing reason codes.

## Payment Terms

| Term      | Default by rung | Variation requires                       |
|-----------|-----------------|------------------------------------------|
| Prepay    | R5, R6          | None (default)                           |
| 50/50     | R2              | Founder approval if shifted              |
| 40/40/20  | R3              | Founder approval if shifted              |
| Monthly   | R4              | Founder approval if shifted              |
| NET-15    | R4              | Founder approval if extended             |
| NET-30    | R6 milestones   | Founder approval if extended beyond 30   |
| NET-45+   | Not allowed unless paired with security deposit. |

The policy adapter denies any `payment_terms_change` without an
escalation record (rule id `payment_terms_require_escalation`).

## Refund Policy

Refunds are bounded and contract-specific.

- R1 — no refund applicable (free).
- R2 — full refund of the second instalment if Dealix cannot deliver
  a defensible ICP. No partial refunds of the first instalment.
- R3 — mid-point payment release is conditional on a green eval
  gate. If the gate is not green at mid-point, the buyer may exit
  with no further payment due and no partial refund of the first
  instalment.
- R4 — pro-rated refund of the unused portion of a month if the
  retainer is paused for a trust violation initiated by Dealix.
- R5, R6 — annual prepay is non-refundable. Pause credits may be
  issued under exceptional circumstances and require founder
  approval.
- R7 — bespoke, written in the partner agreement.

The Finance Copilot raises a flag if any refund commitment is made
verbally and not recorded in the trust ledger.

## Contract Change Limits

Any contract change — scope expansion, scope reduction, term
extension, term reduction, additional seats, additional sectors,
new sub-processor — requires:

1. A written change request from the buyer or from Dealix.
2. A review by the Offer Architect and the Finance Copilot.
3. A founder approval recorded in the trust ledger.
4. An amendment document signed by both parties.

The policy adapter denies any `contract_change` action without an
escalation record (rule id `contract_change_requires_escalation`).

## Anchoring and Bracketing

In sales conversations:

- Quote a band, not a single number, until the scope is verified.
- Anchor at the reference column. Never anchor at the floor.
- Use the ceiling only when the scope variation justifies it (extra
  seats, regulated overlay, multi-BU rollout).
- If the buyer asks "what does this normally cost?", answer with a
  band and the named factors that move within the band.

## Approval Flow

1. Offer Architect drafts the offer with pricing marked
   `PENDING_APPROVAL`.
2. Finance Copilot validates the pricing block against this file:
   floor, ceiling, discount reason code, payment terms.
3. Brand Guardian checks the offer document for guaranteed-outcome
   wording and any pricing language that drifts from the published
   band logic.
4. Trust Guardian checks the refusal-marker library is present.
5. Founder reviews and approves or returns. Approval is recorded in
   the trust ledger with the offer document version and id.
6. Offer Architect updates the pricing marker to `APPROVED` and
   prepares the document for the buyer.

## Audit and Eval

- The Finance Copilot maintains `finance/pricing_audit.csv` with
  every offer's pricing block, discount, payment term, and
  approval id.
- A weekly Finance review checks that no offer document has been
  released with `PENDING_APPROVAL` still marked.
- The Performance Analyst tracks discount frequency by reason code
  and reports it monthly.
- The Trust Guardian raises a flag whenever a discount above 15% is
  approved without a written rationale.

## Pricing Anti-Patterns

- Verbal pricing in a meeting. The conversation can quote bands;
  it cannot commit a number.
- Pricing on a website without founder approval. Dealix does not
  list rung pricing publicly.
- "Promo" pricing. Dealix does not run promotions.
- "Friend pricing". Discounts must have a reason code.
- Quiet price changes. Renewal increases are documented in the
  renewal memo with the rationale.
- Sending a quote by email without the offer document. The offer
  document is the only sanctioned quote.

## Pricing and the Refusal Catalogue

Several pricing scenarios are refusals by default:

- A buyer who requests guaranteed outcomes in exchange for higher
  pricing is declined.
- A buyer who wants to pay outside the published payment terms by
  more than 30 days is declined unless a security deposit is
  provided.
- A buyer who wants Dealix to execute external action automatically
  is declined regardless of price.
- A partner who wants resale rights without a partner agreement is
  declined regardless of revenue share.

## Review Cadence

The pricing guardrails are reviewed quarterly. The review is
recorded in `finance/pricing_review.md`. A review either reaffirms
the bands, refines them, or — rarely — opens a structural change
that requires founder sign-off, an updated Finance Copilot prompt,
and an updated offer-document template.

## Localisation

For non-Saudi buyers, the SAR figures are converted at the date of
the offer document and locked for the term. Currency variation
during the term is absorbed by Dealix unless the offer document
states otherwise. Multi-currency contracts require founder approval.

## Summary

Pricing in Dealix is a part of the trust contract. The bands here
are not a price list; they are a discipline. The discipline is
visible to the buyer in the offer document, the approval marker,
and the trust ledger entry. That visibility is part of how Dealix
earns the right to be trusted with the buyer's revenue motion.
