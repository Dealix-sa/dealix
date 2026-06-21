"""Common interface for payment provider stubs.

These do NOT make live calls. Activating requires the gates in
`docs/payments/PAYMENT_SECURITY_BOUNDARIES.md`.
"""

from __future__ import annotations

from dataclasses import dataclass


class StubNotActivated(RuntimeError):
    """Raised when stub is called without explicit activation."""


@dataclass
class PaymentLinkRequest:
    quote_id: str
    amount: float
    currency: str
    customer_name: str
    description: str


@dataclass
class PaymentLinkResult:
    provider: str
    link_url: str
    provider_link_id: str


class PaymentProvider:
    name: str = "base"

    def create_payment_link(self, request: PaymentLinkRequest) -> PaymentLinkResult:
        raise StubNotActivated(
            f"{self.name} stub is not activated. See docs/payments/PAYMENT_SECURITY_BOUNDARIES.md"
        )

    def verify_webhook(self, payload: bytes, signature: str) -> bool:  # noqa: ARG002
        raise StubNotActivated(f"{self.name} stub is not activated.")
