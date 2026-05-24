"""Dealix payments — Multi-PSP (Moyasar + Hyperpay + Tap planned), PSP router."""

from dealix.payments.hyperpay import HyperpayClient
from dealix.payments.hyperpay import verify_webhook as verify_hyperpay_webhook
from dealix.payments.moyasar import MoyasarClient
from dealix.payments.moyasar import verify_webhook as verify_moyasar_webhook
from dealix.payments.psp_router import (
    PSP,
    CheckoutRequest,
    PSPHealth,
    PSPRouter,
    RoutingDecision,
)

# Backwards-compatible alias — historical callers import verify_webhook
# expecting the Moyasar verifier.
verify_webhook = verify_moyasar_webhook

__all__ = [
    "MoyasarClient",
    "HyperpayClient",
    "verify_webhook",
    "verify_moyasar_webhook",
    "verify_hyperpay_webhook",
    "PSP",
    "PSPHealth",
    "RoutingDecision",
    "CheckoutRequest",
    "PSPRouter",
]
