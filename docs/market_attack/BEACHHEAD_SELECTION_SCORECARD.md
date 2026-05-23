# Beachhead Selection Scorecard

> The scoring instrument behind `BEACHHEAD_SECTOR_STRATEGY.md`. This
> file is the *spec* for `market_attack/beachhead_sector_scorecard.csv`
> and for `scripts/generate_beachhead_sector_scorecard.py`.

## CSV schema (source of truth)

File: `<PRIVATE_OPS>/market_attack/beachhead_sector_scorecard.csv`

| Column                 | Type    | Notes                                              |
| ---------------------- | ------- | -------------------------------------------------- |
| sector                 | string  | e.g. `construction`, `hospitality`, `logistics`    |
| saudi_relevance        | int 1-5 |                                                    |
| buyer_clarity          | int 1-5 |                                                    |
| pain_urgency           | int 1-5 |                                                    |
| high_ticket_potential  | int 1-5 |                                                    |
| proof_fit              | int 1-5 |                                                    |
| delivery_fit           | int 1-5 |                                                    |
| competition_gap        | int 1-5 |                                                    |
| channel_access         | int 1-5 |                                                    |
| trust_risk             | int 1-5 | already inverted (5 = low risk)                    |
| total_score            | int 9-45| sum of the 9 dimensions                            |
| priority               | string  | `P0` / `P1` / `P2` / `hold` / `kill`               |
| next_action            | string  | concrete next step                                 |

## Decision matrix

| total_score | priority | meaning                                              |
| ----------- | -------- | ---------------------------------------------------- |
| ≥ 36        | P0       | beachhead candidate, fund deeply for 90 days         |
| 30 – 35     | P1       | viable, run a focused offer-market fit test          |
| 24 – 29     | P2       | watch, no campaigns yet                              |
| 18 – 23     | hold     | not now; revisit quarterly                           |
| < 18        | kill     | stop investing                                       |

## Inputs

The generator script reads (when available):

- `growth/sector_targets.csv`
- `growth/account_scores.csv`
- `sales/proposal_queue.csv`
- `outreach/conversation_log.csv`

If a file is missing, the script falls back to seeded sectors and
emits a `source=fallback` note in the report. It never raises.

## Output

Markdown report at:
`<PRIVATE_OPS>/market_attack/beachhead_sector_scorecard.md`

Sections:
1. Top sectors (sorted by `total_score` desc)
2. P0 / P1 candidates with `next_action`
3. Hold / kill list (with reason)
4. Generated-at timestamp and input file status

## Run

```bash
make beachhead-scorecard PRIVATE_OPS=/opt/dealix-ops-private
```
