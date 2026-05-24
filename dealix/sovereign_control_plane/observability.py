"""
Observability — §97 / §107.

Aggregates run / tool / approval / outcome / cost / incident counts
from the live stores and surfaces the canonical 7 red flags.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dealix.sovereign_control_plane.agent_runtime import AgentRuntime
from dealix.sovereign_control_plane.approvals import SovereignApprovalCenter
from dealix.sovereign_control_plane.events import EventBus
from dealix.sovereign_control_plane.incidents import IncidentLog
from dealix.sovereign_control_plane.tool_gateway import ToolRegistry
from dealix.sovereign_control_plane.tool_runtime import ToolRuntimeLog
from dealix.sovereign_control_plane.types import (
    ApprovalDecision,
    RiskLevel,
    RunStatus,
)


@dataclass
class TraceRecord:
    correlation_id: str
    events: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {"correlation_id": self.correlation_id, "events": list(self.events)}


class Dashboard:
    def __init__(
        self,
        runtime: AgentRuntime,
        tool_log: ToolRuntimeLog,
        tool_registry: ToolRegistry,
        approvals: SovereignApprovalCenter,
        incidents: IncidentLog,
        bus: EventBus,
    ) -> None:
        self.runtime = runtime
        self.tool_log = tool_log
        self.tool_registry = tool_registry
        self.approvals = approvals
        self.incidents = incidents
        self.bus = bus

    def agent_performance(self) -> dict[str, int]:
        runs = self.runtime.all_runs()
        return {
            "total": len(runs),
            "completed": sum(1 for r in runs if r.status == RunStatus.COMPLETED),
            "blocked": sum(1 for r in runs if r.status == RunStatus.BLOCKED),
            "awaiting_approval": sum(1 for r in runs if r.status == RunStatus.AWAITING_APPROVAL),
        }

    def tool_risk(self) -> dict[str, int]:
        out: dict[str, int] = {lvl.value: 0 for lvl in RiskLevel}
        for t in self.tool_registry.list():
            out[t.risk_level.value] += 1
        return out

    def approval_queue(self) -> dict[str, int]:
        pending = self.approvals.list_pending()
        return {
            "pending": len(pending),
            "by_action": {a: sum(1 for p in pending if p.action_type == a)
                          for a in {p.action_type for p in pending}},
        }

    def outcome_graph(self) -> dict[str, int]:
        runs = self.runtime.all_runs()
        return {"runs": len(runs),
                "with_outcomes": sum(1 for r in runs if r.output)}

    def cost_dashboard(self) -> dict[str, float]:
        # No real spend tracking yet — placeholder structure for parity.
        return {"approvals_pending": float(len(self.approvals.list_pending())),
                "tool_calls": float(len(self.tool_log.all_records()))}

    def incident_dashboard(self) -> dict[str, int]:
        items = self.incidents.list()
        return {
            "total": len(items),
            "open": sum(1 for i in items if i.resolved_at is None),
        }

    def asset_creation(self) -> dict[str, int]:
        # Filled in by the SovereignControlPlane facade using AssetLibrary.
        return {"created": 0, "reused": 0}


class RedFlags:
    """Seven red-flag scanner — §97/§107."""

    def __init__(
        self,
        runtime: AgentRuntime,
        tool_log: ToolRuntimeLog,
        tool_registry: ToolRegistry,
        approvals: SovereignApprovalCenter,
    ) -> None:
        self.runtime = runtime
        self.tool_log = tool_log
        self.tool_registry = tool_registry
        self.approvals = approvals

    def scan(self) -> list[dict[str, Any]]:
        flags: list[dict[str, Any]] = []
        runs = self.runtime.all_runs()
        if any(r.status == RunStatus.COMPLETED and not r.output for r in runs):
            flags.append({"flag": "executions_without_outcomes"})
        approval_ids = {p.approval_id for p in self.approvals.list_pending()}
        for r in self.tool_log.all_records():
            if r.status.value == "executed" and not r.result_preview and not approval_ids:
                flags.append({"flag": "external_actions_without_approval",
                              "tool": r.tool_id})
                break
        for t in self.tool_registry.list():
            if not t.owner_id:
                flags.append({"flag": "tools_without_owner", "tool_id": t.tool_id})
        flags.append({"flag": "agents_without_kpis", "note": "stub"})
        flags.append({"flag": "assets_not_reused", "note": "stub"})
        flags.append({"flag": "customers_without_value_reports", "note": "stub"})
        flags.append({"flag": "partners_without_revenue", "note": "stub"})
        return flags
