"""Tests for the canonical Tenant contracts.

Covers:
  - Deterministic ID generation and idempotency
  - Handle validation
  - Suspension invariants
  - Fail-closed on invalid inputs
  - Builder convenience
  - Entity ownership registry alignment
  - Frozen immutability
"""
from __future__ import annotations

from datetime import UTC, datetime

import pytest

from dealix.company_intelligence.tenant_contracts import (
    CanonicalTenant,
    TenantPlan,
    TenantStatus,
    build_tenant,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _tenant(**overrides: object) -> CanonicalTenant:
    """Build a minimal valid tenant, overriding any fields."""
    defaults: dict[str, object] = dict(
        handle="acme-corp",
        name="Acme Corporation",
        source_id="source-1",
    )
    defaults.update(overrides)
    return build_tenant(**defaults)


# ---------------------------------------------------------------------------
# Deterministic identity
# ---------------------------------------------------------------------------


class TestDeterministicIdentity:
    def test_same_inputs_produce_same_id(self) -> None:
        a = _tenant()
        b = _tenant()
        assert a.tenant_id == b.tenant_id

    def test_different_handle_produces_different_id(self) -> None:
        a = _tenant(handle="acme-corp")
        b = _tenant(handle="beta-inc")
        assert a.tenant_id != b.tenant_id

    def test_tenant_id_format(self) -> None:
        a = _tenant()
        assert a.tenant_id.startswith("tenant_")
        assert len(a.tenant_id) == 7 + 16  # "tenant_" + 16 hex chars

    def test_whitespace_in_handle_is_stripped(self) -> None:
        a = _tenant(handle="  acme-corp  ")
        b = _tenant(handle="acme-corp")
        assert a.tenant_id == b.tenant_id

    def test_name_does_not_affect_id(self) -> None:
        """Name is mutable metadata — it must not affect the stable ID."""
        a = _tenant(name="Acme Corporation")
        b = _tenant(name="Acme Corp")
        assert a.tenant_id == b.tenant_id


# ---------------------------------------------------------------------------
# Handle validation
# ---------------------------------------------------------------------------


class TestHandleValidation:
    def test_short_handle_rejected(self) -> None:
        with pytest.raises(ValueError):
            _tenant(handle="ab")

    def test_min_handle_accepted(self) -> None:
        a = _tenant(handle="abc")
        assert a.handle == "abc"

    def test_long_handle_rejected(self) -> None:
        with pytest.raises(ValueError):
            _tenant(handle="a" * 65)

    def test_max_handle_accepted(self) -> None:
        a = _tenant(handle="a" * 64)
        assert len(a.handle) == 64


# ---------------------------------------------------------------------------
# Suspension invariants
# ---------------------------------------------------------------------------


class TestSuspensionInvariants:
    def test_suspended_requires_suspended_at(self) -> None:
        with pytest.raises(ValueError, match="suspended_at"):
            _tenant(status=TenantStatus.SUSPENDED, suspended_at=None)

    def test_active_forbids_suspended_at(self) -> None:
        with pytest.raises(ValueError, match="suspended_at"):
            _tenant(
                status=TenantStatus.ACTIVE,
                suspended_at=datetime.now(UTC),
            )

    def test_suspended_with_timestamp(self) -> None:
        now = datetime.now(UTC)
        a = _tenant(status=TenantStatus.SUSPENDED, suspended_at=now)
        assert a.status == TenantStatus.SUSPENDED
        assert a.suspended_at == now

    def test_churned_status_accepted(self) -> None:
        a = _tenant(status=TenantStatus.CHURNED)
        assert a.status == TenantStatus.CHURNED


# ---------------------------------------------------------------------------
# Plan and configuration
# ---------------------------------------------------------------------------


class TestPlanConfiguration:
    def test_default_plan_is_pilot(self) -> None:
        a = _tenant()
        assert a.plan == TenantPlan.PILOT

    def test_all_plans_accepted(self) -> None:
        for plan in TenantPlan:
            a = _tenant(plan=plan)
            assert a.plan == plan

    def test_default_timezone(self) -> None:
        a = _tenant()
        assert a.timezone == "Asia/Riyadh"

    def test_default_locale(self) -> None:
        a = _tenant()
        assert a.locale == "ar"

    def test_default_currency(self) -> None:
        a = _tenant()
        assert a.currency == "SAR"

    def test_max_users_minimum(self) -> None:
        with pytest.raises(ValueError):
            _tenant(max_users=0)

    def test_max_users_accepted(self) -> None:
        a = _tenant(max_users=100)
        assert a.max_users == 100


# ---------------------------------------------------------------------------
# Extra field protection
# ---------------------------------------------------------------------------


class TestExtraFieldProtection:
    def test_extra_fields_forbidden(self) -> None:
        a = _tenant()
        data = a.model_dump()
        data["rogue_field"] = "injected"
        with pytest.raises(ValueError):
            CanonicalTenant(**data)


# ---------------------------------------------------------------------------
# Builder defaults
# ---------------------------------------------------------------------------


class TestBuilderDefaults:
    def test_default_status_is_active(self) -> None:
        a = _tenant()
        assert a.status == TenantStatus.ACTIVE

    def test_default_plan_is_pilot(self) -> None:
        a = _tenant()
        assert a.plan == TenantPlan.PILOT

    def test_default_max_users(self) -> None:
        a = _tenant()
        assert a.max_users == 5

    def test_builder_with_full_context(self) -> None:
        a = build_tenant(
            handle="enterprise-alpha",
            name="Enterprise Alpha Ltd.",
            source_id="admin-api",
            status=TenantStatus.ACTIVE,
            plan=TenantPlan.GROWTH,
            timezone="Asia/Dubai",
            locale="en",
            currency="AED",
            max_users=50,
        )
        assert a.plan == TenantPlan.GROWTH
        assert a.timezone == "Asia/Dubai"
        assert a.locale == "en"
        assert a.currency == "AED"
        assert a.max_users == 50


# ---------------------------------------------------------------------------
# Frozen immutability
# ---------------------------------------------------------------------------


class TestFrozenImmutability:
    def test_tenant_is_frozen(self) -> None:
        a = _tenant()
        with pytest.raises(Exception):
            a.status = TenantStatus.SUSPENDED  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Entity ownership registry alignment
# ---------------------------------------------------------------------------


class TestEntityOwnershipAlignment:
    """Verify the contract satisfies the required fields from
    company_intelligence_entity_ownership.json for Tenant."""

    def test_required_fields_present(self) -> None:
        a = _tenant()
        # Required: id, status
        assert hasattr(a, "tenant_id") and a.tenant_id
        assert hasattr(a, "status") and a.status

    def test_empty_handle_rejected(self) -> None:
        """Handle must be at least 3 characters."""
        with pytest.raises(ValueError):
            build_tenant(
                handle="",
                name="Test",
                source_id="source-1",
            )

    def test_empty_name_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_tenant(
                handle="test-handle",
                name="",
                source_id="source-1",
            )

    def test_empty_source_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_tenant(
                handle="test-handle",
                name="Test",
                source_id="",
            )
