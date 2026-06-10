"""ROI Estimator — conservative, estimate-only, governed (no guarantees).

Produces an ROI *range* for an enterprise transformation engagement. Every output
is an estimate (Article 8) and the language never claims a guaranteed outcome
(doctrine: no_guaranteed_sales_claims). Pure + stateless — no DB, no network.

Bands are intentionally conservative: automation/transformation rarely captures
100% of the theoretical ceiling, so a low/high efficiency band is applied.
"""

from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# Efficiency bands — fraction of theoretical value realistically captured.
_TIME_CAPTURE_LOW = 0.40
_TIME_CAPTURE_HIGH = 0.70
_LEAD_CAPTURE_LOW = 0.50
_LEAD_CAPTURE_HIGH = 1.00

_DISCLAIMER = (
    "تقديرات وليست أرقامًا مُتحقَّقة — Estimates, not verified results. "
    "Actuals depend on data quality, adoption, and scope."
)


class ROIInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company_name: str = ""
    manual_hours_per_week: float = Field(default=0.0, ge=0)
    hourly_cost_sar: float = Field(default=60.0, ge=0)
    lost_leads_per_month: float = Field(default=0.0, ge=0)
    avg_deal_value_sar: float = Field(default=0.0, ge=0)
    recovered_conversion_pct: float = Field(default=10.0, ge=0, le=100)
    setup_cost_sar: float = Field(default=0.0, ge=0)
    monthly_cost_sar: float = Field(default=0.0, ge=0)


class ROIEstimate(BaseModel):
    company_name: str = ""
    time_savings_sar_year_min: float = 0.0
    time_savings_sar_year_max: float = 0.0
    recovered_revenue_sar_year_min: float = 0.0
    recovered_revenue_sar_year_max: float = 0.0
    gross_annual_value_sar_min: float = 0.0
    gross_annual_value_sar_max: float = 0.0
    annual_cost_sar: float = 0.0
    net_annual_value_sar_min: float = 0.0
    net_annual_value_sar_max: float = 0.0
    payback_months_min: float | None = None
    payback_months_max: float | None = None
    assumptions: list[str] = Field(default_factory=list)
    disclaimer: str = _DISCLAIMER
    is_estimate: bool = True
    markdown_ar_en: str = ""

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())


def estimate_roi(inp: ROIInput) -> ROIEstimate:
    """Return a conservative ROI range. All figures are estimates."""
    theoretical_time = inp.manual_hours_per_week * 52.0 * inp.hourly_cost_sar
    time_low = theoretical_time * _TIME_CAPTURE_LOW
    time_high = theoretical_time * _TIME_CAPTURE_HIGH

    theoretical_rev = (
        inp.lost_leads_per_month
        * 12.0
        * inp.avg_deal_value_sar
        * (inp.recovered_conversion_pct / 100.0)
    )
    rev_low = theoretical_rev * _LEAD_CAPTURE_LOW
    rev_high = theoretical_rev * _LEAD_CAPTURE_HIGH

    gross_min = time_low + rev_low
    gross_max = time_high + rev_high
    annual_cost = inp.setup_cost_sar + inp.monthly_cost_sar * 12.0
    net_min = gross_min - annual_cost
    net_max = gross_max - annual_cost

    payback_min, payback_max = _payback_window(inp, gross_min, gross_max)

    est = ROIEstimate(
        company_name=inp.company_name,
        time_savings_sar_year_min=round(time_low, 2),
        time_savings_sar_year_max=round(time_high, 2),
        recovered_revenue_sar_year_min=round(rev_low, 2),
        recovered_revenue_sar_year_max=round(rev_high, 2),
        gross_annual_value_sar_min=round(gross_min, 2),
        gross_annual_value_sar_max=round(gross_max, 2),
        annual_cost_sar=round(annual_cost, 2),
        net_annual_value_sar_min=round(net_min, 2),
        net_annual_value_sar_max=round(net_max, 2),
        payback_months_min=payback_min,
        payback_months_max=payback_max,
        assumptions=[
            f"Time-savings capture band: {int(_TIME_CAPTURE_LOW * 100)}–{int(_TIME_CAPTURE_HIGH * 100)}% of theoretical.",
            f"Recovered-lead capture band: {int(_LEAD_CAPTURE_LOW * 100)}–{int(_LEAD_CAPTURE_HIGH * 100)}% of theoretical.",
            f"Recovered-lead conversion assumed at {inp.recovered_conversion_pct:g}%.",
            "Annual cost = setup + 12 × monthly.",
        ],
    )
    est.markdown_ar_en = _render_markdown(inp, est)
    return est


def _payback_window(
    inp: ROIInput, gross_min: float, gross_max: float
) -> tuple[float | None, float | None]:
    """Months to recover setup from monthly net benefit. None if not recoverable."""
    monthly_cost = inp.monthly_cost_sar
    net_monthly_low = gross_min / 12.0 - monthly_cost
    net_monthly_high = gross_max / 12.0 - monthly_cost
    setup = inp.setup_cost_sar
    if setup <= 0:
        return (0.0, 0.0)
    # Faster payback uses the higher monthly net benefit.
    fast = round(setup / net_monthly_high, 1) if net_monthly_high > 0 else None
    slow = round(setup / net_monthly_low, 1) if net_monthly_low > 0 else None
    return (fast, slow)


def _fmt(v: float) -> str:
    return f"{round(v):,}"


def _render_markdown(inp: ROIInput, est: ROIEstimate) -> str:
    title = inp.company_name or "Enterprise"
    lines = [
        f"# تقدير العائد على الاستثمار / ROI Estimate — {title}",
        "",
        "| Driver | Annual estimate (SAR) |",
        "|---|---|",
        f"| Time savings / توفير الوقت | {_fmt(est.time_savings_sar_year_min)}–{_fmt(est.time_savings_sar_year_max)} |",
        f"| Recovered revenue / إيراد مُستعاد | {_fmt(est.recovered_revenue_sar_year_min)}–{_fmt(est.recovered_revenue_sar_year_max)} |",
        f"| **Gross value / القيمة الإجمالية** | **{_fmt(est.gross_annual_value_sar_min)}–{_fmt(est.gross_annual_value_sar_max)}** |",
        f"| Annual cost / التكلفة السنوية | {_fmt(est.annual_cost_sar)} |",
        f"| **Net value / صافي القيمة** | **{_fmt(est.net_annual_value_sar_min)}–{_fmt(est.net_annual_value_sar_max)}** |",
        "",
    ]
    if est.payback_months_min is not None or est.payback_months_max is not None:
        pmin = est.payback_months_min if est.payback_months_min is not None else "—"
        pmax = est.payback_months_max if est.payback_months_max is not None else "—"
        lines.append(f"**Payback / فترة الاسترداد:** ~{pmin}–{pmax} months (estimate)")
        lines.append("")
    lines.append("**Assumptions / الافتراضات:**")
    lines += [f"- {a}" for a in est.assumptions]
    lines += ["", f"> **{est.disclaimer}**"]
    return "\n".join(lines)
