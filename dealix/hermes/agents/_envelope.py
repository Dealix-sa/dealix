"""Shared prompt envelope helper used by all Hermes sub-agent executors."""

from __future__ import annotations

from typing import Any

from ..router import Route


def build_envelope(
    *,
    task: Any,
    route: Route,
    role: str,
    system_constraints: list[str],
    deliverable: str,
) -> dict[str, Any]:
    """Produce a deterministic envelope for downstream LLM clients.

    The envelope embeds:
      - the routed provider + model
      - the doctrine constraints relevant to this sub-agent
      - the intent text
      - the expected deliverable shape
    """
    intent = getattr(task, "intent", "")
    customer_id = getattr(task, "customer_id", "dealix_internal")
    metadata = getattr(task, "metadata", {}) or {}
    return {
        "ok": True,
        "kind": "prompt_envelope",
        "role": role,
        "sub_agent": route.sub_agent,
        "task_class": route.task_class.value,
        "provider": route.gear_config.provider,
        "model_id": route.gear_config.model_id,
        "gear": route.gear.value,
        "max_tokens": route.gear_config.max_tokens,
        "timeout": route.gear_config.timeout,
        "intent": intent,
        "customer_id": customer_id,
        "metadata": metadata,
        "system_constraints": system_constraints,
        "deliverable": deliverable,
    }
