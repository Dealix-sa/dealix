"""Lightweight anomaly detection on MCP call streams."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AnomalyReport:
    server_id: str
    tool_name: str
    anomaly_type: str
    detail: str


@dataclass
class AnomalyDetector:
    call_counts: dict[tuple[str, str], int] = field(default_factory=lambda: defaultdict(int))
    call_threshold: int = 1000

    def observe(self, *, server_id: str, tool_name: str, payload: dict[str, Any]) -> AnomalyReport | None:
        key = (server_id, tool_name)
        self.call_counts[key] += 1
        if self.call_counts[key] > self.call_threshold:
            return AnomalyReport(
                server_id=server_id,
                tool_name=tool_name,
                anomaly_type="rate_spike",
                detail=f"{self.call_counts[key]} calls",
            )
        if "password" in str(payload).lower() or "private_key" in str(payload).lower():
            return AnomalyReport(
                server_id=server_id,
                tool_name=tool_name,
                anomaly_type="sensitive_payload",
                detail="payload contains credential-like content",
            )
        return None
