"""V11 — minute-bucket cache for the founder dashboard payload.

The dashboard composes ~6 heavy aggregations (service counts, reliability
matrix, daily growth loop, weekly scorecard, CEO brief, first-3 board).
Sequential execution costs ~19s on production. Caching the whole payload
on a 60s minute-bucket key cuts repeat reads to <50ms while keeping
deterministic single-source-of-truth semantics.

Hard constraints:
- Cache only deterministic aggregates.
- NEVER cache secrets or customer PII (the underlying composers already
  redact, this layer just stores their output).
- If any sub-section returned a degraded marker we bypass the cache so
  the next call has a chance to recover.
"""
from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

# Keyed by (minute-bucket, builder-identity). Keying by the builder — not just
# the time bucket — keeps each distinct dashboard endpoint (founder dashboard,
# Beast Command Center, …) in its own cache slot. Without this, whichever
# endpoint was called first within a bucket would poison the others with its
# payload (wrong shape / missing fields). See test_constitution_closure.
_CACHE: dict[tuple[int, str], dict[str, Any]] = {}
_DEFAULT_TTL_SECONDS = 60


def _bucket(ttl_seconds: int) -> int:
    return int(time.time() // ttl_seconds)


def _builder_key(builder: Callable[[], dict[str, Any]], cache_key: str | None) -> str:
    if cache_key:
        return cache_key
    module = getattr(builder, "__module__", "") or ""
    qualname = getattr(builder, "__qualname__", None) or repr(builder)
    return f"{module}.{qualname}"


def _has_degraded(payload: dict[str, Any]) -> bool:
    return bool(payload.get("degraded"))


def cached_dashboard_payload(
    builder: Callable[[], dict[str, Any]],
    *,
    ttl_seconds: int = _DEFAULT_TTL_SECONDS,
    cache_key: str | None = None,
) -> dict[str, Any]:
    """Return a cached dashboard payload, rebuilding once per minute bucket.

    The ``builder`` is the no-arg composer that produces a fresh payload. Each
    distinct ``builder`` (or explicit ``cache_key``) gets its own cache slot so
    different dashboards never collide. On a cache miss we call the builder
    once, time it, and stash the result. Degraded payloads are NEVER cached so
    we don't pin a transient failure.
    """
    bucket = _bucket(ttl_seconds)
    key = (bucket, _builder_key(builder, cache_key))
    cached = _CACHE.get(key)
    if cached is not None:
        out = dict(cached)
        out["cache_hit"] = True
        out["source"] = "cache"
        return out

    started = time.perf_counter()
    payload = builder()
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    payload.setdefault("elapsed_ms", elapsed_ms)
    payload.setdefault("source", "live")
    payload["cache_hit"] = False

    if not _has_degraded(payload):
        # Evict stale buckets but keep other builders cached in the current
        # bucket (bounds memory to the live bucket's distinct dashboards).
        for existing in [k for k in _CACHE if k[0] != bucket]:
            del _CACHE[existing]
        _CACHE[key] = payload
    return payload


def reset_cache() -> None:
    """Forget every cached payload — used in tests."""
    _CACHE.clear()
