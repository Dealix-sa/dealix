# Ultimate Delivery OS

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Closing Deals · Focused on Results.

The Delivery OS is the discipline by which Dealix turns a signed
contract into a delivered outcome the customer can use, audit, and
talk about. It is owned by the Delivery Copilot (A2 max) with the
founder as the final sign-off. Delivery is the proof factory; if
delivery is weak, every other system suffers.

## Scope

| Concern                              | Owner                                                          |
| ------------------------------------ | -------------------------------------------------------------- |
| Sprint design                         | Founder + Offer Architect (productized) or Delivery Copilot (custom). |
| Sample sprint execution               | Delivery Copilot.                                              |
| Proposal-to-sprint handoff            | Delivery Copilot + Customer Success.                            |
| QA gates                              | Delivery Copilot + Eval Guardian.                              |
| Handoff to customer                   | Delivery Copilot + Customer Success.                            |
| Proof generation (with consent)       | Delivery Copilot drafts; Proof Safety Agent approves.           |

## Source files

| File                                  | Purpose                                                  |
| ------------------------------------- | -------------------------------------------------------- |
| `sales/proposal_queue.csv`             | Wins land here; delivery picks them up.                  |
| `sales/sample_queue.csv`               | Sample sprints in flight.                                |
| `product/offer_ladder.csv`             | Defines the rungs and their scopes.                      |
| `proof/proof_library.csv`              | Proof outputs from completed sprints.                    |
| `proof/proof_approval_queue.csv`       | Proof approval queue.                                   |

## Founder Console endpoints

| Endpoint                                  | What it shows                                                |
| ----------------------------------------- | ------------------------------------------------------------ |
| `GET /delivery/queue`                      | Per-sprint proposal queue with status.                       |
| `GET /proof/library`                       | Proof library with approval state.                           |
| `GET /control/scorecard`                   | Delivery pillar of the four-pillar scorecard.                |

## The delivery operating model

Dealix delivers through **sprints**. A sprint is a defined,
time-boxed engagement with a specific deliverable, an explicit
acceptance criterion, and a known cost. The two canonical sprint
shapes:

| Shape         | Description                                                                          |
| ------------- | ------------------------------------------------------------------------------------ |
| Sample sprint  | A short, focused engagement that produces a single, customer-relevant artifact.       |
| Productized sprint | A repeatable engagement from the offer ladder with a fixed scope and price.          |

Custom engagements are deliberately rare. Repetition is the path to
margin, quality, and trust.

## The end-to-end flow

```
proposal_queue (won) → sample_queue (in flight) → handoff → outcomes → proof candidate → proof library
```

| Stage                | File state                                                                | Owner               |
| -------------------- | ------------------------------------------------------------------------- | ------------------- |
| Won                   | `sales/proposal_queue.csv` row `status: won`.                              | Founder.            |
| Kickoff               | `sales/sample_queue.csv` row `status: kickoff_scheduled`.                  | Delivery Copilot.   |
| In flight             | `sales/sample_queue.csv` row `status: in_progress`.                        | Delivery Copilot.   |
| QA gate                | Delivery Copilot + Eval Guardian; status `qa_open`.                       | Delivery Copilot.   |
| Acceptance            | Customer accepts; status `accepted`.                                      | Customer + Delivery.|
| Handoff               | Handoff packet shipped; status `handed_off`.                              | Customer Success.   |
| Proof candidate        | `proof/proof_library.csv` row `approval_state: draft`.                    | Delivery Copilot.   |
| Proof published         | `proof/proof_library.csv` row `approval_state: approved`.                | Proof Safety Agent. |

## Sprint design discipline

| Aspect              | Practice                                                       |
| ------------------- | -------------------------------------------------------------- |
| One outcome          | Each sprint has one primary outcome.                            |
| Defined acceptance    | A written acceptance criterion is included in the proposal.    |
| Cost-aware            | Sprint cost is estimated and tracked in the close.             |
| Reusable             | Where the sprint is custom, design with productization in mind.|
| Trust-aligned         | No external communication is sent during the sprint without founder approval. |

## QA gate

Before handoff, every sprint passes a QA gate documented in
`HANDOFF_AND_QA_SYSTEM.md`. The gate includes:

- Brand check (Brand Guardian).
- Phrasing check (no overclaim).
- PII check (Proof Safety Agent, where customer data is involved).
- Outcome trace check (deliverable maps to acceptance criterion).
- Customer-facing message check.

A failed QA gate refuses the handoff until the issues are fixed.

## Acceptance and handoff

Acceptance is documented in writing. The handoff is a packet
containing:

| Item                                | Notes                                                       |
| ----------------------------------- | ----------------------------------------------------------- |
| The primary deliverable              | Format depends on the sprint type.                          |
| The acceptance document               | Signed by customer.                                         |
| The runbook                          | How the customer uses the deliverable operationally.        |
| The next-step recommendation         | What the customer might do next; not a sales pitch.         |
| The proof candidate (if consent)      | A redacted artifact for the proof library.                 |

The Customer Success function takes over from here.

## Proof generation

The Delivery Copilot drafts proof candidates from completed
sprints. The Proof Safety Agent approves before any external use.
The flow:

1. Draft candidate appended to `proof/proof_library.csv` with
   `approval_state: draft`.
2. Customer consent recorded (see `REFERRAL_SYSTEM.md`).
3. Proof Safety Agent runs the proof_safety eval suite.
4. Founder approves via the Founder Console.
5. `approval_state` flips to `approved`.

A proof in `draft` state is invisible externally. A proof in
`approved` state is the only artifact the Brand Guardian may
reference in claims.

## Cadence

| Activity                         | Cadence    |
| -------------------------------- | ---------- |
| Sprint kickoff                   | Within 5 business days of close.        |
| Sprint review (internal)         | Weekly for sprints in flight.           |
| Customer checkpoint              | Per the sprint plan.                    |
| Handoff retrospective             | Within 7 days of handoff.               |
| Proof drafting                    | Within 7 days of handoff (where consent). |

## What the Delivery OS will not do

- Send external communications without founder approval.
- Publish proof without the approval chain.
- Restart a sprint without re-scoping.
- Accept new scope mid-sprint without a contract change.
- Use customer data outside the sprint without explicit consent.

## Discipline

1. One outcome per sprint.
2. Acceptance is written.
3. QA before handoff.
4. Proof requires consent + approval.
5. Productize what we repeat; do not custom-build what already exists.

## Cross-references

- `CLIENT_ONBOARDING_OS.md` for the onboarding entry point.
- `HANDOFF_AND_QA_SYSTEM.md` for the gate.
- `CUSTOMER_SUCCESS_OS.md` for what happens after handoff.
- `EVAL_GATE_V1.md` for the proof safety suite.
- `docs/product/...` for the offer ladder catalog.
