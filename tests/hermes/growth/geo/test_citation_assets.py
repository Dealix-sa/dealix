"""Citation assets require evidence_pack_id and a valid kind."""

from __future__ import annotations

import pytest

from dealix.hermes.growth.geo.citation_assets import list_assets, register, reset


def test_register_requires_evidence_pack() -> None:
    reset()
    register("benchmark", "Sales AI Benchmark 2026", "/research/2026", evidence_pack_id="ep_1")
    assert list_assets()
    with pytest.raises(ValueError):
        register("benchmark", "no-evidence", "/none", evidence_pack_id="")
    with pytest.raises(ValueError):
        register("invented", "x", "/x", evidence_pack_id="ep_2")
