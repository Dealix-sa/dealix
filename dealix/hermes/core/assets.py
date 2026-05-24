"""
Asset store.

Every outcome that produces a learning, a win, or a reusable artifact is
promoted to an Asset — Dealix's compounding moat.
"""

from __future__ import annotations

from uuid import uuid4

from dealix.hermes.core.schemas import HermesAsset


class AssetStore:
    def __init__(self) -> None:
        self._assets: dict[str, HermesAsset] = {}

    def add(self, asset: HermesAsset) -> str:
        aid = str(uuid4())
        self._assets[aid] = asset
        return aid

    def get(self, aid: str) -> HermesAsset | None:
        return self._assets.get(aid)

    def list_by_type(self, asset_type: str) -> list[tuple[str, HermesAsset]]:
        return [(aid, a) for aid, a in self._assets.items() if a.asset_type == asset_type]

    def count(self) -> int:
        return len(self._assets)


_default_store = AssetStore()


def default_store() -> AssetStore:
    return _default_store
