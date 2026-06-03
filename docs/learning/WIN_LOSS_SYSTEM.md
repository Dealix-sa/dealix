# Win/Loss System

## Purpose
Turn every closed deal into a documented learning.

## Where
`dealix-ops-private/pipeline/win_loss_log.md`

## Format
Per deal:

```
## <Company> — <date> — <Won|Lost|Stalled>
- Offer: <rung>
- Score (at close): <0-100>
- Cause (Won): <why they bought>
- Cause (Lost): <why they didn't>
- Surprise: <one thing we didn't expect>
- System update: <what we changed in our system because of this>
```

## Cadence
- Daily: nothing required.
- Weekly: at least one entry per closed-this-week deal.
- Monthly: read all entries from the month; look for patterns.

## Pattern detection
- 3 losses with the same `Cause (Lost)` → adjust the operating system (cadence, proposal, pricing).
- 3 wins with the same `Cause (Won)` → double down on the angle.
- 5 stalls with the same cause → consider retiring that funnel.

## Anti-bias
- Don't blame the buyer in the Cause section unless the data supports it.
- Capture the actual decision criterion the buyer cited, not what we hoped it was.

## Sharing
- Anonymized excerpts can move to `content/proof_library.md` after Trust workflow approval.
