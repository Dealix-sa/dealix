"""Tenant resolution for entitlement (feature-gating) checks.

Entitlement decisions answer "which tenant's plan pays for this call?".
That is the same trust question every tenant-scoped route asks, so the
rules live once in :mod:`api.security.tenant_scope` and this module is a
thin alias kept for the feature-gating call sites.

Do not fork the logic here — a second copy is how the two paths drift.
"""

from __future__ import annotations

from api.security.tenant_scope import (
    TENANT_OVERRIDE_HEADER,
    TenantScopeDenied,
    TenantSource,
    resolve_request_tenant_id,
)

# Names kept for feature-gating call sites and their tests.
EntitlementTenantDenied = TenantScopeDenied
resolve_entitlement_tenant_id = resolve_request_tenant_id

__all__ = [
    "TENANT_OVERRIDE_HEADER",
    "EntitlementTenantDenied",
    "TenantScopeDenied",
    "TenantSource",
    "resolve_entitlement_tenant_id",
    "resolve_request_tenant_id",
]
