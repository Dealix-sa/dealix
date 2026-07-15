"""Tests for the multi-PSP router (Track 2 of the Build-Out Plan)."""

from __future__ import annotations

from decimal import Decimal

import pytest

from dealix.payments.psp_router import (
    PSP,
    CheckoutRequest,
    PSPHealth,
    PSPRouter,
    RoutingDecision,
)


def _req(**overrides):
    base = {
        "amount_sar": Decimal("100"),
        "currency": "SAR",
        "customer_email": "x@example.sa",
        "customer_tenant_id": "tenant-1",
        "description": "Sprint",
        "metadata": {},
    }
    base.update(overrides)
    return CheckoutRequest(**base)


def test_default_chain_picks_moyasar_first():
    router = PSPRouter()
    decision = router.select(_req())
    assert decision.primary == PSP.MOYASAR
    assert PSP.HYPERPAY in decision.fallback_chain
    assert PSP.TAP in decision.fallback_chain
    assert decision.rule_applied == "default"


def test_customer_preference_honored():
    router = PSPRouter()
    decision = router.select(_req(customer_preference=PSP.TAP))
    assert decision.primary == PSP.TAP
    assert PSP.MOYASAR in decision.fallback_chain
    assert decision.rule_applied == "rule_1_customer_preference"


def test_high_value_routes_to_hyperpay():
    router = PSPRouter()
    decision = router.select(_req(amount_sar=Decimal("50000")))
    assert decision.primary == PSP.HYPERPAY
    assert decision.rule_applied == "rule_3_amount_tier"


def test_unhealthy_primary_falls_through():
    router = PSPRouter(
        health_lookup={
            PSP.MOYASAR: PSPHealth(
                psp=PSP.MOYASAR,
                is_healthy=False,
                consecutive_failures=3,
                last_failure_reason="account_inactive_error",
            )
        }
    )
    decision = router.select(_req())
    assert decision.primary != PSP.MOYASAR
    assert decision.rule_applied == "rule_4_health_check"


def test_all_unhealthy_falls_back_to_primary():
    router = PSPRouter(
        health_lookup={
            PSP.MOYASAR: PSPHealth(psp=PSP.MOYASAR, is_healthy=False),
            PSP.HYPERPAY: PSPHealth(psp=PSP.HYPERPAY, is_healthy=False),
            PSP.TAP: PSPHealth(psp=PSP.TAP, is_healthy=False),
        }
    )
    decision = router.select(_req())
    assert decision.primary == PSP.MOYASAR
    assert decision.fallback_chain == []
    assert decision.rule_applied == "rule_4_health_check_no_healthy"


def test_non_sar_currency_routes_to_hyperpay():
    router = PSPRouter()
    decision = router.select(_req(currency="USD"))
    assert decision.primary == PSP.HYPERPAY
    assert decision.rule_applied == "rule_2_currency"


def test_primary_override_via_constructor():
    router = PSPRouter(primary_override=PSP.HYPERPAY)
    decision = router.select(_req())
    assert decision.primary == PSP.HYPERPAY


def test_routing_is_deterministic():
    router = PSPRouter()
    req = _req()
    d1 = router.select(req)
    d2 = router.select(req)
    assert d1 == d2
