"""Partners Module — distribution network (section 118)."""

from dealix.hermes.partners.fit_score import PartnerFitInputs, PartnerFitScorer
from dealix.hermes.partners.onboarding import PartnerOnboarding
from dealix.hermes.partners.partner_risk import PartnerRiskReview
from dealix.hermes.partners.performance import PartnerPerformance
from dealix.hermes.partners.pitch import PartnerPitchBuilder
from dealix.hermes.partners.revenue_share import RevenueShareLedger, RevenueShareEntry
from dealix.hermes.partners.scout import Partner, PartnerScout, PartnerType

__all__ = [
    "Partner",
    "PartnerType",
    "PartnerScout",
    "PartnerFitInputs",
    "PartnerFitScorer",
    "PartnerOnboarding",
    "PartnerPerformance",
    "PartnerPitchBuilder",
    "PartnerRiskReview",
    "RevenueShareEntry",
    "RevenueShareLedger",
]
