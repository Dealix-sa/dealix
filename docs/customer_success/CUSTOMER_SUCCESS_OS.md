# Customer Success OS

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Closing Deals · Built on Trust.

The Customer Success OS is how Dealix turns a won deal into a
durable, expanding, reference-worthy customer relationship. It is
not a single role or a single dashboard. It is a discipline that
runs from contract signing through renewal, with health scoring,
referrals, and expansion as first-class artifacts.

## Scope

| Concern                              | Owner                                                          |
| ------------------------------------ | -------------------------------------------------------------- |
| Onboarding                            | Delivery Copilot + Customer Success.                            |
| Health scoring                        | Customer Success (see `CLIENT_HEALTH_SCORE_SYSTEM.md`).         |
| Renewal motion                        | Customer Success (see `RENEWAL_AND_EXPANSION_OS.md`).           |
| Expansion motion                      | Customer Success + Offer Architect.                             |
| Referrals                             | Partner Revenue Agent (see `REFERRAL_SYSTEM.md`).               |
| Proof generation (with consent)       | Proof Safety Agent.                                            |
| Issue handling and escalation         | Customer Success + Incident Response.                          |

## Source files

| File                                  | Purpose                                                  |
| ------------------------------------- | -------------------------------------------------------- |
| `customer_success/client_health.csv`   | Per-client health, next action, due, owner.              |
| `customer_success/referral_queue.csv`  | Referral targets and status.                             |
| `sales/proposal_queue.csv`             | Tracks renewals and expansions as new proposal rows.     |
| `proof/proof_library.csv`              | Proof candidates, including from consenting customers.   |

## Founder Console endpoints

| Endpoint                                  | What it shows                                                       |
| ----------------------------------------- | ------------------------------------------------------------------- |
| `GET /customer-success/summary`           | Active clients, at-risk count, open referrals.                     |
| `GET /retention/queue`                    | Per-client health and next action.                                 |
| `GET /control/scorecard`                  | Customer success contribution to the delivery pillar.              |

The customer success endpoints are read-only. Mutations are recorded
through the approval and audit flow.

## The success lifecycle

```
Sign → Onboard → Deliver first value → Health-monitor → Renew / Expand
                       │
                       └── Refer (with explicit customer consent)
                       └── Proof (with explicit customer consent)
                       └── Escalate (when health declines)
```

Each stage has a defined exit criterion, an owner, and a CSV row that
records progress.

## Stage 1: Sign

A signed contract triggers:

- A `sales/proposal_queue.csv` row flipped to `status: won`.
- A new entry in `customer_success/client_health.csv` with
  `health: green`, `next_action: kickoff`, owner assigned.
- An audit row referencing the deal id.

## Stage 2: Onboard

Onboarding follows `CLIENT_ONBOARDING_OS.md` in
`docs/delivery/`. The discipline:

| Aspect                                   | Practice                                                  |
| ---------------------------------------- | --------------------------------------------------------- |
| Kickoff within 5 business days            | Calendar-locked.                                          |
| Defined first value milestone             | Documented in the proposal; tracked in the sample queue.  |
| Stakeholder map                           | Captured in onboarding notes.                             |
| Communication cadence                     | Weekly update; monthly review.                            |
| Data access posture                       | PDPL-aligned; access logs in `security/`.                 |

## Stage 3: Deliver first value

The first value milestone is what we deliberately design for. The
Delivery Copilot owns the delivery; the Customer Success function
owns the relational layer. The transition from delivery to ongoing
success is the handoff:

- The Handoff and QA System (`HANDOFF_AND_QA_SYSTEM.md`) checklists
  are completed.
- A success criteria document is filed against the deal.
- The client_health row updates `next_action: first_value_review`.

## Stage 4: Health monitoring

The Client Health Score System
(`CLIENT_HEALTH_SCORE_SYSTEM.md`) computes a per-client score on a
weekly cadence. The score categories:

| Category   | Signal                                                            |
| ---------- | ----------------------------------------------------------------- |
| `green`    | Engagement on plan; outcomes landing; sentiment positive.         |
| `yellow`   | One signal trending wrong; intervention warranted.                |
| `red`      | Multiple signals trending wrong; escalation required.             |
| `at_risk`  | Active churn risk.                                                |

The Founder Console exposes the count of at-risk clients in the
customer success summary.

## Stage 5: Renew and expand

The Renewal and Expansion OS (`RENEWAL_AND_EXPANSION_OS.md`) is the
discipline. Renewal opens 90 days before the contract end. Expansion
follows the offer ladder. Both motions are policy-gated: pricing
changes and contract changes require founder approval.

## Stage 6: Refer and proof

Referrals are handled by the Partner Revenue Agent. A referral row
in `customer_success/referral_queue.csv` requires the customer's
explicit consent. Proof generation requires consent and the Proof
Safety Agent's approval flow.

| Artifact         | Consent type required                  |
| ---------------- | -------------------------------------- |
| Logo use         | Written consent.                       |
| Quote / testimony | Written consent with quote review.    |
| Case study       | Written consent + redaction review.    |
| Referral introduction | Explicit ask + confirmation.       |

## Escalation

When `health` drops to `yellow` or worse:

1. The Customer Success row updates with `next_action: escalate`.
2. A trust flag at `severity: medium` is opened.
3. The founder is informed in the daily brief.
4. The Incident Response Agent may open an incident if there is a
   contractual or delivery risk.

## What Customer Success will not do

- Auto-extend a contract.
- Auto-discount a renewal.
- Use a customer's name externally without consent.
- Mark a customer as a reference without explicit confirmation.
- Move a customer between owners without an audit row.

## Discipline

1. Every client has a health row.
2. Every health row has an owner and a next action.
3. Renewals open 90 days early.
4. Expansion follows the offer ladder, not an ad hoc deal.
5. Referrals and proof require explicit customer consent.

## Cross-references

- `CLIENT_HEALTH_SCORE_SYSTEM.md` for scoring.
- `RENEWAL_AND_EXPANSION_OS.md` for the renewal motion.
- `REFERRAL_SYSTEM.md` for partner referrals.
- `docs/delivery/CLIENT_ONBOARDING_OS.md` for onboarding.
- `docs/delivery/HANDOFF_AND_QA_SYSTEM.md` for the handoff.
