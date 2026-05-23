# LinkedIn Authority System

> The single channel where the founder builds authority publicly. All
> other public channels (Substack, X, podcast) defer to LinkedIn until
> the channel is proven to produce signal.

## Why only LinkedIn first

- Saudi B2B buyers and partners are reachable here.
- Posts can carry sector-specific observations without becoming
  generic.
- Replies and DMs are measurable inputs into the Conversion Command
  Room.

## Post tracker

`<PRIVATE_OPS>/authority/founder_posts.csv`

```
post_id,theme,sector,draft,approval_status,proof_status,
risk_level,next_action
```

- `approval_status` ∈ {`pending`, `approved`, `held`, `rejected`}.
- `proof_status` ∈ {`n_a`, `evidence_required`, `evidence_attached`}.
- `risk_level` ∈ {`low`, `medium`, `high`, `governance_review`}.

## Doctrine

1. No post is published without `approval_status=approved`.
2. No post claims an outcome without `proof_status=evidence_attached`.
3. No reposting of customer logos without explicit permission.
4. No engagement-farming patterns (one-word replies, polls without
   purpose, "Comment X to get my PDF").
