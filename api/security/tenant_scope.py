"""Canonical tenant resolution for any tenant-scoped request.

One rule, one implementation: the tenant that governs a request is derived
from **verified identity**, never from a value the caller supplies. A
caller-declared tenant is an assertion, not a credential — accepting one
turns every object ID into a cross-tenant handle.

Resolution (fail closed at every branch):

1. A normal user is always scoped to their own ``tenant_id``. A declared
   tenant that differs is a cross-tenant attempt and is denied, so it
   surfaces in logs rather than being silently downgraded.
2. A super admin may target another tenant, but only explicitly. Without a
   declared target the request is denied — "no tenant" must never widen to
   "every tenant".
3. A user with no tenant is denied.

Pure functions, so isolation can be tested without an HTTP stack or a
database. Used by the entitlement gate
(``dealix.feature_gating.tenant_context``) and by tenant-scoped routers
such as ``api.routers.pdpl``.
"""

from __future__ import annotations

from typing import Any, Literal

from api.security.rbac import is_super_admin

TenantSource = Literal["authenticated_user", "super_admin_override"]

# Header a super admin uses to target a specific tenant. Honoured ONLY for
# verified super admins (rule 2 above).
TENANT_OVERRIDE_HEADER = "X-Tenant-ID"


class TenantScopeDenied(Exception):
    """Raised when no tenant may be trusted for a request.

    Attributes:
        reason: Stable machine-readable code for audit logs.
        detail: Operator-facing message. Never contains secrets or PII.
    """

    def __init__(self, *, reason: str, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason}: {detail}")


def resolve_request_tenant_id(
    *,
    user_tenant_id: str | None,
    system_role: str | None,
    requested_tenant_id: str | None = None,
) -> tuple[str, TenantSource]:
    """Resolve the tenant that governs this request.

    Args:
        user_tenant_id: ``tenant_id`` of the authenticated user, loaded from
            the database — the only trusted tenant for a normal user.
        system_role: The user's platform role (``super_admin`` or not).
        requested_tenant_id: Tenant declared by the caller (header, query
            param, or body). Attacker-controlled; honoured only for super
            admins.

    Returns:
        ``(tenant_id, source)``; ``source`` records how it was resolved, for
        the audit trail.

    Raises:
        TenantScopeDenied: when no tenant may be trusted.
    """
    requested = (requested_tenant_id or "").strip()

    if is_super_admin(system_role):
        if not requested:
            raise TenantScopeDenied(
                reason="super_admin_tenant_required",
                detail=(
                    "Super-admin requests must name the target tenant "
                    "explicitly before tenant-scoped data is returned."
                ),
            )
        return requested, "super_admin_override"

    tenant_id = (user_tenant_id or "").strip()
    if not tenant_id:
        raise TenantScopeDenied(
            reason="tenant_context_required",
            detail="The authenticated user is not attached to a tenant.",
        )

    if requested and requested != tenant_id:
        raise TenantScopeDenied(
            reason="cross_tenant_access_denied",
            detail=(
                "The declared tenant does not match the authenticated tenant "
                "and is not honoured for non-super-admin users."
            ),
        )

    return tenant_id, "authenticated_user"


def resolve_tenant_for_request(
    request: Any, user: Any, declared_tenant_id: str | None = None
) -> tuple[str, TenantSource]:
    """``resolve_tenant_for_user`` that also honours the override header.

    A super admin must name their target tenant explicitly. They can do so
    in a request body or query string, but the canonical place is the
    ``X-Tenant-ID`` header — so read it here rather than making every route
    remember to. For a normal user the header changes nothing: a value that
    differs from their own tenant is still a cross-tenant denial.
    """
    declared = declared_tenant_id
    if not declared:
        headers = getattr(request, "headers", None)
        if headers is not None:
            declared = headers.get(TENANT_OVERRIDE_HEADER)
    return resolve_tenant_for_user(user, declared)


def resolve_tenant_for_user(
    user: Any, requested_tenant_id: str | None = None
) -> tuple[str, TenantSource]:
    """``resolve_request_tenant_id`` for a loaded user record.

    Convenience wrapper so routers do not each reach for the same two
    attributes and risk reading the wrong one.
    """
    return resolve_request_tenant_id(
        user_tenant_id=getattr(user, "tenant_id", None),
        system_role=getattr(user, "system_role", None),
        requested_tenant_id=requested_tenant_id,
    )
