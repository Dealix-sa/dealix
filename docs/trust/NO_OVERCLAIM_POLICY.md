# No-Overclaim Policy

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

Dealix does not guarantee revenue, sales, or meetings. We do not make
absolute conversion claims. We do not state outcomes that are not
already documented in an approved proof asset. This document is the
authoritative phrasing reference for every agent that produces
external-facing text.

The rules below are enforced at three layers:

1. The eval gate suite `no_guaranteed_claims` (see
   `evals/gates/dealix_agent_eval_gate.yaml`).
2. The policy rule `no_guaranteed_revenue_claims` (see
   `policies/dealix_control_policy.yaml`).
3. The Brand Guardian agent, which is the owner of brand voice and
   the gatekeeper for phrasing reviews.

## The core promise

The promise Dealix makes externally is operational, not
outcome-based. We commit to a method (intelligent deals, deliberate
distribution, audited approvals) and to a level of effort (sprint
delivery, daily founder review). We never commit to a result we have
not already produced and recorded.

## Banned constructions

The following phrases are banned across drafts (outreach, proposals,
marketing copy, samples, public posts). The Brand Guardian regex
patterns and the eval gate cover the common forms; this list is the
canonical human-readable reference.

### Guaranteed outcomes

| Banned                                | Replacement direction                                                |
| ------------------------------------- | -------------------------------------------------------------------- |
| guaranteed revenue                    | the discipline that has produced revenue for clients like X          |
| guaranteed sales                      | a structured sales motion designed for your sector                   |
| guaranteed meetings                   | a tested outreach motion that has produced meetings in your sector   |
| we promise X                          | we commit to the method; X is the outcome we are working toward      |
| we will deliver X by Y                | we will run the sprint and review outcomes weekly                    |
| ensure conversions                    | improve conversion discipline                                        |

### Absolute statistics

| Banned                                | Replacement direction                                                |
| ------------------------------------- | -------------------------------------------------------------------- |
| 100% conversions                      | high conversion in this audited pilot                                |
| 100% results                          | the outcomes for this engagement are listed in the proof pack        |
| zero churn                            | no churn observed in the proof window of N months                    |
| zero failures                         | no failures recorded in the audited period                           |
| always succeeds                       | the pattern that has succeeded in N of N audited engagements         |

### Pricing and contract

| Banned                                | Replacement direction                                                |
| ------------------------------------- | -------------------------------------------------------------------- |
| flat price                            | the rung price is X SAR; final price subject to scoping              |
| lifetime guarantee                    | a renewal motion reviewed annually                                   |
| money-back guarantee                  | a sample sprint with a defined outcome; refunds follow the SOP       |
| unlimited X                           | a defined scope of X; expansion follows the offer ladder             |

Any pricing or refund language must additionally pass the
`pricing_safety` and `proposal_safety` eval suites and the
`pricing_commit_requires_approval` policy rule.

## Allowed phrasing patterns

Approved alternatives express commitment to a method without
asserting an outcome. Examples:

- "We run a defined sample sprint, recorded in the proof pack, and
  review outcomes weekly."
- "Clients in [sector] who completed the sprint have, in audited
  cases, achieved [specific outcome with link to proof asset]."
- "We commit to a structured outreach motion, a weekly review, and
  to escalating blockers to the founder within 24 hours."
- "The offer is priced at [X SAR] for the defined scope; any
  expansion is scoped separately."

These constructions clear the eval gate, clear the policy rule, and
are aligned with the Brand Guardian voice profile.

## Approved vs disallowed examples

| Context              | Disallowed                                                  | Approved                                                                       |
| -------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Outreach hook        | "We guarantee 10 qualified meetings in 30 days."            | "We run a sample sprint and review meeting yield weekly with you."             |
| Proposal benefit     | "100% lead-to-pipeline conversion."                          | "Audited pilots have shown high lead-to-pipeline conversion (see proof pack)." |
| Pricing slide        | "Lifetime guarantee, no refunds needed."                    | "Sample sprint pricing is X SAR. Expansion follows the offer ladder."          |
| Marketing post       | "Dealix promises real revenue for every client."            | "Dealix builds the revenue operating system. Real growth is the work."         |
| Sales close          | "Sign today and we promise sales in 7 days."                | "Sign today and we begin the sample sprint within 48 hours."                   |
| Customer case study  | "Client X tripled revenue thanks to Dealix."                | "Client X reports tripled pipeline over 6 months; see proof asset id 1247."    |
| LinkedIn DM          | "We deliver guaranteed leads."                              | "We are running a sector sprint in [sector]; would a 15-minute look help?"     |
| Reply to objection   | "We will ensure conversions."                               | "We will run the sprint, review outcomes weekly, and adjust the motion."       |

## Quoting numbers

A number that appears in any draft must trace to one of three
sources: the proof library (`proof/proof_library.csv` with
`approval_state: approved`), the founder's own statement, or a public
third-party citation. Each draft that includes a number must carry an
evidence reference. The eval gate suite `evidence_required` enforces
this for high-risk approvals; the Brand Guardian extends the check to
medium-risk drafts.

## Owners and escalation

- The Brand Guardian agent (`brand_guardian` in
  `registries/agent_registry.yaml`) is the owner of voice and
  phrasing.
- The Content Strategist drafts; the Brand Guardian reviews.
- The Trust Guardian raises a flag on any disallowed phrasing that
  reaches the queue.
- The founder is the final approver. The founder may approve a
  specific phrasing exception in writing in the audit ledger; the
  exception applies only to the specific draft id and is not a policy
  change.

## Why this matters

Saudi B2B trust is hard-won. Overclaim is the fastest path to losing
it. The brand promises a method; the method is documented; the
results are documented; nothing else is said externally. This is the
single biggest leverage point we have against eroding trust at scale.
