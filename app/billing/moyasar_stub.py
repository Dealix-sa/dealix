"""Moyasar integration placeholder.

This module intentionally blocks live payment capture until a future PR adds
secrets, webhook verification, tests, and compliance review.
"""

from __future__ import annotations


def create_payment(*args, **kwargs):
    raise RuntimeError("live payment capture is disabled; use manual invoice mode")


def is_live_payment_enabled() -> bool:
    return False
