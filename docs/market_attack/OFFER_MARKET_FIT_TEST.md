# Offer-Market Fit Test

> Structured experiments that prove (or disprove) whether a specific
> offer resonates with a specific sector before scaling. Not "did we
> get likes"; rather, did we get *replies, samples requested, proposals
> sent, payments collected*.

## What counts as a test

Each test is a row in
`<PRIVATE_OPS>/market_attack/offer_market_fit_tests.csv`:

```
test_id,sector,offer,audience,channel,hypothesis,message_angle,
success_metric,result,learning,decision,next_action
```

- **test_id** — `omf-001` style.
- **sector** — one of the beachhead sectors.
- **offer** — name from the offer ladder (e.g. `managed_pilot_499`).
- **audience** — buyer title + segment (e.g. `coo_construction_mid`).
- **channel** — one of `warm_intro`, `partner_referral`, `linkedin_post`,
  `direct_email_approved`, `event_booth`, `webinar`, `whitepaper`.
- **hypothesis** — single sentence: "if we show X to Y, they will Z".
- **success_metric** — quantitative; e.g. `≥ 3 positive replies in 7 days`.
- **result** — what actually happened (numbers).
- **decision** — `scale` / `fix` / `kill` / `hold`.

## Decision logic (operational)

The generator script applies these rules:

| Signal                                        | Decision |
| --------------------------------------------- | -------- |
| ≥ 30% positive_reply_rate AND proposals > 0   | scale    |
| 10–30% positive_reply_rate AND proposals = 0  | fix (refine message or audience) |
| < 10% positive_reply_rate AFTER ≥ 30 contacts | kill     |
| Sample size < 30                              | hold (keep running)              |

The script **never** claims a guaranteed outcome. The report wording
uses "signal observed", "directional", "indicative".

## Report

`make offer-market-fit PRIVATE_OPS=/opt/dealix-ops-private`
generates `<PRIVATE_OPS>/market_attack/offer_market_fit_report.md`:

1. Tests by status (scale / fix / kill / hold).
2. Per-sector signal summary.
3. Open `next_action` items.
4. Recent learnings (rolled up into Market Learning Memory).

## How this feeds the rest

- **Scale** decisions trigger entries into `campaigns/campaign_registry.csv`.
- **Fix** decisions trigger entries into
  `market_attack/objection_library.csv` and the asset factory.
- **Kill** decisions update `beachhead_sector_scorecard.csv`
  (`priority -> hold` or `kill`).
- All decisions append to `MARKET_LEARNING_MEMORY.md`.
