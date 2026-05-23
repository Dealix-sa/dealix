# Partner Outreach Guide

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> Partner outreach at Dealix is founder-led, written, and governed
> by a partner agreement. It is never autonomous or transactional.

Partner outreach is the slowest channel Dealix runs and the most
strategic. A partner relationship at Dealix is a multi-quarter
commitment that culminates in a written partner agreement (R7) or a
co-introduction arrangement that respects the partner's brand and
the buyer's trust. This guide describes how the relationship is
sourced, opened, sustained, and audited.

## Operating Principles

- Partner outreach is founder-led. The Distribution Operator may
  prepare drafts, but the founder sends and follows up.
- Partner outreach respects the partner's brand. Co-branded
  materials require written sign-off from both sides.
- No partner-led engagement bypasses the Dealix trust contract.
  Even when the partner fronts the brand, the policy-as-code, the
  eval gate, and the audit ledger remain Dealix-grade.
- No revenue share, brand carve-out, or co-introduction is
  committed verbally. Everything is written.
- A3 (autonomous external action) is banned across partner-led
  engagements just as it is internally.

## Partner Types

Dealix engages four kinds of partners.

- **Consultancies.** Strategy, transformation, or revenue operations
  firms that want a Dealix-grade operating layer they can deliver
  under their brand or co-brand.
- **Integrators.** Technology consultancies that deliver CRM,
  marketing automation, or data platforms and want Dealix as a
  trust-gated layer above them.
- **Sector bodies.** Industry associations, chambers, or sector
  initiatives that want to lift the trust posture of their member
  companies.
- **Co-introduction partners.** Individuals or firms with sector
  reach who refer engagements but do not deliver themselves.

Each type has a different agreement shape; the operating principles
above are identical.

## Sourcing Partners

Sourcing channels:

- Founder network (the highest signal).
- Sector body referrals.
- Inbound from partners who have read Dealix content (governance
  teardowns are a particularly effective signal).
- Existing R3/R4/R5 buyers who suggest a partner they trust.

Cold partner outreach is rare and reserved for partners whose
positioning aligns with Dealix's trust contract.

## Opening Conversations

The opening conversation is exploratory, not transactional. It
covers:

- The partner's delivery posture (who delivers, what artefacts, what
  cadence).
- The partner's existing buyers and sectors.
- The partner's appetite for the Dealix trust contract — explicit
  consent to operate inside the policy-as-code, the eval gate, and
  the audit ledger.
- The partner's brand expectation (co-brand vs. white-label vs.
  attributed).
- The partner's revenue model.

The conversation ends with either:

- A second meeting scheduled to draft a partner agreement.
- An honest "this is not the right fit" decline.

## Refusal Posture (Partner-Specific)

Dealix declines partnerships where:

- The partner expects to enable A3 autonomous external action.
- The partner expects to publish proof without recorded approval.
- The partner expects pricing flexibility outside the Dealix
  guardrails.
- The partner expects to bypass the eval gate.
- The partner's positioning is incompatible with the Dealix voice
  (guaranteed-outcome marketing, manufactured urgency, vanity
  metric posture).
- The partner operates in a sector on the Dealix refusal list.

A decline is delivered honestly and the rationale is logged in the
trust ledger.

## Drafting the Partner Agreement

The Partner Agreement (R7 in `DEALIX_PRODUCT_LADDER.md`) is the
foundational document. It includes:

- Scope of partner activities.
- Brand carve-out — explicitly what may carry the partner brand,
  what must carry Dealix attribution.
- Eval gate certification process for partner-side delivery teams.
- Revenue share schedule and reporting cadence.
- Trust contract acknowledgement (the partner accepts
  policy-as-code, eval gate, audit ledger).
- Termination terms covering trust violations.

The agreement passes the same approval flow as any Dealix offer
document (Brand Guardian, Trust Guardian, Finance Copilot, founder
approval).

## Co-Branded Materials

Co-branded landing pages, sector reports, and event collateral
require:

- Brand carve-out signed in the partner agreement.
- Brand Guardian eval against the Dealix brand voice and the
  partner's brand voice (where the partner has provided one).
- Trust Guardian eval against the proof-safety contract.
- Joint sign-off (both partner principal and Dealix founder).

A co-branded artefact missing any approval is not published.

## Operating Cadence with Partners

After a partner agreement is in place, Dealix and the partner run a
joint cadence:

- Monthly partner sync: pipeline state, joint artefacts, trust
  posture.
- Quarterly partner review: revenue share reporting, eval gate
  state of partner-side delivery teams, sector overlay readiness.
- Annual partner renewal: written renewal memo with rationale.

The cadence is owned by the founder on the Dealix side. The
Partner Revenue Agent (`docs/ai/` registry entry) tracks the
operational artefacts.

## Co-Introduction Workflow

For co-introduction partners (no delivery, just referrals):

1. Partner identifies a candidate buyer.
2. Partner sends a warm intro (email or LinkedIn DM, by the
   partner, not by Dealix).
3. Dealix follows up with a Diagnostic Engagement Note.
4. Engagement proceeds through the standard rungs.
5. Revenue share, if any, is tracked in
   `customer_success/referral_queue.csv` per the partner agreement.

Co-introduction without a written referral arrangement does not
trigger revenue share; the engagement is processed as a normal R1
inbound.

## Audit and Eval

The Trust Guardian audits partner engagements quarterly:

- Refusal markers present in partner-led offer documents.
- Proof publication approval state across partner-led artefacts.
- Eval gate state of partner-side agents (where they operate).
- Trust ledger entries from partner-led engagements complete.

The Performance Analyst tracks:

- Partner-led engagements by stage.
- Revenue share due vs. paid.
- Partner refusal rate (engagements Dealix or the partner declined).

## Failure Modes

- Partner publishes proof without approval. Failure: trust breach.
  Engagement pauses; the partner agreement's trust clause triggers
  a remediation step or termination.
- Partner attempts to enable A3. Failure: trust breach. Policy
  adapter denies the action; founder is notified.
- Partner discounts beyond guardrails without approval. Failure:
  pricing breach. Finance Copilot flags; revenue share is
  recalculated or withheld pending resolution.
- Partner-led engagement drifts from Dealix voice. Failure: brand
  drift. Brand Guardian flags; partner is re-onboarded.
- Partner uses competitor-bashing language about other partners or
  vendors. Failure: brand drift. Partner is reminded of the brand
  contract; persistent drift triggers termination.

## Termination

Termination of a partner agreement is documented in writing. It
covers:

- The reason (trust violation, brand drift, business decision).
- The handover of in-flight engagements.
- The treatment of revenue share owed.
- The treatment of co-branded materials post-termination.
- The retention of trust ledger entries.

Termination is delivered honestly; surprise terminations are
discouraged unless a high-severity trust breach occurred.

## Anti-Patterns

- "Resell Dealix without an agreement." Banned.
- "White-label without brand carve-out." Banned.
- "Revenue share without reporting cadence." Banned.
- "Partner discount tier that bypasses the pricing guardrails."
  Banned.
- "Partner-led campaign that uses guaranteed-outcome language."
  Banned.

## Cross-References

- Product ladder: `docs/product/DEALIX_PRODUCT_LADDER.md`.
- Offer packaging: `docs/product/OFFER_PACKAGING.md`.
- Pricing guardrails: `docs/product/PRICING_GUARDRAILS.md`.
- Trust contract: `policies/dealix_control_policy.yaml`.
- Agent registry: `registries/agent_registry.yaml`.

## Why Partners Slowly

Partner economics are misleading: the first conversation feels like
leverage, but the trust posture takes quarters to establish. Dealix
moves slowly on partners because each partner-led engagement
inherits the Dealix trust contract whether the partner asked for it
or not. A partner who violates the contract puts Dealix's
reputation at risk; a partner who honours the contract amplifies
it.

The partner channel is the longest-arc bet in the Marketing OS.
This guide is meant to keep it sober — and keep it worth running.
