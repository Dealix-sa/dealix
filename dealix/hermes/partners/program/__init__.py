"""partners.program — modular partner program building blocks."""

from dealix.hermes.partners.program.partner_claims import APPROVED_CLAIMS, PartnerClaim
from dealix.hermes.partners.program.partner_contracts import PartnerProfile, register_partner
from dealix.hermes.partners.program.partner_enablement import PartnerEnablement
from dealix.hermes.partners.program.partner_performance_review import PartnerPerformance, review_partner
from dealix.hermes.partners.program.partner_tiers import PARTNER_TIERS, PartnerTier
from dealix.hermes.partners.program.revenue_share_rules import RevenueShareRule, calculate_share

__all__ = [
    "APPROVED_CLAIMS",
    "PARTNER_TIERS",
    "PartnerClaim",
    "PartnerEnablement",
    "PartnerPerformance",
    "PartnerProfile",
    "PartnerTier",
    "RevenueShareRule",
    "calculate_share",
    "register_partner",
    "review_partner",
]
