"""
Token-saving cache layer: exact-match + semantic caching via Redis.
طبقة الكاش لتوفير التوكنز: مطابقة تامة + كاش دلالي عبر Redis.

Tiers:
  1. In-memory LRU (fast, no network, ephemeral)
  2. Redis exact-match cache (fast, persistent, hash key)
  3. Redis vector/semantic cache (approximate, saves tokens on similar prompts)
     — requires redisvl + Redis Stack (optional, graceful fallback)
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

# ── LRU In-Memory Cache ─────────────────────────────────────────

class LRUCache:
    """Thread-safe in-memory LRU with TTL support."""

    def __init__(self, max_size: int = 256, ttl_seconds: int = 300) -> None:
        self._store: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl_seconds
        self._lock = asyncio.Lock()
        self.hits = 0
        self.misses = 0

    async def get(self, key: str) -> Any | None:
        async with self._lock:
            if key not in self._store:
                self.misses += 1
                return None
            value, ts = self._store[key]
            if time.time() - ts > self.ttl:
                del self._store[key]
                self.misses += 1
                return None
            self._store.move_to_end(key)
            self.hits += 1
            return value

    async def set(self, key: str, value: Any) -> None:
        async with self._lock:
            if key in self._store:
                self._store.move_to_end(key)
            self._store[key] = (value, time.time())
            if len(self._store) > self.max_size:
                self._store.popitem(last=False)

    async def invalidate(self, key: str) -> None:
        async with self._lock:
            self._store.pop(key, None)

    def stats(self) -> dict[str, Any]:
        total = self.hits + self.misses
        return {
            "size": len(self._store),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate_pct": round(self.hits / total * 100, 1) if total else 0.0,
        }


# ── Cache Key ───────────────────────────────────────────────────

def make_cache_key(
    messages: list[dict[str, str]] | str,
    model: str,
    temperature: float = 0.0,
    system: str | None = None,
) -> str:
    """Deterministic cache key from (messages, model, temperature, system)."""
    payload = json.dumps(
        {"m": messages, "model": model, "t": temperature, "sys": system},
        sort_keys=True,
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


# ── Redis Exact-Match Cache ─────────────────────────────────────

@dataclass
class CachedResponse:
    """Cached LLM response stored in Redis."""
    content: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    cached_at: float = field(default_factory=time.time)

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, data: str) -> CachedResponse:
        return cls(**json.loads(data))


class RedisExactCache:
    """
    Redis-backed exact-match cache for LLM responses.
    Key: SHA-256 of (messages, model, temperature, system).
    TTL: configurable, default 1 hour.
    """

    NAMESPACE = "dealix:llm:exact:"

    def __init__(self, redis_url: str, ttl_seconds: int = 3600) -> None:
        self._url = redis_url
        self.ttl = ttl_seconds
        self._client: Any = None
        self.hits = 0
        self.misses = 0

    async def _get_client(self):
        if self._client is None:
            try:
                import redis.asyncio as aioredis  # type: ignore
                self._client = aioredis.from_url(self._url, decode_responses=True)
            except Exception as e:
                logger.warning("Redis unavailable — exact cache disabled: %s", e)
                self._client = False
        return self._client if self._client is not False else None

    async def get(self, key: str) -> CachedResponse | None:
        client = await self._get_client()
        if client is None:
            return None
        try:
            raw = await client.get(self.NAMESPACE + key)
            if raw:
                self.hits += 1
                return CachedResponse.from_json(raw)
            self.misses += 1
        except Exception as e:
            logger.debug("Redis get failed: %s", e)
        return None

    async def set(self, key: str, response: CachedResponse) -> None:
        client = await self._get_client()
        if client is None:
            return
        try:
            await client.setex(self.NAMESPACE + key, self.ttl, response.to_json())
        except Exception as e:
            logger.debug("Redis set failed: %s", e)

    async def invalidate_pattern(self, pattern: str = "*") -> int:
        client = await self._get_client()
        if client is None:
            return 0
        try:
            keys = await client.keys(self.NAMESPACE + pattern)
            if keys:
                return await client.delete(*keys)
        except Exception as e:
            logger.debug("Redis invalidate_pattern failed: %s", e)
        return 0

    def stats(self) -> dict[str, Any]:
        total = self.hits + self.misses
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate_pct": round(self.hits / total * 100, 1) if total else 0.0,
        }


# ── Semantic Cache (redisvl — optional) ─────────────────────────

class SemanticCache:
    """
    Semantic cache using redisvl vector search.
    Returns cached answers for semantically similar queries.
    Falls back gracefully if redisvl is not installed.

    Requires: pip install redisvl + Redis Stack (with RediSearch + RedisJSON)
    """

    def __init__(
        self,
        redis_url: str,
        similarity_threshold: float = 0.92,
        ttl_seconds: int = 7200,
    ) -> None:
        self._url = redis_url
        self.threshold = similarity_threshold
        self.ttl = ttl_seconds
        self._cache: Any = None
        self._available: bool | None = None
        self.hits = 0
        self.misses = 0

    async def _get_cache(self) -> Any | None:
        if self._available is False:
            return None
        if self._cache is not None:
            return self._cache
        try:
            from redisvl.extensions.llmcache import SemanticCache as RVLCache  # type: ignore
            self._cache = RVLCache(
                name="dealix_semantic_cache",
                redis_url=self._url,
                distance_threshold=1.0 - self.threshold,
                ttl=self.ttl,
            )
            self._available = True
            logger.info("SemanticCache: redisvl initialized at %s", self._url)
            return self._cache
        except ImportError:
            logger.info("redisvl not installed — semantic cache disabled")
            self._available = False
        except Exception as e:
            logger.warning("SemanticCache init failed: %s", e)
            self._available = False
        return None

    async def get(self, prompt: str) -> str | None:
        cache = await self._get_cache()
        if cache is None:
            return None
        try:
            results = cache.check(prompt=prompt)
            if results:
                self.hits += 1
                return results[0].get("response")
        except Exception as e:
            logger.debug("SemanticCache.get failed: %s", e)
        self.misses += 1
        return None

    async def set(self, prompt: str, response: str) -> None:
        cache = await self._get_cache()
        if cache is None:
            return
        try:
            cache.store(prompt=prompt, response=response)
        except Exception as e:
            logger.debug("SemanticCache.set failed: %s", e)

    def stats(self) -> dict[str, Any]:
        total = self.hits + self.misses
        return {
            "available": self._available,
            "threshold": self.threshold,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate_pct": round(self.hits / total * 100, 1) if total else 0.0,
        }


# ── Unified Cache Manager ───────────────────────────────────────

class TokenCache:
    """
    Multi-tier cache: LRU → Redis exact → Redis semantic.
    Single entry point for all caching operations.
    """

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        lru_size: int = 512,
        lru_ttl: int = 300,
        exact_ttl: int = 3600,
        semantic_ttl: int = 7200,
        semantic_threshold: float = 0.92,
        enable_semantic: bool = False,
    ) -> None:
        self.lru = LRUCache(max_size=lru_size, ttl_seconds=lru_ttl)
        self.redis = RedisExactCache(redis_url=redis_url, ttl_seconds=exact_ttl)
        self.semantic = SemanticCache(
            redis_url=redis_url,
            similarity_threshold=semantic_threshold,
            ttl_seconds=semantic_ttl,
        ) if enable_semantic else None

    async def get(
        self,
        messages: list[dict[str, str]] | str,
        model: str,
        temperature: float = 0.0,
        system: str | None = None,
    ) -> CachedResponse | None:
        key = make_cache_key(messages, model, temperature, system)

        # Tier 1: LRU
        hit = await self.lru.get(key)
        if hit:
            return hit

        # Tier 2: Redis exact
        hit = await self.redis.get(key)
        if hit:
            await self.lru.set(key, hit)  # warm LRU
            return hit

        # Tier 3: Semantic (single-string prompts only)
        if self.semantic and isinstance(messages, str):
            text = await self.semantic.get(messages)
            if text:
                resp = CachedResponse(
                    content=text, provider="cache", model=model,
                    input_tokens=0, output_tokens=0,
                )
                await self.lru.set(key, resp)
                return resp

        return None

    async def set(
        self,
        messages: list[dict[str, str]] | str,
        model: str,
        response: CachedResponse,
        temperature: float = 0.0,
        system: str | None = None,
    ) -> None:
        key = make_cache_key(messages, model, temperature, system)
        await self.lru.set(key, response)
        await self.redis.set(key, response)
        if self.semantic and isinstance(messages, str):
            await self.semantic.set(messages, response.content)

    def stats(self) -> dict[str, Any]:
        return {
            "lru": self.lru.stats(),
            "redis_exact": self.redis.stats(),
            "semantic": self.semantic.stats() if self.semantic else {"available": False},
        }


# ── Singleton ───────────────────────────────────────────────────

_cache_instance: TokenCache | None = None


def get_token_cache(redis_url: str = "redis://localhost:6379/0") -> TokenCache:
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = TokenCache(redis_url=redis_url)
    return _cache_instance
