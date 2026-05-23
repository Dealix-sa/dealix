# Case Study System

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> Case studies at Dealix are gated by recorded approval. No customer
> name, no logo, no quote, no screenshot is published without an
> explicit approval entry in the trust ledger.

A case study is the highest-trust marketing asset Dealix can produce
and the easiest to misuse. The case study system below makes the
approval flow explicit, the evidence requirements concrete, and the
refusal posture unambiguous.

## Operating Principles

- A case study exists only when the customer has approved, in
  writing, the publication of their participation.
- A case study contains only evidence Dealix can defend. Outcome
  claims travel with method.
- No case study contains "guaranteed", "promised", or any
  outcome-promise wording.
- A case study is dated. Approval has an expiry; case studies are
  re-approved on a defined cadence.
- A case study can be retracted at any time by the customer, with
  no penalty.

## Approval Flow

A case study moves through a strict sequence.

1. **Candidate identification.** The Productization Agent or the
   founder identifies a candidate engagement.
2. **Customer outreach.** The founder approaches the customer with
   a written request describing what the case study would cover,
   what evidence would be cited, and what the customer can refuse.
3. **Customer scoping.** The customer chooses scope: full attribution
   (name, logo, quote), partial attribution (name only, no logo), or
   anonymous (sector and size only).
4. **Draft.** The Content Strategist drafts the case study from
   anonymised audit ledger entries and the customer's input.
5. **Customer review.** The customer reviews the draft and either
   approves the final version, returns it for edits, or declines
   publication.
6. **Trust ledger entry.** The approval is recorded in the trust
   ledger with the customer's signature, the scope, the version
   approved, and the expiry date.
7. **Eval and brand check.** Brand Guardian and Trust Guardian
   evals run on the approved draft.
8. **Founder approval.** The founder approves the publication.
9. **Publication.** A human publishes the case study on the
   approved channels.
10. **Re-approval cadence.** The case study is re-approved at the
    expiry date or at a defined cadence (default: annually).

## Case Study Anatomy

Each case study uses the same anatomy.

1. **Cover.** Customer (per scope), sector, engagement rung,
   timeframe.
2. **Why the engagement.** The customer's situation in plain terms.
3. **What we did.** Specific artefacts produced (not adjectives).
4. **What we did not do.** The refusal posture in action.
5. **What we observed.** Anonymised outcome patterns with method.
6. **What the customer says.** Approved quote (optional).
7. **What we would do differently.** Honest reflection.
8. **What remains uncertain.** Honest gaps.
9. **Disclaimers.** Outcome claims are described, not promised; the
   approval window is stated.

## Scope Options

| Scope                  | Includes                                             |
|------------------------|------------------------------------------------------|
| Full attribution       | Customer name, logo, named quote, role               |
| Named, no logo         | Customer name, role attribution, no logo, no quote   |
| Sector-anonymised      | Sector and size band only; no name, logo, quote      |
| Pattern-only           | Anonymised data point; no identifying detail         |

A customer chooses the scope. Dealix does not negotiate upward.

## Evidence Discipline

Every claim in a case study traces to:

- An anonymised audit ledger entry.
- A customer-provided figure that the customer has explicitly
  approved for publication.
- A public data source (cited).
- A method-documented observation.

A claim without traceable evidence is removed.

## Forbidden in a Case Study

- "Guaranteed", "promised", "we delivered N% growth".
- Unredacted screenshots.
- Confidential pricing or contract detail.
- Customer-specific suppression list detail.
- Customer-specific PDPL or compliance detail beyond what the
  customer has approved.
- "Up to N%" framing without method.
- Vague magnitude claims ("massive", "huge", "transformational").

## Re-Approval and Expiry

- Approval has an expiry date (default: 12 months from publication).
- Sixty days before expiry, the Content Strategist contacts the
  customer for re-approval.
- If the customer does not respond within 30 days of expiry, the
  case study is moved to draft state and removed from public
  surfaces.
- A new version requires a fresh approval entry.

## Retraction

- A customer can request retraction at any time, with no penalty.
- Retraction is processed within 48 business hours.
- The trust ledger records the retraction with the timestamp and
  reason.
- The case study is removed from public surfaces, archived in the
  private ops runtime, and referenced by id in the audit ledger.

## Distribution Channels

Approved case studies may appear on:

- The Dealix sector page corresponding to the case study's sector.
- The Dealix offer page corresponding to the engagement rung.
- The Dealix newsletter (with a link to the full case study).
- A founder LinkedIn post (with the customer's approval to be
  named in the post).
- Sector report excerpts (with the customer's approval to be cited).

A case study is not distributed to paid amplification without
explicit customer approval.

## Approval Markers (Case-Study-Specific)

| Marker                       | Owner                              | States                  |
|------------------------------|------------------------------------|-------------------------|
| `customer_approval`          | Customer (signed)                  | PENDING, APPROVED       |
| `claims_safety`              | Brand Guardian                     | PENDING, APPROVED       |
| `brand_voice`                | Brand Guardian                     | PENDING, APPROVED       |
| `proof_safety`               | Proof Safety Agent                 | PENDING, APPROVED       |
| `founder_approval`           | Founder                            | PENDING, APPROVED       |
| `expiry_date`                | Customer + founder                 | Date                    |

A case study is not published unless all markers are in their
terminal state and `expiry_date` is in the future.

## Eval Tests

The case-study eval set includes:

- Anonymisation check against the audit ledger.
- Customer-approval cross-reference (the customer's signed
  approval must match the published version).
- Claims-safety scan.
- Brand-voice scan.
- Expiry-date check.

A case study that fails any test is blocked from publication.

## Storage

- Drafts and approved versions are stored in the private ops
  runtime under `proof/case_studies/<engagement_id>/`.
- Trust ledger entries reference the case study id and version.
- Customer signature artefacts are stored under
  `proof/case_studies/<engagement_id>/approvals/`.

## Failure Modes

- A case study is published with a customer name without approval.
  Failure: trust breach. Case study retracted within hours; trust
  ledger records the breach; incident response triggered.
- A case study contains a guaranteed-outcome phrase. Failure:
  claims safety. Retracted; eval upgraded.
- A case study's expiry has passed. Failure: governance miss.
  Removed from public surfaces; re-approval requested.
- A customer requests retraction and the case study remains live.
  Failure: process breach. Immediate retraction; trust ledger
  records.
- A partner publishes a Dealix case study without approval.
  Failure: partner agreement breach. Partner is contacted; partner
  agreement's trust clause is invoked.

## Anti-Patterns

- "We can use the logo, we have permission verbally." Verbal
  approval is not approval.
- "We will publish first and ask later." Banned.
- "We can use the case study from a former employer." Approval
  travels with the customer, not with Dealix.
- "We will swap names for a sector mention to skip approval."
  Banned. Sector-anonymised requires the same approval (because
  the engagement signature can still be identifying).

## Metrics That Matter

The Performance Analyst tracks:

- Number of approved case studies by sector and rung.
- Re-approval rate.
- Retraction rate (a low rate is the target, but a zero rate is a
  warning sign of trust risk).
- Qualified conversations sourced from case studies.

## Cross-References

- Marketing OS: `docs/marketing/DEALIX_MARKETING_OS.md`.
- Social proof: `docs/marketing/SOCIAL_PROOF_SYSTEM.md`.
- Trust contract: `policies/dealix_control_policy.yaml`.
- Proof safety agent: `docs/ai/` (registry id `proof_safety_agent`).

## Why Strict

In most B2B marketing, case studies drift over time: a logo here
without re-approval, a quote there without expiry, an outcome
number that exceeds the original method. Dealix runs case studies
with the same discipline as proposals: written approval, expiry,
retraction on demand, audit trail. The cost is fewer case studies.
The benefit is that every case study Dealix publishes can be
defended against any procurement scrutiny, any regulatory review,
and any partner audit. That is the only kind of social proof worth
producing.
