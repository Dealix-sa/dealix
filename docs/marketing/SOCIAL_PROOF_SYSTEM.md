# Social Proof System

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> Social proof at Dealix is gated, dated, and refusable. The default
> is no proof. Proof is added only when there is an approval entry
> in the trust ledger.

Social proof is one of the most abused asset classes in B2B
marketing. Dealix treats it as a contract artefact: every logo,
quote, screenshot, statistic, and reference is a commitment to the
customer and to the reader that it can be defended. This document
defines what counts as social proof at Dealix, how it is approved,
and how it is retired.

## Operating Principles

- The default is no proof. Proof is added only when there is a
  recorded approval.
- No social proof element is published without an expiry date.
- A social proof element can be retracted at any time by the
  customer with no penalty.
- A social proof element travels with its context (date, scope,
  method).
- No social proof element is created by inference (e.g. "they did
  not say no"). Silence is not consent.

## Categories of Social Proof

Dealix recognises seven categories.

1. **Customer logos.** Identifiable brand marks on Dealix surfaces.
2. **Customer names.** Identifiable customer names in copy.
3. **Customer quotes.** Direct quotations attributed to a named
   customer.
4. **Customer videos / interviews.** Recorded customer media.
5. **Case studies.** Detailed engagement narratives (see
   `CASE_STUDY_SYSTEM.md`).
6. **Numerical claims.** Customer-specific or aggregate figures
   used in marketing copy.
7. **Awards, certifications, recognitions.** Third-party badges
   shown on Dealix surfaces.

Each category has its own approval flow and expiry cadence.

## Approval Flow (By Category)

| Category               | Required approval                                                | Default expiry |
|------------------------|------------------------------------------------------------------|----------------|
| Customer logos         | Signed customer approval for logo usage and scope                | 12 months      |
| Customer names         | Signed customer approval, scope-specific                         | 12 months      |
| Customer quotes        | Signed customer approval of the exact wording                    | 12 months      |
| Customer videos        | Signed customer approval; rights to distribute on named channels | 6 months       |
| Case studies           | See `CASE_STUDY_SYSTEM.md`                                       | 12 months      |
| Numerical claims       | Method documented; customer approval for customer-specific data  | 6 months       |
| Awards / certifications| Issuer verification; renewal calendar                            | Per issuer     |

A piece of social proof without an approval entry in the trust
ledger is not displayed.

## Trust Ledger Schema for Social Proof

Each approval entry records:

- `proof_id`
- `category`
- `customer_id` (or `issuer_id` for awards)
- `scope` (specific channels and surfaces where the proof may be
  displayed)
- `approved_version` (the exact wording, logo file, or media
  reference)
- `approval_date`
- `expiry_date`
- `re_approval_status`
- `retraction_status`

## Logo Usage Rules

- Logos are displayed only on surfaces named in the scope.
- Logos are displayed at their approved colour and proportions.
- Logos are not used in paid advertising without explicit approval.
- Logos do not appear alongside a guaranteed-outcome claim.

## Quote Usage Rules

- Quotes are reproduced verbatim from the approved version.
- Quotes are attributed by name, role, and company per the
  approved scope.
- Quotes are not edited for length without re-approval.
- Quotes are not used to imply outcomes outside the engagement
  context.

## Numerical Claim Rules

- A numerical claim must travel with its method.
- A customer-specific numerical claim requires explicit customer
  approval of the number, the method, and the time period.
- An aggregate numerical claim ("across N engagements, we observed
  X pattern") requires an audit ledger source, a minimum sample
  size, and a caveat about confidence interval.
- "Up to N%" framing is forbidden.

## Aggregate Proof

Dealix may produce aggregate proof statements that do not require
per-customer approval. Examples:

- "Across active engagements, we observed [pattern]."
- "In [sector], we observed [pattern]."

Aggregate statements require:

- A minimum sample size (recorded in the trust ledger entry).
- A method (how the observation was made).
- A caveat (what we do not yet know).
- No identifiable detail.

The Proof Safety Agent runs an anonymisation check before any
aggregate proof is published.

## Retraction

- Any customer may request retraction of their proof element at
  any time.
- Retraction is processed within 48 business hours.
- The proof element is removed from public surfaces.
- The trust ledger entry is updated with the retraction timestamp
  and reason.
- The retraction is processed without negotiation.

## Re-Approval Cadence

- Sixty days before expiry, the Content Strategist contacts the
  customer or issuer for re-approval.
- If the customer does not respond within 30 days of expiry, the
  proof element is moved to draft state and removed from public
  surfaces.
- A new version of the proof element requires a fresh approval
  entry.

## Eval Tests

The proof-safety eval set scans Dealix surfaces for:

- Customer names, logos, or quotes that do not match an active
  approval entry.
- Expired proof elements still displayed.
- Numerical claims missing their method.
- Aggregate claims missing their sample size or caveat.
- Award / certification badges that have expired.

A surface that fails any test is removed from public display until
remediated.

## Distribution Channels Where Social Proof Appears

- Landing pages (gated by approval).
- Sector pages (gated by approval and sector scope).
- Sector reports (gated by approval and report-specific scope).
- Founder content (gated by approval and post-specific scope).
- Newsletter (gated by approval and issue-specific scope).
- Proposals (only with customer-specific approval; no proof of
  one customer is shown to another without their approval).

## Failure Modes

- A customer logo appears on a paid ad without paid-ad scope
  approval. Failure: scope breach. Ad is paused; trust ledger
  records.
- A customer quote is published with edits. Failure: wording
  breach. Quote is corrected; trust ledger records.
- An expired award badge is still displayed. Failure: governance
  miss. Badge removed; calendar updated.
- A retracted proof element is still displayed. Failure: process
  breach. Element removed immediately; incident response triggered.
- An aggregate claim is published without method. Failure: claims
  safety. Claim removed; eval upgraded.

## Anti-Patterns

- "Trusted by N companies" with a number that combines paying
  customers, free diagnostic users, and inbound leads. Banned.
- "Average customer sees X% growth" with no method. Banned.
- "As featured in" press strips that link to unrelated mentions.
  Banned.
- "Hand-curated testimonials" sourced from social posts without
  the customer's explicit approval to repurpose. Banned.
- "Logo wall" with logos at different approval states. Banned.

## Storage

- Approval artefacts are stored in the private ops runtime under
  `proof/social_proof/<proof_id>/`.
- Customer signature artefacts are stored alongside the approval.
- Public surfaces are inventoried in
  `marketing/social_proof_inventory.csv` so the Proof Safety Agent
  can audit them periodically.

## Metrics That Matter

The Performance Analyst tracks:

- Number of approved proof elements by category.
- Re-approval rate.
- Retraction rate.
- Public surfaces with active proof elements.

Metrics not optimised for: raw logo count, raw quote count.

## Cross-References

- Marketing OS: `docs/marketing/DEALIX_MARKETING_OS.md`.
- Case study system: `docs/marketing/CASE_STUDY_SYSTEM.md`.
- Trust contract: `policies/dealix_control_policy.yaml`.
- Proof safety agent: `docs/ai/` (registry id `proof_safety_agent`).

## Localisation

For Arabic-speaking customers and surfaces, the approved version of
a proof element is the version in the customer's chosen language.
Translation of an approved quote requires re-approval; Dealix does
not machine-translate customer wording without consent.

## Why So Strict

The first time a customer sees their logo on a Dealix surface
without their approval, the trust is gone. The first time a buyer
encounters an "up to" claim that does not survive procurement
review, the deal is gone. Social proof is a long-arc asset; treated
with discipline it compounds; treated cheaply it evaporates.

Dealix runs the strict version on purpose. Fewer proof elements,
each defensible. Every element retractable on demand. Every
element dated. That posture is what lets Dealix talk about trust
without making trust theatre.
