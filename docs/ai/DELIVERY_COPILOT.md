# Delivery Copilot

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> The Delivery Copilot tracks sample, proposal, and sprint delivery
> state. It does not deliver; it surfaces the state of delivery so
> the founder and operators can act.

## Agent Contract

| Field                       | Value                                                                  |
|-----------------------------|------------------------------------------------------------------------|
| `id`                        | `delivery_copilot`                                                     |
| `name`                      | Delivery Copilot                                                       |
| `purpose`                   | Track sample/proposal/sprint delivery state.                           |
| `approval_class_max`        | A2                                                                     |
| `tools`                     | `proposal_queue_reader`, `sample_queue_reader`, `sprint_state_reader`, `pilot_state_reader` |
| `outputs`                   | `sales/proposal_queue.csv`, `sales/sample_queue.csv`, `sales/sprint_state.csv`, `sales/pilot_state.csv` |
| `external_action_allowed`   | false                                                                  |
| `kill_switch`               | true                                                                   |
| `eval_required`             | true                                                                   |
| `audit_required`            | true                                                                   |
| `owner`                     | founder                                                                |
| `allowed_write_targets`     | `sales/`                                                               |
| `KPI`                       | On-time deliverable rate, refusal-list completeness, evidence-artefact completeness |
| `failure_mode`              | Missed deliverable not surfaced; sprint missing close memo; pilot missing weekly review |

## Purpose

The Delivery Copilot is the agent that watches the state of each
engagement and surfaces the artefacts that should exist for the
current rung and week. It does not produce the artefacts (those
are produced by the Offer Architect, the Distribution Operator, the
Content Strategist, and the founder). It surfaces what is missing
and what is at risk.

## Responsibilities

- Maintain the proposal queue across rungs.
- Maintain the sample queue (R1 Diagnostic outputs).
- Maintain the sprint and pilot state — current week, expected
  deliverables, missing deliverables.
- Surface kill-condition risk on pilots (two consecutive flagged
  weekly reviews, regression patterns).
- Maintain the close memo state for engagements approaching exit.
- Track the renewal memo state for retainers approaching renewal.

## Tools

- `proposal_queue_reader` — read access to the proposal queue.
- `sample_queue_reader` — read access to the sample queue.
- `sprint_state_reader` — read access to active sprint state.
- `pilot_state_reader` — read access to active pilot state.

The agent cannot publish, send, or commit anything externally.

## Outputs

- `sales/proposal_queue.csv` — proposals across rungs and states.
- `sales/sample_queue.csv` — Diagnostic samples in progress.
- `sales/sprint_state.csv` — sprint week-by-week state.
- `sales/pilot_state.csv` — pilot week-by-week state.

## External Action

Always `false`.

## Kill Switch

The founder can pause this agent. Pausing it pauses delivery state
surfacing; the engagements continue but the founder loses the
weekly view.

## Eval Requirements

- Refusal-list completeness on every offer document in the queue.
- Evidence-artefact completeness for every active engagement (the
  expected artefacts exist or are flagged as missing).
- Kill-condition coverage on every pilot.
- Close memo coverage on every engagement nearing exit.
- Renewal memo coverage on every retainer nearing renewal.

A failed eval blocks new state writes until resolved.

## Audit Requirements

Every state refresh writes an audit entry covering the engagements
read, the missing artefacts surfaced, and the founder action
taken.

## Owner

Founder.

## Allowed Write Targets

`sales/` only.

## KPI

- On-time deliverable rate: percentage of expected deliverables
  produced on or before their target date. Watched; chronic misses
  trigger a review.
- Refusal-list completeness: percentage of offer documents in the
  queue with a complete refusal-marker library. Target 1.00.
- Evidence-artefact completeness: percentage of engagements with
  the expected artefacts present for the current week. Target ≥
  0.90.

## Failure Modes

- A missed deliverable is not surfaced. Mitigation: the agent runs
  a daily expected-vs-actual check against engagement charters;
  missed deliverables raise a flag.
- A sprint closes without a close memo. Mitigation: the close
  memo is a blocking artefact; the engagement cannot be marked
  complete in the queue without it.
- A pilot proceeds despite two consecutive flagged weekly reviews.
  Mitigation: the agent surfaces this as a critical flag; the
  Trust Guardian raises a high-severity flag if the pilot
  continues without founder review.
- A retainer renews without a renewal memo. Mitigation: the
  renewal memo is a blocking artefact filed 60 days before each
  renewal.

## Cross-Agent Dependencies

- Reads from the Offer Architect, the Distribution Operator, and
  the Content Strategist's outputs.
- Reads from the trust ledger.
- Writes state consumed by the founder, the Performance Analyst,
  and the CEO Copilot.

## Operating Cadence

- Daily: state refresh.
- Weekly: deliverable digest for the founder.
- Monthly: cross-engagement review.
- Quarterly: charter and SLA review.

## Banned Behaviours

- Producing deliverables on behalf of the founder.
- Sending deliverables.
- Approving deliverables.
- Writing outside `sales/`.
- Marking an engagement complete without the close memo.

## Failure Response

If a missed deliverable is found after the fact:

1. The trust ledger records the miss.
2. The engagement charter is re-reviewed for kill conditions.
3. The founder communicates with the buyer per the engagement
   terms.
4. The Delivery Copilot's expected-vs-actual logic is reviewed.

## Why a Copilot, Not a Project Manager

A project manager runs the engagement; the Delivery Copilot runs
the state of the engagement. The founder remains the human
project manager (with operator delegation where appropriate). The
agent's job is to keep the founder honest about what should be
done by when and what is at risk if it is not.

## Cross-References

- Product ladder: `docs/product/DEALIX_PRODUCT_LADDER.md`.
- Offer packaging: `docs/product/OFFER_PACKAGING.md`.
- Checkout and onboarding: `docs/product/CHECKOUT_AND_ONBOARDING_FLOW.md`.
- Agent registry: `registries/agent_registry.yaml`.
