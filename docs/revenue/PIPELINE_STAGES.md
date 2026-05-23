# Pipeline Stages

The seven stages a lead moves through. Every lead in the pipeline tracker is in exactly one of these stages.

## Purpose
Standardise the language of the pipeline so the founder, the AI, and the pipeline tracker all speak the same vocabulary. Movement between stages is the only valid signal of progress.

## Owner
Sami (Founder).

## Review Cadence
Weekly, during the Weekly CEO Review.

## Inputs
- Lead data from outreach loops.
- Reply data from outbound channels.
- Proposal acceptance / rejection events.
- Payment events from the cash ledger.

## Outputs
- A pipeline tracker where every row has exactly one stage from this list.
- A weekly stage-movement report (counts moving from one stage to the next).
- A retainer eligibility list (customers who became Retainer this month).

## Rules
- A lead cannot skip a stage. Replied must come before Proposal Sent.
- A lead cannot regress without a logged reason in the notes column.
- A lead with no movement in 14 days is auto-flagged for founder review.
- A Paid lead must produce a Delivered artifact within the SLA of the offer rung.

## Metrics
- Count of leads per stage.
- Conversion rate stage to stage.
- Average days in stage.
- Volume reaching Retainer per quarter.

## Evidence
- `pipeline/pipeline_tracker.csv` (private ops) tagged by stage.
- Stage-movement log per week.
- Proposal files, payment confirmations, delivery files, retainer agreements.

## The Seven Stages

### 1. New
- A lead has been added to the tracker.
- No outbound action taken yet.
- Has: company, sector, contact, source.

### 2. Contacted
- The first outbound message has been sent.
- Date and channel of contact logged.
- No reply yet.

### 3. Replied
- The lead replied to outreach.
- Reply content captured.
- Founder has chosen the next action (qualify, propose, or drop).

### 4. Proposal Sent
- A proposal has been sent, mapped to a rung of the offer ladder.
- Proposal file linked.
- Decision date set.

### 5. Paid
- Payment has been received.
- Invoice and receipt logged.
- Delivery loop kicked off.

### 6. Delivered
- The deliverable for the paid rung has been handed over.
- Proof Pack linked.
- Customer satisfaction signal captured (good, mixed, bad).

### 7. Retainer
- Customer has paid for two or more cycles of an ongoing rung (Data Pack, Managed Ops, Dealix OS).
- Retainer agreement signed and logged.
- Quarterly review scheduled.

## Last Reviewed
2026-05-23
