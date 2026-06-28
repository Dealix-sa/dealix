"""Persuasion is honest: no guarantees, no fake proof, no final price/discount."""

from __future__ import annotations

from app.commercial import persuasion, safety
from app.commercial.schemas import COMMERCIAL_MOTIONS


def test_every_motion_has_a_strategy():
    for motion in COMMERCIAL_MOTIONS:
        strat = persuasion.strategy_for(motion)
        assert strat.angle
        assert strat.cta
        assert strat.avoid  # always lists what to avoid


def test_strategies_avoid_guarantees_and_pricing():
    for motion in COMMERCIAL_MOTIONS:
        strat = persuasion.strategy_for(motion)
        joined = " ".join(strat.avoid).lower()
        assert "guaranteed" in joined
        assert "final price" in joined or "discount" in joined


def test_message_and_proof_points_are_claim_safe():
    for motion in COMMERCIAL_MOTIONS:
        strat = persuasion.strategy_for(motion)
        for text in strat.message_points + strat.proof_points:
            assert safety.contains_blocked_claim(text) is None


def test_price_objection_reframe_forbids_discount():
    reframe = persuasion.reframe_objection("price_objection")
    assert "discount" in reframe.lower()
    assert "never" in reframe.lower() or "do not" in reframe.lower()


def test_strategy_for_returns_independent_copies():
    a = persuasion.strategy_for("sales_prospecting")
    a.message_points.append("mutated")
    b = persuasion.strategy_for("sales_prospecting")
    assert "mutated" not in b.message_points
