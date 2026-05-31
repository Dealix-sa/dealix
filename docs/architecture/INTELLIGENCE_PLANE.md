# Hermes Intelligence Plane

The intelligence plane is the union of `hermes.graphs` and the read
side of `hermes.observability`. It answers business questions across
the ledgers maintained by the other planes.

| Question | Graph |
| --- | --- |
| Which offer is most profitable? | `RevenueGraph.revenue_by("offer_id")` |
| Which ICP pays fastest? | `OpportunityGraph.win_rate(offer_id)` joined with payment dates |
| Which partner is highest quality? | `PartnerGraph.revenue()` + `incident_rate()` |
| Which asset raises conversion? | `AssetGraph.revenue_by_asset()` |
| Which risk recurs most? | `RiskGraph.top_categories()` |
| Which channel produces verified revenue? | `RevenueGraph.revenue_by("channel")` |

Graphs are intentionally lightweight Python; in production they back
onto a query engine.
