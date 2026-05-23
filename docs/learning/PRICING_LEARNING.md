# Pricing Learning — تعلّم التسعير

## Purpose
Log every pricing experiment, decision, and observation. Build the empirical basis for sprint pricing rather than guessing at willingness-to-pay.

## Owner
Founder.

## Inputs
- Pricing proposals per deal.
- Negotiation outcomes (price held, discounted, lost).
- Win-loss review data.
- Renewal pricing patterns.

## Outputs
- Pricing experiment register entries.
- Quarterly pricing summary.
- Recommended pricing band per sector and deal size.

## Rules (numbered)
1. Every pricing decision outside the published band is logged.
2. Discounts are logged with reason, magnitude, and outcome.
3. Pricing experiments follow `EXPERIMENT_SYSTEM.md`.
4. Pricing data is private (under `dealix-ops-private/`); only sector-aggregated bands appear in public.
5. No public claims about "average deal size" without a sample size and date.

## Metrics
- Price-held rate per quarter.
- Median discount magnitude when discount granted.
- Renewal price held vs initial sprint price.
- Pricing experiments closed per quarter.

## Cadence
Updated continuously. Reviewed quarterly.

## Evidence (paths)
- `dealix-ops-private/pricing/decisions/`
- `docs/learning/registers/pricing_summary/<quarter>.md` (anonymized aggregate).

## Verifier
Founder.

## Runtime Command
`make learning.pricing.log DEAL=<id>` opens a pricing decision entry.

## Pricing decision entry

```
Deal ID: <id>
Date: YYYY-MM-DD
Sector: <code>
Geo: <country/region>
Buyer size band: <employees>
Proposed price (SAR): <number>
Final price (SAR): <number>
Discount magnitude: <percent>
Discount reason: <choice>
Outcome: closed-won | closed-lost | open
Renewal price (if renewal): <number>
Notes: <one paragraph>
```

## Discount reasons (controlled list)

- First sprint with a new client (acceptable, bounded discount).
- Multi-sprint commitment (acceptable, documented in SOW).
- Strategic sector entry (acceptable, A3 approval required).
- Competitive pressure (logged, founder reviews pattern).
- Operator error in scoping (logged as defect).
- Client budget constraint (logged; pattern triggers band review).

## Pricing experiments

Pricing experiments must follow the experiment system. Example hypothesis: increasing first-sprint price by 15 percent in sector X will hold close rate within 10 percent of baseline, over the next 8 deals in that sector.

Kill rule: close rate drops by more than 25 percent at midpoint (4 deals).

## Quarterly pricing summary

Each quarter, the founder produces an anonymized summary:

- Price-held rate (deals closed at proposed price).
- Median discount when granted.
- Discount-reason frequency table.
- Sector pricing bands (P25, P50, P75 of closed prices).
- Renewal pricing pattern.
- Recommendation on pricing band updates.

## Operating substance
Pricing is the operating variable most often set by guess and least often updated by evidence. Dealix uses the pricing learning register to build evidence over deals so the next price proposal references data rather than instinct.

The discipline of logging every discount with a controlled reason is what makes the data useful. Without controlled reasons, every discount becomes "client requested" and no pattern emerges. With controlled reasons, the founder can see whether discounts are operator-driven (a process problem), sector-driven (a positioning problem), or strategic (an investment).

Pricing experiments are higher-stakes than message or scoring experiments because they affect revenue directly. The kill rule must trigger quickly. We do not run pricing experiments for a full quarter without midpoint checks.

Public claims about pricing are bounded by sample size and date. We do not say "our average sprint is SAR X". We say "across N closed sprints in sector S during period P, the price band was X to Y".

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
