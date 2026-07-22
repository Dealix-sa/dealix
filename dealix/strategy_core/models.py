"""Strict declarative strategy contracts for the canonical Company OS.

The package contains no orchestrator, scheduler, sender, or production mutation.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any, Iterable

_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]{1,63}$")


class ActionKind(StrEnum):
    OBSERVE = "observe"
    ANALYZE = "analyze"
    INTERNAL_DRAFT = "internal_draft"
    INTERNAL_WRITE = "internal_write"
    REPO_WRITE = "repo_write"
    EXTERNAL_DRAFT = "external_draft"
    EXTERNAL_ACTION = "external_action"
    MERGE = "merge"
    PUBLISH = "publish"
    PAYMENT = "payment"
    PRODUCTION = "production"


class Route(StrEnum):
    INTERNAL_EXECUTE = "internal_execute"
    APPROVAL = "approval"
    BLOCKED = "blocked"


def _strict_bool(value: Any, *, field_name: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().casefold()
        if lowered in {"true", "1", "yes", "on"}:
            return True
        if lowered in {"false", "0", "no", "off"}:
            return False
    raise TypeError(f"{field_name} must be a boolean")


def _string_tuple(value: Any, *, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str) or not isinstance(value, Iterable):
        raise TypeError(f"{field_name} must be a sequence of strings")
    items = tuple(value)
    if any(not isinstance(item, str) for item in items):
        raise TypeError(f"{field_name} must contain strings only")
    return tuple(item.strip() for item in items if item.strip())


@dataclass(frozen=True)
class StrategyStep:
    action: str
    kind: ActionKind = ActionKind.ANALYZE
    risk: float = 0.0
    channel: str | None = None
    requires_approval: bool = False
    output: str | None = None
    description: str = ""

    def __post_init__(self) -> None:
        action = self.action.strip().casefold()
        if not action:
            raise ValueError("step action is required")
        try:
            kind = self.kind if isinstance(self.kind, ActionKind) else ActionKind(str(self.kind).strip().casefold())
        except ValueError as exc:
            raise ValueError(f"unsupported strategy step kind: {self.kind}") from exc
        if isinstance(self.risk, bool) or not isinstance(self.risk, (int, float)):
            raise TypeError("step risk must be numeric")
        risk = float(self.risk)
        if not 0.0 <= risk <= 1.0:
            raise ValueError("step risk must be between 0 and 1")
        approval = _strict_bool(self.requires_approval, field_name="requires_approval")
        if self.channel is not None and not isinstance(self.channel, str):
            raise TypeError("channel must be a string or null")
        if self.output is not None and not isinstance(self.output, str):
            raise TypeError("output must be a string or null")
        object.__setattr__(self, "action", action)
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "risk", risk)
        object.__setattr__(self, "requires_approval", approval)
        object.__setattr__(self, "channel", self.channel.strip().casefold() if self.channel else None)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "StrategyStep":
        if not isinstance(payload, dict):
            raise TypeError("strategy step must be an object")
        return cls(
            action=str(payload.get("action") or ""),
            kind=str(payload.get("kind", ActionKind.ANALYZE.value)),
            risk=payload.get("risk", 0.0),
            channel=str(payload["channel"]) if payload.get("channel") else None,
            requires_approval=payload.get("requires_approval", False),
            output=str(payload["output"]) if payload.get("output") else None,
            description=str(payload.get("description") or ""),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["kind"] = self.kind.value
        return payload


@dataclass(frozen=True)
class StrategyDefinition:
    strategy_id: str
    name: str
    goal: str
    enabled: bool = True
    priority: int = 50
    guardrails: tuple[str, ...] = field(default_factory=tuple)
    kpis: tuple[str, ...] = field(default_factory=tuple)
    stop_conditions: tuple[str, ...] = field(default_factory=tuple)
    steps: tuple[StrategyStep, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        strategy_id = self.strategy_id.strip().casefold()
        if not _ID_PATTERN.fullmatch(strategy_id):
            raise ValueError("strategy_id must match [a-z0-9][a-z0-9_-]{1,63}")
        if not self.name.strip():
            raise ValueError("strategy name is required")
        if not self.goal.strip():
            raise ValueError("strategy goal is required")
        enabled = _strict_bool(self.enabled, field_name="enabled")
        if isinstance(self.priority, bool) or not isinstance(self.priority, int):
            raise TypeError("strategy priority must be an integer")
        if not 0 <= self.priority <= 100:
            raise ValueError("strategy priority must be between 0 and 100")
        steps = tuple(self.steps)
        if not steps:
            raise ValueError("strategy must contain at least one step")
        if any(not isinstance(step, StrategyStep) for step in steps):
            raise TypeError("steps must contain StrategyStep objects")
        object.__setattr__(self, "strategy_id", strategy_id)
        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(self, "goal", self.goal.strip())
        object.__setattr__(self, "enabled", enabled)
        object.__setattr__(self, "guardrails", _string_tuple(self.guardrails, field_name="guardrails"))
        object.__setattr__(self, "kpis", _string_tuple(self.kpis, field_name="kpis"))
        object.__setattr__(self, "stop_conditions", _string_tuple(self.stop_conditions, field_name="stop_conditions"))
        object.__setattr__(self, "steps", steps)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "StrategyDefinition":
        if not isinstance(payload, dict):
            raise TypeError("strategy must be an object")
        raw_priority = payload.get("priority", 50)
        if isinstance(raw_priority, bool):
            raise TypeError("strategy priority must be an integer")
        try:
            priority = int(raw_priority)
        except (TypeError, ValueError) as exc:
            raise TypeError("strategy priority must be an integer") from exc
        raw_steps = payload.get("steps")
        if not isinstance(raw_steps, list):
            raise TypeError("strategy steps must be a list")
        return cls(
            strategy_id=str(payload.get("id") or payload.get("strategy_id") or ""),
            name=str(payload.get("name") or ""),
            goal=str(payload.get("goal") or payload.get("objective_ar") or payload.get("objective_en") or ""),
            enabled=payload.get("enabled", True),
            priority=priority,
            guardrails=_string_tuple(payload.get("guardrails"), field_name="guardrails"),
            kpis=_string_tuple(payload.get("kpis"), field_name="kpis"),
            stop_conditions=_string_tuple(payload.get("stop_conditions"), field_name="stop_conditions"),
            steps=tuple(StrategyStep.from_dict(step) for step in raw_steps),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.strategy_id,
            "name": self.name,
            "goal": self.goal,
            "enabled": self.enabled,
            "priority": self.priority,
            "guardrails": list(self.guardrails),
            "kpis": list(self.kpis),
            "stop_conditions": list(self.stop_conditions),
            "steps": [step.to_dict() for step in self.steps],
        }


@dataclass(frozen=True)
class SafetyDecision:
    route: Route
    reason: str
    minimum_autonomy_level: int
    external_action_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["route"] = self.route.value
        return payload
