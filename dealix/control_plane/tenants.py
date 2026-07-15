"""
Section 53 — Tenant & Workspace Model.

A Tenant is the outer boundary (a company, a partner, Dealix-itself).
A Workspace is the inner boundary inside a Tenant — every signal,
opportunity, outcome, asset, and agent run *must* carry both `tenant_id`
and `workspace_id`. No cross-workspace data leakage.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class WorkspaceKind(StrEnum):
    SOVEREIGN = "sovereign_workspace"
    INTERNAL_DEALIX = "internal_dealix_workspace"
    CUSTOMER = "customer_workspace"
    PARTNER = "partner_workspace"
    TRUST = "trust_workspace"
    VENTURE = "venture_workspace"
    MARKETPLACE = "marketplace_workspace"


@dataclass(frozen=True)
class Workspace:
    workspace_id: str
    tenant_id: str
    kind: WorkspaceKind
    display_name: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class Tenant:
    tenant_id: str
    display_name: str
    is_sovereign: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class TenantRegistry:
    def __init__(self) -> None:
        self._tenants: dict[str, Tenant] = {}
        self._workspaces: dict[str, Workspace] = {}

    def register_tenant(self, tenant: Tenant) -> Tenant:
        if tenant.tenant_id in self._tenants:
            raise ValueError(f"tenant already exists: {tenant.tenant_id}")
        self._tenants[tenant.tenant_id] = tenant
        return tenant

    def register_workspace(self, workspace: Workspace) -> Workspace:
        if workspace.tenant_id not in self._tenants:
            raise KeyError(f"unknown tenant: {workspace.tenant_id}")
        if workspace.workspace_id in self._workspaces:
            raise ValueError(f"workspace already exists: {workspace.workspace_id}")
        self._workspaces[workspace.workspace_id] = workspace
        return workspace

    def get_tenant(self, tenant_id: str) -> Tenant:
        try:
            return self._tenants[tenant_id]
        except KeyError as exc:
            raise KeyError(f"unknown tenant: {tenant_id}") from exc

    def get_workspace(self, workspace_id: str) -> Workspace:
        try:
            return self._workspaces[workspace_id]
        except KeyError as exc:
            raise KeyError(f"unknown workspace: {workspace_id}") from exc

    def workspaces_for(self, tenant_id: str) -> list[Workspace]:
        return [w for w in self._workspaces.values() if w.tenant_id == tenant_id]

    def all_tenants(self) -> list[Tenant]:
        return list(self._tenants.values())

    def assert_same_workspace(self, *workspace_ids: str) -> None:
        unique = set(workspace_ids)
        if len(unique) > 1:
            raise PermissionError(
                f"workspace boundary violation: refusing to cross {sorted(unique)}"
            )
