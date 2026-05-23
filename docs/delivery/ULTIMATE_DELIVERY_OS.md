# Ultimate Delivery OS

The Delivery OS is the end-to-end runbook for taking a signed engagement from kickoff to formal handoff and renewal review.

**Source of truth:** `$PRIVATE_OPS/delivery_state.csv`
**Owner:** Delivery Lead
**Trust gate:** A1 for routine state changes; A2 for scope changes or refund-adjacent decisions.

## Lifecycle

| Stage | Owner | Output | Gate |
|-------|-------|--------|------|
| Kickoff | Delivery Lead | Kickoff document, calendar | A1 |
| Discovery | Delivery Lead | Discovery brief | A1 |
| Build | Engineering / Content | Deliverables in QA queue | A1 |
| QA | Delivery Lead | Pass certificate | A1 |
| Release | Delivery Lead | Release event, client comms | A1 |
| Review | Delivery Lead + Client | Review notes | A1 |
| Handoff | Delivery Lead | Handoff pack | A2 |
| Renewal | Founder | Renewal proposal or close | A2 |

Stages are sequential. A jump (release without QA, handoff without review) raises a policy violation in `policies/dealix_control_policy.yaml`.

## Kickoff

The kickoff document is generated from the signed proposal and contains:

- Engagement objective in one sentence.
- Named milestones with target dates.
- Named owners on both sides.
- Communication channels and cadence.
- Data-access plan with PDPL clauses.
- Trust pack reference (`docs/14_trust_os/`).

Kickoff is logged in `delivery_state.csv` with `kickoff_at` and `kickoff_doc_path`.

## Discovery

Discovery is bounded by the proposal scope. The brief contains:

- Current revenue process map.
- Top three friction points by client report.
- Data sources available with provenance.
- Stakeholder map.
- Risk register.

Discovery is the only stage where scope can still flex. After discovery, any scope change runs through the Change Request System (`docs/delivery/CHANGE_REQUEST_SYSTEM.md`).

## Build

The Build stage produces the deliverables enumerated in the proposal. The factory pattern applies (`docs/revenue/REVENUE_FACTORY_OS.md`): every artifact has an input, an output, an owner, and a definition of done.

## Release and review

Release is a single, logged event. The client receives the deliverable plus a one-page summary in EN and AR. A review meeting follows within 5 business days. Review notes feed both renewal and the Capital Ledger (`docs/09_capital_os/CAPITAL_LEDGER.md`).

## Handoff

Handoff produces:

- Final deliverables index.
- Outstanding-item register.
- Renewal recommendation (proceed, modify, close).
- Founder sign-off.

## Failure modes

- **Milestone slip:** a milestone passes without delivery. Detection: nightly job. Recovery: Delivery Lead notifies client within 24 hours with revised date.
- **Scope creep:** client request exceeds discovery scope without a Change Request. Detection: QA layer flags. Recovery: pause work, raise Change Request, re-price if needed.
- **Acceptance dispute:** client rejects a deliverable. Detection: review meeting. Recovery: written dispute log; founder mediates; either re-work or contractual exit.

## Recovery path

If multiple engagements are blocked (shared dependency outage), the founder triages by contractual exposure and notifies affected clients in writing within 24 hours.

## Metrics

- On-time milestone rate.
- Pass-first-time rate from QA.
- Renewal rate at handoff (estimated and verified).
- Defect-escape rate.

## Disclaimer

The Delivery OS is a process model. It does not guarantee any specific commercial outcome. Estimated value is not Verified value.
