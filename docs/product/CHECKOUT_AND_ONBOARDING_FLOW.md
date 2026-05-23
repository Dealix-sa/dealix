# Checkout and Onboarding Flow

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> How a buyer moves from a signed proposal to a working engagement
> for each rung of the Dealix product ladder.

Checkout at Dealix is not a "buy now" button. It is the moment the
trust contract is initialised: data scope, suppression list, eval
gate posture, kill-switch ownership, approval markers — all are
established before any operating work begins. The flow below is
deliberate and repeatable.

## Operating Principles

- No engagement begins before the proposal is signed by both parties
  and the trust ledger has recorded the engagement id.
- No external system is touched on the buyer's behalf during
  onboarding without recorded approval.
- Data scope is established before data is read. Suppression is
  reconciled before drafts are queued.
- Onboarding ends with an artefact, not a meeting.

## Universal Onboarding Stages

Every rung passes through the same five stages, with extensions for
the heavier rungs.

1. **Engagement initialisation.** Trust ledger entry created.
   Engagement id assigned. Proposal version pinned.
2. **Data scope and PDPL posture.** Buyer-side data lead identifies
   which systems Dealix may read and which Dealix may not touch.
   Retention windows agreed.
3. **Suppression and policy mirror.** Suppression list ingested.
   Tenant policy mirror (if any) configured against
   `policies/dealix_control_policy.yaml`.
4. **Agent provisioning.** Relevant Dealix agents enabled at the
   rung's approval class maximum. Kill switch ownership confirmed.
5. **First evidence loop.** A first deliverable is produced, queued,
   and approved through the standard flow.

## Rung-by-Rung Flow

### R1 — Free Sample / Diagnostic

There is no commercial checkout. The flow is:

1. Buyer requests the Diagnostic via the contact form or a founder
   introduction.
2. Diagnostic Engagement Note is sent (free) with the data scope
   clause and the refusal list.
3. Buyer returns the note acknowledged.
4. Dealix produces the Diagnostic Brief and the Scorecard within
   seven business days.
5. The Diagnostic is delivered via the founder, not via an agent.

There is no agent provisioning at this rung. The buyer's data lives
only in the artefacts the buyer has chosen to share.

### R2 — Revenue Sprint

1. Sprint Scope Letter signed by both parties. Trust ledger entry
   created. Engagement id assigned.
2. Kickoff session (45–60 minutes) covering:
   - Data scope (read scope, write scope, refusal scope).
   - Suppression list ingestion.
   - Named buyer-side approver for outreach drafts.
   - Eval gate posture confirmed green.
3. Agent provisioning: Growth Strategist, Distribution Operator,
   Content Strategist, Performance Analyst, Trust Guardian. All at
   their default approval class (A1 or A2 per registry).
4. Week 1 deliverable: ICP sheet draft. Approved by founder
   (Dealix-side) and buyer-side approver.
5. First evidence loop closes when the queue is first populated and
   the first batch of drafts is approved or returned.

### R3 — Managed Pilot

Adds to the R2 flow:

1. Pilot Charter signed by both parties. Charter pins the pilot
   slice (accounts, sectors, channels), the eval gate threshold,
   and the kill conditions.
2. Week 0 baseline: a baseline scorecard is written so weekly
   review packs can show movement.
3. Mid-point decision memo template prepared and filed in the
   engagement folder.
4. Weekly pilot review pack template prepared. The first weekly
   review happens at the end of week 1; the template is used as-is.
5. Kill-switch ownership confirmed on both sides. Either party can
   pause the pilot without a meeting; pause triggers a written
   note in the trust ledger.

### R4 — Revenue Desk Retainer

Adds to the R3 flow:

1. Retainer SLA signed. Data scope agreement signed as a separate
   artefact.
2. Onboarding sprint (2 weeks) to bring the operating loop into
   steady state, even if the buyer is coming from a Pilot.
3. Monthly executive review template configured with buyer
   participants and agenda.
4. Quarterly trust audit calendar entries created.
5. Renewal memo template filed in the engagement folder with a
   trigger 60 days before the first renewal.

### R5 — Founder Console

1. Console Acceptance signed.
2. Tenant provisioning:
   - SSO configuration if the buyer requires it.
   - Tenant policy mirror configured.
   - Tenant agent registry configured (subset of
     `registries/agent_registry.yaml`, never adding A3).
   - Tenant eval gate enabled.
   - Kill switch ownership confirmed (buyer-side; cannot be a
     vendor).
3. Seat provisioning with role-scoped permissions.
4. Walkthrough: founder-led, covering the queue, the approval
   surface, the audit ledger, the eval gate, the kill switch.
5. First evidence loop: the buyer's founder runs one approval
   end-to-end while Dealix is on the call.

### R6 — Enterprise Revenue Intelligence OS

Adds to the R5 flow:

1. Pre-onboarding security review complete and signed off.
2. Master Agreement, Data Processing Agreement, and any
   sector-specific addenda signed.
3. Tenant deployment with documented architecture decision record
   per tenant.
4. Sector overlay enablement, one at a time, each gated by a
   capability review.
5. First quarterly enterprise readiness review scheduled, with the
   buyer's security, data, and compliance leads invited.

### R7 — Partner / White-label Revenue OS

1. Partner Agreement signed with brand carve-out.
2. Eval gate certification of partner-side agents. A partner agent
   that does not pass the certification cannot operate on a buyer.
3. Joint onboarding playbook prepared, documenting where the
   partner brand is used and where Dealix attribution is required.
4. First joint engagement scoped and documented as the reference
   pattern for future partner-led engagements.
5. Revenue share reporting cadence agreed and configured.

## Trust Ledger Entries

Every onboarding stage writes a trust ledger entry with the
following fields:

- `engagement_id`
- `rung`
- `stage`
- `actor` (founder, agent id, buyer-side participant)
- `timestamp`
- `artefact_path` (where the artefact lives in the private ops
  runtime)
- `policy_refs` (rules in force at the time)

Trust ledger entries are not editable. Corrections are appended as
new entries that reference the prior entry.

## Approval Markers in Onboarding

In addition to the proposal's four approval markers, onboarding
adds three more:

| Marker                       | Owner                  | States                   |
|------------------------------|------------------------|--------------------------|
| `data_scope_approval`        | Buyer-side data lead   | PENDING, APPROVED        |
| `suppression_reconciliation` | Trust Guardian         | PENDING, COMPLETE        |
| `kill_switch_acceptance`     | Buyer-side approver    | PENDING, ACCEPTED        |

No agent at any rung is allowed to read buyer data, draft a buyer
artefact, or queue an outreach attempt until all three markers are
in their terminal state for that engagement.

## Onboarding Artefacts

Each rung produces a named onboarding artefact at the end of stage 5:

- R1 — Diagnostic Brief.
- R2 — Week 1 ICP sheet plus an inaugural Distribution queue with
  approved drafts.
- R3 — Pilot Charter plus week 0 baseline scorecard.
- R4 — First monthly executive review pack.
- R5 — Console acceptance memo plus the first end-to-end approval
  run by the buyer's founder.
- R6 — Tenant deployment record plus the first sector overlay
  acceptance.
- R7 — Partner playbook plus the first joint engagement record.

Onboarding ends with an artefact, not with a "we are live" note.

## Common Onboarding Failure Modes

- Data scope not written. Onboarding pauses; no agent reads buyer
  data until the scope is signed.
- Suppression list not provided. Onboarding pauses; no outreach
  queue is populated.
- Kill switch ownership ambiguous. Onboarding pauses; the buyer
  must name an owner.
- Eval gate misconfigured. Onboarding pauses; Eval Guardian agent
  blocks operating work.
- Approval markers missing on the proposal version that triggered
  the engagement. The engagement id is not assigned; onboarding
  cannot start.

## Offboarding (Mentioned Here for Symmetry)

Offboarding mirrors onboarding:

- Final close memo filed.
- Data handed back per the data scope agreement.
- Agents disabled at the rung's tenant scope.
- Trust ledger entries retained per the agreed window.
- Renewal posture recorded.

The engagement is not "ended" verbally. It ends when the close memo
is filed and the trust ledger entry is written.

## Localisation

For Saudi buyers, the onboarding flow honours PDPL by default. Data
residency, retention, and sub-processor disclosure are part of the
data scope conversation, not an afterthought. For GCC buyers in
sector-regulated environments (financial services, healthcare,
public sector readiness), sector overlays are enabled one at a
time, each with its own capability review.

## Cross-References

- Product ladder: `docs/product/DEALIX_PRODUCT_LADDER.md`.
- Offer packaging: `docs/product/OFFER_PACKAGING.md`.
- Pricing guardrails: `docs/product/PRICING_GUARDRAILS.md`.
- Proposal template: `docs/product/PROPOSAL_TEMPLATE_SYSTEM.md`.
- Trust contract: `policies/dealix_control_policy.yaml`.

## Why Onboarding Discipline Matters

Most B2B engagements lose momentum in the first three weeks because
the trust contract is implicit and the operating loop is improvised.
Dealix makes both explicit before any agent does any work. The
onboarding flow is, in itself, evidence that the operating system
will hold under load.
