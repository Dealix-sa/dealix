# Market-Attack System — Surface Index

Read-only index for the market-attack surface. This surface contains
**templates only**, never claims (Doctrine Lock #5).

`scripts/verify_market_attack_system.py` enforces this rule by scanning
every template file for banned claim words.

## Templates

- [`BEACHHEAD_TEMPLATE.md`](BEACHHEAD_TEMPLATE.md) — beachhead sector
  scorecard worksheet.
- [`STRATEGIC_ACCOUNTS_TEMPLATE.md`](STRATEGIC_ACCOUNTS_TEMPLATE.md) —
  strategic-account targeting worksheet.
- [`OFFER_MARKET_FIT_TEMPLATE.md`](OFFER_MARKET_FIT_TEMPLATE.md) —
  offer/market-fit experiment template.

## Founder Console

- `/internal/market-attack` reads `$PRIVATE_OPS/market_attack/*.csv` and
  returns `{data, source, freshness}`.

## Governance

Templates MUST NOT contain:

- Revenue/ROI/growth/sales guarantees.
- Customer names/logos before signed permission.
- Any phrase listed in `scripts/verify_prompt_output_quality.py` ban list.
