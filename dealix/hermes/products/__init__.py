"""
products — productized offers.

Each offer is a typed Python ``Package`` so that growth, delivery, and
the proposal factory all consult the same source of truth.
"""

from dealix.hermes.products.offer_market_fit import (
    PRODUCT_REGISTRY,
    Package,
    register_package,
)
from dealix.hermes.products.packages import (
    AGENCY_WHITE_LABEL_KIT,
    AI_TRUST_KIT,
    EXECUTIVE_PMO_LITE,
    FOUNDER_OS_SETUP,
    MARKET_RADAR_REPORT,
    MCP_RISK_REVIEW,
    REVENUE_HUNTER_PILOT,
)

__all__ = [
    "AGENCY_WHITE_LABEL_KIT",
    "AI_TRUST_KIT",
    "EXECUTIVE_PMO_LITE",
    "FOUNDER_OS_SETUP",
    "MARKET_RADAR_REPORT",
    "MCP_RISK_REVIEW",
    "PRODUCT_REGISTRY",
    "Package",
    "REVENUE_HUNTER_PILOT",
    "register_package",
]
