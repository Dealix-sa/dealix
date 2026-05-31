"""AssetCommercialization — find candidates ready to become products."""

from __future__ import annotations

from dealix.hermes.assets.asset_store import ASSET_STORE, Asset


def commercialization_candidates(
    *, min_reuse: int = 3, min_revenue_sar: float = 10_000.0
) -> list[Asset]:
    return [
        a
        for a in ASSET_STORE.values()
        if a.reuse_count >= min_reuse and a.verified_revenue_influence_sar >= min_revenue_sar
    ]
