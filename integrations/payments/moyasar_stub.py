"""Moyasar payment stub. No live calls."""

from __future__ import annotations

from .base import PaymentProvider


class MoyasarStub(PaymentProvider):
    name = "moyasar"


def is_activated() -> bool:
    """Returns True if the stub has been intentionally activated.

    Activation requires the gates in docs/payments/PAYMENT_SECURITY_BOUNDARIES.md.
    Default is False — the stub raises StubNotActivated until a real impl lands.
    """
    return False
