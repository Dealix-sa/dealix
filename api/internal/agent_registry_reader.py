"""Read registries/agent_registry.yaml for the control plane API."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

REGISTRY_PATH = (
    Path(__file__).resolve().parents[2] / "registries" / "agent_registry.yaml"
)


def _load_yaml() -> dict[str, Any] | None:
    if not REGISTRY_PATH.exists():
        return None
    try:
        import yaml  # type: ignore
    except ImportError:
        return None
    try:
        with REGISTRY_PATH.open("r", encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except OSError:
        return None


@lru_cache(maxsize=1)
def load_registry() -> dict[str, Any]:
    data = _load_yaml()
    if data is None:
        return {"version": 0, "agents": [], "source": "fallback"}
    data["source"] = "runtime"
    return data


# Mutable in-memory enable/disable state for the dev internal API.
# Production wiring should persist this to a database.
_AGENT_STATE: dict[str, dict[str, Any]] = {}


def agents() -> list[dict[str, Any]]:
    registry = load_registry()
    out: list[dict[str, Any]] = []
    for entry in registry.get("agents") or []:
        if not isinstance(entry, dict):
            continue
        merged = dict(entry)
        state = _AGENT_STATE.get(merged.get("id", ""), {})
        merged["enabled"] = state.get("enabled", True)
        merged["last_change_reason"] = state.get("reason")
        merged["last_changed_at"] = state.get("changed_at")
        out.append(merged)
    return out


def set_agent_enabled(agent_id: str, enabled: bool, reason: str | None) -> dict[str, Any]:
    from datetime import datetime, timezone

    found = any(a.get("id") == agent_id for a in load_registry().get("agents", []))
    if not found:
        raise KeyError(f"unknown agent: {agent_id}")
    _AGENT_STATE[agent_id] = {
        "enabled": enabled,
        "reason": reason or "",
        "changed_at": datetime.now(timezone.utc).isoformat(),
    }
    return _AGENT_STATE[agent_id]


def summary() -> dict[str, Any]:
    registry = load_registry()
    agents_list = registry.get("agents") or []
    return {
        "version": registry.get("version", 0),
        "agent_count": len(agents_list),
        "kill_switch_required": True,
        "eval_required": True,
        "source": registry.get("source", "fallback"),
    }
