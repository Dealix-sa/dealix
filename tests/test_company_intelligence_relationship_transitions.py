"""Tests for Relationship state machine transitions.

Covers:
  - Discovery → confirmed → active pipeline
  - Active ↔ inactive recovery cycle
  - Dissolved reachable from all non-terminal states
  - Dissolved as terminal
  - Invalid transition rejection
  - Frozen immutability of original after transition
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.relationship_contracts import (
    EntityType,
    RelationshipStatus,
    RelationshipType,
    build_relationship,
    is_valid_relationship_transition,
    transition_relationship,
    valid_relationship_transitions_from,
)


def _relationship(**overrides: object):
    defaults = dict(
        tenant_id="tenant-a",
        from_id="company-a",
        from_type=EntityType.COMPANY,
        to_id="company-b",
        to_type=EntityType.COMPANY,
        relationship_type=RelationshipType.CUSTOMER,
        source_id="source-1",
    )
    defaults.update(overrides)
    return build_relationship(**defaults)


# ---------------------------------------------------------------------------
# Valid transitions — pipeline
# ---------------------------------------------------------------------------


class TestPipeline:
    def test_discovered_to_confirmed(self) -> None:
        r = _relationship(status=RelationshipStatus.DISCOVERED)
        result = transition_relationship(r, to_status=RelationshipStatus.CONFIRMED)
        assert result.status == RelationshipStatus.CONFIRMED

    def test_confirmed_to_active(self) -> None:
        r = _relationship(status=RelationshipStatus.CONFIRMED)
        result = transition_relationship(r, to_status=RelationshipStatus.ACTIVE)
        assert result.status == RelationshipStatus.ACTIVE

    def test_active_to_inactive(self) -> None:
        r = _relationship(status=RelationshipStatus.ACTIVE)
        result = transition_relationship(r, to_status=RelationshipStatus.INACTIVE)
        assert result.status == RelationshipStatus.INACTIVE

    def test_inactive_to_active(self) -> None:
        r = _relationship(status=RelationshipStatus.INACTIVE)
        result = transition_relationship(r, to_status=RelationshipStatus.ACTIVE)
        assert result.status == RelationshipStatus.ACTIVE


# ---------------------------------------------------------------------------
# Full lifecycle
# ---------------------------------------------------------------------------


class TestFullLifecycle:
    def test_full_relationship_lifecycle(self) -> None:
        """Discovered → confirmed → active → inactive → active → dissolved."""
        r = _relationship(status=RelationshipStatus.DISCOVERED)
        r = transition_relationship(r, to_status=RelationshipStatus.CONFIRMED)
        r = transition_relationship(r, to_status=RelationshipStatus.ACTIVE)
        r = transition_relationship(r, to_status=RelationshipStatus.INACTIVE)
        r = transition_relationship(r, to_status=RelationshipStatus.ACTIVE)
        r = transition_relationship(r, to_status=RelationshipStatus.DISSOLVED)
        assert r.status == RelationshipStatus.DISSOLVED


# ---------------------------------------------------------------------------
# Dissolved from any non-terminal
# ---------------------------------------------------------------------------


class TestDissolvedFromAny:
    @pytest.mark.parametrize("status", [
        RelationshipStatus.DISCOVERED,
        RelationshipStatus.CONFIRMED,
        RelationshipStatus.ACTIVE,
        RelationshipStatus.INACTIVE,
    ])
    def test_dissolved_reachable(self, status: RelationshipStatus) -> None:
        r = _relationship(status=status)
        result = transition_relationship(r, to_status=RelationshipStatus.DISSOLVED)
        assert result.status == RelationshipStatus.DISSOLVED


# ---------------------------------------------------------------------------
# Terminal state
# ---------------------------------------------------------------------------


class TestTerminalState:
    def test_dissolved_is_terminal(self) -> None:
        assert valid_relationship_transitions_from(
            RelationshipStatus.DISSOLVED
        ) == frozenset()

    def test_dissolved_transition_rejected(self) -> None:
        r = _relationship(status=RelationshipStatus.DISSOLVED)
        with pytest.raises(ValueError, match="invalid relationship transition"):
            transition_relationship(r, to_status=RelationshipStatus.ACTIVE)


# ---------------------------------------------------------------------------
# Invalid transitions
# ---------------------------------------------------------------------------


class TestInvalidTransitions:
    def test_discovered_cannot_jump_to_active(self) -> None:
        r = _relationship(status=RelationshipStatus.DISCOVERED)
        with pytest.raises(ValueError, match="invalid relationship transition"):
            transition_relationship(r, to_status=RelationshipStatus.ACTIVE)

    def test_confirmed_cannot_jump_to_inactive(self) -> None:
        r = _relationship(status=RelationshipStatus.CONFIRMED)
        with pytest.raises(ValueError, match="invalid relationship transition"):
            transition_relationship(r, to_status=RelationshipStatus.INACTIVE)

    def test_inactive_cannot_jump_to_confirmed(self) -> None:
        r = _relationship(status=RelationshipStatus.INACTIVE)
        with pytest.raises(ValueError, match="invalid relationship transition"):
            transition_relationship(r, to_status=RelationshipStatus.CONFIRMED)

    def test_is_valid_transition_check(self) -> None:
        assert is_valid_relationship_transition(
            RelationshipStatus.DISCOVERED, RelationshipStatus.CONFIRMED
        )
        assert not is_valid_relationship_transition(
            RelationshipStatus.DISSOLVED, RelationshipStatus.ACTIVE
        )


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


class TestImmutability:
    def test_original_unchanged_after_transition(self) -> None:
        r = _relationship(status=RelationshipStatus.DISCOVERED)
        result = transition_relationship(r, to_status=RelationshipStatus.CONFIRMED)
        assert r.status == RelationshipStatus.DISCOVERED
        assert result.status == RelationshipStatus.CONFIRMED
        assert r.relationship_id == result.relationship_id
