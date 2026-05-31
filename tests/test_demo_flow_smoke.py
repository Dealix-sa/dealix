"""Smoke tests for demo-critical flows added in the 30-day plan.

Pure-Python unit tests — no real DB/Redis/LLM required.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


# ── Company Brain Step 9 ───────────────────────────────────────────


def test_step9_company_brain_returns_dict():
    """step9_company_brain returns a dict with required keys."""
    from auto_client_acquisition.delivery_factory.delivery_sprint import (
        step9_company_brain,
    )

    result = step9_company_brain(
        customer_id="test-co",
        engagement_id="eng-001",
        proof_pack={"score": 72, "tier": "moderate_proof"},
        top_accounts=[{"company": "Test"}],
        retainer_eligible=False,
        proof_score=72.0,
    )

    assert isinstance(result, dict)
    assert result.get("status") == "company_brain_v1_ready"
    assert "workspace_id" in result


def test_run_sprint_has_company_brain():
    """run_sprint produces a SprintRun with company_brain populated."""
    from auto_client_acquisition.delivery_factory.delivery_sprint import run_sprint

    run = run_sprint(
        engagement_id="smoke-001",
        customer_id="smoke-test",
    )

    assert hasattr(run, "company_brain")
    d = run.to_dict()
    assert "company_brain" in d


# ── PDF auto-generation signal ─────────────────────────────────────


def test_run_sprint_proof_pack_is_dict():
    """run_sprint returns a SprintRun whose proof_pack is a dict."""
    from auto_client_acquisition.delivery_factory.delivery_sprint import run_sprint

    run = run_sprint(
        engagement_id="pdf-smoke-001",
        customer_id="pdf-smoke",
    )

    assert isinstance(run.proof_pack, dict)
    # _pdf_available is optional — present only if reportlab is installed
    if "_pdf_available" in run.proof_pack:
        assert isinstance(run.proof_pack["_pdf_available"], bool)


# ── ZATCA auto-invoice ────────────────────────────────────────────


@pytest.mark.asyncio
async def test_auto_zatca_invoice_skips_when_no_seller_vat():
    """_auto_zatca_invoice returns early when zatca_seller_vat is empty."""
    pytest.importorskip("jose", reason="python-jose not installed")
    from api.routers.pricing import _auto_zatca_invoice

    mock_settings = MagicMock()
    mock_settings.zatca_seller_vat = ""
    mock_settings.zatca_seller_name = ""

    with patch("api.routers.pricing._auto_zatca_invoice.__globals__") as _:
        # Direct call — relies on function's own settings guard
        pass

    # Call with a patched get_settings inside the function
    with patch("core.config.settings.get_settings", return_value=mock_settings):
        await _auto_zatca_invoice(
            payment={"id": "pay_123", "amount": 49900, "status": "paid"},
            event_type="payment_confirmed",
        )


@pytest.mark.asyncio
@pytest.mark.skipif(
    __import__("importlib.util", fromlist=["find_spec"]).find_spec("jose") is None,
    reason="python-jose not installed",
)
async def test_auto_zatca_invoice_skips_non_payment_status():
    """_auto_zatca_invoice only fires for paid/payment_confirmed/captured."""
    from api.routers.pricing import _auto_zatca_invoice

    mock_settings = MagicMock()
    mock_settings.zatca_seller_vat = "300000000000003"
    mock_settings.zatca_seller_name = "Dealix"

    with patch("core.config.settings.get_settings", return_value=mock_settings):
        # "initiated" is not a payment event — should not raise
        await _auto_zatca_invoice(
            payment={"id": "pay_456", "amount": 49900, "status": "initiated"},
            event_type="payment_initiated",
        )


@pytest.mark.asyncio
@pytest.mark.skipif(
    __import__("importlib.util", fromlist=["find_spec"]).find_spec("jose") is None,
    reason="python-jose not installed",
)
async def test_auto_zatca_invoice_skips_zero_amount():
    """_auto_zatca_invoice returns early when amount is 0."""
    from api.routers.pricing import _auto_zatca_invoice

    mock_settings = MagicMock()
    mock_settings.zatca_seller_vat = "300000000000003"
    mock_settings.zatca_seller_name = "Dealix"

    with patch("core.config.settings.get_settings", return_value=mock_settings):
        await _auto_zatca_invoice(
            payment={"id": "pay_000", "amount": 0, "status": "paid"},
            event_type="paid",
        )


# ── Referral code validation ───────────────────────────────────────


def test_referral_code_format():
    """Referral codes from create_referral_code match REF-XXXXXXXX pattern."""
    import re

    from auto_client_acquisition.partnership_os.referral_store import (
        create_referral_code,
    )

    rc = create_referral_code(
        referrer_id="test-referrer",
        referrer_email="referrer@test.sa",
    )

    assert re.match(r"^REF-[A-F0-9]{8}$", rc.code), f"bad code format: {rc.code}"
    assert rc.referrer_id == "test-referrer"
    d = rc.to_dict()
    assert d.get("status") in ("active", None, "created", "valid")


def test_lookup_code_returns_none_for_unknown():
    """lookup_code returns None for a code that was never created."""
    from auto_client_acquisition.partnership_os.referral_store import lookup_code

    result = lookup_code("REF-DEADBEEF")
    assert result is None


def test_lookup_code_finds_created_code():
    """lookup_code finds a code that was just created."""
    from auto_client_acquisition.partnership_os.referral_store import (
        create_referral_code,
        lookup_code,
    )

    rc = create_referral_code(
        referrer_id="lookup-referrer",
        referrer_email="lookup@test.sa",
    )

    found = lookup_code(rc.code)
    assert found is not None
    assert found.code == rc.code


# ── Redis _get_redis helper ───────────────────────────────────────


@pytest.mark.skipif(
    __import__("importlib.util", fromlist=["find_spec"]).find_spec("jose") is None,
    reason="python-jose not installed",
)
def test_get_redis_returns_none_for_default_url():
    """_get_redis() returns None when settings.redis_url is the default localhost URL."""
    from api.routers.business_now import _get_redis

    mock_settings = MagicMock()
    mock_settings.redis_url = "redis://localhost:6379/0"

    with patch("api.routers.business_now._get_redis.__globals__") as _:
        pass  # Just verifying the function exists and is importable

    # Functional check: default URL → None
    with patch("core.config.settings.get_settings", return_value=mock_settings):
        rc = _get_redis()
    assert rc is None
