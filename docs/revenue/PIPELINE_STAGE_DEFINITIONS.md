# Pipeline Stage Definitions

This document defines the pipeline stages used in the Revenue Factory.
Each stage has explicit entry criteria, exit criteria, SLA, the artefact
that must exist, and the owner. The point is to make stage transitions
unambiguous and audit-friendly.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Pipeline stages

The pipeline has 7 stages plus three terminal states.

### 1.1 Reply received

- Entry: a reply arrives to an approved outreach.
- Exit: the reply is classified by the Reply Router Machine.
- SLA: classification within 1 working hour.
- Artefact: a row in `outreach/reply_routing.csv`.
- Owner: Distribution Operator.

### 1.2 Qualified

- Entry: the reply classification is `interested` and a qualification
  call is scheduled.
- Exit: qualification call held; persona authority, pain anchor, and
  decision window confirmed.
- SLA: call held within 5 working days.
- Artefact: notes in `sales/qualification_notes.md` with date, named
  participants, and an opportunity_id assigned in `sales/pipeline.csv`.
- Owner: Founder (call) + Delivery Copilot (notes).

### 1.3 Sample sent

- Entry: a sample is approved and delivered.
- Exit: the buyer has reviewed the sample and provided feedback or
  asked a follow-up question.
- SLA: review feedback within 10 working days; bump on day 5 if
  silent.
- Artefact: `sales/sample_queue.csv` row at state = sent and a sample
  document under `samples/{opportunity_id}/`.
- Owner: Delivery Copilot.

### 1.4 Proposal sent

- Entry: proposal approved and delivered.
- Exit: buyer responds with accept, decline, hold, or specific
  negotiation request.
- SLA: response within `decision_window_close_at` (typically 14-30
  days).
- Artefact: `sales/proposal_queue.csv` row at state = sent and a
  proposal document under `proposals/{opportunity_id}/`.
- Owner: Delivery Copilot.

### 1.5 Negotiation

- Entry: buyer requests modifications to price, terms, or scope.
- Exit: a finalised agreement is reached or the buyer declines.
- SLA: 10 working days; longer requires founder approval and a
  recorded reason.
- Artefact: `sales/negotiation_log.md` per opportunity with each
  modification noted; finalised proposal in `proposals/`.
- Owner: Founder (price/terms commits per policy) + Delivery Copilot.

### 1.6 Verbal yes

- Entry: buyer says yes verbally or in informal writing.
- Exit: signed contract.
- SLA: 7 working days.
- Artefact: signed contract under `contracts/{opportunity_id}/`.
- Owner: Founder + Legal lead.

### 1.7 Closed (won)

- Entry: signed contract.
- Exit: handoff to Payment Capture OS and Delivery QA OS.
- SLA: handoff within 1 working day.
- Artefact: row in `finance/payment_capture_queue.csv` and
  `delivery/delivery_kickoff_queue.csv`.
- Owner: Founder.

## 2. Terminal states

- Lost: explicit decline. Recorded in `sales/win_loss_log.md` with the
  documented reason and the next-best ICP/persona signal.
- Hold: paused at the buyer's request, with a date. Returns to the
  prior stage when the date passes.
- Disqualified: post-qualification discovery that the account violates
  a disqualifier in `ICP_SEGMENTATION_SYSTEM.md`. Recorded with
  reason; account moves to suppression-or-watch depending on cause.

## 3. SLA matrix (summary)

| Stage | SLA | Owner |
|---|---|---|
| Reply received | 1 working hour | Distribution Operator |
| Qualified | 5 working days | Founder |
| Sample sent | 10 working days | Delivery Copilot |
| Proposal sent | decision_window | Delivery Copilot |
| Negotiation | 10 working days | Founder |
| Verbal yes | 7 working days | Founder |
| Closed (won) | 1 working day handoff | Founder |

SLA breaches are surfaced in `sales/pipeline_scorecard.csv` and the
weekly operating rhythm.

## 4. Source of truth

`sales/pipeline.csv` — one row per opportunity with the current stage,
last transition timestamp, and owner.

## 5. Approval class

A1 for stage observation. A2 for the artefacts that move stages
forward (sample, proposal, negotiation drafts). A3 not used. Pricing,
term, and contract commits at any stage require founder approval per
the corresponding policy rules.

## 6. Trust gates per stage

- All artefact-bearing stages run their respective trust gates (sample,
  proposal, contract).
- Hold transitions require a recorded buyer-requested reason.
- Disqualified transitions require a citation to the ICP disqualifier
  list.
- Lost transitions require a documented reason and a feedback note.

## 7. KPI

- Average days in stage (per stage).
- Stage-to-stage conversion rate.
- Win rate (closed_won / proposals_sent).
- SLA breach rate.
- Disqualification-after-qualified rate (target: low).

## 8. Failure mode

- Stage skipped without an artefact. Worker rejects; pipeline integrity
  enforced.
- Artefact exists but trust gate failed. Stage transition blocked.
- Negotiation runs over SLA. Founder reviews; explicit extension or
  move to hold.
- Verbal yes without follow-through. Hold/decision path.

## 9. Recovery path

- For skipped stage: re-create the artefact; ledger entry.
- For trust gate failure: rewrite; resume.
- For SLA breach: founder triage; reason recorded.
- For lost without reason: post-mortem in `sales/win_loss_log.md`.

## 10. Cadence

| Cadence | Activity |
|---|---|
| Daily | Pipeline view |
| Weekly | Sales operating rhythm review |
| Monthly | Stage SLA calibration |
| Quarterly | Stage definition review |

## 11. Saudi specifics

- Procurement realism: SLA bands account for Saudi B2B realities.
- Bilingual artefacts respected at every stage.
- Verbal yes is treated with care; relationship density means a verbal
  yes can be real and binding socially, while contract execution may
  take time.

## 12. Non-negotiables

- No stage transition without the required artefact.
- No external commit without founder approval at the right stage.
- No guaranteed claims in any stage artefact.
- A3 not used.

Pipeline integrity is the discipline that turns conversations into
revenue. Loose definitions break the discipline.
