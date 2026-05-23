# Lead Intelligence Base OS

## Purpose
Build a large Saudi B2B opportunity intelligence base separate from the active sales pipeline.

## Scale Targets
- 500 leads across 5 sectors in first phase.
- 1,000 leads after first signals.
- 5,000 leads only after data quality and suppression controls are stable.

## Difference Between Intelligence Base and Pipeline

### Intelligence Base
- Broad market map.
- Researched companies.
- Fit scores.
- Sector tags.

### Pipeline
- Active leads approved for outreach.
- Next action.
- Follow-up state.
- Commercial status.

## Rules
- Intelligence base can scale aggressively.
- Outreach must scale carefully.
- Suppression list must be checked before outreach.
- Every lead has a source.
- Every A lead has a reason.

## Schema — `lead_intelligence_base.csv`
`company,sector,website,country,city,business_type,offer,buyer_titles,public_contact_path,source,fit_score,priority,status,last_researched,last_contacted,reply_status,next_action`

## Promotion Path
Intelligence Base (A-priority + approved) → Pipeline → Outreach Send Queue → Reply Routing → Sample/Proposal → Payment Capture.

## Evidence
- `private-ops/intelligence/lead_intelligence_base.csv`
- `private-ops/pipeline/pipeline_tracker.csv`
