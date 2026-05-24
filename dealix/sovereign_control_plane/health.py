"""
System health snapshot — §107.

The 12-metric snapshot pulled live from the control plane's stores,
plus a re-export of the seven red flags from observability.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dealix.sovereign_control_plane.agent_runtime import AgentRuntime
from dealix.sovereign_control_plane.approvals import SovereignApprovalCenter
from dealix.sovereign_control_plane.assets import AssetLibrary
from dealix.sovereign_control_plane.events import EventBus
from dealix.sovereign_control_plane.incidents import IncidentLog
from dealix.sovereign_control_plane.money_command import MoneyCommand
from dealix.sovereign_control_plane.observability import RedFlags
from dealix.sovereign_control_plane.security_modes import SecurityModeManager
from dealix.sovereign_control_plane.tool_runtime import ToolRuntimeLog
from dealix.sovereign_control_plane.types import (
    ApprovalDecision,
    IncidentSeverity,
    RunStatus,
)


@dataclass
class SystemHealth:
    bus: EventBus
    runtime: AgentRuntime
    tool_log: ToolRuntimeLog
    approvals: SovereignApprovalCenter
    money: MoneyCommand
    assets: AssetLibrary
    incidents: IncidentLog
    security: SecurityModeManager
    red_flags: RedFlags

    def snapshot(self) -> dict[str, Any]:
        runs = self.runtime.all_runs()
        completed = sum(1 for r in runs if r.status == RunStatus.COMPLETED)
        blocked = sum(1 for r in runs if r.status == RunStatus.BLOCKED)
        tool_records = self.tool_log.all_records()
        return {
            "security_mode": self.security.current_mode.value,
            "events_total": len(self.bus.tail(10_000)),
            "agent_runs_total": len(runs),
            "agent_runs_completed": completed,
            "agent_runs_blocked": blocked,
            "tool_calls_total": len(tool_records),
            "tool_calls_blocked": len(self.tool_log.list_blocked()),
            "approvals_pending": len(self.approvals.list_pending()),
            "expected_revenue_sar": self.money.expected_revenue(),
            "assets_total": len(self.assets.list()),
            "incidents_open": sum(
                1 for i in self.incidents.list() if i.resolved_at is None
            ),
            "incidents_critical": sum(
                1 for i in self.incidents.list()
                if i.severity == IncidentSeverity.CRITICAL
            ),
            "red_flags": self.red_flags.scan(),
        }


__all__ = ["SystemHealth", "RedFlags"]
