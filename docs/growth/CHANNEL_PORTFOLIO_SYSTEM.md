# Channel Portfolio System

**Owner:** Operations + Founder
**Source of truth:** This doc + `docs/intelligence/OFFER_CHANNEL_FIT_SYSTEM.md`

## Purpose

The Channel Portfolio System maintains the whitelist of sanctioned distribution channels, monitors per-channel health, allocates capacity across channels, and pauses channels that fall below health thresholds. It is the meta-layer that all other distribution machines obey.

If a channel is not in the portfolio, Dealix does not use it. If a channel's health falls, Dealix pauses it. No exceptions.

## Active channels

| Channel | Use | Status |
|---|---|---|
| LinkedIn DM (warm) | Persona-first outreach with shared context | Active |
| LinkedIn DM (cold) | Persona-first outreach without shared context (capped) | Active, capped |
| Founder-to-founder intro | Highest-trust path; direct Founder activity | Active |
| Referral (customer, peer) | Inbound through trusted introducer | Active |
| Sector event intro | In-person or virtual event-anchored introduction | Active |
| Partner pass-through | Inbound from active partners | Active |
| Contact Form (website) | Inbound from Dealix website | Active |
| Email (warm) | Post-warm-context email to opted persona | Active |
| LinkedIn content (organic) | Founder-voice posts | Active |
| Email broadcast (opted-in) | Periodic update to opted-in audience | Active |

## Channels NOT in the portfolio

| Channel | Why excluded |
|---|---|
| WhatsApp cold | Category rule; PDPL and CITC norms; reputation risk |
| SMS cold | Category rule; CITC norms |
| Email cold (mass) | Category rule; deliverability and trust risk |
| Phone cold | Category rule for launch stage; revisit case-by-case for ABM only with Founder approval |
| Paid display retargeting at named individuals | PDPL friction; trust posture |
| Scraped contact databases | Category rule, absolute |
| LinkedIn automation tools | Platform terms; trust posture |
| Reddit, Discord, niche forums (cold) | Community-norm violation |

## Channel health metrics

Each active channel is monitored on:

| Metric | Threshold |
|---|---|
| Deliverability / acceptance rate | >= 95 percent |
| Reply rate | observed; baseline per channel |
| Negative signal rate (flag, block, opt-out, spam report) | <= 1 percent |
| Platform health (LinkedIn account flags, email blocklist appearances) | 0 |

A channel that breaches the negative-signal threshold or shows platform health issues is paused immediately by the Channel Portfolio System.

## Channel capacity allocation

Capacity is allocated per channel per operator per day:

| Channel | Daily cap per operator |
|---|---|
| LinkedIn DM (warm) | 10 |
| LinkedIn DM (cold) | 3 |
| Email (warm) | 15 |
| Founder-to-founder | Founder discretion |
| Partner pass-through | No cap (response-driven) |
| Contact Form response | No cap (response-driven, <= 1 business day SLA) |

Caps are designed to fit the Founder's approval throughput. Higher caps require explicit Founder approval and a capacity plan.

## Channel rebalancing

Quarterly review:

- Which channels produced the most replies?
- Which channels produced the most converted sprints?
- Which channels had the lowest negative-signal rate?

Allocation is adjusted toward winning channels. Underperforming channels are not removed automatically — Dealix maintains channel diversity even at the cost of efficiency, because over-concentration on one channel is fragile.

## Adding a channel

A new channel enters the portfolio only after:

1. Founder-approved trial (typically 30-60 day pilot, low volume).
2. Trust gate definition (which approval class).
3. Health metrics defined and baselined.
4. Documentation added to this portfolio.
5. Founder + Strategy Office A2 sign-off.

## Removing a channel

A channel is removed from active status when:

- Health threshold breach unresolved after 30 days.
- Category rule violation (e.g., a tool we used updates to require scraping).
- Founder strategic decision.

Removal requires A2 sign-off and a documented reason.

## Source of truth

This doc + the channel health dashboard.

## Approval class

- **A1** — Channel health monitoring.
- **A2** — Channel pause/resume; channel addition/removal.
- **A3** — Public statement about Dealix channel posture.

## Trust gate

- No channel operates outside its documented capacity.
- No channel operates while paused.
- Negative signals trigger immediate pause; resume only after root-cause analysis.

## Owner

- **Code owner:** Operations Engineering (monitoring dashboard).
- **Operational owner:** Operations Lead + Founder.

## Worker script (placeholder)

`workers/channel_portfolio_worker.py` (planned). Runs hourly; aggregates channel health metrics; pauses/resumes channels per rules.

## KPI

| Metric | Target |
|---|---|
| Channel-pause response latency (breach to pause) | <= 1 hour |
| Whitelist compliance (no non-whitelist channel used) | 100 percent |
| Channel diversity index (no channel > 40 percent of outbound volume) | < 0.4 concentration |
| Quarterly rebalance completion | 100 percent |

## Failure mode

- A non-whitelist channel slips into use.
- Channel concentration exceeds 40 percent (fragility).
- A channel breaches health threshold and continues running.
- Capacity caps are bypassed because "the Founder said it's fine just this once."

## Recovery path

1. Pause the offending channel.
2. Audit the past 30 days.
3. Re-enforce caps and whitelist at the queue layer.
4. Document any one-time Founder override in a written exception log; do not normalize.

## What this system does NOT do

- It does not pre-approve channels in bulk.
- It does not auto-launch new channels without Founder sign-off.
- It does not override per-machine approval gates.

## Cross-links

- Distribution War Machine: `docs/growth/DISTRIBUTION_WAR_MACHINE.md`
- Offer-channel fit: `docs/intelligence/OFFER_CHANNEL_FIT_SYSTEM.md`
- Approval policy: `docs/05_governance_os/APPROVAL_POLICY.md`
- WhatsApp boundary: `docs/02_saudi_positioning/WHATSAPP_BOUNDARY.md`

## Disclaimer

Dealix does not guarantee channel performance or reply rates. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
