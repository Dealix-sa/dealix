"""Partner Performance — tracks the active partner ROI."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PartnerPerformanceRow:
    partner_name: str
    leads_delivered: int
    customers_signed: int
    revenue_sar: float
    health: str


class PartnerPerformance:
    def evaluate(
        self,
        *,
        partner_name: str,
        leads_delivered: int,
        customers_signed: int,
        revenue_sar: float,
    ) -> PartnerPerformanceRow:
        if customers_signed >= 3:
            health = "scale"
        elif customers_signed >= 1:
            health = "ok"
        elif leads_delivered == 0:
            health = "at_risk"
        else:
            health = "watch"
        return PartnerPerformanceRow(
            partner_name=partner_name,
            leads_delivered=leads_delivered,
            customers_signed=customers_signed,
            revenue_sar=revenue_sar,
            health=health,
        )
