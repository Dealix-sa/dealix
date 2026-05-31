"""Partner risk scoring — flag suspicious patterns early."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class PartnerRisk(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


@dataclass(frozen=True)
class PartnerRiskAssessment:
    partner_id: str
    risk: PartnerRisk
    reasons: tuple[str, ...]


def evaluate_partner_risk(
    *,
    partner_id: str,
    is_kyc_complete: bool,
    has_sanctions_hit: bool,
    days_since_activity: int,
    disputed_deals: int,
) -> PartnerRiskAssessment:
    reasons: list[str] = []
    if has_sanctions_hit:
        reasons.append("sanctions_hit")
    if not is_kyc_complete:
        reasons.append("kyc_incomplete")
    if disputed_deals > 0:
        reasons.append("disputed_deals")
    if days_since_activity > 90:
        reasons.append("dormant")

    if "sanctions_hit" in reasons or disputed_deals >= 2:
        risk = PartnerRisk.high
    elif reasons:
        risk = PartnerRisk.medium
    else:
        risk = PartnerRisk.low
    return PartnerRiskAssessment(partner_id=partner_id, risk=risk, reasons=tuple(reasons))
