"""Tests for Persona state machine transitions.

Covers:
  - Draft → active activation
  - Active → under_review / retired lifecycle
  - Under review → active recovery
  - Retired as terminal
  - Invalid transition rejection
  - Frozen immutability of original after transition
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.persona_contracts import (
    PersonaStatus,
    build_persona,
    is_valid_persona_transition,
    transition_persona,
    valid_persona_transitions_from,
)


def _persona(**overrides: object):
    defaults = dict(
        tenant_id="tenant-a",
        name="Saudi B2B SaaS Founder",
        source_id="source-1",
        evidence_refs=("manual_observation",),
    )
    defaults.update(overrides)
    return build_persona(**defaults)


# ---------------------------------------------------------------------------
# Valid transitions
# ---------------------------------------------------------------------------


class TestValidTransitions:
    def test_draft_to_active(self) -> None:
        p = _persona(status=PersonaStatus.DRAFT)
        result = transition_persona(p, to_status=PersonaStatus.ACTIVE)
        assert result.status == PersonaStatus.ACTIVE

    def test_draft_to_retired(self) -> None:
        p = _persona(status=PersonaStatus.DRAFT)
        result = transition_persona(p, to_status=PersonaStatus.RETIRED)
        assert result.status == PersonaStatus.RETIRED

    def test_active_to_under_review(self) -> None:
        p = _persona(status=PersonaStatus.ACTIVE)
        result = transition_persona(p, to_status=PersonaStatus.UNDER_REVIEW)
        assert result.status == PersonaStatus.UNDER_REVIEW

    def test_active_to_retired(self) -> None:
        p = _persona(status=PersonaStatus.ACTIVE)
        result = transition_persona(p, to_status=PersonaStatus.RETIRED)
        assert result.status == PersonaStatus.RETIRED

    def test_under_review_to_active(self) -> None:
        p = _persona(status=PersonaStatus.UNDER_REVIEW)
        result = transition_persona(p, to_status=PersonaStatus.ACTIVE)
        assert result.status == PersonaStatus.ACTIVE

    def test_under_review_to_retired(self) -> None:
        p = _persona(status=PersonaStatus.UNDER_REVIEW)
        result = transition_persona(p, to_status=PersonaStatus.RETIRED)
        assert result.status == PersonaStatus.RETIRED


# ---------------------------------------------------------------------------
# Full lifecycle
# ---------------------------------------------------------------------------


class TestFullLifecycle:
    def test_full_persona_lifecycle(self) -> None:
        """Draft → active → under_review → active → retired."""
        p = _persona(status=PersonaStatus.DRAFT)
        p = transition_persona(p, to_status=PersonaStatus.ACTIVE)
        p = transition_persona(p, to_status=PersonaStatus.UNDER_REVIEW)
        p = transition_persona(p, to_status=PersonaStatus.ACTIVE)
        p = transition_persona(p, to_status=PersonaStatus.RETIRED)
        assert p.status == PersonaStatus.RETIRED


# ---------------------------------------------------------------------------
# Terminal state
# ---------------------------------------------------------------------------


class TestTerminalState:
    def test_retired_is_terminal(self) -> None:
        assert valid_persona_transitions_from(PersonaStatus.RETIRED) == frozenset()

    def test_retired_transition_rejected(self) -> None:
        p = _persona(status=PersonaStatus.RETIRED)
        with pytest.raises(ValueError, match="invalid persona transition"):
            transition_persona(p, to_status=PersonaStatus.DRAFT)


# ---------------------------------------------------------------------------
# Invalid transitions
# ---------------------------------------------------------------------------


class TestInvalidTransitions:
    def test_draft_cannot_jump_to_under_review(self) -> None:
        p = _persona(status=PersonaStatus.DRAFT)
        with pytest.raises(ValueError, match="invalid persona transition"):
            transition_persona(p, to_status=PersonaStatus.UNDER_REVIEW)

    def test_under_review_cannot_jump_to_draft(self) -> None:
        p = _persona(status=PersonaStatus.UNDER_REVIEW)
        with pytest.raises(ValueError, match="invalid persona transition"):
            transition_persona(p, to_status=PersonaStatus.DRAFT)

    def test_is_valid_transition_check(self) -> None:
        assert is_valid_persona_transition(
            PersonaStatus.DRAFT, PersonaStatus.ACTIVE
        )
        assert not is_valid_persona_transition(
            PersonaStatus.RETIRED, PersonaStatus.ACTIVE
        )


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


class TestImmutability:
    def test_original_unchanged_after_transition(self) -> None:
        p = _persona(status=PersonaStatus.DRAFT)
        result = transition_persona(p, to_status=PersonaStatus.ACTIVE)
        assert p.status == PersonaStatus.DRAFT
        assert result.status == PersonaStatus.ACTIVE
        assert p.persona_id == result.persona_id
