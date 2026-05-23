# Experiment Engine v2

## Relationship to existing docs
Provides the evidence loop that the rest of the v2 distribution layer relies on:
- `docs/distribution/DISTRIBUTION_PORTFOLIO_V2.md` — weekly Double Down / Maintain / Fix / Kill / Defer decisions consume experiment results.
- `docs/founder/REVENUE_WAR_ROOM_V2.md` — every closed week must include at least one experiment decision.

Aligns with the constitutional principle "no growth without governance" from `docs/00_constitution/NON_NEGOTIABLES.md`.

## Purpose
Run controlled experiments across sectors, channels, messages, offers, samples, and pricing.

## Experiment Types
- sector
- buyer title
- message angle
- CTA
- channel
- sample type
- follow-up cadence
- offer price
- proposal format

## Required Fields
- hypothesis
- target segment
- sample size
- metric
- threshold
- result
- decision
- next action

## Minimum Experiment Size
- 25 outreach actions for early signal.
- 100 leads for sector signal.
- 3 samples for sample quality signal.
- 2 proposals for pricing signal.

## Success Metrics
- reply rate
- positive reply rate
- sample request rate
- proposal rate
- payment conversion
- opt-out / complaint rate
- time to next action

## Rule
Do not scale a channel without experiment evidence.

## Log
Experiment results land in `distribution/experiment_log.csv` (private ops), seeded by `scripts/init_private_ops.sh` with the header:
`date,hypothesis,segment,channel,message_angle,sample_size,metric,threshold,result,decision,next_action`
