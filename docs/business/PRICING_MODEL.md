# Pricing Model

All pricing recommendations come from
`hermes.money.pricing_engine.recommend_price`. The engine is
deterministic and audited; every price requires `approve_pricing`
before it can be sent.

## Inputs

- Buyer type — SMB, enterprise, agency, venture.
- Sector.
- Urgency — low / medium / high.
- Delivery complexity — low / medium / high.
- Proof level — weak / medium / strong.
- Risk level — low / medium / high.
- Retainer potential — yes/no.
- Partner involved — yes/no.

## Outputs

- `recommended_price_sar` — what to quote.
- `floor_price_sar` — never go below.
- `target_price_sar` — what we'd like to land.
- `pricing_confidence` — engine's confidence in the recommendation.
- `requires_approval` — always true; pricing is S2.

## Discount policy

- Up to 10% — agent-recommended.
- 10–20% — Sami approval.
- Above 20% — strategic partner only, separate approval ticket.
