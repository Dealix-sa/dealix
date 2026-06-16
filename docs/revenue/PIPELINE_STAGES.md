# Pipeline Stages

The canonical seven-stage pipeline that every lead must move through. No custom stages, no parallel pipelines.

## Purpose
Standardize how revenue progresses so any agent or operator can read the pipeline tracker and know exactly what action is required next.

## Owner
Sami (Founder, Revenue OS).

## Review Cadence
Weekly during the CEO review.

## Inputs
- `dealix-ops-private/pipeline/pipeline_tracker.csv`.
- Founder approvals on outbound and proposals.
- Customer responses logged from email / DM / call.

## Outputs
- Updated stage values per lead.
- Next action assigned per lead.
- Stage conversion metrics into the scorecard.

## Rules
- Every lead must sit in exactly one stage at any time.
- Movement to a later stage requires evidence (a reply, a sent proposal, a payment).
- Movement to `Paid` requires a logged payment reference.
- `Delivered` requires a linked proof pack.
- A lead with no movement for 14 days must be archived or restarted.

---

## The Seven Stages

### 1. New
- Lead has been added with company, contact, sector, and priority.
- No outreach yet.
- Next action: prepare outbound draft.

### 2. Contacted
- First outbound touch sent (DM, email, or warm intro).
- Timestamp logged.
- Next action: wait, then second touch by day 4.

### 3. Replied
- Lead has responded.
- Next action: qualify and recommend a rung.

### 4. Proposal Sent
- Proposal aligned to a specific offer rung delivered.
- Next action: schedule decision date.

### 5. Paid
- Payment or PO received and logged.
- Next action: open kickoff and move to delivery.

### 6. Delivered
- Sprint or pilot finished. Proof pack delivered. Customer signed acknowledgment.
- Next action: offer the next rung.

### 7. Retainer
- Customer is on Rung 4 or Rung 5.
- Next action: maintain weekly review cadence.

---

## Conversion Targets (Quarterly)

| Transition | Target |
|---|---:|
| New → Contacted | 100% within 48h |
| Contacted → Replied | ≥ 15% |
| Replied → Proposal Sent | ≥ 60% |
| Proposal Sent → Paid | ≥ 30% |
| Paid → Delivered | 100% |
| Delivered → Retainer | ≥ 40% |

## Metrics
- Count of leads at each stage today.
- Conversion ratio between every adjacent stage.
- Median days in each stage.
- Number of leads archived without paying.

## Evidence
- `dealix-ops-private/pipeline/pipeline_tracker.csv` headers match stages.
- Weekly scorecard updates reference live stage counts.
- Approval log shows the founder approved every outbound and proposal.

## Last Reviewed
2026-05-23
