"""Tests for the Five-Rung Commercial Ladder."""

from __future__ import annotations

import pytest

from dealix.commercial_ops.five_rung_ladder import (
    OFFER_LADDER,
    LadderContext,
    calculate_pipeline_value,
    get_offer,
    get_upgrade_path_for_all,
    recommend_upgrade,
)


def test_ladder_has_five_rungs():
    assert len(OFFER_LADDER) == 5


def test_get_offer_returns_correct_tier():
    offer = get_offer("sprint_499")
    assert offer["price_sar"] == 499
    assert offer["rung"] == 1


def test_get_offer_unknown_tier_raises():
    with pytest.raises(KeyError):
        get_offer("nonexistent")  # type: ignore[arg-type]


def test_recommend_upgrade_happy_path():
    ctx = LadderContext(
        current_tier="free_diagnostic",
        months_active=2,
        total_paid_sar=0,
        nps_score=9,
        last_interaction_days=3,
        support_tickets_open=0,
    )
    result = recommend_upgrade(ctx)
    assert result["next_tier"] == "sprint_499"
    assert result["readiness_score"] >= 0
    assert isinstance(result["recommended"], bool)


def test_recommend_upgrade_top_tier_returns_no_upgrade():
    ctx = LadderContext(
        current_tier="custom_ai",
        months_active=12,
        total_paid_sar=25000,
    )
    result = recommend_upgrade(ctx)
    assert result["recommended"] is False


def test_pipeline_value_calculation():
    result = calculate_pipeline_value({"sprint_499": 5, "managed_ops": 2})
    assert result["total_mrr_sar"] == pytest.approx(5 * 499 + 2 * 2999, abs=1)
    assert result["total_arr_sar"] > result["total_mrr_sar"]


def test_upgrade_path_is_sequential():
    path = get_upgrade_path_for_all()
    for i, step in enumerate(path):
        assert step["rung"] == i


def test_low_nps_blocks_upgrade():
    ctx = LadderContext(
        current_tier="sprint_499",
        months_active=3,
        total_paid_sar=499,
        nps_score=4,
        last_interaction_days=2,
        support_tickets_open=0,
    )
    result = recommend_upgrade(ctx)
    assert any("NPS" in b for b in result["blockers"])
