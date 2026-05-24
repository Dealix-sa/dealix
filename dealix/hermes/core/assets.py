"""AssetRegistry — reusable artifacts harvested from outcomes.

Assets are the data moat (section 130). Each one carries its lineage
back to an outcome and tracks reuse + revenue attribution.
"""

from __future__ import annotations

from collections import Counter

from dealix.hermes.core.schemas import Asset, AssetStatus


class AssetRegistry:
    def __init__(self) -> None:
        self._by_id: dict[str, Asset] = {}

    def add(self, asset: Asset) -> Asset:
        if asset.id in self._by_id:
            raise ValueError(f"Duplicate asset id: {asset.id}")
        self._by_id[asset.id] = asset
        return asset

    def mark_reusable(self, asset_id: str) -> Asset:
        a = self._by_id[asset_id]
        a.status = AssetStatus.REUSABLE
        a.touch()
        return a

    def commercialize(self, asset_id: str) -> Asset:
        a = self._by_id[asset_id]
        if a.status not in {AssetStatus.REUSABLE, AssetStatus.COMMERCIALIZED}:
            raise ValueError("Only REUSABLE assets can be commercialized.")
        a.status = AssetStatus.COMMERCIALIZED
        a.touch()
        return a

    def retire(self, asset_id: str, *, reason: str) -> Asset:
        a = self._by_id[asset_id]
        a.status = AssetStatus.RETIRED
        a.payload["retire_reason"] = reason
        a.touch()
        return a

    def record_reuse(self, asset_id: str, *, revenue_sar: float = 0.0) -> Asset:
        a = self._by_id[asset_id]
        a.reuse_count += 1
        a.revenue_attributed_sar += revenue_sar
        a.touch()
        return a

    def get(self, asset_id: str) -> Asset:
        return self._by_id[asset_id]

    def all(self) -> list[Asset]:
        return list(self._by_id.values())

    def by_kind(self) -> Counter[str]:
        return Counter(a.kind for a in self._by_id.values())

    def unreused(self) -> list[Asset]:
        return [a for a in self._by_id.values() if a.reuse_count == 0 and a.status != AssetStatus.RETIRED]


__all__ = ["AssetRegistry"]
