"""Simple in-memory rate limiter for outbound sends.

This is a token-bucket-ish sliding window limiter kept deliberately simple and
dependency-free. It is intended to prevent runaway loops from generating too
many drafts/sends in a short window. It is NOT a distributed rate limiter —
production deployments should back this with Redis, but the interface stays the
same (``within_rate_limits`` / ``record_send_attempt``).

Defaults are conservative and configurable via env:

  OUTBOUND_RATE_LIMIT_PER_MINUTE  (default 30)
  OUTBOUND_RATE_LIMIT_PER_HOUR     (default 300)
"""

from __future__ import annotations

import os
import time
from collections import defaultdict, deque
from threading import Lock
from typing import Mapping

_LOCK = Lock()
# _WINDOW_LOGS[(channel, identifier)] = deque[timestamps]
_WINDOW_LOGS: "defaultdict[tuple[str, str], deque[float]]" = defaultdict(deque)


def _limits(env: Mapping[str, str] | None = None) -> tuple[int, int]:
    e = env if env is not None else os.environ
    try:
        per_min = int(e.get("OUTBOUND_RATE_LIMIT_PER_MINUTE", "30"))
    except ValueError:
        per_min = 30
    try:
        per_hour = int(e.get("OUTBOUND_RATE_LIMIT_PER_HOUR", "300"))
    except ValueError:
        per_hour = 300
    return per_min, per_hour


def _prune(channel: str, identifier: str, now: float) -> None:
    key = (channel, identifier)
    bucket = _WINDOW_LOGS[key]
    while bucket and now - bucket[0] > 3600:
        bucket.popleft()


def within_rate_limits(channel: str, identifier: str, env: Mapping[str, str] | None = None) -> bool:
    """True if a new send to `identifier` via `channel` would stay under limits.

    Does NOT record an attempt — call ``record_send_attempt`` after a successful
    (or simulated) send. An empty identifier is treated as "anonymous" and still
    subject to the global per-minute/per-hour ceiling.
    """
    if not identifier:
        identifier = "__anonymous__"
    per_min, per_hour = _limits(env)
    now = time.time()
    with _LOCK:
        _prune(channel, identifier, now)
        bucket = _WINDOW_LOGS[(channel, identifier)]
        last_min = sum(1 for ts in bucket if now - ts < 60)
        last_hour = len(bucket)
        return last_min < per_min and last_hour < per_hour


def record_send_attempt(channel: str, identifier: str) -> None:
    """Record that a send attempt was made (for rate-limit accounting)."""
    if not identifier:
        identifier = "__anonymous__"
    now = time.time()
    with _LOCK:
        _prune(channel, identifier, now)
        _WINDOW_LOGS[(channel, identifier)].append(now)


def reset_rate_limits() -> None:
    """Clear all rate-limit state (used by tests)."""
    with _LOCK:
        _WINDOW_LOGS.clear()


def current_counts(channel: str, identifier: str) -> dict[str, int]:
    """Return current per-minute and per-hour counts for inspection."""
    if not identifier:
        identifier = "__anonymous__"
    now = time.time()
    with _LOCK:
        _prune(channel, identifier, now)
        bucket = _WINDOW_LOGS[(channel, identifier)]
        return {
            "last_minute": sum(1 for ts in bucket if now - ts < 60),
            "last_hour": len(bucket),
        }