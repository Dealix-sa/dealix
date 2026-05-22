"""Tests for the Market Radar autonomous intelligence module."""

from __future__ import annotations

import pytest

from dealix.intelligence.market_radar import (
    AcquisitionTarget,
    MarketRadar,
    _score_acquisition_target,
    _estimate_addressable_companies,
    _generate_sector_targets,
    _VISION_2030_SECTORS,
)


@pytest.fixture
def radar() -> MarketRadar:
    return MarketRadar()


# ---------------------------------------------------------------------------
# AcquisitionTarget scoring
# ---------------------------------------------------------------------------


def test_score_high_revenue_target() -> None:
    target = AcquisitionTarget(
        company_name="BigCo",
        sector="tech",
        city="Riyadh",
        estimated_revenue_sar=10_000_000,
        years_in_business=7,
        employee_count=60,
        ai_readiness_score=20,
    )
    assert target.acquisition_score >= 70


def test_score_low_ai_readiness_boosts_score() -> None:
    t_low = AcquisitionTarget(
        company_name="LowAI",
        sector="retail",
        city="Riyadh",
        estimated_revenue_sar=2_000_000,
        years_in_business=5,
        employee_count=20,
        ai_readiness_score=10,
    )
    t_high = AcquisitionTarget(
        company_name="HighAI",
        sector="retail",
        city="Riyadh",
        estimated_revenue_sar=2_000_000,
        years_in_business=5,
        employee_count=20,
        ai_readiness_score=80,
    )
    assert t_low.acquisition_score > t_high.acquisition_score


def test_vision_2030_sectors_present() -> None:
    for s in ("tech", "healthcare", "finance", "education", "manufacturing"):
        assert s in _VISION_2030_SECTORS


def test_vision_2030_alignment_boosts_score() -> None:
    t_v2030 = AcquisitionTarget(
        company_name="FinCo",
        sector="finance",  # Vision 2030 sector
        city="Riyadh",
        estimated_revenue_sar=3_000_000,
        years_in_business=5,
        employee_count=30,
        ai_readiness_score=40,
    )
    t_other = AcquisitionTarget(
        company_name="FoodCo",
        sector="food",  # not Vision 2030 priority
        city="Riyadh",
        estimated_revenue_sar=3_000_000,
        years_in_business=5,
        employee_count=30,
        ai_readiness_score=40,
    )
    assert t_v2030.acquisition_score > t_other.acquisition_score


def test_score_capped_at_100() -> None:
    target = AcquisitionTarget(
        company_name="Perfect",
        sector="finance",
        city="Riyadh",
        estimated_revenue_sar=50_000_000,
        years_in_business=10,
        employee_count=200,
        ai_readiness_score=5,
    )
    assert target.acquisition_score <= 100.0


# ---------------------------------------------------------------------------
# MarketRadar.scan_acquisition_targets
# ---------------------------------------------------------------------------


def test_scan_returns_targets(radar: MarketRadar) -> None:
    result = radar.scan_acquisition_targets()
    assert "top_targets" in result
    assert isinstance(result["top_targets"], list)
    assert result["pdpl_compliant"] is True


def test_scan_filters_by_min_score(radar: MarketRadar) -> None:
    result = radar.scan_acquisition_targets(min_score=80.0)
    for t in result["top_targets"]:
        assert t["acquisition_score"] >= 80.0


def test_scan_respects_max_results(radar: MarketRadar) -> None:
    result = radar.scan_acquisition_targets(max_results=3)
    assert len(result["top_targets"]) <= 3


def test_scan_sector_filter(radar: MarketRadar) -> None:
    result = radar.scan_acquisition_targets(sectors=["tech", "finance"])
    assert "tech" in result["sectors_scanned"] or "finance" in result["sectors_scanned"]


def test_scan_sorted_by_score_descending(radar: MarketRadar) -> None:
    result = radar.scan_acquisition_targets()
    scores = [t["acquisition_score"] for t in result["top_targets"]]
    assert scores == sorted(scores, reverse=True)


# ---------------------------------------------------------------------------
# MarketRadar.competitive_threat_score
# ---------------------------------------------------------------------------


def test_threat_high_for_funded_ai_competitor(radar: MarketRadar) -> None:
    result = radar.competitive_threat_score(
        competitor_name="BigAICo",
        competitor_sector="tech",
        has_ai_product=True,
        market_share_pct=25.0,
        has_saudi_presence=True,
        funding_raised_sar=15_000_000,
    )
    assert result["threat_score"] >= 70
    assert result["threat_level"] == "critical"


def test_threat_low_for_unknown_competitor(radar: MarketRadar) -> None:
    result = radar.competitive_threat_score(
        competitor_name="SmallCo",
        competitor_sector="food",
        has_ai_product=False,
        market_share_pct=0.5,
        has_saudi_presence=False,
        funding_raised_sar=0,
    )
    assert result["threat_score"] < 30
    assert result["threat_level"] == "low"


def test_threat_score_capped_at_100(radar: MarketRadar) -> None:
    result = radar.competitive_threat_score(
        competitor_name="MegaCorp",
        competitor_sector="tech",
        has_ai_product=True,
        market_share_pct=50.0,
        has_saudi_presence=True,
        funding_raised_sar=100_000_000,
    )
    assert result["threat_score"] <= 100.0


def test_threat_includes_strategic_response(radar: MarketRadar) -> None:
    result = radar.competitive_threat_score(
        competitor_name="TestComp",
        competitor_sector="retail",
    )
    assert "strategic_response" in result
    assert len(result["strategic_response"]) > 0


# ---------------------------------------------------------------------------
# MarketRadar.revenue_opportunity_map
# ---------------------------------------------------------------------------


def test_opportunity_map_returns_all_sectors(radar: MarketRadar) -> None:
    result = radar.revenue_opportunity_map()
    assert result["sectors_analyzed"] >= 8


def test_opportunity_map_sorted_by_revenue(radar: MarketRadar) -> None:
    result = radar.revenue_opportunity_map()
    revenues = [o["reachable_revenue_sar"] for o in result["opportunities"]]
    assert revenues == sorted(revenues, reverse=True)


def test_opportunity_map_3_month_horizon(radar: MarketRadar) -> None:
    result = radar.revenue_opportunity_map(planning_horizon_months=3)
    assert result["planning_horizon_months"] == 3
    full = radar.revenue_opportunity_map(planning_horizon_months=12)
    # 3-month horizon yields lower reachable revenue than 12-month
    assert result["total_tam_sar"] == full["total_tam_sar"]


def test_opportunity_map_has_top_sector(radar: MarketRadar) -> None:
    result = radar.revenue_opportunity_map()
    assert result["top_sector"] is not None


# ---------------------------------------------------------------------------
# MarketRadar.weekly_market_brief
# ---------------------------------------------------------------------------


def test_weekly_brief_has_required_keys(radar: MarketRadar) -> None:
    brief = radar.weekly_market_brief()
    for key in ("brief_date", "headline_ar", "headline_en", "top_opportunity_sectors",
                "market_signals", "recommended_actions", "pdpl_compliant"):
        assert key in brief


def test_weekly_brief_pdpl_compliant(radar: MarketRadar) -> None:
    brief = radar.weekly_market_brief()
    assert brief["pdpl_compliant"] is True


def test_weekly_brief_has_recommended_actions(radar: MarketRadar) -> None:
    brief = radar.weekly_market_brief()
    assert len(brief["recommended_actions"]) >= 3
    for action in brief["recommended_actions"]:
        assert "priority" in action
        assert "channel" in action


def test_weekly_brief_market_signals_present(radar: MarketRadar) -> None:
    brief = radar.weekly_market_brief()
    assert len(brief["market_signals"]) >= 3
    for sig in brief["market_signals"]:
        assert "signal" in sig
        assert "impact" in sig


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def test_addressable_companies_retail_is_large() -> None:
    count = _estimate_addressable_companies("retail")
    assert count >= 100_000


def test_addressable_companies_unknown_returns_default() -> None:
    count = _estimate_addressable_companies("unknown_sector")
    assert count == 15_000
