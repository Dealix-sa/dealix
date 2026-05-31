"""
Workspace registry — §83.

Each workspace has a type, an owner, a tenant scope, a sensitivity
floor, and a default sovereignty level. The bootstrap method creates
one workspace per WorkspaceType owned by Sami.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dealix.sovereign_control_plane.types import (
    DataSensitivity,
    SovereigntyLevel,
    WorkspaceType,
)


@dataclass
class Workspace:
    workspace_id: str
    kind: WorkspaceType
    owner_id: str
    tenant_id: str
    sensitivity_level: DataSensitivity
    sovereignty_level: SovereigntyLevel
    created_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "workspace_id": self.workspace_id,
            "kind": self.kind.value,
            "owner_id": self.owner_id,
            "tenant_id": self.tenant_id,
            "sensitivity_level": self.sensitivity_level.value,
            "sovereignty_level": self.sovereignty_level.value,
            "created_at": self.created_at,
            "metadata": dict(self.metadata),
        }


_DEFAULT_SENSITIVITY: dict[WorkspaceType, DataSensitivity] = {
    WorkspaceType.SOVEREIGN: DataSensitivity.SOVEREIGN,
    WorkspaceType.DEALIX_INTERNAL: DataSensitivity.CONFIDENTIAL,
    WorkspaceType.CUSTOMER: DataSensitivity.RESTRICTED,
    WorkspaceType.PARTNER: DataSensitivity.CONFIDENTIAL,
    WorkspaceType.TRUST: DataSensitivity.RESTRICTED,
    WorkspaceType.VENTURE: DataSensitivity.CONFIDENTIAL,
    WorkspaceType.MARKETPLACE: DataSensitivity.PUBLIC,
    WorkspaceType.API: DataSensitivity.INTERNAL,
}

_DEFAULT_SOVEREIGNTY: dict[WorkspaceType, SovereigntyLevel] = {
    WorkspaceType.SOVEREIGN: SovereigntyLevel.S3_SAMI_DECISION,
    WorkspaceType.DEALIX_INTERNAL: SovereigntyLevel.S2_SAMI_APPROVAL,
    WorkspaceType.CUSTOMER: SovereigntyLevel.S1_TEAM_NOTIFY,
    WorkspaceType.PARTNER: SovereigntyLevel.S2_SAMI_APPROVAL,
    WorkspaceType.TRUST: SovereigntyLevel.S3_SAMI_DECISION,
    WorkspaceType.VENTURE: SovereigntyLevel.S2_SAMI_APPROVAL,
    WorkspaceType.MARKETPLACE: SovereigntyLevel.S2_SAMI_APPROVAL,
    WorkspaceType.API: SovereigntyLevel.S1_TEAM_NOTIFY,
}


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _new_id() -> str:
    return f"wsp_{uuid.uuid4().hex[:12]}"


class WorkspaceRegistry:
    def __init__(self) -> None:
        self._items: dict[str, Workspace] = {}
        self._by_kind: dict[WorkspaceType, str] = {}
        self._lock = threading.Lock()

    def bootstrap(self, sami_id: str, tenant_id: str = "dealix") -> list[Workspace]:
        with self._lock:
            created: list[Workspace] = []
            for kind in WorkspaceType:
                if kind in self._by_kind:
                    continue
                ws = Workspace(
                    workspace_id=_new_id(),
                    kind=kind,
                    owner_id=sami_id,
                    tenant_id=tenant_id,
                    sensitivity_level=_DEFAULT_SENSITIVITY[kind],
                    sovereignty_level=_DEFAULT_SOVEREIGNTY[kind],
                    created_at=_now_iso(),
                )
                self._items[ws.workspace_id] = ws
                self._by_kind[kind] = ws.workspace_id
                created.append(ws)
            return created

    def create(
        self,
        kind: WorkspaceType,
        owner_id: str,
        tenant_id: str,
        sensitivity_level: DataSensitivity | None = None,
        sovereignty_level: SovereigntyLevel | None = None,
    ) -> Workspace:
        with self._lock:
            ws = Workspace(
                workspace_id=_new_id(),
                kind=kind,
                owner_id=owner_id,
                tenant_id=tenant_id,
                sensitivity_level=sensitivity_level or _DEFAULT_SENSITIVITY[kind],
                sovereignty_level=sovereignty_level or _DEFAULT_SOVEREIGNTY[kind],
                created_at=_now_iso(),
            )
            self._items[ws.workspace_id] = ws
            return ws

    def get(self, workspace_id: str) -> Workspace | None:
        return self._items.get(workspace_id)

    def get_by_kind(self, kind: WorkspaceType) -> Workspace | None:
        wid = self._by_kind.get(kind)
        return self._items.get(wid) if wid else None

    def list_all(self) -> list[Workspace]:
        return list(self._items.values())
