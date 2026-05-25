"""Lightweight guardrails — runtime checks for individual tool calls."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


class GuardrailViolation(Exception):
    """Raised when a guardrail blocks an action."""


@dataclass(frozen=True)
class Guardrail:
    name: str
    predicate: Callable[[dict[str, Any]], bool]
    violation_message: str = "guardrail violated"

    def assert_safe(self, context: dict[str, Any]) -> None:
        if not self.predicate(context):
            raise GuardrailViolation(f"{self.name}: {self.violation_message}")


def no_external_send_without_approval(ctx: dict[str, Any]) -> bool:
    if not ctx.get("external"):
        return True
    return bool(ctx.get("approval_id"))


def no_unregistered_tool(ctx: dict[str, Any]) -> bool:
    return bool(ctx.get("tool_registered"))


def no_silent_failure(ctx: dict[str, Any]) -> bool:
    return bool(ctx.get("audit_written"))


DEFAULT_GUARDRAILS: tuple[Guardrail, ...] = (
    Guardrail(
        name="no_external_send_without_approval",
        predicate=no_external_send_without_approval,
        violation_message="external action attempted without approval_id",
    ),
    Guardrail(
        name="no_unregistered_tool",
        predicate=no_unregistered_tool,
        violation_message="tool is not in the tool registry",
    ),
    Guardrail(
        name="no_silent_failure",
        predicate=no_silent_failure,
        violation_message="action completed without writing audit",
    ),
)
