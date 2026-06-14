"""
Section 54 — Data Classification.

Every record entering the Control Plane carries a `DataClass`. Policies key
off this class to decide who reads, who an Agent receives, and what is
allowed to cross external boundaries.

The golden rule: every Agent receives the *least* context possible.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import IntEnum
from typing import Any

from dealix.control_plane.sovereignty import SovereigntyTier


class DataClass(IntEnum):
    PUBLIC = 0
    INTERNAL = 1
    CONFIDENTIAL = 2
    RESTRICTED = 3
    SOVEREIGN = 4

    @property
    def label(self) -> str:
        return self.name


@dataclass(frozen=True)
class DataRecord:
    record_id: str
    tenant_id: str
    workspace_id: str
    data_class: DataClass
    owner_id: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class _Decision:
    agent_allowed: bool
    external_allowed: bool
    requires_approval: bool


_AGENT_RULES: dict[DataClass, _Decision] = {
    DataClass.PUBLIC: _Decision(True, True, False),
    DataClass.INTERNAL: _Decision(True, False, True),
    DataClass.CONFIDENTIAL: _Decision(True, False, True),
    DataClass.RESTRICTED: _Decision(True, False, True),
    DataClass.SOVEREIGN: _Decision(False, False, True),
}


class DataClassificationPolicy:
    """Static rule book that mirrors the table in Section 54."""

    @staticmethod
    def can_feed_agent(data_class: DataClass, agent_tier: SovereigntyTier) -> bool:
        if data_class is DataClass.SOVEREIGN:
            return agent_tier is SovereigntyTier.SAMI
        if data_class is DataClass.RESTRICTED:
            return agent_tier.at_least(SovereigntyTier.INTERNAL)
        return _AGENT_RULES[data_class].agent_allowed

    @staticmethod
    def can_send_external(data_class: DataClass) -> bool:
        return _AGENT_RULES[data_class].external_allowed

    @staticmethod
    def requires_approval(data_class: DataClass) -> bool:
        return _AGENT_RULES[data_class].requires_approval

    @staticmethod
    def assert_can_export(data_class: DataClass, actor_tier: SovereigntyTier) -> None:
        if data_class is DataClass.SOVEREIGN and actor_tier is not SovereigntyTier.SAMI:
            raise PermissionError("only Sami may export SOVEREIGN data")
        if data_class is DataClass.RESTRICTED and not actor_tier.at_least(
            SovereigntyTier.INTERNAL
        ):
            raise PermissionError("RESTRICTED data export requires Internal+ tier")
