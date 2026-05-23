# Scale / Fix / Kill System

> The single decision framework that prevents Dealix from carrying dead
> sectors, channels, and messages. Run weekly.

## The three decisions

| Decision | When                                                                 | Action                                              |
| -------- | -------------------------------------------------------------------- | --------------------------------------------------- |
| Scale    | Signal is repeating across ≥ 2 weeks and translating into proposals  | Double down: budget, calendar, content, partners    |
| Fix      | Engagement exists, but conversion is weak                            | Iterate message / audience / proof asset, then retest |
| Kill     | No signal after `sample_size ≥ 30`                                   | Stop investing, mark in scorecard                   |

## What we apply this to

- Sectors (via `beachhead_sector_scorecard.csv`)
- Offers (via `offer_market_fit_tests.csv`)
- Channels (via `campaign_results.csv`)
- Messages / angles (via `campaign_assets.csv`)
- Partners (via `partner_pipeline.csv`)

## Mechanics

The weekly review (`make weekly-growth-review` once wired) reads the
above CSVs and emits a markdown decision register at
`<PRIVATE_OPS>/market_attack/scale_fix_kill_decisions_<week>.md`.

The register lists for each item: current signal, last 14-day trend,
proposed decision, and the founder's locked decision.

## Anti-thrash rules

- A sector cannot move `kill → P0` within 30 days without a documented
  trigger event.
- A killed channel cannot be re-opened within 14 days unless the
  founder writes a new hypothesis.
- A scaled channel cannot keep `scale` status if its proposal rate
  drops below 5% for 14 consecutive days.
