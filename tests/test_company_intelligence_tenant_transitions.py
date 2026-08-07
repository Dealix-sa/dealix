"""Tests for Tenant state machine transitions.

Covers:
  - Active → suspended → active recovery
  - Active → churned terminal
  - Suspended → churned terminal
  - Churned is terminal
  - Invalid transition rejection
  - Frozen immutability of original after transition
  - suspended_at auto-set and cleared
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.tenant_contracts import (
    TenantStatus,
    build_tenant,
    is_valid_tenant_transition,
    transition_tenant,
    valid_tenant_transitions_from,
)


def _tenant(**overrides: object):
    defaults = dict(
        handle="test-tenant",
        name="Test Tenant",
        source_id="source-1",
    )
    defaults.update(overrides)
    return build_tenant(**defaults)


# ---------------------------------------------------------------------------
# Valid transitions
# ---------------------------------------------------------------------------


class TestValidTransitions:
    def test_active_to_suspended(self) -> None:
        t = _tenant(status=TenantStatus.ACTIVE)
        result = transition_tenant(t, to_status=TenantStatus.SUSPENDED)
        assert result.status == TenantStatus.SUSPENDED
        assert result.suspended_at is not None

    def test_active_to_churned(self) -> None:
        t = _tenant(status=TenantStatus.ACTIVE)
        result = transition_tenant(t, to_status=TenantStatus.CHURNED)
        assert result.status == TenantStatus.CHURNED

    def test_suspended_to_active(self) -> None:
        t = _tenant(status=TenantStatus.ACTIVE)
        t = transition_tenant(t, to_status=TenantStatus.SUSPENDED)
        result = transition_tenant(t, to_status=TenantStatus.ACTIVE)
        assert result.status == TenantStatus.ACTIVE
        assert result.suspended_at is None

    def test_suspended_to_churned(self) -> None:
        t = _tenant(status=TenantStatus.ACTIVE)
        t = transition_tenant(t, to_status=TenantStatus.SUSPENDED)
        result = transition_tenant(t, to_status=TenantStatus.CHURNED)
        assert result.status == TenantStatus.CHURNED


# ---------------------------------------------------------------------------
# Full lifecycle
# ---------------------------------------------------------------------------


class TestFullLifecycle:
    def test_suspend_recover_cycle(self) -> None:
        """Active → suspended → active → suspended → churned."""
        t = _tenant(status=TenantStatus.ACTIVE)
        t = transition_tenant(t, to_status=TenantStatus.SUSPENDED)
        assert t.suspended_at is not None
        t = transition_tenant(t, to_status=TenantStatus.ACTIVE)
        assert t.suspended_at is None
        t = transition_tenant(t, to_status=TenantStatus.SUSPENDED)
        t = transition_tenant(t, to_status=TenantStatus.CHURNED)
        assert t.status == TenantStatus.CHURNED


# ---------------------------------------------------------------------------
# Terminal state
# ---------------------------------------------------------------------------


class TestTerminalState:
    def test_churned_is_terminal(self) -> None:
        assert valid_tenant_transitions_from(TenantStatus.CHURNED) == frozenset()

    def test_churned_transition_rejected(self) -> None:
        t = _tenant(status=TenantStatus.ACTIVE)
        t = transition_tenant(t, to_status=TenantStatus.CHURNED)
        with pytest.raises(ValueError, match="invalid tenant transition"):
            transition_tenant(t, to_status=TenantStatus.ACTIVE)


# ---------------------------------------------------------------------------
# Invalid transitions
# ---------------------------------------------------------------------------


class TestInvalidTransitions:
    def test_churned_cannot_suspend(self) -> None:
        t = _tenant(status=TenantStatus.ACTIVE)
        t = transition_tenant(t, to_status=TenantStatus.CHURNED)
        with pytest.raises(ValueError, match="invalid tenant transition"):
            transition_tenant(t, to_status=TenantStatus.SUSPENDED)

    def test_is_valid_transition_check(self) -> None:
        assert is_valid_tenant_transition(
            TenantStatus.ACTIVE, TenantStatus.SUSPENDED
        )
        assert not is_valid_tenant_transition(
            TenantStatus.CHURNED, TenantStatus.ACTIVE
        )


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


class TestImmutability:
    def test_original_unchanged_after_transition(self) -> None:
        t = _tenant(status=TenantStatus.ACTIVE)
        result = transition_tenant(t, to_status=TenantStatus.SUSPENDED)
        assert t.status == TenantStatus.ACTIVE
        assert result.status == TenantStatus.SUSPENDED
        assert t.tenant_id == result.tenant_id
