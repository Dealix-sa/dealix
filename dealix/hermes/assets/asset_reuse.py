"""AssetReuse — record a reuse event and optionally tag revenue influence."""

from __future__ import annotations

from dealix.hermes.assets.asset_store import ASSET_STORE, Asset


def record_reuse(asset_id: str, *, verified_revenue_influence_sar: float = 0.0) -> Asset:
    asset = ASSET_STORE.get(asset_id)
    if asset is None:
        raise KeyError(f"unknown asset {asset_id!r}")
    asset.reuse_count += 1
    asset.verified_revenue_influence_sar += verified_revenue_influence_sar
    return asset
