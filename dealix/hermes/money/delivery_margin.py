"""
Delivery margin — know which products are actually profitable.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DeliveryMarginMetrics:
    revenue_sar: float
    total_cost_sar: float
    gross_margin_sar: float
    gross_margin_pct: float
    revision_count: int
    asset_reuse_count: int
    notes: list[str]


def compute_delivery_margin(
    *,
    revenue_sar: float,
    delivery_hours: float,
    blended_hour_cost_sar: float = 250.0,
    agent_cost_sar: float = 0.0,
    other_human_cost_sar: float = 0.0,
    customer_support_hours: float = 0.0,
    revision_count: int = 0,
    asset_reuse_count: int = 0,
) -> DeliveryMarginMetrics:
    if revenue_sar < 0:
        raise ValueError("revenue_sar must be >= 0")
    human_cost = (delivery_hours + customer_support_hours) * blended_hour_cost_sar
    total_cost = human_cost + agent_cost_sar + other_human_cost_sar
    gm = revenue_sar - total_cost
    pct = (gm / revenue_sar * 100) if revenue_sar > 0 else 0.0
    notes: list[str] = []
    if pct < 30:
        notes.append("margin below 30% — reprice or reduce delivery cost")
    if revision_count > 3:
        notes.append("high revision count — tighten requirements gate")
    if asset_reuse_count == 0:
        notes.append("zero asset reuse — investigate productization")
    return DeliveryMarginMetrics(
        revenue_sar=round(revenue_sar, 2),
        total_cost_sar=round(total_cost, 2),
        gross_margin_sar=round(gm, 2),
        gross_margin_pct=round(pct, 2),
        revision_count=revision_count,
        asset_reuse_count=asset_reuse_count,
        notes=notes,
    )
