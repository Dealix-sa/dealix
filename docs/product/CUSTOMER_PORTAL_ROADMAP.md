# Customer Portal Roadmap

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> A roadmap for the customer-facing Dealix portal. This document is
> a roadmap, not a promise. Items here are subject to founder
> approval, capability evaluation, and trust review.

The Customer Portal is a planned surface that lets buyers see, in
their own browser, the state of their Dealix engagement — queues,
approvals, evidence, trust ledger entries. It is the buyer-facing
mirror of the Founder Console. The portal does not exist today; this
document maps how it might come into existence.

## Operating Principles

- A buyer-facing surface must enforce the same trust contract as the
  internal Founder Console. No external send, no proof publication,
  no pricing change, no data export bypasses the policy adapter.
- The portal is read-mostly. Write paths are limited to approvals
  the buyer has explicit authority over (e.g. approving an outreach
  draft for their own domain).
- The portal does not replace the founder. It supplements the
  founder. A buyer can use the portal to see state, but commercial
  commitments still pass through the founder.
- Roadmap items are not commitments. They are candidate scopes that
  must pass founder approval and capability evaluation before they
  are built.

## Why a Portal at All

Three reasons:

- Buyers on heavier rungs (R4, R5, R6) need a self-serve surface to
  see their engagement state without scheduling a meeting.
- A portal makes the trust contract visible. A buyer who can see
  their suppression list, their approvals, and their audit ledger
  has tangible evidence that the operating system works.
- A portal removes ambiguity. "Where is my draft? Did you send
  anything?" becomes a one-click answer.

## What a Portal Is Not

- It is not a CRM. Buyers' own CRMs remain the source of truth for
  their pipeline.
- It is not a marketing automation platform.
- It is not a generic AI assistant.
- It is not a substitute for the proposal, the contract, or the
  trust ledger.

## Roadmap Horizons

The roadmap is staged across three horizons: H0 (today, no portal),
H1 (read-only portal, R4+ tenants), H2 (approval-write portal, R5+
tenants), H3 (multi-BU portal, R6 tenants). Each horizon names the
capability, the trust requirement, and the open questions.

### H0 — Today (No Portal)

State: there is no buyer-facing portal. Buyers receive evidence
through artefacts in the private ops runtime, exported on a defined
cadence (weekly, monthly, quarterly depending on rung).

This horizon stays in place until the H1 trust review is complete.

### H1 — Read-Only Portal (Candidate Scope)

A web surface where the buyer's named approvers can see:

- Engagement metadata: rung, version, start date, term.
- Active agents and their approval class.
- Queue state: draft counts by channel, approval state, suppression
  conflicts.
- Trust ledger entries scoped to the buyer's engagement.
- Eval gate state.

No writes. No buttons that do anything. The portal in H1 is purely
informational.

Trust requirements before H1 ships:

- Tenant isolation is bulletproof and externally audited.
- Identity and access are tied to the buyer's SSO where available;
  otherwise to a hardened identity provider.
- The portal cannot expose another tenant's data under any failure
  mode.
- The portal's data export functionality is bounded and gated.
- PDPL posture is reviewed and signed off.

Open questions:

- Which evidence views are most valuable to a buyer at R4? R5? R6?
- How is the portal localised (Arabic, English)?
- How does the portal handle partner-led engagements at R7?

### H2 — Approval-Write Portal (Candidate Scope)

Adds, on top of H1:

- A buyer-side approver can approve or return an outreach draft
  that targets their domain, with full visibility of `claims_flags`,
  `brand_voice_flags`, suppression conflicts, and evidence links.
- A buyer-side approver can pause an agent that operates on their
  account (kill switch).
- A buyer can acknowledge a trust ledger entry (e.g. quarterly
  trust audit accepted).

The write surface is bounded to approvals the buyer has authority
over by contract. The portal does not let a buyer change pricing,
change the proposal, or change the scope.

Trust requirements before H2 ships:

- The Trust Guardian and Brand Guardian evals run against any
  approval the portal exposes.
- Every approval action writes to the trust ledger and is
  attributable to the named buyer-side approver.
- The portal cannot bypass the policy adapter.
- An approval through the portal carries the same weight, and
  the same audit trail, as an approval through the Founder
  Console.

Open questions:

- What is the precise approval delegation model for an R5 tenant
  with multiple operators?
- How is dispute resolution handled when a buyer-side approver and
  Dealix disagree on a draft?

### H3 — Multi-BU Portal (Candidate Scope)

Adds, on top of H2:

- BU-level isolation within a single buyer tenant. A buyer with
  multiple revenue-bearing BUs can scope each BU's data, approvers,
  and policy mirror.
- Sector overlay visibility. A buyer can see which overlays are
  enabled and the capability evidence for each.
- Audit export tooling. A buyer can request and download an audit
  bundle, gated by the policy adapter.

Trust requirements before H3 ships:

- Enterprise security review is complete for multi-BU isolation.
- Audit export tooling cannot be triggered without an escalation
  recorded under `data_export_requires_escalation`.
- Sector overlay capability evidence is bound to the overlay UI;
  there is no overlay surfaced without evidence.

Open questions:

- Federation across multiple Dealix tenants for partner-led
  engagements at R7.
- Long-term audit retention beyond the buyer's default retention
  window.

## Capabilities Required to Reach Each Horizon

| Capability                          | H1 | H2 | H3 |
|-------------------------------------|----|----|----|
| Tenant isolation                    | required | required | required |
| SSO support                         | recommended | required | required |
| Trust ledger visibility             | required | required | required |
| Eval gate visibility                | recommended | required | required |
| Approval write paths                | not present | required | required |
| Multi-BU scoping                    | not present | not present | required |
| Sector overlay visibility           | not present | not present | required |
| Audit export                        | not present | recommended | required |
| Arabic + English localisation       | recommended | required | required |
| PDPL posture documented per tenant  | required | required | required |

## Roadmap Anti-Patterns to Avoid

- A portal that shows raw data without governance. The portal must
  display the trust state alongside the data state.
- A portal whose approvals bypass the policy adapter. There is no
  fast path through the trust contract.
- A portal that surfaces guaranteed-outcome wording in any view.
  The claims-safety eval applies to portal views as well.
- A portal that lets a buyer enable A3. A3 is banned at every
  horizon.
- A portal whose audit export is unbounded. Exports are gated and
  logged.
- A portal that diverges from the Founder Console without a
  documented reason. Divergence creates a maintenance burden and
  invites trust drift.

## How Buyers See the Roadmap

The roadmap is shared with buyers on R4+ engagements as an honest
horizon plan. Buyers are told:

- "The portal does not exist today. We will tell you when we ship
  H1, and we will not promise H2 or H3 until they are scoped and
  approved."
- "Until then, your engagement state lives in our private ops
  runtime, and you receive evidence on the cadence stated in your
  SLA."

This is the same posture Dealix takes on every other commitment:
no promise without evidence.

## Decision Forum

The portal roadmap is reviewed quarterly in a portal decision
forum. Participants: founder, Trust Guardian (agent + human),
Security Guardian (agent + human), Performance Analyst. Output:

- One of {advance horizon, hold horizon, retire horizon item}.
- A written rationale recorded in `product/portal_review.md`.
- An update to this document.

## Cross-References

- Founder Console pages: `apps/web/`.
- Trust contract: `policies/dealix_control_policy.yaml`.
- Agent registry: `registries/agent_registry.yaml`.
- Product ladder: `docs/product/DEALIX_PRODUCT_LADDER.md`.

## Why a Roadmap, Not a Commitment

Roadmaps are public, commitments are private. The portal roadmap
exists so buyers, partners, and operators understand the direction.
The commitments — what Dealix will ship and when — emerge from the
decision forum and are recorded in the proposal and the trust
ledger, not on the marketing site.

The portal is a long-arc bet that buyer-facing trust visibility is
worth building. Dealix takes that bet seriously, which is why this
document is sober rather than aspirational.
