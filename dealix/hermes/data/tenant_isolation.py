"""
Tenant isolation — ensure two requests on two workspaces never share an
object reference and never leak through joined queries.
"""

from __future__ import annotations

from typing import Any


class TenantIsolationError(Exception):
    pass


def enforce_isolation(records: list[dict[str, Any]], workspace_id: str) -> list[dict[str, Any]]:
    """Reject any record whose ``workspace_id`` does not match the caller's."""
    out: list[dict[str, Any]] = []
    for record in records:
        owner = record.get("workspace_id")
        if owner is None:
            raise TenantIsolationError("record missing workspace_id")
        if owner != workspace_id:
            raise TenantIsolationError(
                f"cross-tenant access denied: record belongs to {owner!r}, "
                f"caller is on {workspace_id!r}"
            )
        out.append(record)
    return out
