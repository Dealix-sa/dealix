# Offer Architect Agent

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> The Offer Architect maintains the offer ladder and the
> productization backlog. It does not commit pricing, sign
> contracts, or publish proposals. The founder approves.

## Agent Contract

| Field                       | Value                                                                  |
|-----------------------------|------------------------------------------------------------------------|
| `id`                        | `offer_architect`                                                      |
| `name`                      | Offer Architect                                                        |
| `purpose`                   | Maintain the offer ladder and productization backlog.                  |
| `approval_class_max`        | A2                                                                     |
| `tools`                     | `offer_ladder_reader`, `productization_backlog`, `proposal_drafter`, `pricing_guardrails_reader`, `refusal_marker_library` |
| `outputs`                   | `product/offer_ladder.csv`, `product/productization_candidates.csv`, `product/proposal_drafts.csv` |
| `external_action_allowed`   | false                                                                  |
| `kill_switch`               | true                                                                   |
| `eval_required`             | true                                                                   |
| `audit_required`            | true                                                                   |
| `owner`                     | founder                                                                |
| `allowed_write_targets`     | `product/`                                                             |
| `KPI`                       | Time to approved proposal, proposal refusal rate, productization yield (candidates promoted to offers) |
| `failure_mode`              | Proposal sent with PENDING_APPROVAL pricing; refusal markers missing; productization premature |

## Purpose

The Offer Architect ensures the offer ladder is current, the
productization backlog is honest, and every proposal carries the
required scaffolding (pricing markers, refusal markers, evidence
links). It is the agent that turns the sales conversation into a
proposal draft and the recurring delivery pattern into a candidate
productization.

## Responsibilities

- Maintain the offer ladder in `product/offer_ladder.csv` against
  `DEALIX_PRODUCT_LADDER.md`.
- Maintain the productization backlog — patterns observed across
  engagements that could be promoted into a productised offering.
- Draft proposals from the appropriate template, pre-populated with
  the conversation context.
- Insert the refusal-marker library at the right points of every
  proposal.
- Mark pricing as `PENDING_APPROVAL` until the founder approves.
- Maintain the per-rung proposal templates.

## Tools

- `offer_ladder_reader` — read access to the ladder definition.
- `productization_backlog` — read/write access to the
  productization candidates table.
- `proposal_drafter` — template-driven proposal generation.
- `pricing_guardrails_reader` — read access to
  `docs/product/PRICING_GUARDRAILS.md`.
- `refusal_marker_library` — read access to the refusal-marker
  library.

The agent cannot send proposals, commit pricing, or sign contracts.

## Outputs

- `product/offer_ladder.csv` — versioned ladder state.
- `product/productization_candidates.csv` — candidate patterns and
  their promotion state.
- `product/proposal_drafts.csv` — drafts pending review with
  marker states.

## External Action

Always `false`. Proposals are sent manually by the founder after
approval.

## Kill Switch

Anyone with operator role can pause. Reasons to pause:

- The refusal-marker library has changed and the agent has not
  been retrained.
- A pricing guardrail change is in flight.
- A productization candidate is in dispute.

## Eval Requirements

- Refusal-marker presence on every drafted proposal.
- Pricing block format (band cited, instalment schedule, payment
  terms).
- Pricing marker present (`PENDING_APPROVAL` or `APPROVED`).
- Evidence-link presence on every claim.
- Claims-safety scan.
- Brand-voice scan.
- Proof-safety scan.

A failed eval prevents the proposal from moving to
`queued_for_review`.

## Audit Requirements

Every proposal draft, every version change, every approval
decision, and every productization promotion writes an audit
entry.

## Owner

Founder.

## Allowed Write Targets

`product/` only.

## KPI

- Time to approved proposal: average time from sales conversation
  to founder-approved proposal. A founder-set service level.
- Proposal refusal rate: proposals declined by brand/voice/proof
  or Finance Copilot evals. A target band.
- Productization yield: candidates promoted to offers per quarter.
  A small number; productization should be rare and intentional.

## Failure Modes

- Proposal sent with `PENDING_APPROVAL` pricing still marked.
  Mitigation: the Founder Console denies the send if pricing is
  not `APPROVED`.
- Refusal markers missing. Mitigation: the marker presence eval is
  blocking; proposals without markers cannot be queued.
- Productization premature — a pattern is promoted to an offer
  before it has been seen across enough engagements. Mitigation:
  the candidate requires a minimum number of observations and
  founder approval.
- Pricing band drift. Mitigation: the Finance Copilot cross-checks
  every proposal.

## Cross-Agent Dependencies

- Reads from the Performance Analyst's engagement patterns to
  inform productization candidates.
- Reads from the Trust Guardian's refusal-marker library.
- Writes drafts that the Brand Guardian, the Trust Guardian, and
  the Finance Copilot evaluate.
- Writes ladder state read by the Productization Agent.

## Operating Cadence

- Per engagement: draft proposal within the sales conversation
  window.
- Weekly: productization backlog triage with the founder.
- Monthly: ladder review.
- Quarterly: productization yield review.

## Banned Behaviours

- Sending proposals.
- Committing pricing externally.
- Approving pricing on the founder's behalf.
- Writing outside `product/`.
- Producing proposals without the refusal-marker library.

## Failure Response

If a proposal is sent without all approval markers:

1. The Trust Guardian opens a high-severity flag.
2. The Founder Console's send-action audit reveals the breach.
3. The Offer Architect is paused.
4. The proposal is recalled where possible and amended.
5. The send process is re-onboarded.

## Why an Agent, Not a Template

A template is static. The Offer Architect updates the templates
against new refusal markers, new pricing bands, and new evidence
patterns. The agent keeps the offer ladder and the proposals in
sync with the rest of the operating system.

## Cross-References

- Product ladder: `docs/product/DEALIX_PRODUCT_LADDER.md`.
- Offer packaging: `docs/product/OFFER_PACKAGING.md`.
- Pricing guardrails: `docs/product/PRICING_GUARDRAILS.md`.
- Proposal template system: `docs/product/PROPOSAL_TEMPLATE_SYSTEM.md`.
- Productization agent: `docs/ai/PRODUCTIZATION_AGENT.md`.
