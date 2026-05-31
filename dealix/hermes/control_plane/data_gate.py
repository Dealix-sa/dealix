"""
DataGate — enforces tenant isolation and data sensitivity caps before
the request reaches the execution layer.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.classifications import SensitivityClass
from dealix.hermes.control_plane.actor_identity import ActorIdentity
from dealix.hermes.control_plane.request_context import RequestContext
from dealix.hermes.data.data_boundary import DataBoundary, get_boundary
from dealix.hermes.identity.agent_identity import AgentIdentity


_SENSITIVITY_ORDER = [
    SensitivityClass.S0,
    SensitivityClass.S1,
    SensitivityClass.S2,
    SensitivityClass.S3,
]


def _exceeds(actual: SensitivityClass, cap: SensitivityClass) -> bool:
    return _SENSITIVITY_ORDER.index(actual) > _SENSITIVITY_ORDER.index(cap)


@dataclass(frozen=True)
class DataDecision:
    allowed: bool
    boundary: DataBoundary | None
    reason: str


def evaluate(
    context: RequestContext,
    actor: ActorIdentity,
    agent: AgentIdentity | None,
) -> DataDecision:
    boundary = get_boundary(context.workspace_id)

    if not actor.can_access_workspace(context.workspace_id):
        return DataDecision(
            allowed=False,
            boundary=boundary,
            reason=f"Actor {actor.actor_id!r} not scoped to workspace {context.workspace_id!r}.",
        )

    if agent is not None:
        if context.workspace_id not in agent.workspace_scope and "*" not in agent.workspace_scope:
            return DataDecision(
                allowed=False,
                boundary=boundary,
                reason=f"Agent {agent.agent_id!r} not scoped to workspace {context.workspace_id!r}.",
            )
        if _exceeds(context.sensitivity, agent.max_data_sensitivity):
            return DataDecision(
                allowed=False,
                boundary=boundary,
                reason=(
                    f"Request sensitivity {context.sensitivity.value} exceeds agent cap "
                    f"{agent.max_data_sensitivity.value}."
                ),
            )

    if boundary is not None and context.external_action and not boundary.external_output_requires_approval:
        # Boundary explicitly does not permit external output at all.
        pass

    if boundary is not None and context.capability in boundary.forbidden_exports:
        return DataDecision(
            allowed=False,
            boundary=boundary,
            reason=f"Capability {context.capability!r} is in the workspace forbidden-export list.",
        )

    return DataDecision(allowed=True, boundary=boundary, reason="Within data boundary.")
