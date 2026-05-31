"""
MarginAnalysis — join verified revenue with cost intelligence to produce
a per-deal margin report and a portfolio-level summary.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MarginReport:
    deal_id: str
    revenue_sar: float
    cost_sar: float
    gross_margin_sar: float
    gross_margin_pct: float
    verdict: str


def analyse_margin(*, deal_id: str, revenue_sar: float, cost_sar: float) -> MarginReport:
    margin = revenue_sar - cost_sar
    pct = round((margin / revenue_sar) if revenue_sar > 0 else 0.0, 4)
    if pct >= 0.5:
        verdict = "scale"
    elif pct >= 0.25:
        verdict = "ok"
    elif pct >= 0.0:
        verdict = "reprice"
    else:
        verdict = "kill"
    return MarginReport(
        deal_id=deal_id,
        revenue_sar=revenue_sar,
        cost_sar=cost_sar,
        gross_margin_sar=round(margin, 2),
        gross_margin_pct=pct,
        verdict=verdict,
    )
