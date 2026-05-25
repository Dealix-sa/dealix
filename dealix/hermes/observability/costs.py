"""Cost tracking — per agent, per tool, per workspace."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict


class CostRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent_id: str
    tool_id: str | None = None
    workspace_id: str = "dealix_internal"
    amount_sar: float


@dataclass
class CostLedger:
    _records: list[CostRecord] = field(default_factory=list)

    def record(self, record: CostRecord) -> CostRecord:
        self._records.append(record)
        return record

    def total_for_agent(self, agent_id: str) -> float:
        return sum(r.amount_sar for r in self._records if r.agent_id == agent_id)

    def total_for_tool(self, tool_id: str) -> float:
        return sum(r.amount_sar for r in self._records if r.tool_id == tool_id)
