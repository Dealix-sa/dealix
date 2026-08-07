"""Repository-layer tenant assertions.

Defends against OWASP API1:2023 BOLA (Broken Object-Level Authorization) at
the point where an object is about to be returned: given the tenant that owns
the request and the tenant stamped on the object, refuse a mismatch.

**Resolution lives elsewhere, deliberately.** This module used to also resolve
the request's tenant, accepting it from — in order — a JWT claim, an
``X-Tenant-ID`` header, an API-key prefix, or a subdomain. The last three are
caller-controlled, and the header branch returned ``source="header"`` for a
*normal* user, so anyone could name any tenant and be believed. That is
precisely the defect removed from the entitlement gate in #971: a
caller-declared tenant is an assertion, not a credential.

None of it was ever called — but it is exactly the abstraction someone wires
up later because it looks like the right shape, and doing so would silently
reopen every hole that has been closed. So the resolver is gone and the
assertions stay.

The canonical resolver is ``api/security/tenant_scope.py``:
``resolve_tenant_for_request`` derives the tenant from verified identity,
denies a mismatching declared tenant, and honours ``X-Tenant-ID`` only for a
verified super admin who names their target explicitly.

Use ``assert_tenant_match`` and ``filter_tenant_scoped_list`` below as defence
in depth — a per-object check still catches joined queries and background
jobs that never passed through a request dependency.
"""
from __future__ import annotations

from typing import Any


class CrossTenantAccessDenied(Exception):
    """Raised when a request attempts to access data outside its tenant.

    Caller (FastAPI route handler / dependency) catches and converts to
    HTTPException(403). The exception itself stays generic so it can
    be raised from non-HTTP contexts (background jobs, CLI scripts).

    Attributes:
        request_tenant: The tenant_id resolved from the request context.
        object_tenant: The tenant_id stamped on the requested object.
        object_type: e.g. "lead" / "customer" / "proof_event".
        object_id: The object identifier (for audit log).
    """

    def __init__(
        self,
        *,
        request_tenant: str,
        object_tenant: str,
        object_type: str,
        object_id: str,
    ) -> None:
        self.request_tenant = request_tenant
        self.object_tenant = object_tenant
        self.object_type = object_type
        self.object_id = object_id
        super().__init__(
            f"Cross-tenant access blocked: request_tenant={request_tenant!r} "
            f"object_tenant={object_tenant!r} object_type={object_type!r} "
            f"object_id={object_id!r}"
        )


def assert_tenant_match(
    *,
    request_tenant: str,
    object_tenant: str,
    object_type: str,
    object_id: str,
    is_super_admin: bool = False,
) -> None:
    """Hard-rule guard — raises ``CrossTenantAccessDenied`` on mismatch.

    Every repository function that returns customer-scoped data MUST
    call this BEFORE returning. Defense in depth — the middleware
    pre-filters but per-object check catches issues like joined queries
    or background jobs that bypass the request layer.

    Args:
        request_tenant: From ``request.state.tenant_context.tenant_id``.
        object_tenant: From the requested object's ``tenant_id`` field.
        object_type: For audit log (e.g. "lead", "proof_event").
        object_id: For audit log.
        is_super_admin: When True, allows cross-tenant access (still
            recorded in audit log by caller).

    Raises:
        CrossTenantAccessDenied: when tenants mismatch and not super admin.
    """
    if is_super_admin:
        return  # super admin can read across tenants
    if not request_tenant or not object_tenant:
        # Either missing → block (Article 8 — never silent fallback)
        raise CrossTenantAccessDenied(
            request_tenant=request_tenant or "(empty)",
            object_tenant=object_tenant or "(empty)",
            object_type=object_type,
            object_id=object_id,
        )
    if request_tenant != object_tenant:
        raise CrossTenantAccessDenied(
            request_tenant=request_tenant,
            object_tenant=object_tenant,
            object_type=object_type,
            object_id=object_id,
        )


def filter_tenant_scoped_list(
    items: list[Any],
    *,
    request_tenant: str,
    tenant_id_attr: str = "tenant_id",
    is_super_admin: bool = False,
) -> list[Any]:
    """Filter a list to only items matching the request's tenant.

    Use when fetching collections — repository returns the unfiltered
    list, this helper enforces the boundary defensively. Super admin
    bypasses (returns the full list).

    Args:
        items: The unfiltered list (each item must have tenant_id_attr).
        request_tenant: From ``request.state.tenant_context.tenant_id``.
        tenant_id_attr: Attribute name on each item (default "tenant_id").
        is_super_admin: When True, returns items unchanged.

    Returns:
        Filtered list. Items without the attribute are EXCLUDED (Article 8 —
        unknown ownership = blocked).
    """
    if is_super_admin:
        return list(items)
    out: list[Any] = []
    for item in items:
        # Support both dict and dataclass/Pydantic
        if hasattr(item, tenant_id_attr):
            obj_tenant = getattr(item, tenant_id_attr, "")
        elif isinstance(item, dict):
            obj_tenant = item.get(tenant_id_attr, "")
        else:
            continue  # unknown ownership → exclude
        if obj_tenant == request_tenant:
            out.append(item)
    return out
