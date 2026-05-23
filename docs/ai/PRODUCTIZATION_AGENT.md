# Productization Agent

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> The Productization Agent promotes repeated client work into
> productised offerings. It does not commit to a new offer; it
> surfaces candidates for founder approval.

## Agent Contract

| Field                       | Value                                                                  |
|-----------------------------|------------------------------------------------------------------------|
| `id`                        | `productization_agent`                                                 |
| `name`                      | Productization Agent                                                   |
| `purpose`                   | Promote repeated client work into offers.                              |
| `approval_class_max`        | A2                                                                     |
| `tools`                     | `productization_backlog`, `pattern_detector`, `evidence_aggregator`    |
| `outputs`                   | `product/productization_candidates.csv`, `product/productization_audit.csv` |
| `external_action_allowed`   | false                                                                  |
| `kill_switch`               | true                                                                   |
| `eval_required`             | true                                                                   |
| `audit_required`            | true                                                                   |
| `owner`                     | founder                                                                |
| `allowed_write_targets`     | `product/`                                                             |
| `KPI`                       | Candidate quality (founder approval rate), promotion yield (candidates promoted to offers), false positive rate |
| `failure_mode`              | Promoting a pattern observed in too few engagements; promoting a pattern that depends on customer-specific context |

## Purpose

The Productization Agent watches the engagement portfolio for
patterns that recur across multiple buyers. When a pattern crosses
defensibility thresholds (minimum engagement count, sector
breadth, evidence quality), the agent surfaces it as a candidate
for promotion into a new offer or a new feature within an existing
rung. The founder reviews and decides.

## Responsibilities

- Detect recurring deliverable patterns across active and closed
  engagements.
- Detect recurring buyer questions that suggest a missing offer.
- Detect recurring refusals that suggest the offer ladder needs a
  new refusal marker.
- Maintain the productization candidates table with state
  (`observing`, `candidate`, `under_review`, `promoted`,
  `declined`).
- Track promotion yield — candidates that become offers and the
  outcomes of those offers.

## Tools

- `productization_backlog` — read/write to candidate state.
- `pattern_detector` — pattern detection across engagement
  artefacts.
- `evidence_aggregator` — aggregates anonymised evidence to support
  candidate proposals.

The agent cannot draft offer documents (the Offer Architect does
that) or commit pricing.

## Outputs

- `product/productization_candidates.csv` — current candidate
  state.
- `product/productization_audit.csv` — promotion decisions and
  outcomes.

## External Action

Always `false`.

## Kill Switch

The founder can pause this agent. Pausing it pauses promotion
candidates from advancing; new patterns can still be observed.

## Eval Requirements

- Minimum engagement count per candidate (defaults: 3 engagements
  for a feature, 5 engagements for a new offer).
- Sector breadth per candidate (at least 2 sectors before
  promotion).
- Evidence aggregation honesty (no aggregation that creates a
  false signal).
- No customer-specific context leakage in candidate descriptions.
- Refusal-marker presence on any new offer candidate.

A failed eval prevents the candidate from advancing.

## Audit Requirements

Every candidate state change writes an audit entry covering the
underlying engagements (anonymised), the evidence, and the
founder action.

## Owner

Founder.

## Allowed Write Targets

`product/` only.

## KPI

- Candidate quality: founder approval rate on candidates advanced
  to `under_review`. Watched; low rate suggests the detector is
  surfacing noise.
- Promotion yield: candidates promoted to offers per quarter.
  Target: small number. Productization should be rare and
  intentional.
- False positive rate: candidates surfaced but later declined.
  Target band; high rate indicates the threshold is too low.

## Failure Modes

- Promoting a pattern observed in too few engagements. Mitigation:
  the minimum engagement count is enforced as a blocking eval.
- Promoting a pattern that depends on customer-specific context.
  Mitigation: the evidence aggregator runs an anonymisation check;
  patterns that cannot be anonymised cannot be promoted.
- Promoting too quickly, producing a thin offer. Mitigation: the
  founder review is required and the promotion is staged
  (observing → candidate → under_review → promoted).
- Missing a real pattern because it does not match the detector's
  templates. Mitigation: the founder can manually add a candidate;
  the detector is reviewed quarterly.

## Cross-Agent Dependencies

- Reads anonymised patterns from the Delivery Copilot and the
  Performance Analyst.
- Reads refusal logs from the Trust Guardian.
- Writes candidates consumed by the Offer Architect.
- Writes promotion outcomes consumed by the founder and the
  Performance Analyst.

## Operating Cadence

- Weekly: pattern detection run; candidates updated.
- Monthly: founder triage of candidates at `candidate` state.
- Quarterly: promotion review with the founder and the Offer
  Architect.

## Banned Behaviours

- Drafting offer documents.
- Committing pricing.
- Adding an offer to the ladder without founder approval.
- Writing outside `product/`.
- Aggregating identifiable customer detail.

## Failure Response

If a candidate is promoted and the resulting offer fails to attract
buyers:

1. The failure is recorded in the productization audit.
2. The offer is retired with a written rationale.
3. The productization detector's threshold is reviewed.
4. The next promotion cycle starts only after the review is
   complete.

## Why Productization Slowly

Premature productization is one of the most common ways a
services business loses its margin and its trust posture. The
Productization Agent moves slowly on purpose: more observation,
more evidence, more refusals. The founder is the gate that turns
observation into offer.

## Cross-References

- Product ladder: `docs/product/DEALIX_PRODUCT_LADDER.md`.
- Offer architect: `docs/ai/OFFER_ARCHITECT_AGENT.md`.
- Performance analyst: `docs/ai/PERFORMANCE_ANALYST_AGENT.md`.
- Trust guardian: `docs/ai/TRUST_GUARDIAN_AGENT.md`.
- Agent registry: `registries/agent_registry.yaml`.
