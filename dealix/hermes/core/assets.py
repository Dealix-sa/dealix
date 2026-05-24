"""Asset Layer — every outcome is reviewed for reusable, capital-grade assets."""

from __future__ import annotations

from threading import RLock

from dealix.hermes.core.schemas import Asset, AssetType, Outcome


class AssetStore:
    def __init__(self) -> None:
        self._items: dict[str, Asset] = {}
        self._lock = RLock()

    def register(
        self,
        outcome: Outcome,
        *,
        asset_type: AssetType | str,
        title: str,
        description: str = "",
        reusable: bool = True,
        commercializable: bool = False,
        asset_location: str = "",
    ) -> Asset:
        asset = Asset(
            outcome_id=outcome.id,
            asset_type=AssetType(asset_type),
            title=title,
            description=description,
            reusable=reusable,
            commercializable=commercializable,
            asset_location=asset_location,
        )
        with self._lock:
            self._items[asset.id] = asset
        return asset

    def get(self, asset_id: str) -> Asset | None:
        with self._lock:
            return self._items.get(asset_id)

    def list(
        self,
        *,
        asset_type: AssetType | str | None = None,
        commercializable_only: bool = False,
    ) -> list[Asset]:
        with self._lock:
            items = list(self._items.values())
        if asset_type:
            tval = AssetType(asset_type).value
            items = [a for a in items if a.asset_type == tval]
        if commercializable_only:
            items = [a for a in items if a.commercializable]
        return sorted(items, key=lambda a: a.created_at, reverse=True)

    def clear(self) -> None:
        with self._lock:
            self._items.clear()


_default_store: AssetStore | None = None


def get_asset_store() -> AssetStore:
    global _default_store
    if _default_store is None:
        _default_store = AssetStore()
    return _default_store
