# Ultimate Product Platform

Source: `${DEALIX_PRIVATE_OPS}/product/productization_candidates.csv`.
Endpoint: `GET /api/v1/internal/product/productization`.
Page: `/product`.

## Lifecycle

1. **Pattern detected** — the productization_agent surfaces a candidate.
2. **Evidence attached** — the founder annotates evidence.
3. **Validated** — sold twice as a repeatable offer.
4. **Productized** — moved to a separate offer in the proposal queue.
5. **Retired** — if not repurchased, archived.

## Stage labels

`detected, validated, productized, retired`.

## Connection to scorecard

`productization_score` rises whenever `proposals > 0` and at least one
candidate has reached `validated` or beyond.
