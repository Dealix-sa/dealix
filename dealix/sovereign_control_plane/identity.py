"""
Identity registry — §82.

Tracks every actor in the control plane (Sami, internal operators,
customers, partners, agents, tools, API clients, marketplace publishers)
and enforces the sovereign ordering: no Agent / Tool / Partner can
override Sami.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dealix.sovereign_control_plane.types import IdentityKind


@dataclass
class Identity:
    identity_id: str
    kind: IdentityKind
    display_name: str
    created_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "identity_id": self.identity_id,
            "kind": self.kind.value,
            "display_name": self.display_name,
            "created_at": self.created_at,
            "metadata": dict(self.metadata),
        }


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


class IdentityRegistry:
    """Thread-safe identity registry with a single SAMI seat."""

    def __init__(self) -> None:
        self._items: dict[str, Identity] = {}
        self._sami_id: str | None = None
        self._lock = threading.Lock()

    def register_sami(self, display_name: str = "Sami") -> Identity:
        with self._lock:
            if self._sami_id is not None:
                existing = self._items[self._sami_id]
                return existing
            ident = Identity(
                identity_id=_new_id("idn"),
                kind=IdentityKind.SAMI,
                display_name=display_name,
                created_at=_now_iso(),
            )
            self._items[ident.identity_id] = ident
            self._sami_id = ident.identity_id
            return ident

    def register(
        self,
        kind: IdentityKind,
        display_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> Identity:
        if kind == IdentityKind.SAMI:
            raise ValueError("use register_sami() for the sovereign seat")
        with self._lock:
            ident = Identity(
                identity_id=_new_id("idn"),
                kind=kind,
                display_name=display_name,
                created_at=_now_iso(),
                metadata=metadata or {},
            )
            self._items[ident.identity_id] = ident
            return ident

    def get(self, identity_id: str) -> Identity | None:
        return self._items.get(identity_id)

    def sami(self) -> Identity | None:
        if self._sami_id is None:
            return None
        return self._items.get(self._sami_id)

    def list_by_kind(self, kind: IdentityKind) -> list[Identity]:
        return [i for i in self._items.values() if i.kind == kind]

    def rank_of(self, identity_id: str) -> int:
        ident = self._items.get(identity_id)
        if ident is None:
            return -1
        return ident.kind.rank()

    def can_override(self, actor_id: str, target_id: str) -> bool:
        """Return True iff actor has strictly higher rank than target.

        Agents, Tools, Partners, API clients can never override Sami.
        """
        actor = self._items.get(actor_id)
        target = self._items.get(target_id)
        if actor is None or target is None:
            return False
        forbidden = {
            IdentityKind.AGENT,
            IdentityKind.TOOL,
            IdentityKind.PARTNER_ADMIN,
            IdentityKind.API_CLIENT,
            IdentityKind.MARKETPLACE_PUBLISHER,
        }
        if target.kind == IdentityKind.SAMI and actor.kind in forbidden:
            return False
        return actor.kind.rank() > target.kind.rank()
