"""
Agent runtime — §95.

Executes the 10-step agent lifecycle: context mint, plan, tool checks,
policy/approval, execution, outcome recording. In ``DRAFT_ONLY``
security mode, any external action is forced to draft and the run
completes without side effects.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dealix.sovereign_control_plane.approvals import SovereignApprovalCenter
from dealix.sovereign_control_plane.context_feed import ContextFeedEngine
from dealix.sovereign_control_plane.events import EventBus, make_event
from dealix.sovereign_control_plane.policy import PolicyEngine
from dealix.sovereign_control_plane.security_modes import SecurityModeManager
from dealix.sovereign_control_plane.tool_gateway import HermesToolGateway
from dealix.sovereign_control_plane.tool_runtime import ToolRuntimeLog
from dealix.sovereign_control_plane.types import (
    DataSensitivity,
    RiskLevel,
    RunStatus,
    ToolCallStatus,
)


@dataclass
class AgentRun:
    run_id: str
    agent_id: str
    workspace_id: str
    status: RunStatus
    input: dict[str, Any]
    plan: list[str]
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    output: dict[str, Any] = field(default_factory=dict)
    started_at: str = ""
    finished_at: str | None = None
    context_id: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "agent_id": self.agent_id,
            "workspace_id": self.workspace_id,
            "status": self.status.value,
            "input": dict(self.input),
            "plan": list(self.plan),
            "tool_calls": list(self.tool_calls),
            "output": dict(self.output),
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "context_id": self.context_id,
            "error": self.error,
        }


class AgentRuntime:
    def __init__(
        self,
        context_feed: ContextFeedEngine,
        policy: PolicyEngine,
        approvals: SovereignApprovalCenter,
        tool_gateway: HermesToolGateway,
        tool_log: ToolRuntimeLog,
        security: SecurityModeManager,
        bus: EventBus,
    ) -> None:
        self.context = context_feed
        self.policy = policy
        self.approvals = approvals
        self.tools = tool_gateway
        self.tool_log = tool_log
        self.security = security
        self.bus = bus
        self._runs: dict[str, AgentRun] = {}
        self._lock = threading.Lock()

    def start(
        self,
        agent_id: str,
        workspace_id: str,
        input: dict[str, Any],
        tools_requested: list[str] | None = None,
    ) -> AgentRun:
        run = AgentRun(
            run_id=f"run_{uuid.uuid4().hex[:12]}",
            agent_id=agent_id, workspace_id=workspace_id,
            status=RunStatus.PENDING, input=dict(input), plan=[],
            started_at=datetime.now(UTC).isoformat(),
        )
        tools_requested = tools_requested or []
        # 1 mint context
        try:
            pkt = self.context.mint(
                agent_id=agent_id, workspace_id=workspace_id,
                purpose=input.get("purpose", "agent_run"),
                sensitivity=DataSensitivity(input.get("sensitivity", "INTERNAL")),
                allowed_use=["read", "plan", "act"], data=input.get("data", {}),
            )
            run.context_id = pkt.context_id
            run.plan.append("context_minted")
        except PermissionError as exc:
            run.status = RunStatus.BLOCKED
            run.error = f"context_refused:{exc}"
            return self._finish(run)
        run.status = RunStatus.RUNNING
        # 2 plan steps
        run.plan.extend(["read_input", "evaluate_policy"])
        # 3 policy
        event = {
            "action_type": input.get("action_type", "internal"),
            "sensitivity": input.get("sensitivity", "INTERNAL"),
        }
        outcomes = self.policy.evaluate(event)
        if any(o.block for o in outcomes):
            run.status = RunStatus.BLOCKED
            run.error = "policy_block"
            return self._finish(run)
        # 4 external-action vs security mode
        is_external = input.get("action_type") == "external"
        if is_external and not self.security.can_execute(
            RiskLevel(input.get("risk_level", "low"))
        ):
            run.plan.append("external_forced_to_draft")
            run.output["draft_only"] = True
        # 5 approval
        if any(o.requires_approval for o in outcomes):
            req = self.approvals.submit(
                requested_by=agent_id, workspace_id=workspace_id,
                action_type="sensitive_workflow",
                sovereignty_level=__import__(
                    "dealix.sovereign_control_plane.types", fromlist=["SovereigntyLevel"]
                ).SovereigntyLevel.S2_SAMI_APPROVAL,
                risk_level=RiskLevel(input.get("risk_level", "medium")),
                summary=f"agent {agent_id} requested action",
                payload_preview=input,
            )
            run.status = RunStatus.AWAITING_APPROVAL
            run.plan.append(f"approval_submitted:{req.approval_id}")
            return self._finish(run)
        # 6 tools
        for tool_id in tools_requested:
            res = self.tools.call(agent_id, tool_id, args=input.get("args", {}), context_packet=pkt)
            run.tool_calls.append(res.to_dict())
            if res.status == ToolCallStatus.BLOCKED:
                run.status = RunStatus.BLOCKED
                run.error = res.reason
                return self._finish(run)
            if res.status == ToolCallStatus.APPROVAL_REQUIRED:
                run.status = RunStatus.AWAITING_APPROVAL
                return self._finish(run)
        # 7 outcome
        run.output.setdefault("ok", True)
        run.status = RunStatus.COMPLETED
        return self._finish(run)

    def _finish(self, run: AgentRun) -> AgentRun:
        run.finished_at = datetime.now(UTC).isoformat()
        with self._lock:
            self._runs[run.run_id] = run
        self.bus.publish(make_event(
            event_type="agent.run.finished", source="agent_runtime",
            payload=run.to_dict(), workspace_id=run.workspace_id,
        ))
        return run

    def get(self, run_id: str) -> AgentRun | None:
        return self._runs.get(run_id)

    def all_runs(self) -> list[AgentRun]:
        return list(self._runs.values())
