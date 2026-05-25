# Growth Model

> A growth model is a sentence with numbers in it. If it is just words,
> it is a wish.

## The Sentence

> Founder-led outbound at **25 named DMs / week** yields **4–6 replies**,
> **2 samples sent**, **1 proposal**, and **1 paid sprint every 2 weeks**.
> Each paid sprint converts to a retainer with probability **0.3–0.5**.
> Retainers contribute **5–10K SAR MRR** each, with churn < **10% / quarter**.

That sentence is the model. Every assumption in it is a target. Every
variance from it is a learning.

## The Math (target steady state, month 3)

| Stage | Conversion target | Volume |
|-------|-------------------|--------|
| Named DMs / month | — | 100 |
| Replies | 20% | 20 |
| Samples sent | 50% of replies | 10 |
| Calls booked | 50% of samples | 5 |
| Proposals sent | 60% of calls | 3 |
| Paid Sprints | 50% of proposals | 1.5 |
| Retainer asks made | 100% of sprints | 1.5 |
| Retainers signed | 40% of asks | 0.6 |

Monthly cash: ~6,750 SAR from sprints + 3–6K SAR new MRR.

By month 6 (4 active retainers + 2 sprints/month):
- Sprints: ~10,000 SAR/month
- MRR: ~25,000–40,000 SAR
- Total monthly revenue: 35,000–50,000 SAR

## The Levers

In priority order:

1. **Reply rate** — driven by ICP precision + hook quality.
2. **Sample → call rate** — driven by sample relevance.
3. **Proposal close rate** — driven by sample → proposal continuity.
4. **Retainer ask rate** — driven by sprint quality + delivery moment.
5. **Volume of DMs** — last lever, not first. Volume on bad targeting
   loses money.

## Bottleneck Detection

If the model is missing target, find the **first** stage where actuals
deviate > 30% from target. Fix that stage before optimising downstream
stages.

```
DMs ──► Replies ──► Samples ──► Calls ──► Proposals ──► Paid ──► Retainers
   ▲          ▲           ▲          ▲             ▲          ▲
   │          │           │          │             │          │
   │          │           │          │             │          └─ retainer quality
   │          │           │          │             └─ proposal-sample fit
   │          │           │          └─ call quality
   │          │           └─ sample relevance
   │          └─ hook + ICP fit
   └─ volume + targeting
```

## Anti-Patterns

- Increasing DM volume to fix a low reply rate (reply rate is a quality
  problem, not a volume problem).
- Adding new channels before reply rate is solved.
- Treating "we got a deal" as evidence the model is healthy. One deal
  is not a model. Three sprints with retainer conversion is.

## Quarterly Update

Every quarter:
1. Refit the model to the last 90 days of actuals.
2. Decide which conversion rate moved enough to update the assumption.
3. Record the change in the Monthly Strategy Review.
