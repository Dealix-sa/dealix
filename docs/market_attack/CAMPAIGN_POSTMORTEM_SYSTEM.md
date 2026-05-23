# Campaign Postmortem System

> Every campaign ends in a postmortem. No exceptions, even for tiny
> warm-intro campaigns. The point is to feed `MARKET_LEARNING_MEMORY.md`.

## When

- Within 7 days of `campaign_registry.status=complete`.
- Within 3 days of `campaign_registry.status=killed`.

## Template

Append to `<PRIVATE_OPS>/campaigns/postmortems.md`:

```
## campaign_id — name

- Sector / offer / channel:
- Hypothesis tested:
- Approval class:
- Volume: queued / approved / sent
- Top of funnel: impressions / clicks
- Mid-funnel: replies / positive_replies
- Bottom: samples / proposals / payments
- Best-performing asset (id):
- Worst-performing asset (id):
- Top objection encountered:
- Decision: scale / fix / kill / hold
- Memory entry written: yes/no, link
- Re-test scheduled:
```

## Doctrine

- No claim like "this campaign converted at X%" without the underlying
  counts in `campaign_results.csv`.
- No "always works" or "never works" — only this campaign in this
  window.
- Postmortem authors are encouraged to write honestly. The verifier
  does not flag pessimistic language; it flags exaggerated language.
