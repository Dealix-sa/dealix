"""Audit event contract for SaaS actions."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class AuditEvent:
    organization_id: str
    workspace_id: str | None
    actor_id: str | None
    action: str
    resource_type: str
    resource_id: str | None
    status: str = "ok"
    created_at: str = ""

    def to_dict(self) -> dict[str, str | None]:
        payload = asdict(self)
        if not payload["created_at"]:
            payload["created_at"] = datetime.now(timezone.utc).isoformat()
        return payload


def build_audit_event(**kwargs) -> dict[str, str | None]:
    return AuditEvent(**kwargs).to_dict()
