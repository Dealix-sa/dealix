"""Metric ingestion + readback."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field


class MetricEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metric: str
    value: float
    tags: dict[str, str] = Field(default_factory=dict)


@dataclass
class MetricRegistry:
    _events: list[MetricEvent] = field(default_factory=list)

    def record(self, event: MetricEvent) -> MetricEvent:
        self._events.append(event)
        return event

    def aggregate(self, metric: str) -> float:
        return sum(e.value for e in self._events if e.metric == metric)

    def by_tag(self, metric: str, tag_key: str) -> dict[str, float]:
        bucket: dict[str, float] = defaultdict(float)
        for e in self._events:
            if e.metric != metric:
                continue
            bucket[e.tags.get(tag_key, "_")] += e.value
        return dict(bucket)
