"""
Agent registry — single source of truth for every agent in Dealix.

The registry is in-memory by default so it can be embedded in pure unit
tests. Production deployments are expected to back it with the existing
Postgres event store (see `auto_client_acquisition.revenue_memory`).
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from dataclasses import dataclass, field
from enum import StrEnum


class AgentLifecycleStage(StrEnum):
    """Ordered lifecycle stages — order matters for promotion checks."""

    PROPOSED = "proposed"
    REGISTERED = "registered"
    RISK_SCORED = "risk_scored"
    TOOL_SCOPED = "tool_scoped"
    CONTEXT_SCOPED = "context_scoped"
    TESTED = "tested"
    DRAFT_ONLY = "draft_only"
    APPROVAL_GATED = "approval_gated"
    LIMITED_AUTONOMY = "limited_autonomy"
    MONITORED = "monitored"
    RESTRICTED = "restricted"
    RETIRED = "retired"


_FORWARD_ORDER: tuple[AgentLifecycleStage, ...] = (
    AgentLifecycleStage.PROPOSED,
    AgentLifecycleStage.REGISTERED,
    AgentLifecycleStage.RISK_SCORED,
    AgentLifecycleStage.TOOL_SCOPED,
    AgentLifecycleStage.CONTEXT_SCOPED,
    AgentLifecycleStage.TESTED,
    AgentLifecycleStage.DRAFT_ONLY,
    AgentLifecycleStage.APPROVAL_GATED,
    AgentLifecycleStage.LIMITED_AUTONOMY,
    AgentLifecycleStage.MONITORED,
)


def is_forward_promotion(
    current: AgentLifecycleStage, target: AgentLifecycleStage
) -> bool:
    """`MONITORED → RESTRICTED` and `* → RETIRED` are always allowed."""
    if target == AgentLifecycleStage.RETIRED:
        return True
    if target == AgentLifecycleStage.RESTRICTED:
        return current in _FORWARD_ORDER
    if current not in _FORWARD_ORDER or target not in _FORWARD_ORDER:
        return False
    return _FORWARD_ORDER.index(target) == _FORWARD_ORDER.index(current) + 1


@dataclass
class AgentRecord:
    """One agent entry. Mutated only via `AgentRegistry`."""

    agent_id: str
    owner: str
    origin: str = "dealix_internal"
    stage: AgentLifecycleStage = AgentLifecycleStage.PROPOSED
    runs: int = 0
    successful_runs: int = 0
    critical_incidents: int = 0
    trust_pass_count: int = 0
    output_corrections: int = 0
    outcomes_logged: int = 0
    tool_scope: tuple[str, ...] = ()
    workspace_scope: tuple[str, ...] = ()
    forbidden_capabilities: tuple[str, ...] = ()
    risk_score: float = 0.0
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    history: list[tuple[float, AgentLifecycleStage, str]] = field(default_factory=list)

    @property
    def trust_pass_rate(self) -> float:
        if self.runs == 0:
            return 0.0
        return self.trust_pass_count / self.runs

    @property
    def success_rate(self) -> float:
        if self.runs == 0:
            return 0.0
        return self.successful_runs / self.runs

    @property
    def correction_rate(self) -> float:
        if self.runs == 0:
            return 0.0
        return self.output_corrections / self.runs

    def snapshot(self) -> dict[str, object]:
        return {
            "agent_id": self.agent_id,
            "owner": self.owner,
            "origin": self.origin,
            "stage": self.stage.value,
            "runs": self.runs,
            "successful_runs": self.successful_runs,
            "critical_incidents": self.critical_incidents,
            "trust_pass_rate": round(self.trust_pass_rate, 4),
            "success_rate": round(self.success_rate, 4),
            "correction_rate": round(self.correction_rate, 4),
            "outcomes_logged": self.outcomes_logged,
            "tool_scope": list(self.tool_scope),
            "workspace_scope": list(self.workspace_scope),
            "forbidden_capabilities": list(self.forbidden_capabilities),
            "risk_score": self.risk_score,
            "history": [(ts, stage.value, note) for ts, stage, note in self.history],
        }


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, AgentRecord] = {}

    def register(self, record: AgentRecord) -> AgentRecord:
        if record.agent_id in self._agents:
            raise ValueError(f"agent_id '{record.agent_id}' already registered")
        record.stage = AgentLifecycleStage.REGISTERED
        record.history.append(
            (time.time(), AgentLifecycleStage.REGISTERED, "initial registration")
        )
        self._agents[record.agent_id] = record
        return record

    def get(self, agent_id: str) -> AgentRecord:
        if agent_id not in self._agents:
            raise KeyError(f"unknown agent_id '{agent_id}'")
        return self._agents[agent_id]

    def __contains__(self, agent_id: str) -> bool:
        return agent_id in self._agents

    def __iter__(self) -> Iterator[AgentRecord]:
        return iter(self._agents.values())

    def __len__(self) -> int:
        return len(self._agents)

    def transition(
        self,
        agent_id: str,
        target: AgentLifecycleStage,
        note: str,
    ) -> AgentRecord:
        record = self.get(agent_id)
        record.stage = target
        record.updated_at = time.time()
        record.history.append((record.updated_at, target, note))
        return record

    def record_run(
        self,
        agent_id: str,
        *,
        successful: bool,
        trust_passed: bool,
        critical_incident: bool = False,
        output_corrected: bool = False,
        outcome_logged: bool = False,
    ) -> AgentRecord:
        record = self.get(agent_id)
        record.runs += 1
        if successful:
            record.successful_runs += 1
        if trust_passed:
            record.trust_pass_count += 1
        if critical_incident:
            record.critical_incidents += 1
        if output_corrected:
            record.output_corrections += 1
        if outcome_logged:
            record.outcomes_logged += 1
        record.updated_at = time.time()
        return record
