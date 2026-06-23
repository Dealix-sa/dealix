"""Outbound safety layer.

All external sends are blocked by default. The policy gate is the single
authority for deciding whether a message may leave the system. Provider
functions are dry-run stubs only — no real network send is performed by this
package.
"""

from app.outbound.policy_gate import (  # noqa: F401
    default_safety_status,
    evaluate_channel_send,
    evaluate_email_send,
    evaluate_sms_send,
    evaluate_whatsapp_send,
    get_outbound_mode,
    is_external_send_enabled,
)

__all__ = [
    "default_safety_status",
    "evaluate_channel_send",
    "evaluate_email_send",
    "evaluate_sms_send",
    "evaluate_whatsapp_send",
    "get_outbound_mode",
    "is_external_send_enabled",
]