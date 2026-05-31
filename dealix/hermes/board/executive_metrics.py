from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExecutiveMetrics:
    verified_revenue_sar: float
    revenue_quality_score: float
    gross_margin_pct: float
    retainer_conversion_pct: float
    pipeline_quality_index: float
    customer_value_delivered_sar: float
    assets_created: int
    assets_reused: int
    trust_incidents: int
    approval_sla_p95_minutes: float
    agent_roi: float
    partner_revenue_sar: float
    founder_time_leverage: float

    def headline_health(self) -> str:
        if (
            self.trust_incidents > 0
            and self.approval_sla_p95_minutes > 240
        ):
            return "amber:trust"
        if self.gross_margin_pct < 30:
            return "amber:margin"
        if self.retainer_conversion_pct < 20:
            return "amber:retention"
        if self.revenue_quality_score < 50:
            return "amber:quality"
        return "green"


def compute_executive_metrics(
    *,
    verified_revenue_sar: float,
    pipeline_proposals_sar: float,
    pipeline_committed_sar: float,
    delivered_costs_sar: float,
    payment_count: int,
    retainer_active_count: int,
    customer_value_delivered_sar: float,
    assets_created: int,
    assets_reused: int,
    trust_incidents: int,
    approval_sla_p95_minutes: float,
    agent_attributable_revenue_sar: float,
    agent_cost_sar: float,
    partner_revenue_sar: float,
    founder_hours_period: float,
    founder_hours_strategic: float,
) -> ExecutiveMetrics:
    gm_pct = (
        ((verified_revenue_sar - delivered_costs_sar) / verified_revenue_sar) * 100
        if verified_revenue_sar > 0
        else 0.0
    )
    retainer_pct = (
        (retainer_active_count / payment_count) * 100 if payment_count > 0 else 0.0
    )
    pipeline_quality = (
        (pipeline_committed_sar / pipeline_proposals_sar)
        if pipeline_proposals_sar > 0
        else 0.0
    )
    quality_score = max(
        0.0,
        min(
            100.0,
            (gm_pct * 0.3)
            + (retainer_pct * 0.3)
            + (pipeline_quality * 100 * 0.2)
            - (trust_incidents * 5),
        ),
    )
    agent_roi = (
        ((agent_attributable_revenue_sar - agent_cost_sar) / agent_cost_sar)
        if agent_cost_sar > 0
        else 0.0
    )
    founder_leverage = (
        (founder_hours_strategic / founder_hours_period)
        if founder_hours_period > 0
        else 0.0
    )
    return ExecutiveMetrics(
        verified_revenue_sar=round(verified_revenue_sar, 2),
        revenue_quality_score=round(quality_score, 2),
        gross_margin_pct=round(gm_pct, 2),
        retainer_conversion_pct=round(retainer_pct, 2),
        pipeline_quality_index=round(pipeline_quality, 4),
        customer_value_delivered_sar=round(customer_value_delivered_sar, 2),
        assets_created=assets_created,
        assets_reused=assets_reused,
        trust_incidents=trust_incidents,
        approval_sla_p95_minutes=round(approval_sla_p95_minutes, 2),
        agent_roi=round(agent_roi, 4),
        partner_revenue_sar=round(partner_revenue_sar, 2),
        founder_time_leverage=round(founder_leverage, 4),
    )
