"""Tenant context helpers for Dealix SaaS foundation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TenantContext:
    organization_id: str
    workspace_id: str | None
    user_id: str | None
    role: str
    source: str = "server"

    def require_workspace(self) -> str:
        if not self.workspace_id:
            raise PermissionError("workspace_id is required")
        return self.workspace_id


def build_demo_tenant_context() -> TenantContext:
    return TenantContext(
        organization_id="demo_org",
        workspace_id="demo_workspace",
        user_id="demo_user",
        role="owner",
        source="demo",
    )


def assert_server_validated_context(context: TenantContext) -> None:
    if not context.organization_id:
        raise PermissionError("missing organization_id")
    if context.source == "client_supplied_only":
        raise PermissionError("tenant context must be server validated")
