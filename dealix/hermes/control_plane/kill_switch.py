"""
KillSwitch — instantly disables an agent, tool, or workflow.

The kill switch is checked at the start of every control-plane call.
Flipping a kill switch is itself an S2 action: it requires Sami in the
normal case, but a system actor can also flip it when triggered by an
incident detector (see ``hermes.observability``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class KillTarget(StrEnum):
    AGENT = "agent"
    TOOL = "tool"
    WORKFLOW = "workflow"
    CAPABILITY = "capability"


@dataclass
class KillEntry:
    target_type: KillTarget
    target_id: str
    reason: str
    triggered_by: str
    triggered_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class KillSwitch:
    def __init__(self) -> None:
        self._entries: dict[tuple[KillTarget, str], KillEntry] = {}

    def kill(self, target_type: KillTarget, target_id: str, reason: str, by: str) -> KillEntry:
        entry = KillEntry(
            target_type=target_type,
            target_id=target_id,
            reason=reason,
            triggered_by=by,
        )
        self._entries[(target_type, target_id)] = entry
        return entry

    def revive(self, target_type: KillTarget, target_id: str) -> None:
        self._entries.pop((target_type, target_id), None)

    def is_killed(self, target_type: KillTarget, target_id: str) -> bool:
        return (target_type, target_id) in self._entries

    def all(self) -> list[KillEntry]:
        return list(self._entries.values())


SWITCH = KillSwitch()


def check_request(*, agent_id: str | None, tool_id: str | None, capability: str) -> KillEntry | None:
    if agent_id and SWITCH.is_killed(KillTarget.AGENT, agent_id):
        return SWITCH._entries[(KillTarget.AGENT, agent_id)]
    if tool_id and SWITCH.is_killed(KillTarget.TOOL, tool_id):
        return SWITCH._entries[(KillTarget.TOOL, tool_id)]
    if SWITCH.is_killed(KillTarget.CAPABILITY, capability):
        return SWITCH._entries[(KillTarget.CAPABILITY, capability)]
    return None
