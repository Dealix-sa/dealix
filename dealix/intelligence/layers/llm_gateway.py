"""
LLM Gateway — unified provider-agnostic interface for Dealix layers.
بوابة موحدة للنماذج اللغوية — مزودون متعددون مع كاش وحماية.

Wraps any provider that follows a simple async `chat(messages) -> str`
contract, plus optional safety pre-check, prompt cache, retry-with-
exponential-backoff, and provider fallback. The gateway never sends real
external messages — Dealix doctrine. It only calls LLM completions.

If no providers are registered, every call returns a deterministic
"degraded" response so layers can be exercised end-to-end without keys.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Iterable, Literal

from dealix.intelligence.layers.prompt_cache import PromptCache
from dealix.intelligence.layers.safety import SafetyClassifier, SafetyResult

ProviderFn = Callable[[list[dict[str, str]], dict[str, Any]], Awaitable[str]]
RouteMode = Literal["first_available", "round_robin", "cheapest"]


@dataclass
class Provider:
    name: str
    fn: ProviderFn
    cost_per_1k_tokens: float = 0.0
    enabled: bool = True
    healthy: bool = True
    last_error: str = ""
    success_count: int = 0
    failure_count: int = 0


@dataclass(frozen=True)
class GatewayResponse:
    text: str
    provider: str
    cached: bool
    safety: SafetyResult
    latency_ms: float
    attempts: int
    degraded: bool
    metadata: dict[str, Any] = field(default_factory=dict)


class LLMGateway:
    """Provider-agnostic LLM front door."""

    def __init__(
        self,
        *,
        cache: PromptCache | None = None,
        safety: SafetyClassifier | None = None,
        max_retries: int = 2,
        base_backoff: float = 0.25,
        route_mode: RouteMode = "first_available",
    ) -> None:
        self._cache = cache or PromptCache()
        self._safety = safety or SafetyClassifier()
        self._max_retries = max_retries
        self._base_backoff = base_backoff
        self._route_mode = route_mode
        self._providers: list[Provider] = []
        self._rr_idx = 0

    # ── Provider registration ─────────────────────────────────────
    def register(
        self,
        name: str,
        fn: ProviderFn,
        *,
        cost_per_1k_tokens: float = 0.0,
        enabled: bool = True,
    ) -> None:
        if not name:
            raise ValueError("provider name required")
        self._providers.append(
            Provider(name=name, fn=fn, cost_per_1k_tokens=cost_per_1k_tokens, enabled=enabled)
        )

    def providers(self) -> list[dict[str, Any]]:
        return [
            {
                "name": p.name,
                "enabled": p.enabled,
                "healthy": p.healthy,
                "cost_per_1k": p.cost_per_1k_tokens,
                "success_count": p.success_count,
                "failure_count": p.failure_count,
                "last_error": p.last_error,
            }
            for p in self._providers
        ]

    # ── Core call ─────────────────────────────────────────────────
    async def chat(
        self,
        messages: list[dict[str, str]],
        *,
        config: dict[str, Any] | None = None,
        use_cache: bool = True,
        cache_ttl: float | None = None,
    ) -> GatewayResponse:
        config = config or {}
        last_user = next(
            (m.get("content", "") for m in reversed(messages) if m.get("role") == "user"),
            "",
        )
        safety_result = self._safety.evaluate(last_user)
        if safety_result.recommended_action == "block":
            return GatewayResponse(
                text="[blocked_by_safety_layer]",
                provider="safety-guard",
                cached=False,
                safety=safety_result,
                latency_ms=0.0,
                attempts=0,
                degraded=True,
                metadata={"reason": "safety.block", "findings": len(safety_result.findings)},
            )

        cache_key = PromptCache.make_key("chat", messages, config)
        if use_cache:
            cached = self._cache.get(cache_key)
            if cached is not None:
                return GatewayResponse(
                    text=cached,
                    provider="cache",
                    cached=True,
                    safety=safety_result,
                    latency_ms=0.0,
                    attempts=0,
                    degraded=False,
                )
        ordered = self._order_providers()
        if not ordered:
            return GatewayResponse(
                text="[no_provider_registered_degraded]",
                provider="degraded",
                cached=False,
                safety=safety_result,
                latency_ms=0.0,
                attempts=0,
                degraded=True,
                metadata={"reason": "no_provider"},
            )

        attempts = 0
        start = time.perf_counter()
        last_err = ""
        for provider in ordered:
            for retry in range(self._max_retries + 1):
                attempts += 1
                try:
                    text = await provider.fn(messages, config)
                    if text is None:
                        raise RuntimeError("provider returned None")
                    provider.success_count += 1
                    if use_cache:
                        self._cache.set(cache_key, text, ttl=cache_ttl)
                    latency_ms = (time.perf_counter() - start) * 1000
                    return GatewayResponse(
                        text=text,
                        provider=provider.name,
                        cached=False,
                        safety=safety_result,
                        latency_ms=round(latency_ms, 2),
                        attempts=attempts,
                        degraded=False,
                    )
                except Exception as exc:  # noqa: BLE001
                    provider.failure_count += 1
                    provider.last_error = repr(exc)[:200]
                    last_err = provider.last_error
                    provider.healthy = False
                    if retry < self._max_retries:
                        await asyncio.sleep(self._base_backoff * (2 ** retry))
                        continue
                    break  # try next provider
        latency_ms = (time.perf_counter() - start) * 1000
        return GatewayResponse(
            text="[all_providers_failed_degraded]",
            provider="degraded",
            cached=False,
            safety=safety_result,
            latency_ms=round(latency_ms, 2),
            attempts=attempts,
            degraded=True,
            metadata={"last_error": last_err},
        )

    # ── Stats ─────────────────────────────────────────────────────
    def stats(self) -> dict[str, Any]:
        return {
            "providers": self.providers(),
            "cache": self._cache.stats(),
            "route_mode": self._route_mode,
            "max_retries": self._max_retries,
        }

    # ── Internals ─────────────────────────────────────────────────
    def _order_providers(self) -> list[Provider]:
        active = [p for p in self._providers if p.enabled]
        if not active:
            return []
        if self._route_mode == "cheapest":
            return sorted(active, key=lambda p: p.cost_per_1k_tokens)
        if self._route_mode == "round_robin" and active:
            self._rr_idx = (self._rr_idx + 1) % len(active)
            return active[self._rr_idx :] + active[: self._rr_idx]
        # first_available: prefer healthy first.
        return sorted(active, key=lambda p: (not p.healthy, p.failure_count))
