# Revenue Forecast System
## Purpose
Estimate likely revenue based on pipeline, probabilities, and payment timing.
## Owner
Sami / Finance owner.
## Review Cadence
Weekly.
## Inputs
- pipeline_value.csv
- proposals
- follow-up dates
- probability
- expected close date
## Outputs
- expected cash
- weighted pipeline
- close risk
- follow-up priority
## Rules
- Forecast is not revenue.
- Only cash collected counts as cash.
- Proposal without decision-maker has low probability.
- No forecast without next action.
## Forecast Bands
- Conservative: high probability only.
- Base: weighted pipeline.
- Upside: all active proposals.
## Evidence
- revenue/pipeline_value.csv
- proposal notes
- payment follow-ups
