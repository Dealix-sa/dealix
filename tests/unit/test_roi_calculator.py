"""Unit tests — governed ROI estimator (estimate-only, no guarantees)."""

from __future__ import annotations

import re

from dealix.commercial.roi_calculator import ROIInput, estimate_roi


def test_returns_ranges_and_is_estimate():
    est = estimate_roi(
        ROIInput(
            company_name="Acme",
            manual_hours_per_week=20,
            hourly_cost_sar=80,
            lost_leads_per_month=10,
            avg_deal_value_sar=5000,
            recovered_conversion_pct=15,
            setup_cost_sar=35000,
            monthly_cost_sar=8000,
        )
    )
    assert est.is_estimate is True
    # Ranges are ordered low <= high
    assert est.time_savings_sar_year_min <= est.time_savings_sar_year_max
    assert est.recovered_revenue_sar_year_min <= est.recovered_revenue_sar_year_max
    assert est.gross_annual_value_sar_min <= est.gross_annual_value_sar_max
    assert est.net_annual_value_sar_min <= est.net_annual_value_sar_max
    # Annual cost = setup + 12 * monthly
    assert est.annual_cost_sar == 35000 + 12 * 8000


def test_no_guarantee_language_in_output():
    est = estimate_roi(ROIInput(manual_hours_per_week=10, hourly_cost_sar=60))
    md = est.markdown_ar_en
    assert re.search(r"\bguarantee", md, re.IGNORECASE) is None
    assert "نضمن" not in md
    assert "Estimates, not verified results" in est.disclaimer


def test_zero_input_is_safe():
    est = estimate_roi(ROIInput())
    assert est.gross_annual_value_sar_min == 0.0
    assert est.gross_annual_value_sar_max == 0.0
    # No setup → payback window is zero (nothing to recover), not a crash.
    assert est.payback_months_min == 0.0


def test_conservative_band_below_theoretical_ceiling():
    # Time-only scenario: 10h/wk * 52 * 100 = 520,000 theoretical/yr.
    est = estimate_roi(ROIInput(manual_hours_per_week=10, hourly_cost_sar=100))
    theoretical = 10 * 52 * 100
    assert est.time_savings_sar_year_max < theoretical  # never claims 100% capture
    assert est.time_savings_sar_year_min < est.time_savings_sar_year_max
