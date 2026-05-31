"""
WorkspaceIdentity — every piece of data lives in a workspace. Workspaces
are isolated: agents can only see data from workspaces they are scoped
to.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class WorkspaceKind(StrEnum):
    DEALIX_INTERNAL = "dealix_internal"
    CUSTOMER = "customer"
    PARTNER = "partner"
    VENTURE = "venture"
    MARKETPLACE = "marketplace"


@dataclass
class WorkspaceIdentity:
    workspace_id: str
    kind: WorkspaceKind
    display_name: str
    owner_actor_id: str
    data_residency: str = "sa"
    pdpl_scope: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "workspace_id": self.workspace_id,
            "kind": self.kind.value,
            "display_name": self.display_name,
            "owner_actor_id": self.owner_actor_id,
            "data_residency": self.data_residency,
            "pdpl_scope": self.pdpl_scope,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }


WORKSPACE_REGISTRY: dict[str, WorkspaceIdentity] = {}


def register_workspace(workspace: WorkspaceIdentity) -> WorkspaceIdentity:
    WORKSPACE_REGISTRY[workspace.workspace_id] = workspace
    return workspace


register_workspace(
    WorkspaceIdentity(
        workspace_id="dealix_internal",
        kind=WorkspaceKind.DEALIX_INTERNAL,
        display_name="Dealix Internal",
        owner_actor_id="sami",
    )
)
