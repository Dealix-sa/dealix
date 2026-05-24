"""Dealix payments — Moyasar (primary) + Tap.company (backup) integrations."""

from dealix.payments.moyasar import MoyasarClient
from dealix.payments.moyasar import verify_webhook as verify_moyasar_webhook
from dealix.payments.tap import TapClient
from dealix.payments.tap import verify_webhook as verify_tap_webhook

# Back-compat alias — existing callers import `verify_webhook` for Moyasar.
verify_webhook = verify_moyasar_webhook

__all__ = [
    "MoyasarClient",
    "TapClient",
    "verify_webhook",
    "verify_moyasar_webhook",
    "verify_tap_webhook",
]
