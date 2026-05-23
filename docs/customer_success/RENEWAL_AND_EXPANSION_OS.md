# Renewal and Expansion OS

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Closing Deals · Driven by Growth.

The Renewal and Expansion OS is the discipline by which Dealix
keeps customers and grows them. Renewals open 90 days before the
contract end. Expansions follow the offer ladder. Both motions are
policy-gated; pricing and contract changes require founder approval.

## Scope

| Motion       | Definition                                                                       |
| ------------ | -------------------------------------------------------------------------------- |
| Renewal      | Extending an existing scope at term end, same or adjusted pricing.                |
| Expansion    | Adding scope, rungs, or seats to an existing contract.                            |
| Cross-sell   | Selling a different offer ladder rung to the same customer.                        |
| Downgrade    | Reducing scope at the customer's request; documented and approved.                |
| Churn save   | A targeted save action when health is red/at_risk.                                 |

The same approval discipline applies to every motion. Pricing
changes always require founder approval. Contract changes always
require escalation.

## Source files

| File                                  | Purpose                                                  |
| ------------------------------------- | -------------------------------------------------------- |
| `customer_success/client_health.csv`   | Drives the timing for the motion.                        |
| `sales/proposal_queue.csv`             | Renewals and expansions land as new proposal rows.        |
| `product/offer_ladder.csv`             | Defines the expansion path.                              |
| `product/productization_candidates.csv` | Tracks new rung candidates.                              |

## Founder Console endpoints

| Endpoint                                  | What it shows                                                |
| ----------------------------------------- | ------------------------------------------------------------ |
| `GET /customer-success/summary`           | Active clients, at-risk count, open referrals.              |
| `GET /retention/queue`                    | Per-client health and next action.                          |
| `GET /product/productization`              | Candidates that could become expansion offers.              |

## Renewal calendar

| Days before term end | Action                                                                         |
| -------------------- | ------------------------------------------------------------------------------ |
| T-90                  | Renewal motion opens. CS lead drafts the renewal frame.                        |
| T-60                  | Internal review with founder. Pricing decision finalized.                      |
| T-45                  | Renewal proposal drafted; queued for founder approval.                          |
| T-30                  | Renewal sent (after approval). Customer review window opens.                    |
| T-14                  | Reminder + clarification window.                                                |
| T-0                   | Renewal effective or contract ends.                                            |

## Pricing posture

- The default posture is "renewal at current price" unless an
  explicit experiment, expansion, or downgrade is in play.
- Price increases require evidence: documented outcomes, scope
  changes, or market posture. The evidence is attached to the
  approval row.
- Price reductions require founder approval; the customer reason is
  recorded.

A pricing change is a `pricing_commit` policy action and is
gated by `pricing_commit_requires_approval`.

## Expansion path

Expansion follows the offer ladder
(`product/offer_ladder.csv`). The Offer Architect maintains the
ladder; the Customer Success function reads it. Examples:

| Current rung   | Next rung                                          |
| -------------- | -------------------------------------------------- |
| Sample sprint   | Retainer rung A (foundational)                     |
| Retainer A      | Retainer B (deeper scope, more sectors)            |
| Retainer B      | Retainer C (multi-team, multi-sector)              |
| Any retainer    | Productized add-on (specific sample variant)        |

Cross-sell may move a customer laterally between rungs in a
different domain.

## Expansion triggers

| Trigger                                              | Action                                                                  |
| ---------------------------------------------------- | ----------------------------------------------------------------------- |
| Outcome landing on plan; client_health green for 60d  | Open expansion conversation.                                            |
| Client requests additional scope                      | Scope the request; draft the expansion proposal.                       |
| New rung released that fits the client's profile      | Surface the rung; do not push.                                          |
| Productization candidate ready                         | Offer as a pilot rung.                                                  |

Expansions are not auto-suggested in customer messages by agents;
they are surfaced internally first and then deliberately opened.

## Downgrade

Downgrades occur when:

| Situation                                          | Path                                                                   |
| -------------------------------------------------- | ---------------------------------------------------------------------- |
| Customer requests reduced scope                     | Document scope; draft a downgrade proposal; founder approves.          |
| Customer budget reduction                           | Same path; preserve the relationship for re-expansion.                 |
| Sample sprint completes; customer not ready for retainer | Lateral move to a smaller productized engagement.                  |

A downgrade is a contract change and is gated by
`contract_change_requires_escalation`.

## Churn save

When `client_health` is `at_risk`:

1. The Customer Success owner drafts a save plan within 5 business
   days.
2. The plan is reviewed by the founder.
3. If a contract change is part of the save (price reduction,
   payment-term change, scope reduction), policy gates apply.
4. The Incident Response Agent opens an incident if there is a
   contractual or operational risk.

The save plan, like all customer-facing actions, requires founder
approval before any external communication.

## Audit events

| Event                          | Action                              | Risk       |
| ------------------------------ | ----------------------------------- | ---------- |
| Renewal proposal sent          | `proposal_send`                     | medium     |
| Pricing change agreed          | `pricing_commit`                     | critical   |
| Contract amendment recorded    | `contract_change`                    | high       |
| Payment-term change agreed     | `payment_terms_change`               | high       |
| Refund issued                  | `refund_commit`                      | critical   |
| Save plan executed             | `risk_accept`                        | high       |

## Anti-patterns

| Anti-pattern                                            | Why                                                                |
| ------------------------------------------------------- | ------------------------------------------------------------------ |
| Auto-renewing without a review                          | Misses the chance to expand and recheck fit.                       |
| Discounting to retain                                   | Erodes the offer ladder; alternative paths first.                  |
| Renegotiating during a delivery crisis                  | Fix the crisis first; renegotiate from a stable posture.            |
| Adding scope without recording a contract change         | Drift erodes margin and accountability.                            |
| Treating expansion as upsell pressure                   | Customer-led expansion only; we surface, we do not push.            |

## Cadence

| Activity                       | Cadence                                              |
| ------------------------------ | ---------------------------------------------------- |
| Renewal calendar review         | Weekly. Look at T-90 to T-0 horizons.                |
| Expansion candidate review      | Monthly.                                             |
| Save plan triage                | Weekly when red/at_risk count > 0.                   |
| Offer ladder review             | Quarterly with Offer Architect and founder.          |

## What this OS will not do

- Auto-extend a contract.
- Auto-discount to win a renewal.
- Push expansion to a yellow or red customer.
- Discuss pricing externally without founder approval.

## Discipline

1. Renewals open 90 days early.
2. Expansion follows the ladder.
3. Downgrades are documented, not hidden.
4. Save plans are founder-led.
5. Every motion produces an audit row.

## Cross-references

- `CUSTOMER_SUCCESS_OS.md` for the overall discipline.
- `CLIENT_HEALTH_SCORE_SYSTEM.md` for trigger thresholds.
- `REVENUE_RECOGNITION_NOTES.md` for accounting impact.
- `docs/product/...` for the offer ladder catalog.
