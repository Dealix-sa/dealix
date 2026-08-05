# Pipeline Stages

## Purpose
Define a single source of truth for sales pipeline stages and stage transitions.

## Owner
Sami / Founder CEO.

## Review Cadence
Daily (movement); weekly (definition).

## Stages

| # | Stage | Definition | Exit Criteria |
|---|-------|------------|---------------|
| 0 | Added | Lead exists in pipeline_tracker.csv with next_action set | First touch attempted |
| 1 | Contacted | First outbound (DM, email, intro) sent | Reply received OR followup #2 sent |
| 2 | Replied | Lead responded; intent captured | Discovery call booked OR explicit no-go |
| 3 | Called | Discovery call completed; notes saved | Proposal scoped |
| 4 | Proposal | Proposal sent with price, scope, follow-up date | Verbal/written intent confirmed |
| 5 | Won | Payment received OR PO/written approval received | Delivery starts |
| 6 | Delivering | Active delivery (sprint/data pack/managed ops) | QA passed and handoff sent |
| 7 | Retainer | Converted to recurring (Managed Ops / Custom AI) | Renewal cycle owned |
| L | Lost | Disqualified or chose not to proceed | Reason logged |

## Mandatory Fields per Lead
- lead_id
- name
- sector
- source
- stage
- next_action
- next_action_date
- owner
- evidence_link (or proof reason)
- notes

## Rules
- A lead without `next_action` is invalid (caught by daily CLI).
- A lead cannot skip from Added to Won.
- Stage 5 (Won) requires payment, PO, or written approval logged in revenue/cash_collected.csv or revenue/pipeline_value.csv.
- Stage 6 (Delivering) requires linkage to a Delivery Control entry.
- Lost leads keep a reason so the learning loop can use them.

## Last Reviewed
2026-05-23
