# Strategic Account List System

> A small, named list of Saudi B2B accounts that — if won — change
> Dealix's trajectory. Never confuse this with a generic lead list.

## CSV schema (source of truth)

File: `<PRIVATE_OPS>/market_attack/strategic_accounts.csv`

| Column             | Notes                                                |
| ------------------ | ---------------------------------------------------- |
| account_id         | `acct-NNN`                                           |
| company            | Legal / display name                                  |
| sector             | One of the beachhead-eligible sectors                |
| website            | If public                                            |
| city               | Riyadh / Jeddah / Dammam / Khobar / …                |
| buyer_title        | Exact title (e.g. "Director of Sales Operations")    |
| why_strategic      | One sentence — proof unlock, sector unlock, capital  |
| trigger_event      | What just happened (funding / RFP / regulation)      |
| estimated_value    | Annual SAR potential                                 |
| relationship_path  | Named human introducer or path                       |
| proof_needed       | Which proof artifact unlocks the conversation        |
| trust_risk         | `low` / `medium` / `high`                            |
| priority           | T0 / T1 / T2 / T3                                    |
| next_action        | Concrete next step                                   |
| status             | `new` / `contacted` / `replied` / `proposal` / `won` / `lost` / `nurture` |

## How it stays small

- Hard ceiling: 25 active T0+T1 accounts at any time.
- T2 watchlist may go up to 75.
- Anything beyond that is parked. Strategic ≠ Big List.

## Generator

`scripts/generate_strategic_account_list.py` produces a markdown
report at `<PRIVATE_OPS>/market_attack/strategic_account_list.md`
listing T0 / T1 accounts with `next_action`, plus an "out of bounds"
section flagging schema violations (missing `relationship_path` on
T0/T1, expired triggers, etc.).

## Run

```bash
make strategic-accounts PRIVATE_OPS=/opt/dealix-ops-private
```
