"""
Hermes Partners — partner fit, revenue share, performance.

Partner module is intentionally thin: it leans on the same offer registry and
revenue graph rather than duplicating logic. The only partner-specific concepts
are: partner fit score, revenue share commercial model, partner-influenced
revenue attribution.
"""

from .partner_registry import Partner, PartnerRegistry, PartnerStatus, PartnerTier
from .fit_scorer import PartnerFitInputs, PartnerFitResult, PartnerFitScorer
from .revenue_share import RevenueShareCalculator, RevenueShareModel, RevenueSplit

__all__ = [
    "Partner",
    "PartnerFitInputs",
    "PartnerFitResult",
    "PartnerFitScorer",
    "PartnerRegistry",
    "PartnerStatus",
    "PartnerTier",
    "RevenueShareCalculator",
    "RevenueShareModel",
    "RevenueSplit",
]
