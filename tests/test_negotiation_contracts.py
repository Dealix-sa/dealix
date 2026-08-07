"""Tests for NegotiationStrategy contracts — boundaries, stages, and safety."""
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
    is_valid_negotiation_stage_transition,
    is_valid_strategy_transition,
    transition_negotiation_stage,
    transition_negotiation_status,
    valid_negotiation_stage_transitions_from,
    valid_strategy_transitions_from,
)

# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


class TestBuildNegotiationStrategy:
    """build_negotiation_strategy produces a valid, deterministic strategy."""

    def test_default_strategy(self) -> None:
        strategy = build_negotiation_strategy(
            tenant_id="t1",
            opportunity_id="opp1",
            source_id="src1",
        )
        assert strategy.tenant_id == "t1"
        assert strategy.opportunity_id == "opp1"
        assert strategy.approach == NegotiationApproach.CONSULTATIVE
        assert strategy.stage == NegotiationStage.DISCOVERY
        assert strategy.status == NegotiationStrategyStatus.DRAFT
        assert strategy.approval_required is True
        assert strategy.strategy_id.startswith("negstrat_")

    def test_deterministic_id(self) -> None:
        s1 = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp1", source_id="src1"
        )
        s2 = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp1", source_id="src2"
        )
        assert s1.strategy_id == s2.strategy_id

    def test_different_opportunities_different_ids(self) -> None:
        s1 = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp1", source_id="src1"
        )
        s2 = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp2", source_id="src1"
        )
        assert s1.strategy_id != s2.strategy_id

    def test_with_boundaries(self) -> None:
        boundaries = (
            NegotiationBoundary(
                boundary_type=NegotiationBoundaryType.PRICE_FLOOR,
                value="2000 SAR",
                is_hard_limit=True,
                evidence_ref="market_rate_study",
            ),
            NegotiationBoundary(
                boundary_type=NegotiationBoundaryType.DISCOUNT_CEILING,
                value="15%",
                is_hard_limit=False,
                description="Soft limit — founder can override",
            ),
        )
        strategy = build_negotiation_strategy(
            tenant_id="t1",
            opportunity_id="opp1",
            source_id="src1",
            boundaries=boundaries,
            max_discount_pct=0.15,
        )
        assert len(strategy.boundaries) == 2
        assert strategy.boundaries[0].is_hard_limit is True
        assert strategy.max_discount_pct == 0.15

    def test_with_value_anchors_and_concessions(self) -> None:
        strategy = build_negotiation_strategy(
            tenant_id="t1",
            opportunity_id="opp1",
            source_id="src1",
            value_anchors=(
                "30-day measurable pilot",
                "No CRM replacement required",
                "Human approval on all external actions",
            ),
            concession_sequence=(
                "Extended pilot from 30 to 45 days",
                "Included one additional department",
                "Monthly billing instead of upfront",
            ),
            walkaway_conditions=(
                "Client demands guaranteed revenue",
                "No willingness to provide data access",
            ),
        )
        assert len(strategy.value_anchors) == 3
        assert len(strategy.concession_sequence) == 3
        assert len(strategy.walkaway_conditions) == 2

    def test_with_objection_responses(self) -> None:
        strategy = build_negotiation_strategy(
            tenant_id="t1",
            opportunity_id="opp1",
            source_id="src1",
            objection_responses=(
                ("Too expensive", "Let's look at the ROI over 30 days"),
                ("We have a CRM", "Dealix overlays — no replacement needed"),
            ),
        )
        assert len(strategy.objection_responses) == 2

    def test_with_cultural_notes(self) -> None:
        strategy = build_negotiation_strategy(
            tenant_id="t1",
            opportunity_id="opp1",
            source_id="src1",
            cultural_notes="Client values personal relationship; prefer Arabic",
            relationship_context="Referred by existing customer; warm intro",
        )
        assert "personal relationship" in strategy.cultural_notes


# ---------------------------------------------------------------------------
# Safety invariants
# ---------------------------------------------------------------------------


class TestNegotiationSafetyInvariants:
    """Model validator enforces negotiation safety rules."""

    def test_approval_required_always_true(self) -> None:
        """approval_required=False must raise — negotiations always need approval."""
        with pytest.raises(ValueError, match="always require approval"):
            CanonicalNegotiationStrategy(
                tenant_id="t1",
                strategy_id="negstrat_fake",
                opportunity_id="opp1",
                approach=NegotiationApproach.CONSULTATIVE,
                approval_required=False,  # ← must fail
                evidence_refs=("ev1",),
                source_id="src1",
            )

    def test_no_evidence_or_value_anchors_raises(self) -> None:
        with pytest.raises(
            ValueError, match="at least one value anchor or evidence reference"
        ):
            build_negotiation_strategy(
                tenant_id="t1",
                opportunity_id="opp1",
                source_id="src1",
                value_anchors=(),
                evidence_refs=(),
            )

    def test_frozen_model(self) -> None:
        strategy = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp1", source_id="src1"
        )
        with pytest.raises(Exception):
            strategy.max_discount_pct = 0.99  # type: ignore[misc]

    def test_max_discount_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            build_negotiation_strategy(
                tenant_id="t1",
                opportunity_id="opp1",
                source_id="src1",
                max_discount_pct=1.5,  # > 1.0
            )


# ---------------------------------------------------------------------------
# Stage transitions (negotiation lifecycle)
# ---------------------------------------------------------------------------


class TestNegotiationStageTransitions:
    """Stage transitions follow the negotiation lifecycle."""

    def test_discovery_to_positioning(self) -> None:
        strategy = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp1", source_id="src1"
        )
        moved = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.POSITIONING
        )
        assert moved.stage == NegotiationStage.POSITIONING
        assert moved.strategy_id == strategy.strategy_id

    def test_full_win_path(self) -> None:
        strategy = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp1", source_id="src1"
        )
        strategy = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.POSITIONING
        )
        strategy = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.PROPOSAL
        )
        strategy = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.CLOSING
        )
        strategy = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.CLOSED_WON
        )
        assert strategy.stage == NegotiationStage.CLOSED_WON

    def test_counter_offer_loop(self) -> None:
        """Counter ↔ Proposal can loop as offers go back and forth."""
        strategy = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp1", source_id="src1"
        )
        strategy = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.POSITIONING
        )
        strategy = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.PROPOSAL
        )
        strategy = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.COUNTER
        )
        strategy = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.PROPOSAL
        )
        strategy = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.COUNTER
        )
        assert strategy.stage == NegotiationStage.COUNTER

    def test_stalemate_recovery(self) -> None:
        strategy = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp1", source_id="src1"
        )
        strategy = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.POSITIONING
        )
        strategy = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.PROPOSAL
        )
        strategy = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.STALEMATE
        )
        # Can recover from stalemate back to counter
        strategy = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.COUNTER
        )
        assert strategy.stage == NegotiationStage.COUNTER

    def test_walkaway_to_closed_lost(self) -> None:
        strategy = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp1", source_id="src1"
        )
        strategy = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.WALKAWAY
        )
        strategy = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.CLOSED_LOST
        )
        assert strategy.stage == NegotiationStage.CLOSED_LOST

    def test_closed_won_is_terminal(self) -> None:
        valid = valid_negotiation_stage_transitions_from(NegotiationStage.CLOSED_WON)
        assert len(valid) == 0

    def test_closed_lost_is_terminal(self) -> None:
        valid = valid_negotiation_stage_transitions_from(NegotiationStage.CLOSED_LOST)
        assert len(valid) == 0

    def test_invalid_stage_transition_raises(self) -> None:
        strategy = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp1", source_id="src1"
        )
        with pytest.raises(ValueError, match="invalid negotiation stage transition"):
            transition_negotiation_stage(
                strategy, to_stage=NegotiationStage.CLOSING  # can't skip
            )

    def test_is_valid_stage_transition_helper(self) -> None:
        assert is_valid_negotiation_stage_transition(
            NegotiationStage.DISCOVERY, NegotiationStage.POSITIONING
        )
        assert not is_valid_negotiation_stage_transition(
            NegotiationStage.DISCOVERY, NegotiationStage.CLOSING
        )


# ---------------------------------------------------------------------------
# Status transitions (strategy lifecycle)
# ---------------------------------------------------------------------------


class TestNegotiationStatusTransitions:
    """Status transitions follow the strategy management lifecycle."""

    def test_draft_to_active(self) -> None:
        strategy = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp1", source_id="src1"
        )
        active = transition_negotiation_status(
            strategy, to_status=NegotiationStrategyStatus.ACTIVE
        )
        assert active.status == NegotiationStrategyStatus.ACTIVE

    def test_active_to_paused_and_back(self) -> None:
        strategy = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp1", source_id="src1"
        )
        strategy = transition_negotiation_status(
            strategy, to_status=NegotiationStrategyStatus.ACTIVE
        )
        strategy = transition_negotiation_status(
            strategy, to_status=NegotiationStrategyStatus.PAUSED
        )
        strategy = transition_negotiation_status(
            strategy, to_status=NegotiationStrategyStatus.ACTIVE
        )
        assert strategy.status == NegotiationStrategyStatus.ACTIVE

    def test_completed_is_terminal(self) -> None:
        valid = valid_strategy_transitions_from(NegotiationStrategyStatus.COMPLETED)
        assert len(valid) == 0

    def test_abandoned_is_terminal(self) -> None:
        valid = valid_strategy_transitions_from(NegotiationStrategyStatus.ABANDONED)
        assert len(valid) == 0

    def test_invalid_status_transition_raises(self) -> None:
        strategy = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp1", source_id="src1"
        )
        with pytest.raises(ValueError, match="invalid negotiation status transition"):
            transition_negotiation_status(
                strategy, to_status=NegotiationStrategyStatus.COMPLETED
            )

    def test_is_valid_strategy_transition_helper(self) -> None:
        assert is_valid_strategy_transition(
            NegotiationStrategyStatus.DRAFT,
            NegotiationStrategyStatus.ACTIVE,
        )
        assert not is_valid_strategy_transition(
            NegotiationStrategyStatus.COMPLETED,
            NegotiationStrategyStatus.ACTIVE,
        )


# ---------------------------------------------------------------------------
# ID preservation
# ---------------------------------------------------------------------------


class TestNegotiationIdPreservation:
    """Deterministic IDs survive stage and status transitions."""

    def test_id_stable_across_stage_transitions(self) -> None:
        strategy = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp1", source_id="src1"
        )
        original_id = strategy.strategy_id
        moved = transition_negotiation_stage(
            strategy, to_stage=NegotiationStage.POSITIONING
        )
        assert moved.strategy_id == original_id

    def test_id_stable_across_status_transitions(self) -> None:
        strategy = build_negotiation_strategy(
            tenant_id="t1", opportunity_id="opp1", source_id="src1"
        )
        original_id = strategy.strategy_id
        active = transition_negotiation_status(
            strategy, to_status=NegotiationStrategyStatus.ACTIVE
        )
        assert active.strategy_id == original_id
