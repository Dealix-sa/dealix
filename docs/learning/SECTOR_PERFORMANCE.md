# Sector Performance

> Which sectors actually convert. Drives ICP weights + playbook investment.

## Storage

`learning/sector_performance.csv` (private):

```
sector, period, leads_sourced, qualified, replies, calls_booked, proposals_sent, sprints_sold, sprints_delivered, retainers_signed, cash_collected_sar, avg_deal_size, avg_days_to_close
```

## Monthly Review

```markdown
# Sector Performance Review — YYYY-MM

## Leaderboard
| Sector | Leads | Qualified | Replies | Calls | Proposals | Wins | Cash SAR |
|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... |

## Conversion By Sector
| Sector | Lead→Qual | Qual→Reply | Reply→Call | Call→Prop | Prop→Win |
|---|---|---|---|---|---|
| ... | ___% | ___% | ___% | ___% | ___% |

## Decisions
- Double down on: _____
- Maintain: _____
- Reduce: _____
- Stop: _____
```

## Promotion Rule (Tier 2 → Tier 1)

A sector earns Tier 1 status when:
- ≥ 3 paid sprints delivered
- Average conversion rate ≥ benchmark across funnel
- A sector playbook exists with shipped-sprint evidence
- Trust posture clean (no incidents in that sector)

## Demotion Rule (Tier 1 → Tier 2 → Off)

A sector loses Tier 1 status when:
- < 1 paid sprint in 90 days
- Reply rate < 5% for 60 days
- Recurrent trust friction (suppression rate above baseline)

## ICP Weight Update Trigger

When a sector shifts tier, update `ICP_SCORING_MODEL.md` weights:
- Promoted sector: +5 to "active in sector we have proof in"
- Demoted sector: re-weighted in next quarterly recalibration

## Cohort Analysis (when n ≥ 5)

Track per sector:
- LTV (Managed Ops cohort, 6+ months retention)
- Time to first cash
- Margin per rung
- Referral generation rate
- Case-study consent rate

## Anti-Patterns

- Chasing a sector with one early win as "proven"
- Abandoning a sector after one bad month
- Switching sectors weekly (no compounding)
- Mixing sector data without segmentation
- Treating "interesting" as "convertible"

## What This Refuses

- Sector decisions without data (or with n < 5)
- Allowing a Tier 1 sector to coast (rule: ship a sprint or lose status)
- Letting sector strategy override 90-day focus
- Pretending sector trends are stable in < 90 days
