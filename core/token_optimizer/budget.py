"""
Budget guard for LLM calls — enforces per-call and per-session token/cost limits.
حارس الميزانية — يطبّق حدود التوكنز والتكلفة لكل نداء وجلسة.
"""
from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import Any

from core.token_optimizer.counter import CostEstimate, count_tokens, estimate_cost

logger = logging.getLogger(__name__)


class BudgetExceededError(Exception):
    """Raised when a call would exceed the configured budget."""
    def __init__(self, reason: str, estimate: CostEstimate | None = None):
        super().__init__(reason)
        self.estimate = estimate


@dataclass
class BudgetConfig:
    """Budget limits for a session or feature.

    Set any limit to None to disable that check.
    """
    max_input_tokens_per_call: int | None = 100_000   # ~100k tokens per call
    max_output_tokens_per_call: int | None = 8_000
    max_cost_per_call_usd: float | None = 0.50        # $0.50 per call
    max_tokens_per_session: int | None = 1_000_000    # 1M tokens per session
    max_cost_per_session_usd: float | None = 5.0      # $5 per session
    warn_threshold_pct: float = 0.80                  # warn at 80% of limit


@dataclass
class SessionUsage:
    """Accumulates usage within a session."""
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cached_tokens: int = 0
    total_calls: int = 0
    total_cost_usd: float = 0.0
    session_start: float = field(default_factory=time.time)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock, repr=False)

    async def record(
        self,
        input_tokens: int,
        output_tokens: int,
        cached_tokens: int,
        cost_usd: float,
    ) -> None:
        async with self._lock:
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens
            self.total_cached_tokens += cached_tokens
            self.total_calls += 1
            self.total_cost_usd += cost_usd

    @property
    def total_tokens(self) -> int:
        return self.total_input_tokens + self.total_output_tokens

    @property
    def cache_hit_rate(self) -> float:
        if self.total_input_tokens == 0:
            return 0.0
        return self.total_cached_tokens / self.total_input_tokens

    @property
    def elapsed_seconds(self) -> float:
        return time.time() - self.session_start

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_calls": self.total_calls,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_cached_tokens": self.total_cached_tokens,
            "total_tokens": self.total_tokens,
            "cache_hit_rate_pct": round(self.cache_hit_rate * 100, 1),
            "total_cost_usd": round(self.total_cost_usd, 4),
            "elapsed_seconds": round(self.elapsed_seconds, 1),
        }


class BudgetGuard:
    """
    Enforces token and cost budgets before and after LLM calls.

    Usage:
        guard = BudgetGuard(BudgetConfig(max_cost_per_call_usd=0.10))
        guard.check_pre_call(input_text, model="claude-sonnet-4-6")
        response = await client.chat(...)
        await guard.record_post_call(response)
    """

    def __init__(self, config: BudgetConfig | None = None) -> None:
        self.config = config or BudgetConfig()
        self.session = SessionUsage()

    def check_pre_call(
        self,
        input_text: str | int,
        model: str = "claude-sonnet-4-6",
        estimated_output_tokens: int = 512,
    ) -> CostEstimate:
        """
        Check budget BEFORE sending the request.
        Raises BudgetExceededError if any limit would be exceeded.
        Returns CostEstimate for logging.
        """
        tokens = (
            input_text if isinstance(input_text, int)
            else count_tokens(str(input_text), model)
        )
        est = estimate_cost(tokens, model, estimated_output_tokens)
        cfg = self.config

        # Per-call checks
        if cfg.max_input_tokens_per_call and tokens > cfg.max_input_tokens_per_call:
            raise BudgetExceededError(
                f"Input tokens {tokens:,} exceeds per-call limit "
                f"{cfg.max_input_tokens_per_call:,}",
                est,
            )
        if cfg.max_cost_per_call_usd and est.total_cost_usd > cfg.max_cost_per_call_usd:
            raise BudgetExceededError(
                f"Estimated cost ${est.total_cost_usd:.4f} exceeds per-call limit "
                f"${cfg.max_cost_per_call_usd:.4f}",
                est,
            )

        # Session-level checks
        if cfg.max_tokens_per_session:
            projected = self.session.total_tokens + tokens + estimated_output_tokens
            if projected > cfg.max_tokens_per_session:
                raise BudgetExceededError(
                    f"Session would reach {projected:,} tokens, limit is "
                    f"{cfg.max_tokens_per_session:,}",
                    est,
                )
            # Warning threshold
            pct = projected / cfg.max_tokens_per_session
            if pct >= cfg.warn_threshold_pct:
                logger.warning(
                    "Session at %.0f%% of token limit (%s/%s)",
                    pct * 100,
                    projected,
                    cfg.max_tokens_per_session,
                )

        if cfg.max_cost_per_session_usd:
            projected_cost = self.session.total_cost_usd + est.total_cost_usd
            if projected_cost > cfg.max_cost_per_session_usd:
                raise BudgetExceededError(
                    f"Session would cost ${projected_cost:.4f}, limit is "
                    f"${cfg.max_cost_per_session_usd:.4f}",
                    est,
                )

        return est

    async def record_post_call(
        self,
        input_tokens: int,
        output_tokens: int,
        cached_tokens: int = 0,
        model: str = "claude-sonnet-4-6",
    ) -> None:
        """Record actual usage after a completed call."""
        from core.token_optimizer.counter import _resolve_prices
        prices = _resolve_prices(model)
        cost = (
            (input_tokens - cached_tokens) * prices.get("input", 0) / 1_000_000
            + cached_tokens * prices.get("cache_read", prices.get("input", 0)) / 1_000_000
            + output_tokens * prices.get("output", 0) / 1_000_000
        )
        await self.session.record(input_tokens, output_tokens, cached_tokens, cost)

    def reset_session(self) -> None:
        """Reset session counters (e.g. on new conversation)."""
        self.session = SessionUsage()

    def usage_dict(self) -> dict[str, Any]:
        return self.session.to_dict()


# ── Module-level default guard ──────────────────────────────────
_default_guard: BudgetGuard | None = None


def get_default_guard() -> BudgetGuard:
    global _default_guard
    if _default_guard is None:
        _default_guard = BudgetGuard()
    return _default_guard


def budget_check(
    max_tokens: int | None = None,
    max_cost_usd: float | None = None,
):
    """
    Decorator that checks token/cost budget before an async LLM call.

    Usage:
        @budget_check(max_tokens=50_000, max_cost_usd=0.20)
        async def my_llm_call(prompt: str) -> str:
            ...
    """
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            cfg = BudgetConfig(
                max_input_tokens_per_call=max_tokens,
                max_cost_per_call_usd=max_cost_usd,
            )
            guard = BudgetGuard(cfg)
            # Extract prompt from first str arg or 'prompt' kwarg
            text = kwargs.get("prompt") or kwargs.get("messages") or (args[0] if args else "")
            if isinstance(text, list):
                text = " ".join(m.get("content", "") if isinstance(m, dict) else str(m) for m in text)
            guard.check_pre_call(str(text))
            return await fn(*args, **kwargs)
        return wrapper
    return decorator
