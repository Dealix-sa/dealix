# Account Scoring Model

**Owner:** Strategy Office + Operators
**Source of truth:** This doc + `docs/intelligence/ICP_SEGMENTATION_SYSTEM.md` + `docs/intelligence/TRIGGER_EVENT_SYSTEM.md`

## Purpose

Account scoring assigns a numeric score (0-100) to every candidate account in active sectors, and assigns each account to a tier. The score drives where operator attention goes this week.

## Scoring model (0-100)

The score is the weighted sum of four pillars.

| Pillar | Max points | What it measures |
|---|---|---|
| ICP fit | 40 | How closely the account matches the active ICP definition |
| Trigger strength | 25 | Volume and recency of qualified triggers |
| Buyer access | 20 | Identifiability and reachability of the named persona |
| Offer-channel fit | 15 | Whether a Dealix sprint cleanly maps to the account's likely pain |

Sum = 100 max.

## ICP fit (0-40)

| Sub-criterion | Points |
|---|---|
| Sector matches active Tier-A or Tier-B sector | 10 |
| Company size within ICP band | 8 |
| Revenue band within ICP band | 6 |
| Geography matches | 4 |
| Sales motion compatible | 4 |
| Tech maturity compatible | 4 |
| Trust posture compatible (audit-conscious, founder-led) | 4 |

## Trigger strength (0-25)

| Sub-criterion | Points |
|---|---|
| At least one qualified trigger in last 30 days | 10 |
| Two or more compounding triggers in last 90 days | 8 |
| Capital trigger (funding, M&A) in last 90 days | 4 |
| Talent trigger (new HoS, new GTM) in last 90 days | 3 |

## Buyer access (0-20)

| Sub-criterion | Points |
|---|---|
| Named persona individual identified (LinkedIn or public source) | 8 |
| At least one sanctioned channel to reach them (LinkedIn, referral, event) | 6 |
| Founder-to-founder warm path available | 4 |
| At least one prior touchpoint logged (peer mention, event greeting) | 2 |

## Offer-channel fit (0-15)

| Sub-criterion | Points |
|---|---|
| One Dealix sprint clearly maps to account's likely pain | 8 |
| Price band fits the account's likely budget | 4 |
| Sprint duration fits the account's likely decision speed | 3 |

## Tier assignment

| Tier | Score | Action |
|---|---|---|
| Tier A | 75-100 | Active engagement; weekly persona-tailored outreach |
| Tier B | 55-74 | Nurture; monthly content touch, watch for new triggers |
| Tier C | 35-54 | Monitor; quarterly check |
| Out | 0-34 | Park; do not engage unless trigger upgrade |

## Tier counts (caps)

| Tier | Max active count per operator |
|---|---|
| Tier A | 25 |
| Tier B | 75 |
| Tier C | Unlimited (passive) |

If Tier A exceeds 25, the operator is over-extended. Force the bottom-scoring accounts down to Tier B.

## Scoring cadence

| Activity | Frequency |
|---|---|
| Full rescore for active sectors | Weekly |
| Trigger decay (90+ day) | Weekly |
| ICP fit re-evaluation | Monthly |
| Buyer access re-confirmation (still in role?) | Monthly |
| Offer-channel fit recalibration | Per sprint |

## Anti-patterns

1. Inflating an account's score because the founder wants to chase it.
2. Holding an account in Tier A for 6 months without a sprint conversation.
3. Counting an unqualified trigger toward Trigger Strength.
4. Scoring an out-of-ICP account into Tier A on Trigger Strength alone.

## Trust gate

| Action | Approval class |
|---|---|
| Internal rescore | A1 — Operator |
| Manual tier override (against rubric) | A2 — Founder + Operator |
| Adding a new scoring sub-criterion | A2 — Founder + Strategy Office |

## Scoring artifact format

Each active account carries a scoring record:

```
account_id: ACME-001
sector: cybersecurity_b2b
icp_fit: 36/40
trigger_strength: 18/25
buyer_access: 16/20
offer_channel_fit: 12/15
total: 82/100
tier: A
last_scored: 2026-05-18
notes:
  - Qualified trigger: new Head of Sales announced 2026-04-22 (LinkedIn public)
  - Persona: Head of Sales identified
  - Sprint mapping: Trigger Activation Sprint
```

This record lives in the operator's account tracker, not in this doc.

## Failure mode

- Scoring rubric is bypassed; tier is set by feel.
- Stale scores drive this week's outreach.
- Operator Tier A list balloons to 50; nothing gets adequate attention.

## Recovery path

1. Re-run the weekly scoring with the documented rubric.
2. Force Tier A back to the cap.
3. Re-evidence any manual override with a written justification line.

## Disclaimer

Account scores are directional, not predictive. A high score does not guarantee response, meeting, or conversion. Dealix does not guarantee revenue from any scored account. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
