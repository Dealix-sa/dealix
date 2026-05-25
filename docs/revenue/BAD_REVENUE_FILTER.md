# Bad Revenue Filter

> Money is not a synonym for revenue. Some money costs more than it pays.

## What counts as bad revenue

A deal is "bad revenue" if **any one** of these is true:

1. The customer is outside ICP and would never repeat.
2. Delivery requires a one-off process we cannot template.
3. The price is below the floor in `REVENUE_MODEL.md`.
4. Delivery would require a trust exception (overclaim, fake guarantee,
   private data leak risk).
5. The customer's payment behaviour at quote stage is hostile (refuses
   PO, demands net 90, refuses written scope).
6. The customer requires an AI agent autonomy level above current policy.
7. The customer's industry is on the explicit refusal list (gambling,
   regulated finance without compliance counsel, political campaigning).

## The Bad Revenue Cost Equation

```
True cost of a deal =
    founder hours × opportunity cost per hour
  + cash cost of tools
  + trust risk (incident probability × incident cost)
  + scope creep risk
  - learning value
  - moat value
```

A deal is bad revenue when the True Cost > revenue collected, even if
revenue collected is non-zero.

## The Founder Refusal Script

> "We appreciate the interest. Based on what you have described, we are
> not the right fit because [specific reason]. We can refer you to
> [option] if that helps."

Refusal scripts go in `docs/sales/`.

## Why we refuse

- Bad revenue trains the wrong delivery muscles.
- Bad revenue produces no case study and no referral.
- Bad revenue absorbs founder hours away from compounding work.
- Bad revenue creates trust incidents that damage future deals.

## Approved exceptions

A deal that fails the filter may still be taken **only** with:

- Founder Go decision via `GO_NO_GO_DECISION_SYSTEM.md`
- A named strategic reason (e.g. anchor case study)
- A documented reversal trigger
- An explicit time-box

## Logging refusals

Every refused deal is logged with:

- Account, date
- Reason refused
- Estimated revenue declined
- Referral made (yes/no, to whom)

Tracked in `dealix-ops-private/sales/refusals.csv`.

## Review

Monthly: count refusals, estimated revenue declined, and learn from the
**pattern** of who is asking us for things we refuse. Pattern = ICP signal.
