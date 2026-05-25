"""Market signals are validated and stored, unknown kinds raise."""

from __future__ import annotations

import pytest

from dealix.hermes.growth import market_signals


def test_ingest_known_and_reject_unknown() -> None:
    market_signals.reset()
    sig = market_signals.ingest("deal_won", "acc_1", value_sar=50_000)
    assert sig.kind == "deal_won"
    assert market_signals.list_signals("deal_won")[0].account_id == "acc_1"
    with pytest.raises(ValueError):
        market_signals.ingest("invented", "acc_2")
