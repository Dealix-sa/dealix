"""Lightweight metric registry."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Metric:
    name: str
    value: float = 0.0
    samples: list[float] = field(default_factory=list)

    def inc(self, amount: float = 1.0) -> None:
        self.value += amount
        self.samples.append(self.value)


METRICS_REGISTRY: dict[str, Metric] = {
    name: Metric(name)
    for name in (
        "agent_runs_total",
        "tool_calls_total",
        "trust_blocks_total",
        "approval_pending_total",
        "verified_revenue_sar",
        "campaign_attributed_revenue_sar",
        "outcomes_logged_total",
        "assets_created_total",
        "incidents_total",
    )
}


def observe(name: str, amount: float = 1.0) -> Metric:
    metric = METRICS_REGISTRY.setdefault(name, Metric(name))
    metric.inc(amount)
    return metric
