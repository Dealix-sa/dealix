"""Tests for the M&A Radar API router."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.routers.m_and_a import (
    TargetCompany,
    build_proposal,
    _compute_multiplier,
    _offer_tier,
    SECTOR_MULTIPLIER_TABLE,
)


# ---------------------------------------------------------------------------
# Pure-function tests (no HTTP)
# ---------------------------------------------------------------------------


def test_multiplier_base_is_4() -> None:
    target = TargetCompany(
        name="Test Co",
        sector="retail",
        annual_revenue_sar=1_000_000,
        net_profit_margin=0.10,
        num_employees=20,
        years_in_business=5,
        owner_willing_to_stay=False,  # avoid +0.5 bonus
    )
    mult = _compute_multiplier(target)
    assert mult == pytest.approx(4.0, abs=0.1)


def test_multiplier_tech_sector_adds_bonus() -> None:
    target = TargetCompany(
        name="TechCo",
        sector="tech",
        annual_revenue_sar=2_000_000,
        net_profit_margin=0.15,
        num_employees=50,
        years_in_business=4,
    )
    mult = _compute_multiplier(target)
    assert mult > 4.0


def test_multiplier_high_margin_adds_bonus() -> None:
    target = TargetCompany(
        name="HighMargin Co",
        sector="services",
        annual_revenue_sar=1_000_000,
        net_profit_margin=0.25,  # > 20%
        num_employees=15,
        years_in_business=6,
    )
    mult = _compute_multiplier(target)
    assert mult > 4.0


def test_multiplier_young_company_penalty() -> None:
    target = TargetCompany(
        name="Startup",
        sector="retail",
        annual_revenue_sar=500_000,
        net_profit_margin=0.05,
        num_employees=5,
        years_in_business=1,  # < 2 years
    )
    mult = _compute_multiplier(target)
    assert mult < 4.0


def test_multiplier_capped_at_8() -> None:
    target = TargetCompany(
        name="Unicorn",
        sector="tech",
        annual_revenue_sar=50_000_000,
        net_profit_margin=0.35,
        num_employees=200,
        years_in_business=8,
        has_real_estate=True,
        has_ip=True,
        owner_willing_to_stay=True,
    )
    mult = _compute_multiplier(target)
    assert mult <= 8.0


def test_multiplier_floor_at_2_5() -> None:
    target = TargetCompany(
        name="Struggling Co",
        sector="food",
        annual_revenue_sar=100_000,
        net_profit_margin=0.02,
        num_employees=3,
        years_in_business=1,
        owner_willing_to_stay=False,
    )
    mult = _compute_multiplier(target)
    assert mult >= 2.5


def test_build_proposal_ebitda_calculation() -> None:
    target = TargetCompany(
        name="LogiCo",
        sector="logistics",
        annual_revenue_sar=2_000_000,
        net_profit_margin=0.15,
        num_employees=40,
        years_in_business=7,
    )
    proposal = build_proposal(target)
    assert proposal.ebitda_sar == pytest.approx(300_000, abs=1)
    assert proposal.valuation_sar > proposal.ebitda_sar


def test_build_proposal_split_is_60_40() -> None:
    target = TargetCompany(
        name="RetailX",
        sector="retail",
        annual_revenue_sar=1_000_000,
        net_profit_margin=0.10,
        num_employees=25,
        years_in_business=5,
    )
    proposal = build_proposal(target)
    assert proposal.upfront_cash_sar == pytest.approx(proposal.valuation_sar * 0.60, abs=1)
    assert proposal.earnout_sar == pytest.approx(proposal.valuation_sar * 0.40, abs=1)


def test_loi_contains_company_name() -> None:
    target = TargetCompany(
        name="HealthPlus",
        sector="healthcare",
        annual_revenue_sar=5_000_000,
        net_profit_margin=0.18,
        num_employees=80,
        years_in_business=9,
    )
    proposal = build_proposal(target)
    assert "HealthPlus" in proposal.loi_text_en
    assert "HealthPlus" in proposal.loi_text_ar


def test_offer_tier_mapping() -> None:
    assert _offer_tier(7.5) == "aggressive"
    assert _offer_tier(5.5) == "serious"
    assert _offer_tier(3.0) == "exploratory"


def test_sector_multiplier_table_has_entries() -> None:
    assert "tech" in SECTOR_MULTIPLIER_TABLE
    assert "retail" in SECTOR_MULTIPLIER_TABLE
    assert SECTOR_MULTIPLIER_TABLE["tech"]["base"] == 4.0
