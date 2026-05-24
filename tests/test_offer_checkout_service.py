"""OfferCheckoutService — Phase 1 end-to-end orchestration tests.

Validates:
  - idempotency key determinism + reuse
  - intake guard rejects bad payloads with no Moyasar call
  - free diagnostic flow (no Moyasar invocation)
  - escalation classes never mint a Moyasar invoice via self-serve
  - auto-approve offers mint exactly one invoice and cache it
"""

from __future__ import annotations

from typing import Any

import pytest

from auto_client_acquisition.governance_os.lawful_basis import LawfulBasis
from dealix.payments.checkout import (
    OFFER_CATALOG,
    CheckoutResult,
    InMemoryCheckoutStore,
    OfferCheckoutService,
    compute_idempotency_key,
)


class _SpyHostedPaymentFactory:
    """Records every call; returns a deterministic stub invoice."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def __call__(self, **kwargs: Any) -> dict[str, Any]:
        self.calls.append(kwargs)
        return {
            "id": f"inv_{len(self.calls)}",
            "url": f"https://moyasar.test/pay/inv_{len(self.calls)}",
            "status": "initiated",
        }


@pytest.fixture
def service() -> tuple[OfferCheckoutService, _SpyHostedPaymentFactory]:
    spy = _SpyHostedPaymentFactory()
    svc = OfferCheckoutService(
        store=InMemoryCheckoutStore(),
        hosted_payment_factory=spy,
        callback_base_url="https://api.dealix.test",
    )
    return svc, spy


def test_idempotency_key_deterministic():
    a = compute_idempotency_key(source_passport_id="p1", offer_id="sprint_499")
    b = compute_idempotency_key(source_passport_id="p1", offer_id="sprint_499")
    assert a == b
    assert a != compute_idempotency_key(source_passport_id="p2", offer_id="sprint_499")
    assert a != compute_idempotency_key(source_passport_id="p1", offer_id="data_pack_1500")


def test_offer_catalog_has_five_offers():
    assert set(OFFER_CATALOG.keys()) == {
        "diagnostic_free",
        "sprint_499",
        "data_pack_1500",
        "managed_ops_retainer",
        "custom_ai",
    }


@pytest.mark.asyncio
async def test_auto_approve_sprint_mints_invoice(service):
    svc, spy = service
    result = await svc.checkout(
        offer_id="sprint_499",
        source_passport_id="passport_001",
        lawful_basis=LawfulBasis.CONSENT,
        consent_given=True,
        customer_handle="ahmad",
        locale="ar",
    )
    assert result.status == "ok"
    assert result.invoice_id.startswith("inv_")
    assert result.hosted_payment_url.startswith("https://moyasar.test/pay/")
    assert result.amount_halalas == 49_900
    assert len(spy.calls) == 1
    call = spy.calls[0]
    assert call["offer_id"] == "sprint_499"
    assert call["source_passport_id"] == "passport_001"
    assert call["callback_url"] == "https://api.dealix.test/api/v1/webhooks/moyasar"
    assert call["idempotency_key"] == result.idempotency_key


@pytest.mark.asyncio
async def test_idempotent_replay_returns_cached_result(service):
    svc, spy = service
    a = await svc.checkout(
        offer_id="sprint_499",
        source_passport_id="passport_002",
        lawful_basis=LawfulBasis.CONSENT,
        consent_given=True,
    )
    b = await svc.checkout(
        offer_id="sprint_499",
        source_passport_id="passport_002",
        lawful_basis=LawfulBasis.CONSENT,
        consent_given=True,
    )
    assert a.idempotency_key == b.idempotency_key
    assert a.invoice_id == b.invoice_id
    assert a.hosted_payment_url == b.hosted_payment_url
    assert len(spy.calls) == 1  # second call must NOT hit Moyasar


@pytest.mark.asyncio
async def test_free_diagnostic_no_moyasar_call(service):
    svc, spy = service
    result = await svc.checkout(
        offer_id="diagnostic_free",
        source_passport_id="passport_003",
        lawful_basis=LawfulBasis.CONSENT,
        consent_given=True,
    )
    assert result.status == "free"
    assert result.invoice_id is None
    assert result.hosted_payment_url is None
    assert result.amount_halalas == 0
    assert len(spy.calls) == 0


@pytest.mark.asyncio
async def test_custom_ai_always_escalates(service):
    svc, spy = service
    result = await svc.checkout(
        offer_id="custom_ai",
        source_passport_id="passport_004",
        lawful_basis=LawfulBasis.CONTRACT,
        consent_given=False,
    )
    assert result.status == "escalated"
    assert result.approval_class == "escalate_always"
    assert result.invoice_id is None
    assert len(spy.calls) == 0  # no Moyasar call for escalate path


@pytest.mark.asyncio
async def test_managed_ops_first_time_escalates(service):
    svc, spy = service
    result = await svc.checkout(
        offer_id="managed_ops_retainer",
        source_passport_id="passport_005",
        lawful_basis=LawfulBasis.CONSENT,
        consent_given=True,
    )
    assert result.status == "escalated"
    assert len(spy.calls) == 0


@pytest.mark.asyncio
async def test_intake_violation_rejected_without_moyasar_call(service):
    svc, spy = service
    result = await svc.checkout(
        offer_id="sprint_499",
        source_passport_id="",  # missing passport
        lawful_basis=LawfulBasis.CONSENT,
        consent_given=True,
    )
    assert result.status == "rejected"
    assert result.verdict is not None
    assert "source_passport_id_missing" in result.verdict.violation_codes
    assert len(spy.calls) == 0


@pytest.mark.asyncio
async def test_forbidden_pattern_rejected(service):
    svc, spy = service
    result = await svc.checkout(
        offer_id="sprint_499",
        source_passport_id="passport_006",
        lawful_basis=LawfulBasis.CONSENT,
        consent_given=True,
        free_text="please cold whatsapp blast my entire list immediately",
    )
    assert result.status == "rejected"
    assert "channel_pattern_forbidden" in result.verdict.violation_codes
    assert len(spy.calls) == 0


@pytest.mark.asyncio
async def test_unknown_offer_rejected_without_idem_key(service):
    svc, spy = service
    result = await svc.checkout(
        offer_id="space_offer",
        source_passport_id="passport_007",
        lawful_basis=LawfulBasis.CONSENT,
        consent_given=True,
    )
    assert result.status == "rejected"
    assert len(spy.calls) == 0


@pytest.mark.asyncio
async def test_factory_required_for_paid_offers():
    svc = OfferCheckoutService(
        store=InMemoryCheckoutStore(),
        hosted_payment_factory=None,  # not configured
    )
    with pytest.raises(RuntimeError) as exc:
        await svc.checkout(
            offer_id="sprint_499",
            source_passport_id="p",
            lawful_basis=LawfulBasis.CONSENT,
            consent_given=True,
        )
    assert "hosted_payment_factory" in str(exc.value)


def test_checkout_result_to_dict_serializable():
    import json

    r = CheckoutResult(
        status="ok",
        offer_id="sprint_499",
        idempotency_key="abc",
        approval_class="auto_approve",
        invoice_id="inv_1",
        hosted_payment_url="https://moyasar.test/pay/inv_1",
        amount_halalas=49_900,
        currency="SAR",
    )
    json.dumps(r.to_dict(), ensure_ascii=False)
