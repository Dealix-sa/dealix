"""Tests for the JSONL-backed NPS ledger (B4 — Delivery / Ops)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.growth_v10 import nps_ledger


@pytest.fixture(autouse=True)
def _isolated_ledger(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_NPS_LEDGER_PATH", str(tmp_path / "nps.jsonl"))
    nps_ledger.clear_for_test()
    yield
    nps_ledger.clear_for_test()


def test_record_and_list_response():
    r = nps_ledger.record_response(
        customer_handle="acme_co",
        nps_round="sprint_d14",
        score=9,
    )
    assert r.band == "promoter"
    assert r.response_id.startswith("nps_")
    rows = nps_ledger.list_responses(customer_handle="acme_co")
    assert len(rows) == 1
    assert rows[0].score == 9


def test_verbatim_is_pii_redacted():
    r = nps_ledger.record_response(
        customer_handle="acme_co",
        nps_round="partner_m1",
        score=8,
        verbatim="Great work, reach me at founder@acme.com or 0501234567",
    )
    assert "founder@acme.com" not in r.verbatim_redacted
    assert "0501234567" not in r.verbatim_redacted


def test_invalid_round_and_score_rejected():
    with pytest.raises(ValueError):
        nps_ledger.record_response(
            customer_handle="acme_co", nps_round="bad_round", score=5,
        )
    with pytest.raises(ValueError):
        nps_ledger.record_response(
            customer_handle="acme_co", nps_round="sprint_d14", score=11,
        )
    with pytest.raises(ValueError):
        nps_ledger.record_response(
            customer_handle="", nps_round="sprint_d14", score=5,
        )


def test_aggregate_nps_score():
    for score in (10, 9, 8, 3):  # 2 promoters, 1 passive, 1 detractor
        nps_ledger.record_response(
            customer_handle="acme_co", nps_round="sprint_d14", score=score,
        )
    agg = nps_ledger.aggregate()
    assert agg["responses_count"] == 4
    assert agg["promoters"] == 2
    assert agg["detractors"] == 1
    # NPS = 50% promoters - 25% detractors = 25.0
    assert agg["nps_score"] == 25.0


def test_aggregate_empty_ledger():
    agg = nps_ledger.aggregate()
    assert agg["responses_count"] == 0
    assert agg["nps_score"] is None
