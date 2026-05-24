"""Tiny in-memory rate limiter.

Tokens are minted per (capability_id, caller) at a configurable rate. The
limiter is sufficient for the kernel's smoke tests — production should
swap in a Redis-backed limiter.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from time import monotonic


@dataclass
class RateLimit:
    capacity: int
    refill_per_second: float


@dataclass
class RateLimiter:
    limits: dict[str, RateLimit] = field(default_factory=dict)
    _buckets: dict[tuple[str, str], tuple[float, float]] = field(default_factory=dict)

    def configure(self, capability_id: str, limit: RateLimit) -> None:
        self.limits[capability_id] = limit

    def acquire(self, capability_id: str, caller: str, *, tokens: int = 1) -> bool:
        limit = self.limits.get(capability_id)
        if not limit:
            return True
        key = (capability_id, caller)
        now = monotonic()
        bucket, last = self._buckets.get(key, (float(limit.capacity), now))
        bucket = min(limit.capacity, bucket + (now - last) * limit.refill_per_second)
        if bucket < tokens:
            self._buckets[key] = (bucket, now)
            return False
        self._buckets[key] = (bucket - tokens, now)
        return True


__all__ = ["RateLimit", "RateLimiter"]
