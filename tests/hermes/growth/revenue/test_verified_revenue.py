"""Verified revenue ledger rejects records lacking an evidence_pack_id."""

from __future__ import annotations

import pytest

from dealix.hermes.growth.revenue.verified_revenue import list_records, record, total


def test_record_requires_evidence_pack() -> None:
    rec = record("acc_1", 50_000, evidence_pack_id="ep_1", notes="signed contract")
    assert rec.amount_sar == 50_000
    assert total("acc_1") == 50_000
    assert list_records("acc_1")[-1].evidence_pack_id == "ep_1"
    with pytest.raises(ValueError):
        record("acc_2", 12_000, evidence_pack_id="")
