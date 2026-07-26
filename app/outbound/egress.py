"""The single chokepoint every outbound message must pass through.

Dealix documents a kill switch: with ``EXTERNAL_SEND_ENABLED=false`` and
``OUTBOUND_MODE=draft_only``, nothing leaves the building. That guarantee was
not enforced. ``api/routers/email_send.py``, ``gmail_send.py`` and
``integrations/email.py`` contained no reference to either variable, and
``policy_gate`` — which implements the rules correctly — had no live importer.
The only thing standing between a configured provider key and a real send was
an ``approved`` row in the database.

Approval is a good control. It is not the same control as the kill switch, and
the repository promised both.

Why the transport layer
-----------------------
Gating at the router would not work here. There are at least three independent
egress points, and two of them are reachable with no HTTP request in the call
stack at all:

* ``auto_client_acquisition/email/gmail_send.py`` POSTs directly to the Gmail API
* ``integrations/email.py`` talks to Resend / SendGrid / SMTP
* ``integrations/whatsapp.py`` talks to the Meta Cloud API

``notifications/founder_alerts.py`` and two ``scripts/`` entry points call into
these without passing through FastAPI. So the guard wraps the functions that
actually touch the network — the last point where "a message is about to leave"
is still true.

Scope: the kill switch, not message quality
-------------------------------------------
This guard answers exactly one question: *is external sending permitted at all,
right now?* It deliberately does not evaluate consent, suppression, unsubscribe
links or claim rules. Those live in ``policy_gate``'s channel checks and in
``auto_client_acquisition.email.compliance`` and run earlier, per message, where
a rejection can be explained to a human.

Mixing the two would mean a content rule could silently authorise a send, or a
master switch could reject a message for a spelling reason. Keeping them apart
means this file is small enough to be obviously correct.

Fail-closed
-----------
Any unexpected error inside the guard blocks the send. A guard that cannot
determine whether sending is permitted has, by definition, not established that
it is. The worst outcome of a bug here is a draft that does not go out; the
worst outcome of failing open is an unapproved message reaching a real company.
"""

from __future__ import annotations

import functools
import logging
import os
from collections.abc import Callable, Mapping
from typing import Any, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])

#: Channel → environment flags that must *all* be true for that channel.
#: These names are fixed by CLAUDE.md's outbound safety policy.
CHANNEL_FLAGS: dict[str, tuple[str, ...]] = {
    "email": ("EMAIL_SEND_ENABLED",),
    "whatsapp": ("WHATSAPP_SEND_ENABLED", "WHATSAPP_ALLOW_LIVE_SEND"),
    "sms": ("SMS_SEND_ENABLED",),
}

#: The only OUTBOUND_MODE under which anything may leave.
CONTROLLED_LIVE = "controlled_live"

_TRUE_VALUES = {"1", "true", "yes", "on"}


class EgressBlocked(RuntimeError):
    """Raised when a send is attempted while outbound is disabled.

    Callers that want a clean API response rather than an exception should
    catch this and translate it — see ``api/routers/email_send.py``.
    """

    def __init__(self, channel: str, reason: str) -> None:
        super().__init__(f"outbound blocked for {channel}: {reason}")
        self.channel = channel
        self.reason = reason


def _flag_is_true(env: Mapping[str, str], key: str) -> bool:
    return env.get(key, "").strip().lower() in _TRUE_VALUES


def egress_permitted(
    channel: str, env: Mapping[str, str] | None = None
) -> tuple[bool, str]:
    """Return ``(permitted, reason)`` for a channel.

    Unknown channels are refused: a new channel must opt in explicitly rather
    than inherit permission by omission.
    """
    e = env if env is not None else os.environ

    if not _flag_is_true(e, "EXTERNAL_SEND_ENABLED"):
        return False, "external_send_disabled"

    mode = (e.get("OUTBOUND_MODE") or "draft_only").strip().lower()
    if mode != CONTROLLED_LIVE:
        return False, f"mode_not_controlled_live:{mode}"

    flags = CHANNEL_FLAGS.get(channel)
    if flags is None:
        return False, f"unknown_channel:{channel}"

    for flag in flags:
        if not _flag_is_true(e, flag):
            return False, f"channel_flag_false:{flag}"

    return True, "ok"


def assert_egress_permitted(
    channel: str, env: Mapping[str, str] | None = None
) -> None:
    """Raise :class:`EgressBlocked` unless sending is permitted. Fail-closed."""
    try:
        permitted, reason = egress_permitted(channel, env)
    except Exception as exc:  # deliberate catch-all: unknown state must block
        # If the guard itself failed we have not established that sending is
        # permitted, so we must not send.
        logger.error(
            "egress_guard_error channel=%s error=%s — blocking (fail-closed)",
            channel,
            exc,
        )
        raise EgressBlocked(channel, "guard_error") from exc

    if not permitted:
        logger.warning("egress_blocked channel=%s reason=%s", channel, reason)
        raise EgressBlocked(channel, reason)


def guarded_egress(
    channel: str, on_blocked: Callable[[str], Any] | None = None
) -> Callable[[F], F]:
    """Decorate a function that puts a message on the wire.

    Apply this to the narrowest function that performs the network call, not to
    a dispatcher above it — a dispatcher gains new provider branches over time
    and each one would silently bypass the guard.

    Draft-creating functions must NOT be decorated. Drafts are the safe path
    and have to keep working while outbound is disabled; that is the whole
    point of ``draft_only`` mode.

    ``on_blocked`` receives the block reason and returns what the function
    should return instead of sending. Prefer it wherever the function has a
    result type: these senders are called from cron scripts and alert helpers
    that expect a value, and turning a disabled channel into an exception
    would convert a normal operating state into an incident. Without it the
    guard raises :class:`EgressBlocked`.

    Either way nothing reaches the network — the difference is only how the
    refusal is reported.
    """

    def decorator(func: F) -> F:
        if _is_coroutine(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                blocked = _blocked_reason(channel)
                if blocked is not None:
                    if on_blocked is not None:
                        return on_blocked(blocked)
                    raise EgressBlocked(channel, blocked)
                return await func(*args, **kwargs)

            async_wrapper.__egress_channel__ = channel  # type: ignore[attr-defined]
            return async_wrapper  # type: ignore[return-value]

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            blocked = _blocked_reason(channel)
            if blocked is not None:
                if on_blocked is not None:
                    return on_blocked(blocked)
                raise EgressBlocked(channel, blocked)
            return func(*args, **kwargs)

        sync_wrapper.__egress_channel__ = channel  # type: ignore[attr-defined]
        return sync_wrapper  # type: ignore[return-value]

    return decorator


def _blocked_reason(channel: str) -> str | None:
    """Return the reason a send is blocked, or ``None`` when permitted.

    Fail-closed: if the check itself raises, the send is blocked.
    """
    try:
        permitted, reason = egress_permitted(channel)
    except Exception as exc:  # deliberate catch-all: unknown state must block
        logger.error(
            "egress_guard_error channel=%s error=%s — blocking (fail-closed)",
            channel,
            exc,
        )
        return "guard_error"

    if permitted:
        return None

    logger.warning("egress_blocked channel=%s reason=%s", channel, reason)
    return reason


def _is_coroutine(func: Callable[..., Any]) -> bool:
    import inspect

    return inspect.iscoroutinefunction(func)
