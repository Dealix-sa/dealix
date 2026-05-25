"""
Attribution Graph — يربط الدخل المُتحقق بالحملات/الرسائل/الشركاء/الأصول/الوكلاء.
يفصل بين مصدر التأثير وقيمة التأثير (المهم: لا تعدّ نفس الـ revenue مرتين
عبر قنوات).
"""

from __future__ import annotations

import threading
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum


class AttributionDimension(StrEnum):
    CAMPAIGN = "campaign"
    CHANNEL = "channel"
    MESSAGE = "message"
    PARTNER = "partner"
    ASSET = "asset"
    AGENT = "agent"
    ICP = "icp"
    EXPERIMENT = "experiment"


@dataclass
class AttributionLink:
    link_id: str
    revenue_id: str
    dimension: AttributionDimension
    dimension_value: str
    weight: float = 1.0  # 0..1 — multi-touch
    recorded_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class AttributionGraph:
    def __init__(self) -> None:
        self._links: list[AttributionLink] = []
        self._by_revenue: dict[str, list[AttributionLink]] = defaultdict(list)
        self._lock = threading.Lock()

    def attribute(self, link: AttributionLink) -> AttributionLink:
        if not 0 <= link.weight <= 1:
            raise ValueError("attribution weight must be within [0, 1]")
        with self._lock:
            existing = self._by_revenue[link.revenue_id]
            if sum(l.weight for l in existing) + link.weight > 1.0 + 1e-6:
                raise ValueError(
                    f"attribution weights for revenue `{link.revenue_id}` exceed 1.0"
                )
            self._links.append(link)
            existing.append(link)
            return link

    def attributed_to(
        self, dimension: AttributionDimension
    ) -> dict[str, float]:
        with self._lock:
            stats: dict[str, float] = defaultdict(float)
            for link in self._links:
                if link.dimension == dimension:
                    stats[link.dimension_value] += link.weight
            return dict(stats)


__all__ = ["AttributionDimension", "AttributionGraph", "AttributionLink"]
