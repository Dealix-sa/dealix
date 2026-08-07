"""Tests for PartnershipOpportunity state machine transitions.

Covers:
  - Full pipeline transitions from signal_detected to active
  - Terminal state (dissolved) enforcement
  - Invalid transition rejection
  - Bidirectional active ↔ paused
  - Frozen immutability of original after transition
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.partnership_contracts import (
    PartnershipStage,
    PartnershipType,
    build_partnership_opportunity,
    is_valid_partnership_transition,
    transition_partnership,
    valid_partnership_transitions_from,
)


def _partnership(**overrides: object):
    defaults = dict(
        tenant_id="tenant-a",
        company_id="company-1",
        partnership_type=PartnershipType.CHANNEL_PARTNER,
        source_id="source-1",
    )
    defaults.update(overrides)
    return build_partnership_opportunity(**defaults)


# ---------------------------------------------------------------------------
# Full pipeline
# ---------------------------------------------------------------------------


class TestFullPipeline:
    def test_signal_to_researched(self) -> None:
        p = _partnership(stage=PartnershipStage.SIGNAL_DETECTED)
        t = transition_partnership(p, to_stage=PartnershipStage.RESEARCHED)
        assert t.stage == PartnershipStage.RESEARCHED

    def test_researched_to_qualified(self) -> None:
        p = _partnership(stage=PartnershipStage.RESEARCHED)
        t = transition_partnership(p, to_stage=PartnershipStage.QUALIFIED)
        assert t.stage == PartnershipStage.QUALIFIED

    def test_qualified_to_proposal_drafted(self) -> None:
        p = _partnership(stage=PartnershipStage.QUALIFIED)
        t = transition_partnership(p, to_stage=PartnershipStage.PROPOSAL_DRAFTED)
        assert t.stage == PartnershipStage.PROPOSAL_DRAFTED

    def test_proposal_drafted_to_under_review(self) -> None:
        p = _partnership(stage=PartnershipStage.PROPOSAL_DRAFTED)
        t = transition_partnership(p, to_stage=PartnershipStage.UNDER_REVIEW)
        assert t.stage == PartnershipStage.UNDER_REVIEW

    def test_under_review_to_approved(self) -> None:
        p = _partnership(stage=PartnershipStage.UNDER_REVIEW)
        t = transition_partnership(p, to_stage=PartnershipStage.APPROVED)
        assert t.stage == PartnershipStage.APPROVED

    def test_approved_to_active(self) -> None:
        p = _partnership(stage=PartnershipStage.APPROVED)
        t = transition_partnership(p, to_stage=PartnershipStage.ACTIVE)
        assert t.stage == PartnershipStage.ACTIVE

    def test_full_pipeline_traversal(self) -> None:
        """Walk the entire happy path."""
        p = _partnership(stage=PartnershipStage.SIGNAL_DETECTED)
        for next_stage in [
            PartnershipStage.RESEARCHED,
            PartnershipStage.QUALIFIED,
            PartnershipStage.PROPOSAL_DRAFTED,
            PartnershipStage.UNDER_REVIEW,
            PartnershipStage.APPROVED,
            PartnershipStage.ACTIVE,
        ]:
            p = transition_partnership(p, to_stage=next_stage)
        assert p.stage == PartnershipStage.ACTIVE


# ---------------------------------------------------------------------------
# Active ↔ paused cycle
# ---------------------------------------------------------------------------


class TestActivePausedCycle:
    def test_active_to_paused(self) -> None:
        p = _partnership(stage=PartnershipStage.ACTIVE)
        t = transition_partnership(p, to_stage=PartnershipStage.PAUSED)
        assert t.stage == PartnershipStage.PAUSED

    def test_paused_to_active(self) -> None:
        p = _partnership(stage=PartnershipStage.PAUSED)
        t = transition_partnership(p, to_stage=PartnershipStage.ACTIVE)
        assert t.stage == PartnershipStage.ACTIVE

    def test_pause_cycle(self) -> None:
        p = _partnership(stage=PartnershipStage.ACTIVE)
        p = transition_partnership(p, to_stage=PartnershipStage.PAUSED)
        p = transition_partnership(p, to_stage=PartnershipStage.ACTIVE)
        assert p.stage == PartnershipStage.ACTIVE


# ---------------------------------------------------------------------------
# Dissolved from any non-terminal state
# ---------------------------------------------------------------------------


class TestDissolvedFromAny:
    @pytest.mark.parametrize("stage", [
        PartnershipStage.SIGNAL_DETECTED,
        PartnershipStage.RESEARCHED,
        PartnershipStage.QUALIFIED,
        PartnershipStage.PROPOSAL_DRAFTED,
        PartnershipStage.UNDER_REVIEW,
        PartnershipStage.APPROVED,
        PartnershipStage.ACTIVE,
        PartnershipStage.PAUSED,
    ])
    def test_can_dissolve_from_any_stage(self, stage: PartnershipStage) -> None:
        p = _partnership(stage=stage)
        t = transition_partnership(p, to_stage=PartnershipStage.DISSOLVED)
        assert t.stage == PartnershipStage.DISSOLVED


# ---------------------------------------------------------------------------
# Terminal state
# ---------------------------------------------------------------------------


class TestTerminalState:
    def test_dissolved_has_no_transitions(self) -> None:
        assert valid_partnership_transitions_from(PartnershipStage.DISSOLVED) == frozenset()

    def test_dissolved_transition_rejected(self) -> None:
        p = _partnership(stage=PartnershipStage.DISSOLVED)
        with pytest.raises(ValueError, match="invalid partnership transition"):
            transition_partnership(p, to_stage=PartnershipStage.SIGNAL_DETECTED)


# ---------------------------------------------------------------------------
# Invalid transitions
# ---------------------------------------------------------------------------


class TestInvalidTransitions:
    def test_signal_cannot_jump_to_active(self) -> None:
        p = _partnership(stage=PartnershipStage.SIGNAL_DETECTED)
        with pytest.raises(ValueError, match="invalid partnership transition"):
            transition_partnership(p, to_stage=PartnershipStage.ACTIVE)

    def test_researched_cannot_jump_to_approved(self) -> None:
        p = _partnership(stage=PartnershipStage.RESEARCHED)
        with pytest.raises(ValueError, match="invalid partnership transition"):
            transition_partnership(p, to_stage=PartnershipStage.APPROVED)

    def test_is_valid_transition_check(self) -> None:
        assert is_valid_partnership_transition(
            PartnershipStage.SIGNAL_DETECTED,
            PartnershipStage.RESEARCHED,
        )
        assert not is_valid_partnership_transition(
            PartnershipStage.SIGNAL_DETECTED,
            PartnershipStage.ACTIVE,
        )


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


class TestImmutability:
    def test_original_unchanged_after_transition(self) -> None:
        p = _partnership(stage=PartnershipStage.SIGNAL_DETECTED)
        t = transition_partnership(p, to_stage=PartnershipStage.RESEARCHED)
        assert p.stage == PartnershipStage.SIGNAL_DETECTED
        assert t.stage == PartnershipStage.RESEARCHED
        assert p.partnership_id == t.partnership_id
