"""Verify offer routing logic produces correct recommendations."""
from __future__ import annotations

from os_runtime.offer_router import route

REQUIRED_OFFER_KEYS = {"id", "name", "price_range_sar", "rationale"}


def test_high_score_returns_at_least_one_offer() -> None:
    offers = route({"score": 80})
    assert len(offers) >= 1


def test_high_score_includes_agentic_pilot() -> None:
    offers = route({"score": 80})
    ids = {o["id"] for o in offers}
    assert "AWP" in ids, "High-score company should be recommended the agentic_workflow_pilot (AWP)"


def test_low_score_returns_audit_only() -> None:
    offers = route({"score": 20})
    assert len(offers) >= 1
    ids = {o["id"] for o in offers}
    assert "WFA" in ids, "Low-score company should be recommended ai_workflow_audit (WFA)"


def test_low_score_does_not_include_pilot() -> None:
    offers = route({"score": 20})
    ids = {o["id"] for o in offers}
    assert "AWP" not in ids, "Low-score company should not be recommended the pilot"


def test_mid_score_returns_audit() -> None:
    offers = route({"score": 55})
    assert len(offers) >= 1
    ids = {o["id"] for o in offers}
    assert "WFA" in ids


def test_all_returned_offers_have_required_keys() -> None:
    for score in [20, 55, 80]:
        offers = route({"score": score})
        for offer in offers:
            missing = REQUIRED_OFFER_KEYS - set(offer.keys())
            assert not missing, f"Offer missing keys {missing} for score={score}"


def test_returns_list_type() -> None:
    result = route({"score": 75})
    assert isinstance(result, list)


def test_score_zero_returns_audit() -> None:
    offers = route({"score": 0})
    assert len(offers) >= 1
    ids = {o["id"] for o in offers}
    assert "WFA" in ids


def test_score_exactly_70_threshold() -> None:
    offers = route({"score": 70})
    ids = {o["id"] for o in offers}
    assert "AWP" in ids, "Score of 70 should qualify for the pilot"


def test_price_range_sar_is_string() -> None:
    offers = route({"score": 80})
    for offer in offers:
        assert isinstance(offer["price_range_sar"], str)
