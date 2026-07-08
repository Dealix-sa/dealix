"""Model router strategy (advisory, no live calls).

This module documents *how* the engine would route a drafting task to a model,
without making any network call, reading any secret, or exposing any endpoint.
The daily runner works fully offline; model routing is a plan, not a live client.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelRoute:
    task: str
    tier: str
    provider_hint: str
    rationale: str


# Routing policy. No URLs, no keys. A real client would read config/secrets at
# call time from a private, authenticated worker — never from this repo.
ROUTES = (
    ModelRoute(
        task="short_internal_classification",
        tier="local_small",
        provider_hint="ollama-local (private, testing/simple tasks)",
        rationale="Cheap, private, no external dependency for low-stakes tasks.",
    ),
    ModelRoute(
        task="outreach_draft",
        tier="hosted_quality",
        provider_hint="provider-with-auth (draft-only; human approves before send)",
        rationale="Quality matters for customer-facing copy; still draft-only.",
    ),
    ModelRoute(
        task="long_market_report",
        tier="hosted_quality",
        provider_hint="provider-with-auth or vLLM GPU worker (private network)",
        rationale="Long context; run on a private worker, never public.",
    ),
)


def route_for(task: str) -> ModelRoute:
    for route in ROUTES:
        if route.task == task:
            return route
    return ROUTES[0]


def routing_safety_notes() -> list[str]:
    return [
        "No large LLM runs inside the Railway production API.",
        "AI worker is separate, private-network only, authenticated, rate-limited.",
        "No model provider keys are committed or printed.",
        "No public Ollama/vLLM endpoint without auth + firewall + rate limits.",
    ]
