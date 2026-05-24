"""
Section 61 — Agent Runtime Lifecycle.

The canonical pipeline an Agent Run *must* traverse:

    Created → Context Loaded → Policy Checked → Tools Authorized
    → Execution Started → Guardrails Applied → Output Validated
    → Trust Checked → Approval Requested if needed → Outcome Required
    → Completed / Blocked

The registry tracks every run and refuses to declare a run COMPLETED
unless its `outcome_required` flag is satisfied (an outcome was logged).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class AgentRunStatus(StrEnum):
    CREATED = "created"
    CONTEXT_LOADED = "context_loaded"
    POLICY_CHECKED = "policy_checked"
    TOOLS_AUTHORIZED = "tools_authorized"
    EXECUTING = "executing"
    GUARDRAILS_APPLIED = "guardrails_applied"
    OUTPUT_VALIDATED = "output_validated"
    TRUST_CHECKED = "trust_checked"
    APPROVAL_REQUESTED = "approval_requested"
    OUTCOME_PENDING = "outcome_pending"
    COMPLETED = "completed"
    BLOCKED = "blocked"


_LIFECYCLE_ORDER: tuple[AgentRunStatus, ...] = (
    AgentRunStatus.CREATED,
    AgentRunStatus.CONTEXT_LOADED,
    AgentRunStatus.POLICY_CHECKED,
    AgentRunStatus.TOOLS_AUTHORIZED,
    AgentRunStatus.EXECUTING,
    AgentRunStatus.GUARDRAILS_APPLIED,
    AgentRunStatus.OUTPUT_VALIDATED,
    AgentRunStatus.TRUST_CHECKED,
    AgentRunStatus.APPROVAL_REQUESTED,
    AgentRunStatus.OUTCOME_PENDING,
    AgentRunStatus.COMPLETED,
)


@dataclass
class AgentRun:
    run_id: str
    agent_id: str
    workspace_id: str
    input_hash: str
    context_id: str | None = None
    tools_requested: list[str] = field(default_factory=list)
    tools_allowed: list[str] = field(default_factory=list)
    guardrails_result: str = "pending"
    trust_result: str = "pending"
    approval_status: str = "not_required"
    approval_id: str | None = None
    output_id: str | None = None
    outcome_required: bool = True
    outcome_id: str | None = None
    status: AgentRunStatus = AgentRunStatus.CREATED
    blocked_reason: str | None = None
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    def advance(self, target: AgentRunStatus) -> None:
        if self.status is AgentRunStatus.BLOCKED:
            raise ValueError(f"run {self.run_id} is blocked")
        if target is AgentRunStatus.BLOCKED:
            self.status = AgentRunStatus.BLOCKED
            return
        try:
            current_index = _LIFECYCLE_ORDER.index(self.status)
            target_index = _LIFECYCLE_ORDER.index(target)
        except ValueError as exc:
            raise ValueError(f"unknown lifecycle status: {exc}") from exc
        if target_index < current_index:
            raise ValueError(
                f"cannot regress run {self.run_id} from {self.status.value} to {target.value}"
            )
        self.status = target

    def block(self, reason: str) -> None:
        self.status = AgentRunStatus.BLOCKED
        self.blocked_reason = reason
        self.completed_at = datetime.now(UTC)

    def complete(self) -> None:
        if self.outcome_required and self.outcome_id is None:
            raise ValueError(
                f"run {self.run_id} cannot complete without logging an outcome"
            )
        self.status = AgentRunStatus.COMPLETED
        self.completed_at = datetime.now(UTC)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "agent_id": self.agent_id,
            "workspace_id": self.workspace_id,
            "input_hash": self.input_hash,
            "context_id": self.context_id,
            "tools_requested": list(self.tools_requested),
            "tools_allowed": list(self.tools_allowed),
            "guardrails_result": self.guardrails_result,
            "trust_result": self.trust_result,
            "approval_status": self.approval_status,
            "approval_id": self.approval_id,
            "output_id": self.output_id,
            "outcome_required": self.outcome_required,
            "outcome_id": self.outcome_id,
            "status": self.status.value,
            "blocked_reason": self.blocked_reason,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


class AgentRunRegistry:
    def __init__(self) -> None:
        self._runs: dict[str, AgentRun] = {}

    def start(
        self,
        *,
        agent_id: str,
        workspace_id: str,
        input_hash: str,
        outcome_required: bool = True,
    ) -> AgentRun:
        run = AgentRun(
            run_id=f"run_{uuid.uuid4().hex[:12]}",
            agent_id=agent_id,
            workspace_id=workspace_id,
            input_hash=input_hash,
            outcome_required=outcome_required,
        )
        self._runs[run.run_id] = run
        return run

    def get(self, run_id: str) -> AgentRun:
        try:
            return self._runs[run_id]
        except KeyError as exc:
            raise KeyError(f"unknown run: {run_id}") from exc

    def all(self) -> list[AgentRun]:
        return list(self._runs.values())

    def runs_for(self, agent_id: str) -> list[AgentRun]:
        return [r for r in self._runs.values() if r.agent_id == agent_id]

    def stuck_without_outcome(self) -> list[AgentRun]:
        return [
            r
            for r in self._runs.values()
            if r.status is AgentRunStatus.COMPLETED
            and r.outcome_required
            and r.outcome_id is None
        ]
