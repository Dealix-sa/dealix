"""Governed dispatch — the agent + gate decision for one stage action.

Combines two checks before any stage runs:
  1. Agent identity (#9): the stage worker and the conductor are
     registered, active, and within their autonomy bounds.
  2. The auto-exec gate: only A0 / R0-R1 / not-S3 / not-never-auto
     actions may auto-execute; everything else needs approval.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.agent_os import AgentStatus, AutonomyLevel, get_agent
from auto_client_acquisition.full_ops_os.agents import CONDUCTOR_ID
from auto_client_acquisition.full_ops_os.dispatcher import (
    agent_for_stage,
    director_for_stage,
)
from auto_client_acquisition.full_ops_os.gate import GateDecision, evaluate_gate
from auto_client_acquisition.full_ops_os.stages import Stage, stage_spec

# Dispatch modes.
AUTO_EXECUTE = "auto_execute"
APPROVAL_REQUIRED = "approval_required"
BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class DispatchDecision:
    """The governed decision for running one stage."""

    stage: Stage
    action_type: str
    worker_agent: str
    director_agent: str
    conductor_agent: str
    gate: GateDecision
    mode: str  # AUTO_EXECUTE | APPROVAL_REQUIRED | BLOCKED
    reason: str

    @property
    def is_blocked(self) -> bool:
        return self.mode == BLOCKED

    @property
    def auto_executes(self) -> bool:
        return self.mode == AUTO_EXECUTE

    def to_dict(self) -> dict[str, object]:
        return {
            "stage": self.stage.name,
            "action_type": self.action_type,
            "worker_agent": self.worker_agent,
            "director_agent": self.director_agent,
            "conductor_agent": self.conductor_agent,
            "gate": self.gate.to_dict(),
            "mode": self.mode,
            "reason": self.reason,
        }


def _agent_blocked_reason(agent_id: str, *, role: str) -> str | None:
    """Return a block reason if the agent is missing or killed, else None."""
    card = get_agent(agent_id)
    if card is None:
        return f"{role}_not_registered:{agent_id}"
    if card.status == AgentStatus.KILLED.value:
        return f"{role}_killed:{agent_id}"
    return None


def governed_dispatch(stage: Stage) -> DispatchDecision:
    """Decide how a stage runs: auto-execute, queue for approval, or block."""
    spec = stage_spec(stage)
    worker = agent_for_stage(stage)
    director = director_for_stage(stage)
    gate = evaluate_gate(spec.action_type)

    def decide(mode: str, reason: str) -> DispatchDecision:
        return DispatchDecision(
            stage=stage,
            action_type=spec.action_type,
            worker_agent=worker,
            director_agent=director,
            conductor_agent=CONDUCTOR_ID,
            gate=gate,
            mode=mode,
            reason=reason,
        )

    # 1. Identity gate — worker, director, conductor must all be sound.
    for agent_id, role in (
        (worker, "worker"),
        (director, "director"),
        (CONDUCTOR_ID, "conductor"),
    ):
        blocked = _agent_blocked_reason(agent_id, role=role)
        if blocked is not None:
            return decide(BLOCKED, blocked)

    # 2. Only an L4 conductor may auto-execute an internal action.
    conductor = get_agent(CONDUCTOR_ID)
    if gate.auto_exec_allowed:
        if conductor is None or conductor.autonomy_level < int(
            AutonomyLevel.L4_AUTO_WITH_AUDIT
        ):
            return decide(APPROVAL_REQUIRED, "conductor_below_L4")
        return decide(AUTO_EXECUTE, gate.reason)

    return decide(APPROVAL_REQUIRED, gate.reason)


__all__ = [
    "AUTO_EXECUTE",
    "APPROVAL_REQUIRED",
    "BLOCKED",
    "DispatchDecision",
    "governed_dispatch",
]
