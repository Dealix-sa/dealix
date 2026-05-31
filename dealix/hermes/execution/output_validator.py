"""
Output Validator — يتحقق أن مخرج النموذج يطابق العقد البنيوي قبل ما يكمّل
لأي مرحلة (trust gate / approval / execute). يفصل التحقق البنيوي
(JSON shape / required fields) عن التحقق الدلالي (trust gate).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValidationReport:
    valid: bool
    issues: list[str] = field(default_factory=list)
    normalized: dict[str, Any] = field(default_factory=dict)


class OutputValidator:
    """Schema-light validator (no pydantic dep, runs in any context)."""

    def __init__(
        self,
        *,
        required_fields: list[str],
        max_text_chars: int = 8000,
    ) -> None:
        self._required = required_fields
        self._max_chars = max_text_chars

    def validate(self, output: dict[str, Any]) -> ValidationReport:
        report = ValidationReport(valid=True, normalized=dict(output))

        if not isinstance(output, dict):
            report.valid = False
            report.issues.append("output is not a dict")
            return report

        for field_name in self._required:
            if field_name not in output:
                report.valid = False
                report.issues.append(f"missing field `{field_name}`")

        text = output.get("text")
        if isinstance(text, str) and len(text) > self._max_chars:
            report.valid = False
            report.issues.append(
                f"text exceeds max chars ({len(text)} > {self._max_chars})"
            )
        return report


__all__ = ["OutputValidator", "ValidationReport"]
