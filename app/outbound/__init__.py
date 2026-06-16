"""Dealix Controlled Live Outbound System.

Coordinates verified, approved, rate-limited outbound messaging across
email and WhatsApp for Saudi B2B revenue operations.
"""

from app.outbound.config import OutboundSettings
from app.outbound.policy_gate import PolicyGate, PolicyVerdict
from app.outbound.rate_limiter import RateLimiter
from app.outbound.runner import ControlledOutboundRunner

__all__ = [
    "ControlledOutboundRunner",
    "OutboundSettings",
    "PolicyGate",
    "PolicyVerdict",
    "RateLimiter",
]
