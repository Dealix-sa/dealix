"""Stripe payment stub. No live calls."""

from __future__ import annotations

from .base import PaymentProvider


class StripeStub(PaymentProvider):
    name = "stripe"


def is_activated() -> bool:
    return False
