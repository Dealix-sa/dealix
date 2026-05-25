"""Runtime guardrails — applied to every MCP call as it executes."""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.trust.guardrails import (
    DEFAULT_GUARDRAILS,
    Guardrail,
    GuardrailViolation,
)


@dataclass
class RuntimeGuardrails:
    rails: tuple[Guardrail, ...] = field(default_factory=lambda: DEFAULT_GUARDRAILS)

    def enforce(self, context: dict) -> list[str]:
        violations: list[str] = []
        for rail in self.rails:
            try:
                rail.assert_safe(context)
            except GuardrailViolation as exc:
                violations.append(str(exc))
        return violations
