"""
Token counter and cost estimator for Dealix LLM calls.
عدّاد التوكنز ومحسب التكلفة لنداءات النموذج اللغوي.

Uses tiktoken for OpenAI-compatible tokenization.
Falls back to char/4 heuristic for non-OpenAI models.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

# Cost per million tokens (USD) — updated 2026-05
# Source: official pricing pages
COST_TABLE: dict[str, dict[str, float]] = {
    # Anthropic
    "claude-opus-4-8":          {"input": 15.0,  "output": 75.0,  "cache_write": 18.75, "cache_read": 1.5},
    "claude-sonnet-4-6":        {"input": 3.0,   "output": 15.0,  "cache_write": 3.75,  "cache_read": 0.3},
    "claude-haiku-4-5":         {"input": 0.8,   "output": 4.0,   "cache_write": 1.0,   "cache_read": 0.08},
    "claude-sonnet-4-5-20250929": {"input": 3.0, "output": 15.0,  "cache_write": 3.75,  "cache_read": 0.3},
    # OpenAI
    "gpt-4o":                   {"input": 2.5,   "output": 10.0},
    "gpt-4o-mini":              {"input": 0.15,  "output": 0.6},
    "gpt-4-turbo":              {"input": 10.0,  "output": 30.0},
    # DeepSeek
    "deepseek-chat":            {"input": 0.14,  "output": 0.28},
    "deepseek-reasoner":        {"input": 0.55,  "output": 2.19},
    # Groq (Llama)
    "llama-3.3-70b-versatile":  {"input": 0.59,  "output": 0.79},
    "llama-3.1-8b-instant":     {"input": 0.05,  "output": 0.08},
    # GLM
    "glm-4":                    {"input": 0.14,  "output": 0.14},
    # Gemini
    "gemini-1.5-pro":           {"input": 1.25,  "output": 5.0},
    "gemini-1.5-flash":         {"input": 0.075, "output": 0.3},
}

# Canonical tiktoken encoding per model family
_ENCODING_ALIASES: dict[str, str] = {
    "gpt-4o": "o200k_base",
    "gpt-4": "cl100k_base",
    "gpt-3.5": "cl100k_base",
    "default": "cl100k_base",
}


def _get_encoding(model: str):
    """Return tiktoken encoding for model, or None if tiktoken not installed."""
    try:
        import tiktoken  # type: ignore
        try:
            return tiktoken.encoding_for_model(model)
        except KeyError:
            alias = next(
                (enc for key, enc in _ENCODING_ALIASES.items() if key in model),
                _ENCODING_ALIASES["default"],
            )
            return tiktoken.get_encoding(alias)
    except ImportError:
        return None


def count_tokens(text: str, model: str = "claude-sonnet-4-6") -> int:
    """
    Count tokens in text for a given model.
    Falls back to len(text) // 4 if tiktoken unavailable.
    """
    enc = _get_encoding(model)
    if enc is not None:
        return len(enc.encode(text))
    return max(1, len(text) // 4)


def count_messages_tokens(
    messages: list[dict[str, str]],
    model: str = "claude-sonnet-4-6",
    system: str | None = None,
) -> int:
    """Count total tokens across a messages list + optional system prompt."""
    total = 0
    if system:
        total += count_tokens(system, model)
    for msg in messages:
        total += count_tokens(msg.get("content", ""), model)
        total += 4  # role overhead per message
    total += 2  # reply priming
    return total


@dataclass
class CostEstimate:
    """Token counts and cost estimate before sending a request."""
    input_tokens: int
    model: str
    estimated_output_tokens: int = 512
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    _prices: dict[str, float] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        self._prices = _resolve_prices(self.model)

    @property
    def input_cost_usd(self) -> float:
        p = self._prices
        read_cost = self.cache_read_tokens * p.get("cache_read", p.get("input", 0)) / 1_000_000
        write_cost = self.cache_write_tokens * p.get("cache_write", p.get("input", 0)) / 1_000_000
        regular = (self.input_tokens - self.cache_read_tokens - self.cache_write_tokens)
        regular_cost = max(0, regular) * p.get("input", 0) / 1_000_000
        return regular_cost + read_cost + write_cost

    @property
    def output_cost_usd(self) -> float:
        return self.estimated_output_tokens * self._prices.get("output", 0) / 1_000_000

    @property
    def total_cost_usd(self) -> float:
        return self.input_cost_usd + self.output_cost_usd

    def to_dict(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "input_tokens": self.input_tokens,
            "estimated_output_tokens": self.estimated_output_tokens,
            "cache_read_tokens": self.cache_read_tokens,
            "cache_write_tokens": self.cache_write_tokens,
            "input_cost_usd": round(self.input_cost_usd, 6),
            "output_cost_usd": round(self.output_cost_usd, 6),
            "total_cost_usd": round(self.total_cost_usd, 6),
        }


def _resolve_prices(model: str) -> dict[str, float]:
    """Find best-matching price entry for model name."""
    # Exact match first
    if model in COST_TABLE:
        return COST_TABLE[model]
    # Prefix match
    for key, prices in COST_TABLE.items():
        if model.startswith(key) or key in model:
            return prices
    logger.warning("No price table entry for model=%s — using $3/$15 default", model)
    return {"input": 3.0, "output": 15.0}


def estimate_cost(
    text_or_tokens: str | int,
    model: str = "claude-sonnet-4-6",
    estimated_output_tokens: int = 512,
    cache_read_tokens: int = 0,
) -> CostEstimate:
    """
    Estimate cost before sending a request.

    Usage:
        est = estimate_cost(system_prompt + user_msg, model="claude-sonnet-4-6")
        if est.total_cost_usd > 0.10:
            raise BudgetExceeded(...)
    """
    tokens = (
        text_or_tokens
        if isinstance(text_or_tokens, int)
        else count_tokens(text_or_tokens, model)
    )
    return CostEstimate(
        input_tokens=tokens,
        model=model,
        estimated_output_tokens=estimated_output_tokens,
        cache_read_tokens=cache_read_tokens,
    )


def token_summary(text: str, model: str = "claude-sonnet-4-6") -> dict[str, Any]:
    """Quick summary dict: tokens + cost for a text."""
    n = count_tokens(text, model)
    est = estimate_cost(n, model)
    return {
        "chars": len(text),
        "tokens": n,
        "chars_per_token": round(len(text) / n, 2) if n else 0,
        "cost_usd": round(est.total_cost_usd, 6),
        "model": model,
    }
