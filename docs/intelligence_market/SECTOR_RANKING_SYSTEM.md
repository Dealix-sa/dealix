# Sector Ranking System

A composite ranking of Saudi B2B sectors against Dealix's wedge.

## 1. Initial target sectors

| # | Sector | Why it fits Dealix |
|---|---|---|
| 1 | ERP / CRM implementers | High deal size, deep PDPL exposure, audit-hungry. |
| 2 | Cybersecurity | Trust-led buyers; alignment with our trust gate story. |
| 3 | B2B agencies | Need a residual operating system to keep clients. |
| 4 | Logistics / industrial services | Long cycles, founder-led, low automation. |
| 5 | Consulting / digital transformation | Repeat buyers, proof-driven. |
| 6 | SaaS / software | Speed of adoption; bias to operating tools. |
| 7 | Enterprise services | Large ACV, compliance non-negotiable. |
| 8 | Saudi high-ticket B2B providers | Founder-led, brand-sensitive, governance-aware. |

## 2. Composite score (per sector)

`score = 0.30·DealSize + 0.25·BuyerAccessibility + 0.20·Trust-gateRelevance + 0.15·DataAvailability + 0.10·CompetitiveDensity`

All five sub-scores 0–100. Composite is rounded to an integer.

## 3. Sub-score definitions

- **DealSize** — typical first-deal ACV in SAR (banded).
- **BuyerAccessibility** — % of named decision-makers with a public
  professional presence; warm-intro density.
- **Trust-gateRelevance** — strength of compliance / audit pressure
  for buyers in the sector.
- **DataAvailability** — % of accounts where we can fill the ICP card
  without manual enrichment.
- **CompetitiveDensity** — inverted: high crowd → low score.

## 4. Outputs

`growth/sector_targets.csv` with columns:

```
sector_id,sector_name,score,deal_size,buyer_accessibility,
trust_gate_relevance,data_availability,competitive_density,
sample_account_count,fallback_share,collected_at,source
```

## 5. Guardrails

- Sectors are **recommended**, not auto-targeted.
- No external action is taken against a sector without an explicit
  campaign-level founder approval in the queue.
- Fallback share > 30 % marks the row `provisional`.

## 6. Refresh

Monthly recomputation. The output ledger keeps every revision so
trend lines remain visible.
