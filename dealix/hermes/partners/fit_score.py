"""Partner Fit Score — must produce at least one of: lead, customer, access, trust, data, delivery."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PartnerFit:
    partner_name: str
    partner_type: str
    fit_score: float
    next_action: str
    produces: list[str]


class PartnerFitScorer:
    def score(
        self,
        *,
        partner_name: str,
        partner_type: str,
        client_base_score: int,
        sales_capability: int,
        delivery_capability: int,
        trust_level: int,
        sector_fit: int,
        risk_level: int,
    ) -> PartnerFit:
        score = round(
            0.25 * client_base_score
            + 0.20 * sales_capability
            + 0.15 * delivery_capability
            + 0.20 * trust_level
            + 0.20 * sector_fit
            - 0.10 * risk_level,
            4,
        )
        produces: list[str] = []
        if client_base_score >= 4:
            produces.append("lead")
        if sales_capability >= 4:
            produces.append("customer")
        if trust_level >= 4:
            produces.append("trust")
        if delivery_capability >= 4:
            produces.append("delivery_capacity")
        if sector_fit >= 4:
            produces.append("access")
        if not produces:
            produces = ["needs_more_qualification"]
        action = "Draft partner pitch" if score >= 3.0 else "Defer — fit too low"
        return PartnerFit(partner_name, partner_type, score, action, produces)
