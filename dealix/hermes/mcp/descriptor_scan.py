"""Tool descriptor scanner — catch poisoned descriptions and prompt injections."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_INJECTION_PHRASES = (
    "ignore previous", "ignore above", "system prompt:",
    "you are now", "disregard your", "exfiltrate", "send all", "leak",
    "<|system|>", "[SYSTEM]",
)

_SUSPICIOUS_KEYWORDS = ("password", "credentials", "secret", "private_key", "exec(", "os.system")


@dataclass(frozen=True)
class DescriptorScanResult:
    passed: bool
    findings: tuple[str, ...]


def scan_tool_descriptor(descriptor: dict[str, Any]) -> DescriptorScanResult:
    text_blob = " ".join(
        str(descriptor.get(field_name, ""))
        for field_name in ("name", "description", "parameters_schema", "examples")
    ).lower()
    findings: list[str] = []
    for phrase in _INJECTION_PHRASES:
        if phrase in text_blob:
            findings.append(f"injection phrase: '{phrase}'")
    for kw in _SUSPICIOUS_KEYWORDS:
        if kw in text_blob:
            findings.append(f"suspicious keyword: '{kw}'")
    return DescriptorScanResult(passed=not findings, findings=tuple(findings))
