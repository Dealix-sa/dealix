"""Board-level KPI dataclass and constructor."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BoardMetrics:
    period: str
    verified_revenue_sar: float
    revenue_quality_grade: str
    pipeline_quality_grade: str
    gross_margin: float
    retainer_conversion: float
    agent_roi: float
    trust_incidents: int
    approvals_pending: int
    assets_created: int
    assets_reused: int
    partner_revenue_sar: float
    founder_time_leverage_hours: float


def build(
    *,
    period: str,
    verified_revenue_sar: float,
    revenue_quality_grade: str,
    pipeline_quality_grade: str,
    gross_margin: float,
    retainer_conversion: float,
    agent_roi: float,
    trust_incidents: int,
    approvals_pending: int,
    assets_created: int,
    assets_reused: int,
    partner_revenue_sar: float,
    founder_time_leverage_hours: float,
) -> BoardMetrics:
    """Construct a validated BoardMetrics snapshot for the given period."""
    return BoardMetrics(
        period=period,
        verified_revenue_sar=float(verified_revenue_sar),
        revenue_quality_grade=revenue_quality_grade,
        pipeline_quality_grade=pipeline_quality_grade,
        gross_margin=float(gross_margin),
        retainer_conversion=float(retainer_conversion),
        agent_roi=float(agent_roi),
        trust_incidents=int(trust_incidents),
        approvals_pending=int(approvals_pending),
        assets_created=int(assets_created),
        assets_reused=int(assets_reused),
        partner_revenue_sar=float(partner_revenue_sar),
        founder_time_leverage_hours=float(founder_time_leverage_hours),
    )
