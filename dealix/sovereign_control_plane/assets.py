"""
Asset library — §100.

Captures the reusable artefacts Dealix creates (templates, proposal
shells, playbooks, prompts) and tracks the reuse + revenue impact that
makes them commercialisable.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any


@dataclass
class Asset:
    asset_id: str
    kind: str
    title: str
    payload: dict[str, Any]
    created_by: str
    tags: list[str] = field(default_factory=list)
    reuse_count: int = 0
    revenue_influenced_sar: float = 0.0
    conversion_impact: float = 0.0
    quality_score: float = 0.0
    trust_score: float = 0.0
    commercializable: bool = False
    created_at: str = ""
    last_reused_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "kind": self.kind,
            "title": self.title,
            "payload": dict(self.payload),
            "created_by": self.created_by,
            "tags": list(self.tags),
            "reuse_count": self.reuse_count,
            "revenue_influenced_sar": self.revenue_influenced_sar,
            "conversion_impact": self.conversion_impact,
            "quality_score": self.quality_score,
            "trust_score": self.trust_score,
            "commercializable": self.commercializable,
            "created_at": self.created_at,
            "last_reused_at": self.last_reused_at,
        }


class AssetLibrary:
    def __init__(self) -> None:
        self._items: dict[str, Asset] = {}
        self._lock = threading.Lock()

    def register(
        self,
        kind: str,
        title: str,
        payload: dict[str, Any],
        created_by: str,
        tags: list[str] | None = None,
    ) -> Asset:
        with self._lock:
            asset = Asset(
                asset_id=f"ast_{uuid.uuid4().hex[:12]}",
                kind=kind, title=title, payload=dict(payload),
                created_by=created_by, tags=list(tags or []),
                created_at=datetime.now(UTC).isoformat(),
            )
            self._items[asset.asset_id] = asset
            return asset

    def get(self, asset_id: str) -> Asset | None:
        return self._items.get(asset_id)

    def list(self) -> list[Asset]:
        return list(self._items.values())

    def mark_reused(self, asset_id: str, revenue_attributed: float = 0.0) -> Asset:
        with self._lock:
            asset = self._items.get(asset_id)
            if asset is None:
                raise KeyError(asset_id)
            asset.reuse_count += 1
            asset.revenue_influenced_sar = round(
                asset.revenue_influenced_sar + revenue_attributed, 2
            )
            asset.last_reused_at = datetime.now(UTC).isoformat()
            if asset.reuse_count >= 3 and asset.revenue_influenced_sar > 0:
                asset.commercializable = True
            return asset

    def reevaluate(self) -> list[Asset]:
        cutoff = datetime.now(UTC) - timedelta(days=30)
        stale: list[Asset] = []
        for a in self._items.values():
            if a.reuse_count == 0:
                try:
                    created = datetime.fromisoformat(a.created_at)
                except ValueError:
                    continue
                if created < cutoff:
                    stale.append(a)
        return stale

    def commercializable_set(self) -> list[Asset]:
        return [a for a in self._items.values() if a.commercializable]
