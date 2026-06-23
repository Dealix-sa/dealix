"""Channel router — maps channel names to their gate checks and provider stubs.

The router does not send. It resolves which channel-specific evaluator and
provider stub apply for a given channel name, and returns a routing decision
that the caller can use to dispatch (or, in controlled_live mode, to invoke the
provider stub which is itself a dry-run).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from app.outbound import policy_gate
from app.outbound.provider_router import (
    ProviderCall,
    get_provider_stub,
)

CHANNEL_EMAIL = "email"
CHANNEL_WHATSAPP = "whatsapp"
CHANNEL_SMS = "sms"
KNOWN_CHANNELS = (CHANNEL_EMAIL, CHANNEL_WHATSAPP, CHANNEL_SMS)


@dataclass(frozen=True)
class RouteDecision:
    """Result of routing a send request to a channel."""

    channel: str
    supported: bool
    evaluator: Callable[..., Any] | None
    provider: ProviderCall | None
    reason: str


def _evaluator_for(channel: str) -> Callable[..., Any] | None:
    if channel == CHANNEL_EMAIL:
        return policy_gate.evaluate_email_send
    if channel == CHANNEL_WHATSAPP:
        return policy_gate.evaluate_whatsapp_send
    if channel == CHANNEL_SMS:
        return policy_gate.evaluate_sms_send
    return None


def route(channel: str) -> RouteDecision:
    """Resolve the evaluator and provider stub for a channel."""
    evaluator = _evaluator_for(channel)
    provider = get_provider_stub(channel)
    if evaluator is None or provider is None:
        return RouteDecision(
            channel=channel,
            supported=False,
            evaluator=None,
            provider=None,
            reason="unsupported_channel",
        )
    return RouteDecision(
        channel=channel,
        supported=True,
        evaluator=evaluator,
        provider=provider,
        reason="ok",
    )


def evaluate_and_route(
    channel: str,
    message: Mapping[str, Any],
    contact: Mapping[str, Any],
    env: Mapping[str, str] | None = None,
):
    """Route to the channel evaluator and return its SendEvaluation.

    If the channel is unsupported, returns a synthetic blocked evaluation.
    """
    decision = route(channel)
    if not decision.supported or decision.evaluator is None:
        return policy_gate.evaluate_channel_send(channel, message, contact, env)
    return decision.evaluator(message, contact, env)