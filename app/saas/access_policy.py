"""Role-based SaaS access policy for Dealix."""

from __future__ import annotations

ROLE_PERMISSIONS = {
    "owner": {"*"},
    "admin": {"workspace:read", "workspace:write", "team:read", "team:write", "billing:read", "audit:read"},
    "operator": {"workspace:read", "workflow:run", "report:read"},
    "viewer": {"workspace:read", "report:read"},
    "billing_admin": {"billing:read", "billing:write"},
}


def has_permission(role: str, permission: str) -> bool:
    permissions = ROLE_PERMISSIONS.get(role, set())
    return "*" in permissions or permission in permissions


def require_permission(role: str, permission: str) -> None:
    if not has_permission(role, permission):
        raise PermissionError(f"role {role!r} is missing permission {permission!r}")
