from __future__ import annotations

import pytest

from dealix.hermes.sovereignty import FounderTimeLedger


def test_founder_ledger_tracks_unproductive_hours():
    ledger = FounderTimeLedger()
    ledger.log(
        "delivery", 4, offer_id="ai_trust_kit", produces_asset=True
    )
    ledger.log(
        "customer email", 2, offer_id="ai_trust_kit",
    )
    ledger.log(
        "scoping call", 1, produces_retainer=True
    )
    assert ledger.total_hours() == 7.0
    assert ledger.unproductive_hours() == 2.0
    by_offer = ledger.hours_by_offer()
    assert by_offer["ai_trust_kit"] == 6.0
    assert by_offer["unallocated"] == 1.0


def test_log_rejects_zero_hours():
    ledger = FounderTimeLedger()
    with pytest.raises(ValueError):
        ledger.log("noop", 0)
