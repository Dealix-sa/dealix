"""Tests for the Negotiation Intelligence Engine.

Covers boundary checking, position assessment, move recommendation,
and safety invariants.
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.negotiation_contracts import (
    CanonicalNegotiationStrategy,
    NegotiationApproach,
    NegotiationBoundary,
    NegotiationBoundaryType,
    NegotiationStage,
    NegotiationStrategyStatus,
    build_negotiation_strategy,
    transition_negotiation_stage,
)
from dealix.company_intelligence.negotiation_engine import (
    BoundaryCheckResult,
    BoundaryStatus,
    MoveType,
    NegotiationAssessment,
    PositionStrength,
    RecommendedMove,
    assess_position,
    check_boundaries,
    recommend_move,
)

TENANT = "tenant_test_neg"
SOURCE = "test_source"


def _make_strategy(**overrides):
    defaults = {
        "tenant_id": TENANT,
        "opportunity_id": "opp_001",
        "source_id": SOURCE,
        "value_anchors": (
            "AI-powered revenue intelligence",
            "30-day measurable pilot",
            "No long-term commitment",
        ),
        "concession_sequence": (
            "extended trial period",
            "additional training sessions",
            "quarterly review cadence",
        ),
        "walkaway_conditions": ("below cost threshold",),
    }
    defaults.update(overrides)
    return build_negotiation_strategy(**defaults)


# -----------------------------------------------------------------------
# Boundary checking
# -----------------------------------------------------------------------


class TestBoundaryChecking:
    def test_price_floor_violation(self):
        strategy = _make_strategy(
            boundaries=(
                NegotiationBoundary(
                    boundary_type=NegotiationBoundaryType.PRICE_FLOOR,
                    value="5000",
                    is_hard_limit=True,
                ),
            ),
        )
        results = check_boundaries(
            strategy, current_values={"price_floor": "4000"}
        )
        assert len(results) == 1
        assert results[0].status == BoundaryStatus.HARD_VIOLATION
        assert "below floor" in results[0].message

    def test_price_floor_within(self):
        strategy = _make_strategy(
            boundaries=(
                NegotiationBoundary(
                    boundary_type=NegotiationBoundaryType.PRICE_FLOOR,
                    value="5000",
                    is_hard_limit=True,
                ),
            ),
        )
        results = check_boundaries(
            strategy, current_values={"price_floor": "6000"}
        )
        assert len(results) == 1
        assert results[0].status == BoundaryStatus.WITHIN

    def test_discount_ceiling_violation(self):
        strategy = _make_strategy(
            boundaries=(
                NegotiationBoundary(
                    boundary_type=NegotiationBoundaryType.DISCOUNT_CEILING,
                    value="0.2",
                    is_hard_limit=False,
                ),
            ),
        )
        results = check_boundaries(
            strategy, current_values={"discount_ceiling": "0.3"}
        )
        assert len(results) == 1
        assert results[0].status == BoundaryStatus.SOFT_WARNING

    def test_missing_value_treated_as_within(self):
        strategy = _make_strategy(
            boundaries=(
                NegotiationBoundary(
                    boundary_type=NegotiationBoundaryType.PRICE_FLOOR,
                    value="5000",
                    is_hard_limit=True,
                ),
            ),
        )
        results = check_boundaries(strategy, current_values={})
        assert len(results) == 1
        assert results[0].status == BoundaryStatus.WITHIN
        assert results[0].current_value == "unknown"

    def test_multiple_boundaries(self):
        strategy = _make_strategy(
            boundaries=(
                NegotiationBoundary(
                    boundary_type=NegotiationBoundaryType.PRICE_FLOOR,
                    value="5000",
                    is_hard_limit=True,
                ),
                NegotiationBoundary(
                    boundary_type=NegotiationBoundaryType.DISCOUNT_CEILING,
                    value="0.15",
                    is_hard_limit=True,
                ),
                NegotiationBoundary(
                    boundary_type=NegotiationBoundaryType.TIMELINE_MINIMUM,
                    value="3",
                    is_hard_limit=False,
                ),
            ),
        )
        results = check_boundaries(
            strategy,
            current_values={
                "price_floor": "6000",      # within
                "discount_ceiling": "0.2",   # violation
                "timeline_minimum": "2",     # soft warning
            },
        )
        assert len(results) == 3
        statuses = {r.boundary.boundary_type: r.status for r in results}
        assert statuses[NegotiationBoundaryType.PRICE_FLOOR] == BoundaryStatus.WITHIN
        assert statuses[NegotiationBoundaryType.DISCOUNT_CEILING] == BoundaryStatus.HARD_VIOLATION
        assert statuses[NegotiationBoundaryType.TIMELINE_MINIMUM] == BoundaryStatus.SOFT_WARNING


# -----------------------------------------------------------------------
# Position assessment
# -----------------------------------------------------------------------


class TestPositionAssessment:
    def test_basic_assessment(self):
        strategy = _make_strategy()
        assessment = assess_position(strategy, source_id=SOURCE)
        assert isinstance(assessment, NegotiationAssessment)
        assert assessment.tenant_id == TENANT
        assert assessment.strategy_id == strategy.strategy_id
        assert assessment.requires_human_decision is True

    def test_deterministic_id(self):
        strategy = _make_strategy()
        a1 = assess_position(strategy, source_id=SOURCE)
        a2 = assess_position(strategy, source_id=SOURCE)
        assert a1.assessment_id == a2.assessment_id
        assert a1.assessment_id.startswith("negassess_")

    def test_hard_violation_critical_position(self):
        strategy = _make_strategy(
            boundaries=(
                NegotiationBoundary(
                    boundary_type=NegotiationBoundaryType.PRICE_FLOOR,
                    value="5000",
                    is_hard_limit=True,
                ),
            ),
        )
        assessment = assess_position(
            strategy,
            source_id=SOURCE,
            current_values={"price_floor": "3000"},
        )
        assert assessment.position_strength == PositionStrength.CRITICAL
        assert assessment.has_hard_violations is True

    def test_strong_position_with_leverage(self):
        strategy = _make_strategy()
        assessment = assess_position(
            strategy,
            source_id=SOURCE,
            leverage_score=0.8,
        )
        assert assessment.position_strength == PositionStrength.STRONG

    def test_concession_tracking(self):
        strategy = _make_strategy()
        assessment = assess_position(
            strategy,
            source_id=SOURCE,
            concessions_made=("extended trial period",),
        )
        assert "extended trial period" in assessment.concessions_made
        assert "additional training sessions" in assessment.concessions_remaining
        assert assessment.total_concession_value_pct == pytest.approx(0.33, abs=0.01)

    def test_all_concessions_made_weak_position(self):
        strategy = _make_strategy()
        assessment = assess_position(
            strategy,
            source_id=SOURCE,
            concessions_made=(
                "extended trial period",
                "additional training sessions",
                "quarterly review cadence",
            ),
        )
        assert len(assessment.concessions_remaining) == 0
        assert assessment.total_concession_value_pct == pytest.approx(1.0)
        assert assessment.position_strength == PositionStrength.WEAK


# -----------------------------------------------------------------------
# Move recommendation
# -----------------------------------------------------------------------


class TestMoveRecommendation:
    def test_basic_recommendation(self):
        strategy = _make_strategy()
        assessment = assess_position(strategy, source_id=SOURCE)
        move = recommend_move(assessment, strategy, source_id=SOURCE)
        assert isinstance(move, RecommendedMove)
        assert move.approval_required is True
        assert move.execution_allowed is False

    def test_deterministic_id(self):
        strategy = _make_strategy()
        assessment = assess_position(strategy, source_id=SOURCE)
        m1 = recommend_move(assessment, strategy, source_id=SOURCE)
        m2 = recommend_move(assessment, strategy, source_id=SOURCE)
        assert m1.move_id == m2.move_id
        assert m1.move_id.startswith("negmove_")

    def test_discovery_stage_anchors(self):
        strategy = _make_strategy(stage=NegotiationStage.DISCOVERY)
        assessment = assess_position(strategy, source_id=SOURCE)
        move = recommend_move(assessment, strategy, source_id=SOURCE)
        assert move.move_type == MoveType.ANCHOR
        assert "value" in move.description.lower()

    def test_counter_stage_concedes_when_available(self):
        strategy = _make_strategy(stage=NegotiationStage.COUNTER)
        # Need to transition to COUNTER stage properly
        strategy_at_counter = build_negotiation_strategy(
            tenant_id=TENANT,
            opportunity_id="opp_counter",
            source_id=SOURCE,
            stage=NegotiationStage.COUNTER,
            value_anchors=("value_a",),
            concession_sequence=("concession_1", "concession_2"),
        )
        assessment = assess_position(strategy_at_counter, source_id=SOURCE)
        move = recommend_move(assessment, strategy_at_counter, source_id=SOURCE)
        assert move.move_type == MoveType.CONCEDE
        assert "concession_1" in move.description

    def test_counter_stage_holds_when_exhausted(self):
        strategy = build_negotiation_strategy(
            tenant_id=TENANT,
            opportunity_id="opp_hold",
            source_id=SOURCE,
            stage=NegotiationStage.COUNTER,
            value_anchors=("value_a",),
            concession_sequence=("c1", "c2"),
        )
        assessment = assess_position(
            strategy,
            source_id=SOURCE,
            concessions_made=("c1", "c2"),
        )
        move = recommend_move(assessment, strategy, source_id=SOURCE)
        assert move.move_type == MoveType.HOLD_FIRM

    def test_closing_stage_closes(self):
        strategy = build_negotiation_strategy(
            tenant_id=TENANT,
            opportunity_id="opp_close",
            source_id=SOURCE,
            stage=NegotiationStage.CLOSING,
            value_anchors=("value_a",),
        )
        assessment = assess_position(strategy, source_id=SOURCE)
        move = recommend_move(assessment, strategy, source_id=SOURCE)
        assert move.move_type == MoveType.CLOSE

    def test_hard_violation_walks_away(self):
        strategy = _make_strategy(
            boundaries=(
                NegotiationBoundary(
                    boundary_type=NegotiationBoundaryType.PRICE_FLOOR,
                    value="5000",
                    is_hard_limit=True,
                ),
            ),
        )
        assessment = assess_position(
            strategy,
            source_id=SOURCE,
            current_values={"price_floor": "2000"},
        )
        move = recommend_move(assessment, strategy, source_id=SOURCE)
        assert move.move_type == MoveType.WALK_AWAY

    def test_talking_points_from_strategy(self):
        strategy = _make_strategy()
        assessment = assess_position(strategy, source_id=SOURCE)
        move = recommend_move(assessment, strategy, source_id=SOURCE)
        assert len(move.talking_points) > 0
        assert move.talking_points[0] == "AI-powered revenue intelligence"


# -----------------------------------------------------------------------
# Safety invariants
# -----------------------------------------------------------------------


class TestNegotiationEngineSafety:
    def test_move_always_requires_approval(self):
        with pytest.raises(ValueError, match="require.*approval"):
            RecommendedMove(
                tenant_id=TENANT,
                move_id="negmove_fake",
                assessment_id="negassess_fake",
                strategy_id="negstrat_fake",
                move_type=MoveType.ANCHOR,
                description="test",
                rationale="test",
                approval_required=False,
                execution_allowed=False,
                source_id=SOURCE,
            )

    def test_move_never_allows_execution(self):
        with pytest.raises(ValueError, match="never authorize execution"):
            RecommendedMove(
                tenant_id=TENANT,
                move_id="negmove_fake",
                assessment_id="negassess_fake",
                strategy_id="negstrat_fake",
                move_type=MoveType.ANCHOR,
                description="test",
                rationale="test",
                approval_required=True,
                execution_allowed=True,
                source_id=SOURCE,
            )

    def test_assessment_flags_hard_violations(self):
        """Cannot have hard violations without flagging them."""
        hard_boundary = NegotiationBoundary(
            boundary_type=NegotiationBoundaryType.PRICE_FLOOR,
            value="5000",
            is_hard_limit=True,
        )
        check = BoundaryCheckResult(
            boundary=hard_boundary,
            status=BoundaryStatus.HARD_VIOLATION,
            current_value="3000",
        )
        with pytest.raises(ValueError, match="has_hard_violations"):
            NegotiationAssessment(
                tenant_id=TENANT,
                assessment_id="negassess_fake",
                strategy_id="negstrat_fake",
                opportunity_id="opp_fake",
                current_stage=NegotiationStage.DISCOVERY,
                position_strength=PositionStrength.CRITICAL,
                boundary_checks=(check,),
                has_hard_violations=False,
                source_id=SOURCE,
            )
