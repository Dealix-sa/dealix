"""
graphs — small in-memory graphs that answer business questions like
"which offer is the most profitable" or "which channel produces the
highest-quality verified revenue".

These are intentionally lightweight: they're driven by the ledgers in
other modules. In production they're backed by a query engine.
"""

from dealix.hermes.graphs.asset_graph import AssetGraph
from dealix.hermes.graphs.opportunity_graph import OpportunityGraph
from dealix.hermes.graphs.outcome_graph import OutcomeGraph
from dealix.hermes.graphs.partner_graph import PartnerGraph
from dealix.hermes.graphs.revenue_graph import RevenueGraph
from dealix.hermes.graphs.risk_graph import RiskGraph
from dealix.hermes.graphs.sector_graph import SectorGraph

__all__ = [
    "AssetGraph",
    "OpportunityGraph",
    "OutcomeGraph",
    "PartnerGraph",
    "RevenueGraph",
    "RiskGraph",
    "SectorGraph",
]
