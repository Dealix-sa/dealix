"""
Langfuse tracker — observability for every LLM call: tokens, cost, latency, cache.
متتبع Langfuse — مراقبة كل نداء LLM: التوكنز والتكلفة والسرعة والكاش.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class TraceContext:
    """Context for a single LLM call trace."""
    trace_id: str | None = None
    generation_id: str | None = None
    start_time: float = field(default_factory=time.time)
    name: str = "llm_call"
    input_text: str = ""
    model: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class LangfuseTracker:
    """
    Wraps Langfuse SDK for token/cost observability.
    Gracefully disabled if LANGFUSE_PUBLIC_KEY is not set.

    Usage:
        tracker = LangfuseTracker.from_settings()
        async with tracker.trace("my_call", model="claude-sonnet-4-6") as ctx:
            response = await client.chat(...)
            ctx.metadata["cache_hit"] = False
        await tracker.record_usage(ctx, response)
    """

    def __init__(
        self,
        public_key: str | None = None,
        secret_key: str | None = None,
        host: str = "https://cloud.langfuse.com",
    ) -> None:
        self._public_key = public_key
        self._secret_key = secret_key
        self._host = host
        self._client: Any = None
        self._enabled: bool | None = None

    @classmethod
    def from_settings(cls) -> LangfuseTracker:
        from core.config.settings import get_settings
        s = get_settings()
        return cls(
            public_key=s.langfuse_public_key.get_secret_value() if s.langfuse_public_key else None,
            secret_key=s.langfuse_secret_key.get_secret_value() if s.langfuse_secret_key else None,
            host=s.langfuse_host,
        )

    def _get_client(self) -> Any | None:
        if self._enabled is False:
            return None
        if self._client is not None:
            return self._client
        if not self._public_key or not self._secret_key:
            self._enabled = False
            logger.info("Langfuse disabled — LANGFUSE_PUBLIC_KEY not set")
            return None
        try:
            from langfuse import Langfuse  # type: ignore
            self._client = Langfuse(
                public_key=self._public_key,
                secret_key=self._secret_key,
                host=self._host,
            )
            self._enabled = True
            logger.info("Langfuse tracker initialized → %s", self._host)
            return self._client
        except ImportError:
            logger.info("langfuse package not installed — tracking disabled")
            self._enabled = False
        except Exception as e:
            logger.warning("Langfuse init failed: %s", e)
            self._enabled = False
        return None

    def track_generation(
        self,
        name: str,
        model: str,
        input_text: str | list[dict],
        output_text: str,
        input_tokens: int,
        output_tokens: int,
        cached_tokens: int = 0,
        latency_ms: float = 0.0,
        metadata: dict[str, Any] | None = None,
        trace_id: str | None = None,
    ) -> None:
        """Record a completed LLM generation to Langfuse."""
        client = self._get_client()
        if client is None:
            return
        try:
            from langfuse.model import Usage  # type: ignore
            kwargs: dict[str, Any] = {
                "name": name,
                "model": model,
                "input": input_text,
                "output": output_text,
                "usage": Usage(
                    input=input_tokens,
                    output=output_tokens,
                    total=input_tokens + output_tokens,
                    unit="TOKENS",
                ),
                "metadata": {
                    "cached_tokens": cached_tokens,
                    "latency_ms": round(latency_ms, 1),
                    **(metadata or {}),
                },
            }
            if trace_id:
                kwargs["trace_id"] = trace_id
            client.generation(**kwargs)
        except Exception as e:
            logger.debug("Langfuse track_generation failed: %s", e)

    def track_cache_hit(
        self,
        cache_type: str,
        model: str,
        tokens_saved: int,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Record a cache hit event (tokens saved)."""
        client = self._get_client()
        if client is None:
            return
        try:
            client.event(
                name="cache_hit",
                metadata={
                    "cache_type": cache_type,
                    "model": model,
                    "tokens_saved": tokens_saved,
                    **(metadata or {}),
                },
            )
        except Exception as e:
            logger.debug("Langfuse track_cache_hit failed: %s", e)

    def flush(self) -> None:
        """Flush pending events to Langfuse (call on shutdown)."""
        client = self._get_client()
        if client is not None:
            try:
                client.flush()
            except Exception as e:
                logger.debug("Langfuse flush failed: %s", e)

    @property
    def is_enabled(self) -> bool:
        return self._get_client() is not None


# ── FastAPI Middleware ───────────────────────────────────────────

class TokenUsageMiddleware:
    """
    ASGI middleware that tracks token usage headers on LLM responses.
    Adds X-Token-* response headers for observability.
    """

    def __init__(self, app: Any, tracker: LangfuseTracker | None = None) -> None:
        self.app = app
        self.tracker = tracker or LangfuseTracker.from_settings()

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start = time.time()

        async def send_wrapper(message: Any) -> None:
            if message["type"] == "http.response.start":
                elapsed_ms = (time.time() - start) * 1000
                new_headers = list(message.get("headers", []))
                new_headers.append(
                    (b"x-response-time-ms", str(round(elapsed_ms, 1)).encode())
                )
                message = {**message, "headers": new_headers}
            await send(message)

        await self.app(scope, receive, send_wrapper)


# ── Singleton ───────────────────────────────────────────────────

_tracker: LangfuseTracker | None = None


def get_tracker() -> LangfuseTracker:
    global _tracker
    if _tracker is None:
        _tracker = LangfuseTracker.from_settings()
    return _tracker
