"""Guardrails — input + output sanitization.

Catches the obvious failure modes called out in section 114 / 115:

* Prompt-injection markers in untrusted text.
* Secrets / API keys leaking through agent output.
* Unstructured output where structured output is required.

Guardrails are pure functions. They return a ``GuardrailReport`` rather
than raising, so callers can choose to log, ask, or block.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from pydantic import ValidationError

from dealix.hermes.core.schemas import StructuredOutput


@dataclass(frozen=True)
class GuardrailViolation:
    kind: str
    detail: str
    severity: str = "medium"


@dataclass
class GuardrailReport:
    violations: list[GuardrailViolation] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.violations

    @property
    def max_severity(self) -> str:
        if not self.violations:
            return "none"
        order = {"low": 0, "medium": 1, "high": 2}
        return max(self.violations, key=lambda v: order.get(v.severity, 0)).severity


_INJECTION_PATTERNS = (
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.I),
    re.compile(r"disregard\s+(the\s+)?system\s+prompt", re.I),
    re.compile(r"reveal\s+(your|the)\s+system\s+prompt", re.I),
    re.compile(r"</?(system|assistant|sovereign)>", re.I),
    re.compile(r"jailbreak", re.I),
)

_SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"AIza[0-9A-Za-z\-_]{35}"),
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),
    re.compile(r"-----BEGIN (?:RSA|OPENSSH|EC|PGP) PRIVATE KEY-----"),
)


class Guardrails:
    """Stateless. Safe to share across the kernel."""

    def scan_input(self, text: str) -> GuardrailReport:
        report = GuardrailReport()
        for pat in _INJECTION_PATTERNS:
            if pat.search(text or ""):
                report.violations.append(
                    GuardrailViolation(
                        kind="prompt_injection",
                        detail=f"matched pattern: {pat.pattern}",
                        severity="high",
                    )
                )
                break
        return report

    def scan_output(self, text: str) -> GuardrailReport:
        report = GuardrailReport()
        for pat in _SECRET_PATTERNS:
            if pat.search(text or ""):
                report.violations.append(
                    GuardrailViolation(
                        kind="secret_leak",
                        detail=f"pattern: {pat.pattern}",
                        severity="high",
                    )
                )
        return report

    def validate_structured(self, payload: dict[str, Any]) -> GuardrailReport:
        report = GuardrailReport()
        try:
            StructuredOutput(**payload)
        except ValidationError as exc:
            report.violations.append(
                GuardrailViolation(
                    kind="unstructured_output",
                    detail=str(exc),
                    severity="medium",
                )
            )
        return report


__all__ = ["GuardrailReport", "GuardrailViolation", "Guardrails"]
