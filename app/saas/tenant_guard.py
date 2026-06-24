"""Tenant boundary guard."""

from __future__ import annotations

from api.tenant_context import TenantContext, assert_server_validated_context


def assert_same_organization(context: TenantContext, resource_organization_id: str) -> None:
    assert_server_validated_context(context)
    if context.organization_id != resource_organization_id:
        raise PermissionError("cross-tenant access denied")


def assert_workspace_access(context: TenantContext, resource_workspace_id: str | None) -> None:
    assert_server_validated_context(context)
    if resource_workspace_id is None:
        return
    if context.workspace_id != resource_workspace_id:
        raise PermissionError("cross-workspace access denied")
