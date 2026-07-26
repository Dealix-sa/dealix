"""Canonical tenant resolution for entitlement (feature-gating) checks.

Entitlement decisions answer "which tenant's plan pays for this call?".
That question must be answered from **verified identity only** — never
from a browser-controlled header — otherwise any authenticated user can
have their feature access evaluated against another tenant's plan.

Resolution rules (fail closed at every branch):

1. A normal user is always evaluated against their own ``tenant_id``.
   A mismatching ``X-Tenant-ID`` is treated as a cross-tenant attempt and
   denied, so spoofing surfaces in logs instead of being silently ignored.
2. A super admin may target another tenant explicitly via ``X-Tenant-ID``.
   Without that header there is no global entitlement view — the request
   is denied, because "no tenant" must never mean "every feature".
3. A user without a tenant is denied.

The helpers here are pure functions so tenant-isolation behaviour can be
tested without an HTTP stack or a database.
"""

from __future__ import annotations

from typing import Literal

from api.security.rbac import is_super_admin

TenantSource = Literal["authenticated_user", "super_admin_override"]

# Header a super admin uses to target a specific tenant. It is honoured
# ONLY for verified super admins (rule 2 above).
TENANT_OVERRIDE_HEADER = "X-Tenant-ID"


class EntitlementTenantDenied(Exception):
    """Raised when no entitlement tenant may be resolved for a request.

    Attributes:
        reason: Stable machine-readable code for audit logs.
        detail: Operator-facing message. Never contains secrets.
    """

    def __init__(self, *, reason: str, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason}: {detail}")


def resolve_entitlement_tenant_id(
    *,
    user_tenant_id: str | None,
    system_role: str | None,
    requested_tenant_id: str | None = None,
) -> tuple[str, TenantSource]:
    """Resolve the tenant whose entitlements govern this request.

    Args:
        user_tenant_id: ``tenant_id`` of the authenticated user, loaded
            from the database — the only trusted tenant for normal users.
        system_role: The user's platform role (``super_admin`` or not).
        requested_tenant_id: Raw ``X-Tenant-ID`` header value, if sent.
            Attacker-controlled; honoured only for super admins.

    Returns:
        ``(tenant_id, source)`` where source records how it was resolved,
        for the audit trail.

    Raises:
        EntitlementTenantDenied: when no tenant may be trusted.
    """
    requested = (requested_tenant_id or "").strip()

    if is_super_admin(system_role):
        if not requested:
            raise EntitlementTenantDenied(
                reason="super_admin_tenant_required",
                detail=(
                    "Super-admin entitlement checks require an explicit "
                    f"{TENANT_OVERRIDE_HEADER} header naming the target tenant."
                ),
            )
        return requested, "super_admin_override"

    tenant_id = (user_tenant_id or "").strip()
    if not tenant_id:
        raise EntitlementTenantDenied(
            reason="tenant_context_required",
            detail="The authenticated user is not attached to a tenant.",
        )

    if requested and requested != tenant_id:
        raise EntitlementTenantDenied(
            reason="cross_tenant_entitlement_denied",
            detail=(
                f"{TENANT_OVERRIDE_HEADER} does not match the authenticated "
                "tenant and is not honoured for non-super-admin users."
            ),
        )

    return tenant_id, "authenticated_user"
