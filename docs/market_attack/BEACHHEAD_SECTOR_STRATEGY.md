# Beachhead Sector Strategy

> Dealix attacks one Saudi B2B sector at a time. The Beachhead is the
> sector where the *next 90 days* of sales, content, partner, and product
> energy will be concentrated.

## Why one sector

- Compounding proof: 5 wins in one sector beat 5 wins in 5 sectors.
- Authority follows depth, not breadth.
- Sales motion ramps faster when objections, vocabulary, and triggers
  repeat.
- Capital and founder time are scarce.

## Selection criteria (9 dimensions, 1-5 each)

| Dimension              | Question                                                          |
| ---------------------- | ----------------------------------------------------------------- |
| saudi_relevance        | How central is this sector to Vision 2030 / Saudi B2B?            |
| buyer_clarity          | Can we name the exact buyer title and where they live online?     |
| pain_urgency           | Is the pain bleeding now, or "nice to have"?                      |
| high_ticket_potential  | Can a single account pay 25k–100k SAR/year without friction?      |
| proof_fit              | Do our existing proofs / case studies map to this sector?         |
| delivery_fit           | Can current delivery capacity handle a win without breaking SLA?  |
| competition_gap        | Is there a clear, defensible white space?                         |
| channel_access         | Can we reach buyers via warm intros / partners / events / search? |
| trust_risk             | Inverse — high regulatory / PDPL risk lowers score                |

A `total_score` of **≥ 30** is the threshold to declare a beachhead.

## Process

1. Run `make beachhead-scorecard` to refresh the markdown report.
2. Founder reviews and locks the top sector for the next 90 days.
3. All campaigns, partner outreach, content angles, and strategic accounts
   in the next 90 days must list `sector = <locked beachhead>`.
4. At day 90, re-score and decide: **Hold**, **Expand**, or **Switch**.

## What changes when a beachhead is locked

- `growth/sector_targets.csv` reorders priority.
- Campaign factory only approves new campaigns whose `sector` matches.
- Authority engine generates posts/angles for the beachhead only.
- Strategic account list is pruned to the beachhead sector.
- Sales-asset factory generates one-pagers, samples, and proposals
  scoped to the beachhead.

## Anti-patterns (auto-flagged by verifier)

- Locking a beachhead with `total_score < 30`.
- More than one sector tagged `priority = P0` at the same time.
- Campaigns running against non-beachhead sectors without a `next_action`
  documenting why (e.g. opportunistic warm intro).
