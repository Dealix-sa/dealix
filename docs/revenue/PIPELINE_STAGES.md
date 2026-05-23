# Pipeline Stages — Operating Definitions

> The schema for `pipeline/pipeline_tracker.csv` (private repo).
> If you change a stage name or definition here, you must migrate the tracker.

## Schema

```
lead_id, name, company, sector, fit_score, source, stage, stage_entered_at, last_action_at, owner, value_sar, notes
```

## Stage Enum

```
lead
qualified
contacted
replied
sample_sent
call_booked
proposal_sent
paid
delivered
retainer
closed_lost
suppressed
```

## Stage Aging Rules

| Stage | Max age before action required |
|---|---|
| lead | 7 days |
| qualified | 7 days |
| contacted | 14 days (after last message) |
| replied | 3 days |
| sample_sent | 14 days |
| call_booked | 7 days (before call) / 7 days (after, for proposal) |
| proposal_sent | 21 days |
| paid | 1 day (kick off delivery) |
| delivered | 14 days (open retainer convo) |
| retainer | n/a (renewal cycle managed in client_success) |

A row exceeding max age without `last_action_at` update gets flagged in tomorrow's Daily Brief.

## Stage Transitions (allowed)

```
lead → qualified → contacted → replied → sample_sent → call_booked → proposal_sent → paid → delivered → retainer
   ↓        ↓          ↓          ↓           ↓             ↓               ↓
suppressed (from any stage on disqualifier / opt-out)
   ↓        ↓          ↓          ↓           ↓             ↓               ↓
closed_lost (from any post-contacted stage on prospect rejection)
```

No skipping. No reverse moves (except contacted → suppressed on opt-out).

## Value Estimation Per Stage

| Stage | Value used for forecasting |
|---|---|
| lead | 0 (don't forecast pre-qualified) |
| qualified | 0 (still uncommitted) |
| contacted | 0 |
| replied | 0 |
| sample_sent | 10% × expected deal size |
| call_booked | 25% × expected deal size |
| proposal_sent | 50% × expected deal size |
| paid | 100% × deal size |
| delivered | 100% (recognized) |
| retainer | monthly value × expected retention months |

Expected deal sizes (use these defaults; override per row when known):
- Sprint: SAR 499
- Data Pack: SAR 1,500
- Managed Ops: SAR 2,999 × 12 = SAR 35,988 LTV
- Custom AI: SAR 50,000 average annual

## Stage Move Logging

Every stage move must include:
- `prior_stage`
- `new_stage`
- `transition_reason` (one phrase)
- `transition_timestamp`
- `transition_owner` (founder or agent name)

The transition log is appended to `pipeline/stage_transitions.csv` (private).

## Forbidden

- Editing `stage_entered_at` after the fact
- Removing rows (use `suppressed` or `closed_lost` instead)
- Setting stage to a future state (paid before payment confirmation)
- Stage moves without `last_action_at` update

## Review Cadence

- Daily: flagged-aging rows reviewed in Brief
- Weekly: average age per stage; identify slow stages
- Monthly: stage transition reasons — what patterns?
