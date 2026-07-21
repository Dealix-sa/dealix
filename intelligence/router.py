"""
Dealix Intelligence Router

Routes cognitive tasks to the right model + strategy based on:
- Task type (reasoning, generation, extraction, classification)
- Latency requirement
- Cost budget
- Required output quality
- Data sensitivity (Saudi PII/PDPL)

This is the central brain of the Dealix AI layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class TaskType(str, Enum):
    REASONING = "reasoning"           # complex multi-step decisions
    GENERATION = "generation"         # outreach, copy, documents
    EXTRACTION = "extraction"         # structured data from text
    CLASSIFICATION = "classification" # scoring, routing, tagging
    SUMMARIZATION = "summarization"   # briefs, reports
    CODE = "code"                     # code generation/review
    VISION = "vision"                 # image understanding


class Urgency(str, Enum):
    REALTIME = "realtime"             # < 500ms
    FAST = "fast"                     # < 2s
    NORMAL = "normal"                 # < 10s
    BATCH = "batch"                   # no hard limit


@dataclass(frozen=True)
class RoutingDecision:
    provider: str
    model: str
    strategy: str
    reason: str
    estimated_cost_usd: float
    max_latency_ms: int
    force_json: bool
    temperature: float


class IntelligenceRouter:
    """Routes tasks to optimal model + execution strategy."""

    # Cost per 1M tokens (input/output) — updated periodically
    COST_TABLE: dict[str, tuple[float, float]] = {
        "openai/gpt-4o": (5.00, 15.00),
        "openai/gpt-4o-mini": (0.15, 0.60),
        "anthropic/claude-3-5-sonnet": (3.00, 15.00),
        "anthropic/claude-3-haiku": (0.25, 1.25),
        "google/gemini-1.5-pro": (3.50, 10.50),
        "google/gemini-1.5-flash": (0.35, 0.70),
    }

    LATENCY_TABLE: dict[str, int] = {
        "openai/gpt-4o": 2000,
        "openai/gpt-4o-mini": 500,
        "anthropic/claude-3-5-sonnet": 2500,
        "anthropic/claude-3-haiku": 700,
        "google/gemini-1.5-pro": 2200,
        "google/gemini-1.5-flash": 600,
    }

    def __init__(self):
        self._call_log: list[dict[str, Any]] = []

    def route(
        self,
        task_type: TaskType,
        urgency: Urgency = Urgency.NORMAL,
        budget_usd: float | None = None,
        requires_saudi_context: bool = False,
        requires_json: bool = False,
        input_tokens_estimate: int = 1000,
        output_tokens_estimate: int = 500,
    ) -> RoutingDecision:
        """Select the best model for a task."""

        # PDPL-sensitive data prefers providers with strong enterprise commitments
        if requires_saudi_context and urgency in (Urgency.REALTIME, Urgency.FAST):
            return self._decide(
                "anthropic", "claude-3-haiku", "fast_saudi",
                "Low-latency Saudi-context task with PDPL awareness", input_tokens_estimate, output_tokens_estimate,
                requires_json, 0.2,
            )

        if task_type == TaskType.REASONING and urgency != Urgency.REALTIME:
            return self._decide(
                "anthropic", "claude-3-5-sonnet", "deep_reasoning",
                "Complex reasoning with high accuracy requirement", input_tokens_estimate, output_tokens_estimate,
                requires_json, 0.3,
            )

        if task_type == TaskType.GENERATION and urgency == Urgency.BATCH:
            return self._decide(
                "openai", "gpt-4o", "quality_generation",
                "High-quality Arabic/English bilingual generation", input_tokens_estimate, output_tokens_estimate,
                requires_json, 0.6,
            )

        if task_type == TaskType.CODE:
            return self._decide(
                "openai", "gpt-4o", "code",
                "Code generation and review", input_tokens_estimate, output_tokens_estimate,
                requires_json, 0.2,
            )

        if urgency == Urgency.REALTIME:
            return self._decide(
                "openai", "gpt-4o-mini", "ultra_fast",
                "Minimum latency for real-time UI", input_tokens_estimate, output_tokens_estimate,
                requires_json, 0.1,
            )

        # Default: cost-effective quality
        return self._decide(
            "google", "gemini-1.5-flash", "balanced",
            "Balanced cost/quality for general tasks", input_tokens_estimate, output_tokens_estimate,
            requires_json, 0.25,
        )

    def _decide(
        self,
        provider: str,
        model: str,
        strategy: str,
        reason: str,
        input_tokens: int,
        output_tokens: int,
        force_json: bool,
        temperature: float,
    ) -> RoutingDecision:
        key = f"{provider}/{model}"
        in_cost, out_cost = self.COST_TABLE.get(key, (1.0, 3.0))
        est_cost = (input_tokens / 1_000_000 * in_cost) + (output_tokens / 1_000_000 * out_cost)
        latency = self.LATENCY_TABLE.get(key, 1500)

        decision = RoutingDecision(
            provider=provider,
            model=model,
            strategy=strategy,
            reason=reason,
            estimated_cost_usd=round(est_cost, 6),
            max_latency_ms=latency,
            force_json=force_json,
            temperature=temperature,
        )
        self._call_log.append({
            "decision": decision,
            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
        })
        return decision

    def report(self) -> dict[str, Any]:
        return {
            "total_routes": len(self._call_log),
            "last_10_routes": self._call_log[-10:],
        }
