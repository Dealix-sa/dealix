# Offer-Market Fit Scorecard

> Companion to `OFFER_MARKET_FIT_TEST.md`. This file is the spec for
> the *report* that summarises a portfolio of offer-market fit tests.

## Scoring per test

A test gets a numeric `signal_score` (0-100) computed from:

```
signal_score =
   40 * normalize(positive_reply_rate, target=30%)
 + 30 * normalize(proposal_rate, target=10%)
 + 20 * normalize(sample_or_meeting_rate, target=15%)
 + 10 * normalize(payment_rate, target=3%)
```

Each `normalize(x, target)` is `min(1.0, x/target)`.

`signal_score ≥ 60` → eligible for `scale`.
`30 ≤ signal_score < 60` → `fix`.
`signal_score < 30` after sample_size ≥ 30 → `kill`.

## Per-sector aggregates

The report rolls up:

- best `signal_score` test in that sector
- median positive_reply_rate
- count of tests in each decision bucket
- recommended next campaign for that sector

## Anti-vanity guardrails

The report deliberately excludes:

- impressions
- likes / claps / shares
- "engagement rate"

These do not predict revenue. The verifier flags any report that adds
these columns to the scoring formula.
