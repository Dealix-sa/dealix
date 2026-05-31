"""Unit tests for api/routers/saudi_revenue_advisor.py.

Pure unit tests — no HTTP client, no DB, no async.
Imports business-logic functions directly from the router module.
"""

from __future__ import annotations

import pytest

from api.routers.saudi_revenue_advisor import (
    _KNOWN_SECTORS,
    _SEASONAL_TIMING,
    compute_deal_coaching,
    get_deal_velocity,
    get_pricing_guidance,
    get_seasonal_timing,
)


# ---------------------------------------------------------------------------
# Pricing guidance
# ---------------------------------------------------------------------------


def test_pricing_guidance_b2b_saas() -> None:
    result = get_pricing_guidance("b2b_saas")

    assert result["sector"] == "b2b_saas"
    assert result["min_sar"] == 2_000
    assert result["max_sar"] == 25_000
    assert result["avg_sar"] == 8_000
    assert result["pricing_model"] == "monthly_retainer"
    assert result["justification_ar"]
    assert result["justification_en"]
    assert result["disclaimer_ar"] == "هذه تقديرات — ليست ضمانات"
    assert result["disclaimer_en"] == "These are estimates — not guarantees"
    assert result["governance_decision"] == "ALLOW_WITH_REVIEW"


@pytest.mark.parametrize(
    "sector",
    [
        "b2b_saas",
        "agency",
        "healthcare_clinic",
        "real_estate",
        "logistics",
        "fintech",
        "engineering",
    ],
)
def test_pricing_guidance_all_sectors(sector: str) -> None:
    result = get_pricing_guidance(sector)

    assert result["sector"] == sector
    assert isinstance(result["min_sar"], (int, float))
    assert isinstance(result["max_sar"], (int, float))
    assert result["min_sar"] <= result["avg_sar"] <= result["max_sar"]
    assert result["pricing_model"]
    assert "disclaimer_ar" in result
    assert "disclaimer_en" in result
    assert result["governance_decision"] == "ALLOW_WITH_REVIEW"


def test_pricing_guidance_unknown_sector_raises_key_error() -> None:
    with pytest.raises(KeyError):
        get_pricing_guidance("nonexistent_sector_xyz")


def test_pricing_guidance_disclaimer_present_on_all_sectors() -> None:
    for sector in _KNOWN_SECTORS:
        result = get_pricing_guidance(sector)
        assert result["disclaimer_ar"], f"Missing AR disclaimer for {sector}"
        assert result["disclaimer_en"], f"Missing EN disclaimer for {sector}"


# ---------------------------------------------------------------------------
# Deal velocity
# ---------------------------------------------------------------------------


def test_deal_velocity_fintech() -> None:
    result = get_deal_velocity("fintech")

    assert result["sector"] == "fintech"
    assert isinstance(result["avg_days_to_close"], int)
    assert result["avg_days_to_close"] > 0
    assert isinstance(result["typical_decision_makers"], list)
    assert len(result["typical_decision_makers"]) >= 1
    assert isinstance(result["top_objections"], list)
    assert len(result["top_objections"]) >= 1
    assert isinstance(result["success_factors"], list)
    assert len(result["success_factors"]) >= 1
    assert result["governance_decision"] == "ALLOW_WITH_REVIEW"


def test_deal_velocity_unknown_sector_raises_key_error() -> None:
    with pytest.raises(KeyError):
        get_deal_velocity("made_up_sector")


@pytest.mark.parametrize("sector", list(_KNOWN_SECTORS))
def test_deal_velocity_all_known_sectors(sector: str) -> None:
    result = get_deal_velocity(sector)
    assert result["avg_days_to_close"] > 0
    assert result["governance_decision"] == "ALLOW_WITH_REVIEW"


# ---------------------------------------------------------------------------
# Seasonal timing
# ---------------------------------------------------------------------------


def test_seasonal_timing_returns_list() -> None:
    result = get_seasonal_timing()

    assert "windows" in result
    assert isinstance(result["windows"], list)
    assert len(result["windows"]) >= 4


def test_seasonal_timing_each_window_has_required_fields() -> None:
    result = get_seasonal_timing()
    required = {"period", "period_ar", "impact", "recommendation_ar", "recommendation_en"}

    for window in result["windows"]:
        for field in required:
            assert field in window, f"Field '{field}' missing from window: {window.get('period')}"


def test_seasonal_timing_has_ramadan_entry() -> None:
    windows = get_seasonal_timing()["windows"]
    periods = [w["period"] for w in windows]
    assert any("Ramadan" in p for p in periods), "Expected a Ramadan timing entry"


def test_seasonal_timing_governance_decision() -> None:
    result = get_seasonal_timing()
    assert result["governance_decision"] == "ALLOW_WITH_REVIEW"


def test_seasonal_timing_internal_data_unchanged() -> None:
    # Confirm the module-level constant is intact (not mutated by the function).
    result = get_seasonal_timing()
    assert result["windows"] is _SEASONAL_TIMING


# ---------------------------------------------------------------------------
# Deal coach
# ---------------------------------------------------------------------------


def test_deal_coach_high_urgency() -> None:
    # days_in_pipeline >= 60 => urgency == "high"
    result = compute_deal_coaching(
        sector="b2b_saas",
        deal_size_sar=10_000,
        decision_maker_title="CEO",
        days_in_pipeline=65,
    )

    assert result["urgency"] == "high"
    assert isinstance(result["recommended_actions"], list)
    assert len(result["recommended_actions"]) == 3
    assert isinstance(result["risk_factors"], list)
    assert len(result["risk_factors"]) >= 1
    assert result["next_best_action_ar"]
    assert result["next_best_action_en"]
    assert result["governance_decision"] == "ALLOW_WITH_REVIEW"


def test_deal_coach_low_urgency() -> None:
    # days_in_pipeline < 30 => urgency == "low"
    result = compute_deal_coaching(
        sector="agency",
        deal_size_sar=5_000,
        decision_maker_title="Marketing Director",
        days_in_pipeline=7,
    )

    assert result["urgency"] == "low"
    assert result["governance_decision"] == "ALLOW_WITH_REVIEW"
    assert result["disclaimer_ar"]
    assert result["disclaimer_en"]


def test_deal_coach_medium_urgency() -> None:
    # 30 <= days_in_pipeline < 60 => urgency == "medium"
    result = compute_deal_coaching(
        sector="logistics",
        deal_size_sar=9_000,
        decision_maker_title="Operations Director",
        days_in_pipeline=40,
    )

    assert result["urgency"] == "medium"


def test_deal_coach_validates_governance() -> None:
    result = compute_deal_coaching(
        sector="fintech",
        deal_size_sar=50_000,
        decision_maker_title="CFO",
        days_in_pipeline=50,
    )

    assert result["governance_decision"] == "ALLOW_WITH_REVIEW"
    assert "risk_factors" in result
    # fintech should always carry a regulatory risk note
    regulatory_note_present = any(
        "regulatory" in rf.lower() or "sama" in rf.lower() or "fintech" in rf.lower()
        for rf in result["risk_factors"]
    )
    assert regulatory_note_present, (
        f"Expected a fintech regulatory risk factor. Got: {result['risk_factors']}"
    )


def test_deal_coach_cfo_title_gets_roi_action() -> None:
    result = compute_deal_coaching(
        sector="real_estate",
        deal_size_sar=12_000,
        decision_maker_title="CFO",
        days_in_pipeline=10,
    )
    actions_text = " ".join(result["recommended_actions"]).lower()
    assert "roi" in actions_text or "payback" in actions_text


def test_deal_coach_large_deal_triggers_zatca_action() -> None:
    result = compute_deal_coaching(
        sector="engineering",
        deal_size_sar=25_000,
        decision_maker_title="Project Director",
        days_in_pipeline=5,
    )
    actions_text = " ".join(result["recommended_actions"]).lower()
    assert "zatca" in actions_text or "formal proposal" in actions_text


def test_deal_coach_returns_three_recommended_actions() -> None:
    result = compute_deal_coaching(
        sector="b2b_saas",
        deal_size_sar=3_000,
        decision_maker_title="CTO",
        days_in_pipeline=15,
    )
    assert len(result["recommended_actions"]) == 3


def test_deal_coach_disclaimer_present() -> None:
    result = compute_deal_coaching(
        sector="healthcare_clinic",
        deal_size_sar=7_500,
        decision_maker_title="Clinic Director",
        days_in_pipeline=20,
    )
    assert result["disclaimer_ar"] == "هذه تقديرات — ليست ضمانات"
    assert result["disclaimer_en"] == "These are estimates — not guarantees"


def test_deal_coach_unknown_sector_uses_fallback() -> None:
    # Should not raise — unknown sector falls back to default velocity
    result = compute_deal_coaching(
        sector="unknown_sector",
        deal_size_sar=5_000,
        decision_maker_title="CEO",
        days_in_pipeline=10,
    )
    assert "urgency" in result
    assert result["governance_decision"] == "ALLOW_WITH_REVIEW"
