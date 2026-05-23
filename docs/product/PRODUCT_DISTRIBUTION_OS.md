# Product Distribution OS

The Product Distribution OS defines how Dealix products move from the founder's announcement to a paying client. It is the path from rung-zero awareness to rung-1 sample.

**Source of truth:** `$PRIVATE_OPS/distribution_state.csv`
**Owner:** Founder + Marketing Lead
**Trust gate:** A2 — distribution channels, partner contracts, and paid distribution require founder approval.

## Channels

| Channel | Type | Owner | Cost basis |
|---------|------|-------|-----------|
| Founder-led content | Owned | Founder | Time |
| Newsletter | Owned | Marketing Lead | Time + tool |
| Sector reports | Owned | Marketing Lead | Time |
| Direct introductions | Earned | Customer Success Lead | Relationship |
| Partner channel | Earned | Partner Lead | Revenue share |
| Conference / event | Earned | Founder | Time + travel |
| Paid media | Paid | Marketing Lead | SAR (capped) |

Cold automation (bulk DM sequences, scraped lists, automated LinkedIn invites) is not a Dealix distribution channel.

## Cadence

| Channel | Cadence |
|---------|---------|
| Founder-led content | 2-3 posts per week (`docs/marketing/FOUNDER_LED_CONTENT_SYSTEM.md`) |
| Newsletter | Weekly (`docs/marketing/NEWSLETTER_SYSTEM.md`) |
| Sector reports | Monthly (`docs/marketing/SECTOR_REPORT_SYSTEM.md`) |
| Partner enablement | Quarterly briefing |
| Paid media | Campaigns with explicit budget caps |

## From channel to sample

1. A prospect engages with a channel artifact.
2. Self-served signup or DM lands in the inbound queue.
3. Reply Routing System classifies (`docs/revenue/REPLY_ROUTING_SYSTEM.md`).
4. Revenue Lead qualifies; if ICP fit, opportunity is promoted to Sample Factory queue (`docs/revenue/SAMPLE_FACTORY.md`).
5. Sample is produced, approved (A1), and delivered.

The end-state of distribution is a delivered sample, not a closed deal.

## Attribution

Every distribution artifact carries a tracking convention so that the Sample Factory queue knows the entry channel. Attribution is in `$PRIVATE_OPS/attribution_log.csv`. Attribution is for internal learning; it is not published externally unless aggregated and anonymised.

## Paid media guardrails

| Guardrail | Threshold |
|-----------|-----------|
| Monthly paid spend cap | configured in `$PRIVATE_OPS/distribution_budget.csv` |
| Per-campaign cap | configured per campaign |
| Allowed networks | listed in distribution policy |
| Required disclosures | "Paid promotion" tag on every paid post |

A change to caps requires founder approval (A2).

## Failure modes

- **Channel violation:** an outbound message is sent through a banned channel (cold DM, scraped list). Detection: policy engine + audit. Recovery: stop, apologise, log root cause.
- **Attribution loss:** an inbound arrives with no tracked channel. Detection: nightly job. Recovery: best-effort reconstruction; the row is flagged unattributed, not silently bucketed.
- **Budget breach:** paid spend exceeds cap. Detection: real-time monitor. Recovery: pause campaign; founder approves any further spend.

## Recovery path

If distribution data is corrupted, the founder freezes new paid campaigns until attribution is reliable. Owned channels continue at reduced cadence.

## Metrics

- Inbound leads by channel (estimated).
- Sample-Factory conversion by channel (estimated).
- Paid spend vs budget by month (verified).
- Cost per sample by channel (estimated; see `docs/finance/AI_UNIT_ECONOMICS_SYSTEM.md`).

## Disclaimer

Distribution increases the chance of conversation; it does not guarantee revenue. Estimated value is not Verified value.
