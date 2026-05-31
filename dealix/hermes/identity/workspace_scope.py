"""
Workspace scope enforcement.

An agent identity scoped to workspace `dealix_internal` cannot operate on
a record belonging to `customer_xyz` even if its capability_scope allows
the operation.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.identity.agent_identity import AgentIdentity


@dataclass
class WorkspaceViolation:
    agent_id: str
    requested_workspace: str
    reason: str


def enforce_workspace(
    identity: AgentIdentity, requested_workspace: str
) -> WorkspaceViolation | None:
    if requested_workspace not in identity.workspace_scope:
        return WorkspaceViolation(
            agent_id=identity.agent_id,
            requested_workspace=requested_workspace,
            reason=(
                f"agent workspace_scope={list(identity.workspace_scope)} does not "
                f"include '{requested_workspace}'"
            ),
        )
    return None
