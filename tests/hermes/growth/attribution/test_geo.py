"""GEO attribution credits revenue surfaced via AI engines."""

from __future__ import annotations

from dealix.hermes.growth.attribution import _base, geo


def test_geo_attribution() -> None:
    _base.reset()
    geo.attribute("perplexity", 12_500, evidence_pack_id="ep_1")
    assert geo.total("perplexity") == 12_500
