"""HermesAgent — the base every domain agent inherits from."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.data.context_packets import ContextPacket
from dealix.hermes.trust.agent_registry import AgentCard


class AgentInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    context: ContextPacket
    arguments: dict[str, Any] = Field(default_factory=dict)


class AgentExecution(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent_id: str
    output: dict[str, Any] = Field(default_factory=dict)
    requires_approval: bool = False
    tools_used: list[str] = Field(default_factory=list)
    evidence_pack_id: str | None = None
    notes: str = ""


@dataclass
class HermesAgent:
    """Subclass and override `run` per domain."""

    card: AgentCard

    @property
    def agent_id(self) -> str:
        return self.card.agent_id

    def run(self, request: AgentInput) -> AgentExecution:  # pragma: no cover - subclass override
        raise NotImplementedError(
            f"agent {self.card.agent_id} did not implement run()"
        )
