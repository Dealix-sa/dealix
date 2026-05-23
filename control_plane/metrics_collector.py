"""
Metrics collector.

Hash-map style sink for counters and gauges. Adapters can ship these to
PostHog / Sentry / a CSV depending on the deployment. Keeping the core
type tiny makes it easy to test the rest of the control plane.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Mapping


class MetricsCollector:
    def __init__(self) -> None:
        self._counters: dict[str, int] = defaultdict(int)
        self._gauges: dict[str, float] = {}

    def incr(self, name: str, by: int = 1) -> None:
        self._counters[name] += by

    def gauge(self, name: str, value: float) -> None:
        self._gauges[name] = float(value)

    def snapshot(self) -> dict[str, Mapping[str, float]]:
        return {
            "counters": dict(self._counters),
            "gauges": dict(self._gauges),
        }
