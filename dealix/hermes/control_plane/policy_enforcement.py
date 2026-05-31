"""
PolicyEnforcement — composes the platform-level policy checks (sovereignty,
trust, data, tool, kill switch, runtime mode) into one verdict.

The verdict is what ``ControlPlaneRuntime`` consults before deciding
whether to execute, queue for approval, or refuse.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.control_plane import data_gate as data_gate
from dealix.hermes.control_plane import kill_switch as kill_switch
from dealix.hermes.control_plane import runtime_modes as runtime_modes
from dealix.hermes.control_plane import sovereignty_gate as sovereignty_gate
from dealix.hermes.control_plane import tool_gate as tool_gate
from dealix.hermes.control_plane import trust_gate as trust_gate
from dealix.hermes.control_plane.actor_identity import ActorIdentity
from dealix.hermes.control_plane.request_context import RequestContext
from dealix.hermes.identity.agent_identity import AgentIdentity


@dataclass
class PolicyVerdict:
    allowed: bool
    requires_approval: bool
    sovereignty: sovereignty_gate.SovereigntyDecision
    trust: trust_gate.TrustDecision
    data: data_gate.DataDecision
    tool: tool_gate.ToolDecision
    kill: kill_switch.KillEntry | None
    runtime_mode: runtime_modes.RuntimeMode
    blockers: list[str] = field(default_factory=list)

    def reasons(self) -> tuple[str, ...]:
        return tuple(self.blockers)


def evaluate(
    context: RequestContext,
    actor: ActorIdentity,
    agent: AgentIdentity | None,
) -> PolicyVerdict:
    blockers: list[str] = []

    kill_entry = kill_switch.check_request(
        agent_id=agent.agent_id if agent else None,
        tool_id=context.tool_id,
        capability=context.capability,
    )
    if kill_entry is not None:
        blockers.append(f"kill_switch: {kill_entry.reason}")

    sovereignty = sovereignty_gate.evaluate(context, actor)
    if sovereignty.blocked:
        blockers.append(f"sovereignty_blocked: {sovereignty.reason}")

    trust = trust_gate.evaluate(context)
    if trust.blocked:
        for f in trust.findings:
            blockers.append(f"trust_{f.code}: {f.message}")

    data = data_gate.evaluate(context, actor, agent)
    if not data.allowed:
        blockers.append(f"data_gate: {data.reason}")

    tool = tool_gate.evaluate(context, agent)
    if not tool.allowed:
        blockers.append(f"tool_gate: {tool.reason}")

    mode = runtime_modes.STATE.current
    if mode.is_lockdown and context.external_action:
        blockers.append("runtime_mode: SOVEREIGN_LOCKDOWN — no external actions.")
    if mode == runtime_modes.RuntimeMode.DRAFT_ONLY and context.external_action:
        blockers.append("runtime_mode: DRAFT_ONLY — external actions disabled.")

    return PolicyVerdict(
        allowed=not blockers,
        requires_approval=sovereignty.requires_sami,
        sovereignty=sovereignty,
        trust=trust,
        data=data,
        tool=tool,
        kill=kill_entry,
        runtime_mode=mode,
        blockers=blockers,
    )
