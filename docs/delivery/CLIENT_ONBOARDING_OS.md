# Client Onboarding OS

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Closing Deals.

The Client Onboarding OS is the first five business days of a new
customer relationship. The bar is high: kickoff within five business
days, a defined first-value milestone, a stakeholder map, and a
documented communication cadence. The onboarding is owned jointly by
Delivery Copilot and Customer Success.

## Scope

| Concern                          | Owner                                                          |
| -------------------------------- | -------------------------------------------------------------- |
| Kickoff scheduling               | Delivery Copilot.                                              |
| Contract and DPA confirmation     | Founder + Legal.                                              |
| Data access posture               | Security Guardian.                                            |
| Stakeholder map                   | Customer Success.                                              |
| First-value milestone definition  | Delivery Copilot + Customer.                                  |
| Communication cadence             | Customer Success.                                              |
| Trust posture briefing             | Trust Guardian + Founder.                                     |

## Source files

| File                                  | Purpose                                                  |
| ------------------------------------- | -------------------------------------------------------- |
| `sales/proposal_queue.csv`             | The won proposal triggers onboarding.                    |
| `sales/sample_queue.csv`               | Sample sprint kickoff registered here.                   |
| `customer_success/client_health.csv`   | First health row written at kickoff.                     |

## The five-day onboarding plan

### Day 0: Contract close

| Task                                                              | Owner                |
| ----------------------------------------------------------------- | -------------------- |
| Audit row: `action: contract_won`, `risk: low`.                    | Founder Console.     |
| Internal handoff packet from Sales to Delivery.                    | Delivery Copilot.    |
| Initial client_health row written: `health: green`, next action: `kickoff`. | Customer Success. |

### Day 1: Welcome and scheduling

| Task                                                              | Owner                |
| ----------------------------------------------------------------- | -------------------- |
| Welcome message drafted (no overclaim, brand-aligned).             | Distribution Operator. |
| Founder approves and sends welcome.                                | Founder.             |
| Kickoff meeting scheduled within 5 business days.                  | Delivery Copilot.    |
| DPA executed if not already in place.                              | Founder + Legal.     |

### Day 2–3: Stakeholder mapping and access

| Task                                                              | Owner                |
| ----------------------------------------------------------------- | -------------------- |
| Stakeholder map captured in onboarding notes.                       | Customer Success.    |
| Customer data access posture confirmed (read-only by default).      | Security Guardian.   |
| Suppression list updated with any customer-facing identities that should not be cold-contacted. | Trust Guardian. |

### Day 4: Kickoff

| Task                                                              | Owner                |
| ----------------------------------------------------------------- | -------------------- |
| Kickoff meeting held.                                              | Founder + Customer.  |
| First-value milestone agreed and documented.                       | Delivery Copilot.    |
| Communication cadence agreed (weekly update, monthly review).      | Customer Success.    |
| Trust posture briefed: no external communications without approval, audit ledger discipline, suppression posture. | Trust Guardian. |

### Day 5: Sprint plan

| Task                                                              | Owner                |
| ----------------------------------------------------------------- | -------------------- |
| Sprint plan written; row appended to `sales/sample_queue.csv`.    | Delivery Copilot.    |
| Sprint plan reviewed with customer.                                | Founder.             |
| QA gate criteria documented.                                       | Delivery Copilot.    |
| Internal sprint board updated.                                     | Delivery Copilot.    |

## Discipline beyond day five

After day five, the engagement enters the sprint lifecycle (see
`ULTIMATE_DELIVERY_OS.md`). The onboarding artifacts persist:

- The first-value milestone is the anchor for delivery.
- The stakeholder map drives renewals and expansion.
- The communication cadence locks the rhythm.

## Data posture

| Aspect                              | Practice                                                          |
| ----------------------------------- | ----------------------------------------------------------------- |
| Customer data ingest                 | Only what is needed for the sprint.                                |
| Storage location                     | Application database; never the private ops runtime.              |
| Access control                       | Role-based, audit-logged.                                          |
| Cross-border posture                 | Per `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.                      |
| Deletion at end                      | Per `docs/DATA_RETENTION_POLICY.md`.                               |

## Trust briefing

Every onboarding includes a 10-minute trust briefing. The points
covered:

1. Every external action requires founder approval; A3 is banned.
2. Suppression posture: the customer can request additions at any
   time.
3. Audit ledger: every approval and decision is logged.
4. Eval gate: every draft passes the gate before reaching the
   founder.
5. Pricing, contract, and payment terms cannot change without
   recorded approval.

The briefing is recorded as an audit row with
`action: trust_briefing`, `risk: low`.

## Founder Console exposure

The Founder Console does not yet expose an onboarding endpoint
directly. Onboarding status surfaces via:

- `/delivery/queue` (sprint pipeline).
- `/retention/queue` (client_health rows).
- `/customer-success/summary` (active client count).

## Anti-patterns

| Anti-pattern                                          | Why                                                                  |
| ----------------------------------------------------- | -------------------------------------------------------------------- |
| Delayed kickoff                                        | Trust erodes; momentum is lost.                                       |
| Undefined first-value milestone                        | The sprint becomes a long slog with no clear outcome.                 |
| Stakeholder map skipped                                | Renewals and expansion suffer later.                                  |
| Communication cadence undefined                        | Customer feels neglected; health drops.                              |
| Trust briefing skipped                                 | Customer's expectations may misalign with operating discipline.      |

## Cadence

| Activity                       | Cadence                                          |
| ------------------------------ | ------------------------------------------------ |
| Kickoff                        | Within 5 business days of contract close.        |
| Welcome message                | Day 1.                                           |
| First-value milestone agreement | Day 4 (kickoff).                                 |
| Onboarding retrospective       | Day 30.                                          |

## Discipline

1. Five business days, no exceptions.
2. One first-value milestone, written.
3. Stakeholder map captured.
4. Trust briefing recorded.
5. Communication cadence locked.

## Cross-references

- `ULTIMATE_DELIVERY_OS.md` for what happens after onboarding.
- `HANDOFF_AND_QA_SYSTEM.md` for the QA gate before handoff.
- `CUSTOMER_SUCCESS_OS.md` for the ongoing relationship.
- `ACCESS_CONTROL_MODEL.md` for data posture.
