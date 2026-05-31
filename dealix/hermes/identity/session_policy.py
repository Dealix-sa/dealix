"""
Session policy — TTL + idle timeout + max-operations cap per session.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field


@dataclass
class SessionPolicy:
    ttl_seconds: int = 3600
    idle_timeout_seconds: int = 600
    max_operations: int = 200

    def __post_init__(self) -> None:
        if self.ttl_seconds <= 0 or self.idle_timeout_seconds <= 0:
            raise ValueError("ttl_seconds and idle_timeout_seconds must be positive")
        if self.max_operations <= 0:
            raise ValueError("max_operations must be positive")


@dataclass
class SessionState:
    session_id: str
    agent_id: str
    policy: SessionPolicy
    started_at: float = field(default_factory=time.time)
    last_used_at: float = field(default_factory=time.time)
    operations_used: int = 0
    revoked: bool = False


def start_session(agent_id: str, policy: SessionPolicy) -> SessionState:
    return SessionState(
        session_id=str(uuid.uuid4()),
        agent_id=agent_id,
        policy=policy,
    )


def validate_session(session: SessionState, *, now: float | None = None) -> tuple[bool, str]:
    """Mutates session.operations_used / last_used_at if the session is valid."""
    if session.revoked:
        return False, "session_revoked"
    now = now or time.time()
    if now - session.started_at > session.policy.ttl_seconds:
        return False, "session_ttl_exceeded"
    if now - session.last_used_at > session.policy.idle_timeout_seconds:
        return False, "session_idle_timeout"
    if session.operations_used + 1 > session.policy.max_operations:
        return False, "session_max_operations"
    session.operations_used += 1
    session.last_used_at = now
    return True, "ok"
