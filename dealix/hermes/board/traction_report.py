from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TractionReport:
    period: str
    verified_revenue_sar: float
    retainer_active_count: int
    paying_customers: int
    nps: float | None
    case_studies_published: int
    partner_count: int
    notes: list[str]


def build_traction_report(
    period: str,
    *,
    verified_revenue_sar: float,
    retainer_active_count: int,
    paying_customers: int,
    case_studies_published: int,
    partner_count: int,
    nps: float | None = None,
    notes: list[str] | None = None,
) -> TractionReport:
    return TractionReport(
        period=period,
        verified_revenue_sar=round(verified_revenue_sar, 2),
        retainer_active_count=retainer_active_count,
        paying_customers=paying_customers,
        nps=nps,
        case_studies_published=case_studies_published,
        partner_count=partner_count,
        notes=list(notes or []),
    )
