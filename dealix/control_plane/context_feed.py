"""
Sections 55–56 — Context Feed Engine + Context Packet.

No Agent reads the database directly. The Engine builds a scoped,
expiring `ContextPacket` for each `(agent_id, purpose)` combination,
and stamps it with `allowed_use`, `sensitivity`, and `workspace_id`.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

from dealix.control_plane.data_classification import DataClass


class AllowedUse(StrEnum):
    DRAFT_ONLY = "draft_only"
    INTERNAL_ANALYSIS = "internal_analysis"
    EXTERNAL_SEND = "external_send"
    APPROVAL_REVIEW = "approval_review"
    AUDIT_REPLAY = "audit_replay"
    ASSET_BUILD = "asset_build"


@dataclass(frozen=True)
class ContextPacket:
    context_id: str
    agent_id: str
    purpose: str
    workspace_id: str
    sensitivity: DataClass
    allowed_use: frozenset[AllowedUse]
    data: Mapping[str, Any]
    expires_at: datetime
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def is_expired(self, *, now: datetime | None = None) -> bool:
        moment = now or datetime.now(UTC)
        return moment >= self.expires_at

    def assert_use(self, use: AllowedUse) -> None:
        if use not in self.allowed_use:
            raise PermissionError(
                f"context {self.context_id} forbids use={use.value}; "
                f"allowed={sorted(u.value for u in self.allowed_use)}"
            )
        if self.is_expired():
            raise PermissionError(f"context {self.context_id} has expired")


ContextBuilder = Callable[[str], Mapping[str, Any]]


class ContextFeedEngine:
    """Scoped context provider — *only* surface what the Agent needs."""

    def __init__(self, *, default_ttl_seconds: int = 900) -> None:
        self._default_ttl = timedelta(seconds=default_ttl_seconds)
        self._builders: dict[str, ContextBuilder] = {}
        self._issued: dict[str, ContextPacket] = {}

    def register_builder(self, agent_id: str, builder: ContextBuilder) -> None:
        self._builders[agent_id] = builder

    def issue(
        self,
        *,
        agent_id: str,
        purpose: str,
        workspace_id: str,
        sensitivity: DataClass,
        allowed_use: frozenset[AllowedUse] | set[AllowedUse],
        seed: Mapping[str, Any] | None = None,
        ttl_seconds: int | None = None,
    ) -> ContextPacket:
        builder = self._builders.get(agent_id)
        built = dict(builder(purpose)) if builder else {}
        if seed:
            built.update(dict(seed))
        ttl = timedelta(seconds=ttl_seconds) if ttl_seconds else self._default_ttl
        packet = ContextPacket(
            context_id=f"ctx_{uuid.uuid4().hex[:12]}",
            agent_id=agent_id,
            purpose=purpose,
            workspace_id=workspace_id,
            sensitivity=sensitivity,
            allowed_use=frozenset(allowed_use),
            data=built,
            expires_at=datetime.now(UTC) + ttl,
        )
        self._issued[packet.context_id] = packet
        return packet

    def get(self, context_id: str) -> ContextPacket:
        try:
            return self._issued[context_id]
        except KeyError as exc:
            raise KeyError(f"unknown context: {context_id}") from exc

    def revoke(self, context_id: str) -> None:
        self._issued.pop(context_id, None)

    def active(self) -> list[ContextPacket]:
        return [p for p in self._issued.values() if not p.is_expired()]
