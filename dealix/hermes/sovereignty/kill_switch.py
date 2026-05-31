"""Kill switch — instantly suspend any agent, tool, workflow, or workspace."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class KillTarget(StrEnum):
    agent = "agent"
    tool = "tool"
    workflow = "workflow"
    mcp_server = "mcp_server"
    customer_workspace = "customer_workspace"
    partner_workspace = "partner_workspace"
    public_api = "public_api"
    marketplace_listing = "marketplace_listing"
    external_actions = "external_actions"


@dataclass
class KillRecord:
    target_type: KillTarget
    target_id: str
    reason: str
    killed_by: str
    killed_at: str
    restored_at: str | None = None


@dataclass
class KillSwitch:
    _kills: dict[tuple[KillTarget, str], KillRecord] = field(default_factory=dict)

    def kill(
        self,
        target_type: KillTarget,
        target_id: str,
        *,
        reason: str,
        killed_by: str = "Sami",
    ) -> KillRecord:
        record = KillRecord(
            target_type=target_type,
            target_id=target_id,
            reason=reason,
            killed_by=killed_by,
            killed_at=datetime.now(UTC).isoformat(),
        )
        self._kills[(target_type, target_id)] = record
        return record

    def restore(self, target_type: KillTarget, target_id: str) -> KillRecord | None:
        key = (target_type, target_id)
        if key not in self._kills:
            return None
        rec = self._kills[key]
        if rec.restored_at is None:
            self._kills[key] = KillRecord(**{
                **rec.__dict__,
                "restored_at": datetime.now(UTC).isoformat(),
            })
        return self._kills[key]

    def is_killed(self, target_type: KillTarget, target_id: str) -> bool:
        rec = self._kills.get((target_type, target_id))
        return rec is not None and rec.restored_at is None

    def list_active(self) -> list[KillRecord]:
        return [r for r in self._kills.values() if r.restored_at is None]
