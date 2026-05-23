# Revenue Factory OS

The Revenue Factory OS is the layer that turns approved outreach into
revenue. It owns the path from a positive reply to a signed retainer or
won pilot — through samples, proposals, reply routing, objection
handling, pipeline stages, and operating rhythm.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. What the Revenue Factory is

The Revenue Factory is the system that:

1. Routes inbound replies to the correct next step.
2. Produces the right artefact (sample, proposal, contract draft).
3. Manages the pipeline stages and their definitions.
4. Runs the weekly operating rhythm.
5. Handles objections from a structured library.
6. Coordinates with the finance and delivery OSs at close.

It is not a CRM. It does not pretend to be a forecasting engine. It is
the deterministic, auditable production line for revenue events.

## 2. Components

- `SAMPLE_FACTORY.md` — produces sample artefacts (diagnostics,
  sector briefs, audit-style outputs) for qualified buyers.
- `PROPOSAL_FACTORY.md` — drafts proposals from a parametric template.
- `REPLY_ROUTING_SYSTEM.md` — the human-side reply routing playbook
  (the agent-side router lives in `growth/REPLY_ROUTER_MACHINE.md`).
- `OBJECTION_LIBRARY_SYSTEM.md` — the structured library of common
  objections and approved responses.
- `PIPELINE_STAGE_DEFINITIONS.md` — pipeline stages and their exit
  criteria.
- `SALES_OPERATING_RHYTHM.md` — daily/weekly/monthly cadence.
- `PAYMENT_CAPTURE_OS.md` — see `docs/finance/`.
- `DELIVERY_QA_OS.md` — see `docs/delivery/`.
- `RETENTION_REFERRAL_OS.md` — see `docs/client_success/`.
- `PROOF_APPROVAL_OS.md` — see `docs/proof/`.

## 3. Pipeline shape

```
Approved Outreach -> Reply -> Routed Reply
        |                            |
        v                            v
   Qualified Call <--- Suggested Next Step
        |
        v
   Sample Factory  -> Sample Sent -> Sample Reviewed
        |
        v
   Proposal Factory -> Proposal Sent -> Decision Window
        |
        v
   Won (Pilot or Retainer)  /  Lost  /  Hold
        |
        v
   Payment Capture OS (Finance)
        |
        v
   Delivery QA OS (Delivery)
        |
        v
   Retention and Referral OS (Customer Success)
        |
        v
   Proof Approval OS (Proof)
        |
        v
   Back into Demand (via Proof-to-Demand and Content-to-Demand)
```

Every transition is recorded; nothing happens without a named owner and
a recorded approval at the relevant trust gate.

## 4. Source of truth

`sales/proposal_queue.csv` and `sales/sample_queue.csv` are the
canonical store for pipeline artefacts. `sales/pipeline.csv` is the
single canonical pipeline view (one row per opportunity).

## 5. Approval classes used

- A1: pipeline observation, stage transitions that do not require
  external action.
- A2: artefact drafting (sample, proposal) and outbound action
  recommendations.
- A3: banned.

## 6. Non-negotiables

- No guaranteed-revenue language in samples, proposals, follow-ups, or
  pipeline summaries.
- No external send by any agent.
- No commitment to pricing, refund, payment terms, or contract
  modification without explicit founder approval (policy rule
  `pricing_commit_requires_approval`).
- No proof publication without proof safety approval.
- A3 banned (policy rule `no_a3_auto`).

## 7. Owners

- Pipeline: Delivery Copilot agent + Founder.
- Samples and Proposals: Delivery Copilot agent + Founder approval per
  draft.
- Reply routing: Distribution Operator + Founder approval per reply
  next-step.
- Finance handoff: Finance Copilot.
- Delivery handoff: Delivery Copilot.
- Proof: Proof Safety Agent.

## 8. KPI

- Reply-to-Qualified-Call Rate.
- Qualified-Call-to-Sample Rate.
- Sample-to-Proposal Rate.
- Proposal Win Rate.
- Average Days in Stage (per stage).
- Pipeline Stalls (stages over SLA, surfaced weekly).
- Net Cash Captured per Won Opportunity (handoff to Finance OS).

These are reported in `sales/pipeline_scorecard.csv` and the founder's
weekly scorecard.

## 9. Failure modes (system-level)

| Failure | Recovery |
|---|---|
| Sample drift to generic | Sample Factory rewrites; root cause review |
| Proposal includes guaranteed claim | Brand Guardian blocks; ledger entry |
| Stage stalls in "proposal sent" | SLA breach surfaced; founder follow-up |
| Reply routing miss | Reply router calibration; ledger entry |
| Finance handoff gap | Reconciliation sprint; finance OS run |
| Delivery handoff gap | Delivery OS picks up; backfill in `sales/pipeline.csv` |

## 10. Cadence

| Cadence | Activity |
|---|---|
| Daily | Pipeline view; new replies routed |
| Weekly | Sales operating rhythm meeting; SLA review |
| Monthly | Win/loss analysis; objection library update |
| Quarterly | Pipeline-stage calibration; SLA reset |

## 11. Saudi specifics

- Decision windows can be longer than typical SaaS markets; SLA bands
  are tuned for Saudi B2B reality.
- Bilingual pipeline support: every pipeline artefact respects the
  buyer's operating language.
- Procurement realism is built into stage definitions.

## 12. Output summary

- `sales/pipeline.csv`
- `sales/sample_queue.csv`
- `sales/proposal_queue.csv`
- `sales/pipeline_scorecard.csv`
- `sales/win_loss_log.md`

## 13. Reads from

- `outreach/reply_routing.csv` (inbound replies).
- `customer_success/referral_queue.csv` (partner-introduced
  opportunities).
- `growth/abm_queue.csv` (ABM plays).
- `proof/proof_library.csv` (proof artefacts).
- `finance/cash_collected.csv` (close confirmation).

The Revenue Factory is the layer where the system stops being theory
and starts being money. It is also the layer most exposed to trust
risk. Its restraint is the source of its compounding.
