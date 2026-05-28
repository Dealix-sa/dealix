"""Hermes agent wrappers — one executor per Claude Code sub-agent.

Each wrapper is a callable matching the orchestrator's Executor signature:
    (HermesTask, Route) -> dict[str, Any]

They do NOT call LLMs directly. They prepare a structured `prompt_envelope`
that the caller (or the higher-level founder workflow) feeds to the LLM
client. This keeps the orchestrator pure and lets tests cover dispatch
without network access.

The default `route_to_agent_executor` picks the right wrapper based on
Route.sub_agent.
"""

from __future__ import annotations

from typing import Any, Callable

from ..router import Route
from .content_executor import content_executor
from .delivery_executor import delivery_executor
from .engineer_executor import engineer_executor
from .pm_executor import pm_executor
from .sales_executor import sales_executor


Executor = Callable[..., dict[str, Any]]


_SUB_AGENT_TO_EXECUTOR: dict[str, Executor] = {
    "dealix-pm": pm_executor,
    "dealix-engineer": engineer_executor,
    "dealix-content": content_executor,
    "dealix-sales": sales_executor,
    "dealix-delivery": delivery_executor,
}


def route_to_agent_executor(task: Any, route: Route) -> dict[str, Any]:
    """Default top-level executor — dispatches to the matching sub-agent wrapper."""
    fn = _SUB_AGENT_TO_EXECUTOR.get(route.sub_agent)
    if fn is None:
        return {"ok": False, "kind": "no_executor", "error": f"unknown sub_agent: {route.sub_agent}"}
    return fn(task, route)


__all__ = [
    "route_to_agent_executor",
    "pm_executor",
    "engineer_executor",
    "content_executor",
    "sales_executor",
    "delivery_executor",
]
