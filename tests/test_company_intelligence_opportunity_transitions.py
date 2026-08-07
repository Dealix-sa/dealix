"""Tests for Opportunity stage state machine transitions.

Covers:
  - Linear pipeline progression: research → qualify → … → won
  - Fallback to lost/parked from any pipeline stage
  - Parked recovery to research/qualify
  - Lost → parked reconsideration
  - Won as terminal
  - Invalid transition rejection
  - Frozen immutability of original after transition
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence import (
    CanonicalOpportunity,
    OpportunityStage,
    is_valid_opportunity_transition,
    transition_opportunity,
    valid_opportunity_transitions_from,
)


def _opportunity(**overrides: object) -> CanonicalOpportunity:
    defaults: dict[str, object] = dict(
        tenant_id="tenant-a",
        opportunity_id="opp-1",
        company_id="company-1",
        offer_id="offer-1",
        stage=OpportunityStage.RESEARCH,
        score=50,
        next_action="prepare discovery brief",
        proof_target="approved discovery outcome",
    )
    defaults.update(overrides)
    return CanonicalOpportunity(**defaults)


# ---------------------------------------------------------------------------
# Pipeline progression
# ---------------------------------------------------------------------------


class TestPipelineProgression:
    def test_research_to_qualify(self) -> None:
        o = _opportunity(stage=OpportunityStage.RESEARCH)
        result = transition_opportunity(o, to_stage=OpportunityStage.QUALIFY)
        assert result.stage == OpportunityStage.QUALIFY

    def test_qualify_to_approval(self) -> None:
        o = _opportunity(stage=OpportunityStage.QUALIFY)
        result = transition_opportunity(o, to_stage=OpportunityStage.APPROVAL)
        assert result.stage == OpportunityStage.APPROVAL

    def test_approval_to_conversation(self) -> None:
        o = _opportunity(stage=OpportunityStage.APPROVAL)
        result = transition_opportunity(o, to_stage=OpportunityStage.CONVERSATION)
        assert result.stage == OpportunityStage.CONVERSATION

    def test_conversation_to_pilot(self) -> None:
        o = _opportunity(stage=OpportunityStage.CONVERSATION)
        result = transition_opportunity(o, to_stage=OpportunityStage.PILOT)
        assert result.stage == OpportunityStage.PILOT

    def test_pilot_to_proof(self) -> None:
        o = _opportunity(stage=OpportunityStage.PILOT)
        result = transition_opportunity(o, to_stage=OpportunityStage.PROOF)
        assert result.stage == OpportunityStage.PROOF

    def test_proof_to_commercial(self) -> None:
        o = _opportunity(stage=OpportunityStage.PROOF)
        result = transition_opportunity(o, to_stage=OpportunityStage.COMMERCIAL)
        assert result.stage == OpportunityStage.COMMERCIAL

    def test_commercial_to_won(self) -> None:
        o = _opportunity(stage=OpportunityStage.COMMERCIAL)
        result = transition_opportunity(o, to_stage=OpportunityStage.WON)
        assert result.stage == OpportunityStage.WON


# ---------------------------------------------------------------------------
# Full lifecycle
# ---------------------------------------------------------------------------


class TestFullLifecycle:
    def test_full_pipeline_to_won(self) -> None:
        """Research → qualify → … → commercial → won."""
        o = _opportunity(stage=OpportunityStage.RESEARCH)
        for stage in [
            OpportunityStage.QUALIFY,
            OpportunityStage.APPROVAL,
            OpportunityStage.CONVERSATION,
            OpportunityStage.PILOT,
            OpportunityStage.PROOF,
            OpportunityStage.COMMERCIAL,
            OpportunityStage.WON,
        ]:
            o = transition_opportunity(o, to_stage=stage)
        assert o.stage == OpportunityStage.WON

    def test_park_and_restart(self) -> None:
        """Research → parked → research → qualify → lost."""
        o = _opportunity(stage=OpportunityStage.RESEARCH)
        o = transition_opportunity(o, to_stage=OpportunityStage.PARKED)
        o = transition_opportunity(o, to_stage=OpportunityStage.RESEARCH)
        o = transition_opportunity(o, to_stage=OpportunityStage.QUALIFY)
        o = transition_opportunity(o, to_stage=OpportunityStage.LOST)
        assert o.stage == OpportunityStage.LOST


# ---------------------------------------------------------------------------
# Lost/Parked from any pipeline stage
# ---------------------------------------------------------------------------


class TestFallback:
    @pytest.mark.parametrize("stage", [
        OpportunityStage.RESEARCH,
        OpportunityStage.QUALIFY,
        OpportunityStage.APPROVAL,
        OpportunityStage.CONVERSATION,
        OpportunityStage.PILOT,
        OpportunityStage.PROOF,
        OpportunityStage.COMMERCIAL,
    ])
    def test_lost_reachable_from_pipeline(
        self, stage: OpportunityStage
    ) -> None:
        o = _opportunity(stage=stage)
        result = transition_opportunity(o, to_stage=OpportunityStage.LOST)
        assert result.stage == OpportunityStage.LOST

    @pytest.mark.parametrize("stage", [
        OpportunityStage.RESEARCH,
        OpportunityStage.QUALIFY,
        OpportunityStage.APPROVAL,
        OpportunityStage.CONVERSATION,
        OpportunityStage.PILOT,
        OpportunityStage.PROOF,
        OpportunityStage.COMMERCIAL,
    ])
    def test_parked_reachable_from_pipeline(
        self, stage: OpportunityStage
    ) -> None:
        o = _opportunity(stage=stage)
        result = transition_opportunity(o, to_stage=OpportunityStage.PARKED)
        assert result.stage == OpportunityStage.PARKED


# ---------------------------------------------------------------------------
# Recovery from parked/lost
# ---------------------------------------------------------------------------


class TestRecovery:
    def test_lost_to_parked(self) -> None:
        o = _opportunity(stage=OpportunityStage.LOST)
        result = transition_opportunity(o, to_stage=OpportunityStage.PARKED)
        assert result.stage == OpportunityStage.PARKED

    def test_parked_to_research(self) -> None:
        o = _opportunity(stage=OpportunityStage.PARKED)
        result = transition_opportunity(o, to_stage=OpportunityStage.RESEARCH)
        assert result.stage == OpportunityStage.RESEARCH

    def test_parked_to_qualify(self) -> None:
        o = _opportunity(stage=OpportunityStage.PARKED)
        result = transition_opportunity(o, to_stage=OpportunityStage.QUALIFY)
        assert result.stage == OpportunityStage.QUALIFY


# ---------------------------------------------------------------------------
# Terminal state
# ---------------------------------------------------------------------------


class TestTerminalState:
    def test_won_is_terminal(self) -> None:
        assert valid_opportunity_transitions_from(
            OpportunityStage.WON
        ) == frozenset()

    def test_won_transition_rejected(self) -> None:
        o = _opportunity(stage=OpportunityStage.WON)
        with pytest.raises(ValueError, match="invalid opportunity transition"):
            transition_opportunity(o, to_stage=OpportunityStage.RESEARCH)


# ---------------------------------------------------------------------------
# Invalid transitions
# ---------------------------------------------------------------------------


class TestInvalidTransitions:
    def test_research_cannot_skip_to_pilot(self) -> None:
        o = _opportunity(stage=OpportunityStage.RESEARCH)
        with pytest.raises(ValueError, match="invalid opportunity transition"):
            transition_opportunity(o, to_stage=OpportunityStage.PILOT)

    def test_lost_cannot_go_to_won(self) -> None:
        o = _opportunity(stage=OpportunityStage.LOST)
        with pytest.raises(ValueError, match="invalid opportunity transition"):
            transition_opportunity(o, to_stage=OpportunityStage.WON)

    def test_parked_cannot_skip_to_commercial(self) -> None:
        o = _opportunity(stage=OpportunityStage.PARKED)
        with pytest.raises(ValueError, match="invalid opportunity transition"):
            transition_opportunity(o, to_stage=OpportunityStage.COMMERCIAL)

    def test_is_valid_transition_check(self) -> None:
        assert is_valid_opportunity_transition(
            OpportunityStage.RESEARCH, OpportunityStage.QUALIFY
        )
        assert not is_valid_opportunity_transition(
            OpportunityStage.WON, OpportunityStage.RESEARCH
        )


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


class TestImmutability:
    def test_original_unchanged_after_transition(self) -> None:
        o = _opportunity(stage=OpportunityStage.RESEARCH)
        result = transition_opportunity(o, to_stage=OpportunityStage.QUALIFY)
        assert o.stage == OpportunityStage.RESEARCH
        assert result.stage == OpportunityStage.QUALIFY
        assert o.opportunity_id == result.opportunity_id
