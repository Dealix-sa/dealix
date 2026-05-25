from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AgentAttribution:
    agent_id: str
    confidence: float

    def __post_init__(self) -> None:
        if not self.agent_id:
            raise ValueError("agent_id required")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be in [0,1]")
