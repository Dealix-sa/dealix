from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class PartnerTier(StrEnum):
    APPLICANT = "applicant"
    REGISTERED = "registered"
    AUTHORIZED = "authorized"
    CERTIFIED = "certified"
    STRATEGIC = "strategic"


@dataclass
class PartnerTierAssignment:
    tier: PartnerTier
    rationale: list[str]


def classify_partner_tier(
    *,
    enablement_score: float,
    verified_revenue_sar_last_12mo: float,
    customer_complaints: int,
    compliance_pass: bool,
    has_signed_partner_agreement: bool,
) -> PartnerTierAssignment:
    rationale: list[str] = []
    if not has_signed_partner_agreement:
        rationale.append("no signed partner agreement")
        return PartnerTierAssignment(PartnerTier.APPLICANT, rationale)
    if not compliance_pass:
        rationale.append("compliance check failed")
        return PartnerTierAssignment(PartnerTier.APPLICANT, rationale)
    if customer_complaints >= 3:
        rationale.append(f"{customer_complaints} customer complaints")
        return PartnerTierAssignment(PartnerTier.REGISTERED, rationale)
    if verified_revenue_sar_last_12mo >= 500_000 and enablement_score >= 80:
        rationale.append("strategic thresholds met")
        return PartnerTierAssignment(PartnerTier.STRATEGIC, rationale)
    if verified_revenue_sar_last_12mo >= 150_000 and enablement_score >= 60:
        rationale.append("certified thresholds met")
        return PartnerTierAssignment(PartnerTier.CERTIFIED, rationale)
    if verified_revenue_sar_last_12mo >= 25_000 and enablement_score >= 40:
        rationale.append("authorized thresholds met")
        return PartnerTierAssignment(PartnerTier.AUTHORIZED, rationale)
    rationale.append("registered baseline")
    return PartnerTierAssignment(PartnerTier.REGISTERED, rationale)
