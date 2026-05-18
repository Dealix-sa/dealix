# Service Economics

Track **margin, risk, and upsell** per service—expand what pays; starve what burns you.

**Note:** Figures below are **illustrative** only. Replace with your actual costs, blended rates, and risk load.

> **Canonical pricing source:** [`OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md).
> Ladder-rung rows use canonical prices (recomputed); non-ladder rows are
> internal-planning estimates priced as Rung 5 / SOW only.

| Service | Price (SAR) | Hours (plan) | Direct cost (SAR) | Gross margin | Risk | Upsell |
|---------|------------:|-------------:|-------------------:|-------------:|------|--------|
| Free AI Ops Diagnostic | 0 (free) | ~0.5 | < 2 | n/a | Low | High (routes to Sprint) |
| 7-Day Revenue Proof Sprint (Rung 1) | 499 | 2–3 | ~10 | ~85% | Medium | High |
| Data-to-Revenue Pack (Rung 2) | 1,500 | 5–8 | ~20 | ~75% | Medium | High |
| Managed Revenue Ops (Rung 3) | 2,999–4,999/mo | 10–15/mo | ~50/mo | ~70% | Med | High |
| AI Quick Win Sprint (non-ladder) | custom (Rung 5/SOW) | *set* | *set* | *calc* | Low–Med | Med |
| Company Brain Sprint (non-ladder) | custom (Rung 5/SOW) | 50 | 6,000 | recompute per SOW | High | High |

## Rule

Do not scale a service with **weak margin** and **high governance load** unless it is **strategic** (learns the market, unlocks retainer). Document the strategic thesis in [`../growth/EXPANSION_OFFER_SYSTEM.md`](../growth/EXPANSION_OFFER_SYSTEM.md).

## Inputs to maintain monthly

- Time logs (category: delivery / QA / sales / rework)
- Rework rate by service
- Sprint → retainer conversion
- Incident cost (governance / client recovery)

**Links:** [`SERVICE_REGISTRY.md`](SERVICE_REGISTRY.md), [`PRICING.md`](PRICING.md), [`PRICING_DECISION.md`](PRICING_DECISION.md).
