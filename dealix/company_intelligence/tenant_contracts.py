"""Canonical Tenant contracts for Company Intelligence.

A Tenant is the top-level isolation boundary in Dealix. Every data row
carries a tenant_id for strict scoping. The canonical contract provides
a persistence-neutral representation that normalizes the existing
TenantRecord (db/models.py) and TenantContext (platform_v10) without
replacing either.

The models are persistence-neutral: no database, network, or LLM calls.

Entity ownership: Tenant → tenant_and_auth
    (existing tenant/auth models and request context).
Required fields: id, status.
Forbidden parallel names: WorkspaceTenant, ClientTenant.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class TenantStatus(StrEnum):
    """Lifecycle states for a tenant."""

    ACTIVE = "active"
    SUSPENDED = "suspended"
    CHURNED = "churned"


class TenantPlan(StrEnum):
    """Available subscription plans."""

    PILOT = "pilot"
    STARTER = "starter"
    GROWTH = "growth"
    SCALE = "scale"


# ---------------------------------------------------------------------------
# Stable ID generation
# ---------------------------------------------------------------------------


def _stable_tenant_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"tenant_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Canonical Tenant contract
# ---------------------------------------------------------------------------


class CanonicalTenant(BaseModel):
    """One normalized tenant representation.

    Tenants are the root isolation boundary. Every entity in the
    execution spine carries a tenant_id scoped to one subscribing
    enterprise client.

    Key invariants:
      - Handle must be 3-64 characters.
      - Name cannot be empty.
      - Suspended tenants must have a suspended_at timestamp.
      - Active tenants must not have a suspended_at timestamp.
      - Tenant ID is deterministic from handle.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString

    # Details
    handle: str = Field(..., min_length=3, max_length=64)
    name: NonEmptyString

    # Configuration
    status: TenantStatus = TenantStatus.ACTIVE
    plan: TenantPlan = TenantPlan.PILOT
    timezone: str = "Asia/Riyadh"
    locale: str = "ar"
    currency: str = "SAR"

    # Limits
    max_users: int = Field(default=5, ge=1)

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    suspended_at: datetime | None = None

    # Provenance
    source_id: NonEmptyString

    @model_validator(mode="after")
    def enforce_tenant_invariants(self) -> CanonicalTenant:
        # suspended_at must be timezone-aware if set
        if self.suspended_at is not None and self.suspended_at.tzinfo is None:
            raise ValueError("suspended_at must be timezone-aware")

        # Suspended tenants must have suspended_at
        if self.status == TenantStatus.SUSPENDED and self.suspended_at is None:
            raise ValueError("suspended tenants must have a suspended_at timestamp")

        # Active tenants must not have suspended_at
        if self.status == TenantStatus.ACTIVE and self.suspended_at is not None:
            raise ValueError("active tenants must not have a suspended_at timestamp")

        # Verify deterministic ID
        expected_id = _stable_tenant_id({
            "handle": self.handle,
        })
        if self.tenant_id != expected_id:
            raise ValueError("tenant_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------

_TENANT_TRANSITIONS: dict[TenantStatus, frozenset[TenantStatus]] = {
    TenantStatus.ACTIVE: frozenset({TenantStatus.SUSPENDED, TenantStatus.CHURNED}),
    TenantStatus.SUSPENDED: frozenset({TenantStatus.ACTIVE, TenantStatus.CHURNED}),
    TenantStatus.CHURNED: frozenset(),  # terminal
}


def valid_tenant_transitions_from(status: TenantStatus) -> frozenset[TenantStatus]:
    """Return the set of valid target states from *status*."""
    return _TENANT_TRANSITIONS.get(status, frozenset())


def is_valid_tenant_transition(
    from_status: TenantStatus,
    to_status: TenantStatus,
) -> bool:
    """Check whether *from_status* → *to_status* is a valid transition."""
    return to_status in valid_tenant_transitions_from(from_status)


def transition_tenant(
    tenant: CanonicalTenant,
    *,
    to_status: TenantStatus,
    suspended_at: datetime | None = None,
) -> CanonicalTenant:
    """Return a new CanonicalTenant with *to_status* applied.

    Raises ValueError on invalid transitions. The original is never mutated.
    """
    if not is_valid_tenant_transition(tenant.status, to_status):
        raise ValueError(
            f"invalid tenant transition: {tenant.status.value} → {to_status.value}"
        )
    updates: dict[str, Any] = {"status": to_status}
    if to_status == TenantStatus.SUSPENDED:
        updates["suspended_at"] = suspended_at or datetime.now(UTC)
    elif to_status == TenantStatus.ACTIVE:
        updates["suspended_at"] = None
    return tenant.model_copy(update=updates)


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_tenant(
    *,
    handle: str,
    name: str,
    source_id: str,
    status: TenantStatus = TenantStatus.ACTIVE,
    plan: TenantPlan = TenantPlan.PILOT,
    timezone: str = "Asia/Riyadh",
    locale: str = "ar",
    currency: str = "SAR",
    max_users: int = 5,
    suspended_at: datetime | None = None,
) -> CanonicalTenant:
    """Build a deterministic, normalized tenant."""

    handle = handle.strip()

    tenant_id = _stable_tenant_id({
        "handle": handle,
    })

    return CanonicalTenant(
        tenant_id=tenant_id,
        handle=handle,
        name=name,
        status=status,
        plan=plan,
        timezone=timezone,
        locale=locale,
        currency=currency,
        max_users=max_users,
        suspended_at=suspended_at,
        source_id=source_id,
    )
