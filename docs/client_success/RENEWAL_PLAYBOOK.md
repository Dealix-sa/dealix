# Renewal Playbook

> Run for every Managed Ops cycle (monthly auto-renewal with explicit notice).

## Renewal Cadence

- Notice sent 7 days before each cycle: "Just confirming month {N+1} starts {date}"
- Cycle starts only after invoice paid
- 30-day notice to cancel any time

## Standard Renewal (months 1 → 12)

Each month:
- 7 days before cycle end: send confirmation email
- Includes: scope unchanged, price unchanged, link to invoice
- Client confirms by paying the invoice
- No silent auto-charge — explicit invoice every month

## Tier Move Renewal (2,999 → 4,999)

Triggered when:
- Client signals expansion (more prospects, more sectors, etc.)
- OR founder identifies clear capacity for upgrade

Process:
1. Founder writes 1-page "upgrade rationale" — what they get for +2K/mo
2. Client review + decision (1 week)
3. New contract → first 4,999 invoice → new cycle starts

## Annual Renewal Discussion (month 12)

- 30 days before: schedule annual review (60 min)
- Review:
  - 12 months of activity (deliverables, wins, learnings)
  - Health score trajectory
  - What changed in their business
  - What they need next 12 months
- Outcome options:
  - Continue Managed Ops at current tier
  - Expand to 4,999 tier
  - Move to Revenue Desk (Custom AI)
  - Annual prepay (10% discount per `PRICING_STRATEGY.md`)
  - Graceful wind-down

## Renewal Refusal

We may decline to renew if:
- Client repeatedly bypasses approval gates (Trust risk)
- Client wants scope changes that violate productized model
- Client has consistently low health score (< 40 for 4+ weeks)
- Founder bandwidth at cap and other clients better fit growth

Decline gracefully:
- 30-day notice
- Clean handoff with full deliverables
- No bad-mouthing
- Logged in `clients/{client}/STATUS.md` as `declined_renewal`

## Annual Prepay

- 10% discount if all 12 months paid up front
- Cash collected immediately
- Pro-rated refund per `BILLING_POLICY.md` if cancelled mid-year
- Trust posture remains identical

## Renewal Metrics

- Monthly renewal rate: target ≥ 95%
- Annual renewal rate (month 12 active → month 13 active): target ≥ 75%
- Expansion rate at renewal: target ≥ 25%
- Renewal-triggered upsell to Revenue Desk: track count

## What This Refuses

- Auto-charge without notice
- Annual lock-in without prepay option
- Last-minute price changes at renewal
- "Renewal discount" pressure (no discounts at renewal — same price or upgrade)
- Renewing clients who are clearly poor fit (we don't optimize for short-term MRR)
