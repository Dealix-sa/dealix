# Delivery QA OS

The Delivery QA OS owns the post-sale delivery lifecycle and the
quality gates that prevent shipping bad work. It coordinates kickoff,
sprint cadence, change requests, QA reviews, handoffs, and renewals.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Move every closed-won engagement into delivery with a clean kickoff,
keep it on cadence, and apply quality gates before any artefact lands
with the client. No surprise scope; no surprise delays; no surprise
deliverables.

## 2. Input

Sources:

- `sales/pipeline.csv` (rows at stage = closed_won).
- `contracts/{opportunity_id}/` (signed contract; scope).
- `product/offer_ladder.csv` (delivery spec for the offer).
- `delivery/playbooks/{offer_id}.md` (offer-specific playbook).
- `delivery/sprint_template.md`.
- `proof/proof_library.csv` (existing approved proof, where relevant).
- `customer_success/onboarding_template.md`.

Each closed_won opportunity automatically enters
`delivery/delivery_kickoff_queue.csv`.

## 3. Output

Queues and artefacts:

- `delivery/delivery_kickoff_queue.csv` — engagements awaiting kickoff.
- `delivery/sprint_log.csv` — sprint-by-sprint state per engagement.
- `delivery/change_request_queue.csv` — change requests with approval
  state.
- `delivery/qa_queue.csv` — artefacts awaiting QA review.
- `delivery/handoff_queue.csv` — handoffs to client team.
- `delivery/renewals_queue.csv` — engagements approaching renewal.

`delivery/sprint_log.csv` columns:

- `sprint_id`
- `engagement_id`
- `sprint_index`
- `start_at`, `end_at`
- `planned_outcomes` — pipe-delimited
- `actual_outcomes`
- `qa_state` — drafted | reviewed | approved | rejected
- `state` — planned | active | review | complete | held
- `notes`

## 4. Source of truth

`delivery/sprint_log.csv` for engagement state. `contracts/` for scope.
`delivery/playbooks/` for the operating spec per offer.

## 5. Approval class

A1 for sprint observation and QA scoring. A2 for any artefact that
goes to the client (sprint output, QA report, handoff package). A3
banned. Scope changes always require founder + client approval.

## 6. Trust gate

- Scope integrity: deliverables must match the contract; out-of-scope
  work goes through the change request queue.
- QA gate: every client-facing artefact passes a documented QA review
  before send.
- Guarantee scan: no guaranteed-outcome language in any deliverable.
- Brand voice check.
- Confidentiality: deliverables respect customer-specific redaction
  posture; no other-customer data appears.
- Audit: every state transition is logged.

## 7. Owner

`delivery_copilot` agent. Allowed write target: `sales/` (per
registry; delivery artefacts that touch sales references) and
`delivery/` via operator-mediated writes.

## 8. Worker

`scripts/dealix_delivery_qa.py` (planned). The worker:

1. Reads closed_won opportunities and creates kickoff queue entries.
2. Reads the playbook for the offer and instantiates sprint templates.
3. Manages QA queue for each client-facing artefact.
4. Surfaces change requests for founder approval.
5. Tracks renewals approaching the contract end date.

## 9. KPI

- Kickoff Cycle Time (closed_won -> kickoff).
- On-time Sprint Completion Rate.
- QA First-Pass Rate.
- Change Request Latency.
- Client Acceptance Rate (artefacts accepted on first review).
- Renewal Conversion Rate.

## 10. Failure mode

- Scope creep without a change request. Worker enforces; founder
  reviews.
- Sprint slips silently. Worker raises alert at day-7 of slippage.
- QA gate bypassed. Worker rejects; ledger entry.
- Artefact reveals other-customer data. Trust Guardian halts; critical
  incident.
- Renewal missed. Worker raises 60 days before end-of-contract.

## 11. Recovery path

- For scope creep: change request opened; founder + client approval
  before continuation.
- For sprint slippage: sprint replan; client notified; root cause.
- For QA bypass: artefact recalled if possible; ledger entry; incident.
- For confidentiality breach: incident opened; client notified per
  contract.
- For missed renewal: renewal recovery sprint.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Daily | Sprint state update; QA queue review |
| Weekly | Engagement review with client (per playbook) |
| Monthly | Delivery review; renewal pipeline |
| Quarterly | Playbook audit; QA criterion calibration |

## 13. Saudi specifics

- Bilingual deliverables; the playbook captures the language profile.
- PDPL alignment in delivery artefacts; customer data residency
  respected.
- Procurement-aligned milestones; payment milestones often track to
  sprint completion.

## 14. Non-negotiables

- No client-facing artefact without QA approval.
- No scope change without contract change request.
- No guaranteed-outcome language.
- No other-customer data in any deliverable.
- A3 not used.

Delivery is the second sale. The system treats every deliverable as a
proof artefact-in-the-making.
