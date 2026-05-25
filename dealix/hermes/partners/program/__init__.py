"""
Partner program.
"""

from __future__ import annotations

from dealix.hermes.partners.program.approved_claims import (
    ApprovedClaimsCheck,
    check_partner_claim,
)
from dealix.hermes.partners.program.co_marketing import (
    CoMarketingProposal,
    review_co_marketing,
)
from dealix.hermes.partners.program.compliance import (
    PartnerComplianceCheck,
    run_partner_compliance,
)
from dealix.hermes.partners.program.enablement import (
    EnablementProgress,
    score_enablement,
)
from dealix.hermes.partners.program.performance_review import (
    PartnerPerformanceReview,
    review_partner_performance,
)
from dealix.hermes.partners.program.revenue_share import (
    RevenueShareSplit,
    compute_revenue_share,
)
from dealix.hermes.partners.program.tiers import (
    PartnerTier,
    classify_partner_tier,
)

__all__ = [
    "PartnerTier",
    "classify_partner_tier",
    "ApprovedClaimsCheck",
    "check_partner_claim",
    "EnablementProgress",
    "score_enablement",
    "CoMarketingProposal",
    "review_co_marketing",
    "RevenueShareSplit",
    "compute_revenue_share",
    "PartnerComplianceCheck",
    "run_partner_compliance",
    "PartnerPerformanceReview",
    "review_partner_performance",
]
