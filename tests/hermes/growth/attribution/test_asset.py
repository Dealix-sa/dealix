"""Asset attribution captures revenue tied to reusable content/proof assets."""

from __future__ import annotations

from dealix.hermes.growth.attribution import _base, asset


def test_asset_attribution() -> None:
    _base.reset()
    asset.attribute("asset_benchmark_2026", 25_000, evidence_pack_id="ep_1")
    assert asset.total("asset_benchmark_2026") == 25_000
