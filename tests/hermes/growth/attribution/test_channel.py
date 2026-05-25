"""Channel attribution requires evidence_pack_id and aggregates totals."""

from __future__ import annotations

import pytest

from dealix.hermes.growth.attribution import _base, channel


def test_channel_attribution_aggregates_with_evidence() -> None:
    _base.reset()
    channel.attribute("inbound", 10_000, evidence_pack_id="ep_1")
    channel.attribute("inbound", 5_000, evidence_pack_id="ep_2")
    assert channel.total("inbound") == 15_000
    with pytest.raises(ValueError):
        channel.attribute("inbound", 1.0, evidence_pack_id="")
