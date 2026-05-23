# Closing Playbook

> What the founder does between "proposal sent" and "payment received".
> Detailed scripts live in `sales/closing_playbook.md` (private repo).

## Stages Of A Close

```
Proposal Sent → Reviewed → Objections Surfaced → Resolved → Paid
```

Each stage has a default action + a default follow-up timing.

## Timing

| Day | Action |
|---|---|
| Day 0 | Send proposal (per `PROPOSAL_RULES.md`) |
| Day 2 | Soft check: "did this reach you OK?" |
| Day 5 | If silent: "any questions on the scope or timeline?" |
| Day 8 | If silent: founder voice note / call attempt |
| Day 14 | If silent: explicit "still considering or should we close this out?" |
| Day 21 | If silent: close as `closed_lost` with `no_decision` reason |

Aging is logged automatically in the pipeline tracker.

## Common Objections + Closes

### "Price is high"
- Reframe: cost of doing nothing (lost deals × deal size, founder hours)
- Offer Rung-down (Sprint instead of Managed Ops), don't discount the asked rung
- Show evidence pack — what they get for the money

### "Need to think about it"
- Ask: "Is there a specific concern, or is the timing wrong?"
- If concern: address specifically; if timing: propose a calendar date to revisit
- Never let it sit indefinitely — set the revisit date in the moment

### "Need to talk to my partner / team"
- Offer to send a one-page summary they can share
- Offer a joint 15-min call to walk through together
- Set a specific decision date

### "Can you do X custom?"
- Answer: "Not in our productized lineup. Here's what fits closest."
- Refer to `OFFER_LADDER.md` rung
- If they insist on custom: thank them, recommend a consultant referral, close as `closed_lost / not_productized`

### "Send me more info"
- This means: not now, polite-no
- Send the requested info once
- Schedule one follow-up at day 14
- Don't pursue further unless they re-engage

### "We're already working with X"
- Acknowledge respectfully
- Ask: "Would it be useful to look at this in 90 days when you have results from them?"
- Schedule the 90-day check-in
- Do not disparage the competitor

## Closing Heuristics

- **Always be willing to lose the deal.** If the buyer doesn't fit, walk away. The walk-away gives you leverage and protects the customer cohort.
- **Always state the price first, never apologize for it.** The price is the productized price.
- **Always ask for the close.** Don't leave the meeting without "shall we kick off Monday?"
- **Always document the decision.** Win or lose, log it the same day.

## What The Founder Brings To Every Close Call

- Restated buyer need (from discovery)
- Proposal PDF
- Evidence pack
- Calendar slot for kick-off (offer 2 dates)
- Invoice template ready (so payment can start immediately)
- Trust + governance one-liner

## Forbidden Closing Behaviors

- Fake urgency ("only 2 slots left this week" if not literally true)
- Fake scarcity ("price goes up Monday" if not literally true)
- Implying we have customers we don't have
- Bundling extras to close (cheapens the productized model)
- Discounting silently (every discount logged in `pricing_experiments.md`)
- Closing while feeling pressure to hit a number (signals → walk away)

## Post-Close Actions

When `paid`:
1. Log payment in `revenue/cash_collected.csv` (private)
2. Send tax invoice within 24 hours
3. Send kick-off message + calendar invite
4. Move stage to `paid`
5. Open delivery workspace per `docs/delivery/`

## Review Cadence

- Per close attempt: founder logs win/loss reason
- Weekly: % proposals → paid (target 35%)
- Monthly: objection pattern review — what's most common, what closes best

## What This Playbook Refuses

- Multi-month "nurture" sequences without explicit prospect consent
- Pressure tactics
- Buying / selling proxies for outcomes ("guaranteed leads")
- Letting a deal sit in proposal_sent stage > 21 days without resolution
