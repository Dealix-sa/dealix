# Proposal Template System

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> A proposal at Dealix is the second delivery of the engagement.
> This document defines the blueprint, approval markers, and
> evidence requirements every Dealix proposal must satisfy.

A Dealix proposal is not a sales document. It is a working artefact
the buyer can use to make a decision and, after signature, to hold
Dealix to the contract. The proposal template system makes that
explicit and consistent across rungs.

## Operating Principles

- One rung, one proposal. There is no "menu" proposal that bundles
  multiple rungs without explicit founder approval.
- The proposal is generated against the same skeleton used in
  `OFFER_PACKAGING.md`, with rung-specific extensions.
- Pricing on the proposal carries `PENDING_APPROVAL` or `APPROVED`
  markers. A proposal without a marker is not a valid proposal.
- Every claim in the proposal points to evidence inside the private
  ops runtime. Unverifiable claims are stripped by the Brand
  Guardian eval before approval.

## Proposal Sections

### Section 1 — Header

- Buyer name, Dealix counterpart.
- Rung name (Sprint, Pilot, Retainer, Console, Enterprise, Partner).
- Version (`v1`, `v1.1`, …).
- Date.
- Approval state (`PENDING_APPROVAL` / `APPROVED`).
- Trust ledger reference id (added after founder approval).

### Section 2 — Why This Proposal

A short paragraph (3–6 sentences) naming the buyer's current
revenue posture in plain terms. No jargon, no adjectives. This
section answers: "Why are we writing this proposal at all?"

### Section 3 — Scope

Bulleted, specific, deterministic. Each bullet is a deliverable that
can be traced to a file in the private ops runtime.

- For Sprints: ICP sheet, account scoring model, outreach queue,
  content kit, trust posture upgrades.
- For Pilots: charter, weekly review pack, mid-point decision
  memo, close memo.
- For Retainers: monthly executive review, quarterly trust audit,
  ongoing queue maintenance.
- For Console: seat list, policy mirror, agent registry, eval gate
  acceptance.
- For Enterprise: tenant deployment, sector overlays, architecture
  decision record, audit export.
- For Partner: brand carve-out, eval gate certification, revenue
  share schedule.

"Up to" language is forbidden. Each line is a commitment or not at
all.

### Section 4 — Out of Scope

Just as important as scope. Items here are written explicitly so the
buyer cannot later assume they were included. The Out of Scope
section includes the universal refusals (no external send
automation, no proof publication without approval, no pricing
change without founder approval, no data export without escalation,
no A3) plus any engagement-specific refusals.

### Section 5 — Evidence We Will Produce

A list of artefacts written to the private ops runtime, each with a
file path and a one-line schema reference. For example:

- `sprint/<account>/icp.md` — Markdown.
- `sprint/<account>/account_scoring.csv` — columns: account_id,
  signal_weight, sector, status.
- `outreach/queue.csv` — columns: channel, target_id,
  relationship_status, draft_body, claims_flags, approval_state.

A buyer can read this section and know exactly what they will
receive and where it will live.

### Section 6 — Review and Decision Rhythm

Cadence (weekly / monthly / quarterly), participants, and decision
rights. For Pilots and Retainers, this section also names the
kill conditions.

### Section 7 — Trust Gate

Names the policy-as-code rules in force, the eval gate at start of
engagement, the suppression list contract, and the approval flow
for any artefact that could touch the outside world.

### Section 8 — Pricing

- The band from `PRICING_GUARDRAILS.md`.
- The specific quoted number.
- The instalment schedule.
- The payment terms.
- The discount (if any) with the reason code.
- The approval marker.

### Section 9 — Term, Renewal, Exit

- Start date, end date.
- Renewal logic (filed 60 days before renewal where applicable).
- Exit terms — what happens to the work, to the data, and to the
  audit ledger entries.

### Section 10 — Approval Markers

- Buyer signature block.
- Dealix founder approval marker.
- Trust ledger reference id (filled in once recorded).

## Approval Markers Reference

A proposal carries up to four approval markers, each with a state.

| Marker                         | Owner                | States                                |
|--------------------------------|----------------------|---------------------------------------|
| `pricing_approval`             | Founder              | PENDING, APPROVED, RETURNED           |
| `brand_voice_approval`         | Brand Guardian (agent + founder review) | PENDING, APPROVED, RETURNED |
| `trust_contract_approval`      | Trust Guardian (agent + founder review) | PENDING, APPROVED, RETURNED |
| `finance_pricing_audit`        | Finance Copilot      | PENDING, APPROVED, FLAGGED            |

A proposal is sent to the buyer only when all four markers are
`APPROVED`. The Founder Console enforces this.

## Evidence Requirements

A proposal section is invalid if its claims do not trace to one of:

- The Dealix product ladder (`DEALIX_PRODUCT_LADDER.md`).
- The pricing guardrails (`PRICING_GUARDRAILS.md`).
- The policy-as-code (`policies/dealix_control_policy.yaml`).
- The agent registry (`registries/agent_registry.yaml`).
- The eval gate definition (`evals/gates/dealix_agent_eval_gate.yaml`).
- An artefact that already exists in the private ops runtime.

The Brand Guardian eval flags any claim that has no traceable
evidence. The proposal cannot be approved until the flag is
resolved.

## Anti-Guarantee Rules

A proposal must not contain:

- "Guaranteed revenue", "guaranteed sales", or "guaranteed
  meetings".
- "We will deliver X by Y" where X is an outcome rather than an
  artefact.
- "Up to N%" improvement claims without a written method and
  evidence.
- Customer logos or testimonials that lack a recorded approval.
- Screenshots of identifiable buyer data, including from prior
  engagements.

The claims-safety eval scans every draft. Violations block the
proposal at the Brand Guardian approval step.

## Template Files

The proposal templates live in the private ops runtime under
`templates/proposals/` and are not stored in this repository.
Templates available:

- `sprint_scope_letter_template.md`
- `pilot_charter_template.md`
- `retainer_sla_template.md`
- `console_acceptance_template.md`
- `enterprise_master_agreement_template.md`
- `enterprise_data_processing_agreement_template.md`
- `partner_agreement_template.md`

Each template includes:

- The section skeleton above.
- The refusal-marker library inserted at the relevant points.
- Approval-marker blocks for each of the four markers.
- A placeholder block for evidence file paths.
- A version block.

## Version Control

Every proposal is versioned. A material change creates a new
version. A signed proposal is immutable; subsequent changes are
amendments. Versions are filed under
`proposals/<account>/<rung>/v<N>/` in the private ops runtime.

## Drafting Workflow

1. Sales conversation logged in the Founder Console.
2. Offer Architect generates a draft proposal from the relevant
   template, pre-populated with the conversation context.
3. Brand Guardian agent runs the claims-safety and brand-voice
   evals.
4. Trust Guardian agent confirms the refusal-marker library is
   present.
5. Finance Copilot validates the pricing block.
6. Offer Architect resolves flags and queues the proposal for
   founder review.
7. Founder approves or returns. Approval is recorded in the trust
   ledger with the proposal id and version.
8. Approved proposal is sent to the buyer by the founder (manually,
   never by an agent).
9. Buyer signature returns. The signed copy is filed under
   `proposals/<account>/<rung>/v<N>/signed/`.

## Failure Modes

- Proposal sent without all four approval markers: blocked at the
  Founder Console. The send action is denied.
- Proposal containing guaranteed-outcome wording: blocked by the
  claims-safety eval. Returned to the Offer Architect.
- Proposal containing unapproved customer reference: blocked by
  the proof-safety eval. Returned with a note.
- Proposal with pricing outside the guardrails: blocked by the
  Finance Copilot. Requires a founder rationale before re-review.
- Proposal that does not name the trust gate: returned by the
  Trust Guardian.

## Storage and Retention

- Drafts live in the private ops runtime; never in this repository.
- Signed proposals are retained per the buyer's data scope
  agreement.
- Audit ledger entries referencing the proposal are retained per
  Dealix's standard retention window unless the buyer requires a
  shorter window in a sector-specific overlay.

## Cross-References

- Offer packaging: `docs/product/OFFER_PACKAGING.md`.
- Pricing guardrails: `docs/product/PRICING_GUARDRAILS.md`.
- Sales scripts: `docs/product/SALES_SCRIPTS.md`.
- Trust contract: `policies/dealix_control_policy.yaml`.
- Agent registry: `registries/agent_registry.yaml`.

## Why Proposal Discipline Matters

Most buyers have lived through proposals that pad scope with
adjectives, hide pricing in a fine-print appendix, and avoid the
question of what the vendor will refuse to do. A Dealix proposal
flips all three: scope is deterministic, pricing is bracketed and
approval-marked, and refusal is explicit. The proposal itself is
evidence that the operating system works as advertised.
