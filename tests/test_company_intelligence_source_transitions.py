"""Tests for Source state machine transitions.

Covers:
  - Active → stale recovery cycle
  - Terminal states (retired, blocked)
  - Invalid transition rejection
  - Frozen immutability of original after transition
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.source_contracts import (
    SourceStatus,
    SourceType,
    build_source,
    is_valid_source_transition,
    transition_source,
    valid_source_transitions_from,
)


def _source(**overrides: object):
    defaults = dict(
        tenant_id="tenant-a",
        deduplication_key="key-1",
        name="Test Source",
        source_type=SourceType.MANUAL,
    )
    defaults.update(overrides)
    return build_source(**defaults)


# ---------------------------------------------------------------------------
# Valid transitions
# ---------------------------------------------------------------------------


class TestValidTransitions:
    def test_active_to_stale(self) -> None:
        s = _source(status=SourceStatus.ACTIVE)
        t = transition_source(s, to_status=SourceStatus.STALE)
        assert t.status == SourceStatus.STALE

    def test_stale_to_active(self) -> None:
        s = _source(status=SourceStatus.STALE)
        t = transition_source(s, to_status=SourceStatus.ACTIVE)
        assert t.status == SourceStatus.ACTIVE

    def test_active_to_retired(self) -> None:
        s = _source(status=SourceStatus.ACTIVE)
        t = transition_source(s, to_status=SourceStatus.RETIRED)
        assert t.status == SourceStatus.RETIRED

    def test_active_to_blocked(self) -> None:
        s = _source(status=SourceStatus.ACTIVE)
        t = transition_source(s, to_status=SourceStatus.BLOCKED)
        assert t.status == SourceStatus.BLOCKED

    def test_stale_to_retired(self) -> None:
        s = _source(status=SourceStatus.STALE)
        t = transition_source(s, to_status=SourceStatus.RETIRED)
        assert t.status == SourceStatus.RETIRED

    def test_stale_to_blocked(self) -> None:
        s = _source(status=SourceStatus.STALE)
        t = transition_source(s, to_status=SourceStatus.BLOCKED)
        assert t.status == SourceStatus.BLOCKED

    def test_staleness_recovery_cycle(self) -> None:
        s = _source(status=SourceStatus.ACTIVE)
        s = transition_source(s, to_status=SourceStatus.STALE)
        s = transition_source(s, to_status=SourceStatus.ACTIVE)
        assert s.status == SourceStatus.ACTIVE


# ---------------------------------------------------------------------------
# Terminal states
# ---------------------------------------------------------------------------


class TestTerminalStates:
    @pytest.mark.parametrize("status", [
        SourceStatus.RETIRED,
        SourceStatus.BLOCKED,
    ])
    def test_terminal_has_no_transitions(self, status: SourceStatus) -> None:
        assert valid_source_transitions_from(status) == frozenset()

    @pytest.mark.parametrize("status", [
        SourceStatus.RETIRED,
        SourceStatus.BLOCKED,
    ])
    def test_terminal_transition_rejected(self, status: SourceStatus) -> None:
        s = _source(status=status)
        with pytest.raises(ValueError, match="invalid source transition"):
            transition_source(s, to_status=SourceStatus.ACTIVE)


# ---------------------------------------------------------------------------
# Invalid transitions
# ---------------------------------------------------------------------------


class TestInvalidTransitions:
    def test_is_valid_transition_check(self) -> None:
        assert is_valid_source_transition(
            SourceStatus.ACTIVE, SourceStatus.STALE
        )
        assert not is_valid_source_transition(
            SourceStatus.RETIRED, SourceStatus.ACTIVE
        )


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


class TestImmutability:
    def test_original_unchanged_after_transition(self) -> None:
        s = _source(status=SourceStatus.ACTIVE)
        t = transition_source(s, to_status=SourceStatus.STALE)
        assert s.status == SourceStatus.ACTIVE
        assert t.status == SourceStatus.STALE
        assert s.source_id == t.source_id
