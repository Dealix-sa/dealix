# Offer Router Agent

## Role
Select the optimal Dealix offer for each company based on tier, sector, and buyer readiness.

## Inputs
- Enriched company + buyer map
- config/offers.yml
- config/sectors.yml

## Routing Logic
| Tier | Sector | Buyer Signal | Offer |
|------|--------|--------------|-------|
| C    | Any    | Cold         | Rung 1 (Free Diagnostic) |
| B    | Any    | Cold         | Rung 1 or 2 |
| B    | Any    | Warm         | Rung 2 (Sprint) |
| A    | Any    | Cold         | Rung 2 or 3 |
| A    | Any    | Warm         | Rung 4 (Managed Ops) |
| A    | Legal/Finance | Any | Rung 5 (Custom) — founder review |

## Output
```json
{
  "company_id": "string",
  "selected_offer": "rung_1-5",
  "offer_rationale": "string",
  "cta_ar": "string",
  "cta_en": "string",
  "routed_at": "ISO8601"
}
```
