"""Per-tool risk metrics — anomalies, blocks, denials."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ToolRiskMetric:
    tool_id: str
    blocks: int
    anomalies: int
    last_seen_at: str | None


@dataclass
class ToolRiskMonitor:
    _blocks: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    _anomalies: dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def record_block(self, tool_id: str) -> None:
        self._blocks[tool_id] += 1

    def record_anomaly(self, tool_id: str) -> None:
        self._anomalies[tool_id] += 1

    def snapshot(self) -> list[ToolRiskMetric]:
        all_tools = set(self._blocks.keys()) | set(self._anomalies.keys())
        return [
            ToolRiskMetric(
                tool_id=t,
                blocks=self._blocks.get(t, 0),
                anomalies=self._anomalies.get(t, 0),
                last_seen_at=None,
            )
            for t in all_tools
        ]
