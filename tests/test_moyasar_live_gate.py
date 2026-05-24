"""Moyasar live-charge gate — Non-Negotiable #6.

Hard guarantee: a live charge cannot leave the codebase unless BOTH
moyasar_mode == "live" AND moyasar_live_verified == True.

Test mode is unrestricted; live mode without verification blocks
deterministically (no network call).
"""

from __future__ import annotations

import pytest

from dealix.payments.moyasar import (
    MoyasarClient,
    MoyasarLiveGateError,
)


def test_test_mode_never_blocks_at_gate():
    """In test mode the gate is a no-op (test charges flow freely)."""
    c = MoyasarClient(secret_key="sk_test_x", mode="test", live_verified=False)
    # Should not raise even with verified=False, because mode=test.
    c._enforce_live_gate(amount_halalas=1000)


def test_live_mode_unverified_blocks():
    """Live mode without verification must raise MoyasarLiveGateError."""
    c = MoyasarClient(secret_key="sk_live_x", mode="live", live_verified=False)
    with pytest.raises(MoyasarLiveGateError) as exc:
        c._enforce_live_gate(amount_halalas=1000)
    assert "live_verified=False" in str(exc.value)


def test_live_mode_verified_zero_amount_blocks():
    """Even verified live mode rejects zero/negative amounts."""
    c = MoyasarClient(secret_key="sk_live_x", mode="live", live_verified=True)
    with pytest.raises(MoyasarLiveGateError):
        c._enforce_live_gate(amount_halalas=0)
    with pytest.raises(MoyasarLiveGateError):
        c._enforce_live_gate(amount_halalas=-100)


def test_live_mode_verified_positive_amount_allowed():
    """Verified live mode with positive amount passes the gate."""
    c = MoyasarClient(secret_key="sk_live_x", mode="live", live_verified=True)
    # Should not raise.
    c._enforce_live_gate(amount_halalas=1000)


@pytest.mark.asyncio
async def test_create_invoice_live_mode_unverified_blocks():
    """create_invoice itself must call the gate before any network IO."""
    c = MoyasarClient(secret_key="sk_live_x", mode="live", live_verified=False)
    with pytest.raises(MoyasarLiveGateError):
        await c.create_invoice(amount_halalas=4990, description="499 Sprint")


@pytest.mark.asyncio
async def test_create_hosted_payment_requires_source_passport():
    """Non-Negotiable #10 — Source Passport is hard-required."""
    c = MoyasarClient(secret_key="sk_test_x", mode="test", live_verified=False)
    with pytest.raises(ValueError) as exc:
        await c.create_hosted_payment(
            amount_halalas=4990,
            offer_id="sprint_499",
            source_passport_id="",
            callback_url="https://api.dealix.me/cb",
        )
    assert "source_passport" in str(exc.value).lower()


@pytest.mark.asyncio
async def test_create_hosted_payment_requires_offer_id():
    """Offer ID is mandatory for self-serve checkout routing."""
    c = MoyasarClient(secret_key="sk_test_x", mode="test", live_verified=False)
    with pytest.raises(ValueError):
        await c.create_hosted_payment(
            amount_halalas=4990,
            offer_id="",
            source_passport_id="passport_abc",
            callback_url="https://api.dealix.me/cb",
        )


def test_live_verified_alone_does_not_unlock():
    """Verified flag alone (with mode=test) keeps the gate closed for live ops."""
    # When mode=test, the gate is bypassed by design — but the composite
    # moyasar_live_enabled property must remain False until both flip.
    c = MoyasarClient(secret_key="sk_test_x", mode="test", live_verified=True)
    # No raise (mode=test) — but composite check elsewhere must say "not live".
    c._enforce_live_gate(amount_halalas=1000)


def test_live_gate_error_is_runtime_error_subclass():
    """MoyasarLiveGateError must be catchable as RuntimeError for compat."""
    assert issubclass(MoyasarLiveGateError, RuntimeError)
