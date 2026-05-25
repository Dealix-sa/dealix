"""
SessionPolicy — the per-session caps that wrap an Agent's identity.

An identity says "this agent *may* hold these capabilities". A session
policy clamps that down further for a single run: shorter expiry, fewer
tools, a single workspace, optional one-shot scope.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from dealix.hermes.identity.agent_identity import AgentIdentity


@dataclass(frozen=True)
class SessionPolicy:
    session_id: str
    agent_id: str
    workspace_id: str
    capabilities: tuple[str, ...]
    allowed_tools: tuple[str, ...]
    expires_at: datetime
    one_shot: bool = False
    metadata: dict[str, str] = field(default_factory=dict)

    @staticmethod
    def issue(
        *,
        agent: AgentIdentity,
        workspace_id: str,
        capabilities: tuple[str, ...] | None = None,
        allowed_tools: tuple[str, ...] | None = None,
        ttl_minutes: int = 30,
        one_shot: bool = False,
    ) -> SessionPolicy:
        caps = tuple(c for c in (capabilities or agent.capabilities) if c in agent.capabilities)
        tools = tuple(t for t in (allowed_tools or agent.allowed_tools) if t in agent.allowed_tools)
        return SessionPolicy(
            session_id=f"sess_{uuid.uuid4().hex[:10]}",
            agent_id=agent.agent_id,
            workspace_id=workspace_id,
            capabilities=caps,
            allowed_tools=tools,
            expires_at=datetime.now(UTC) + timedelta(minutes=ttl_minutes),
            one_shot=one_shot,
        )

    @property
    def expired(self) -> bool:
        return datetime.now(UTC) > self.expires_at
