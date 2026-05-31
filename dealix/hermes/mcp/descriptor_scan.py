"""
Tool descriptor scan — looks for hidden instructions in descriptions
("tool shadowing" attacks).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_HIDDEN_INSTRUCTION_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"(?i)ignore\s+previous"), "hidden_override"),
    (re.compile(r"(?i)you\s+must\s+(also\s+)?call"), "hidden_chain_call"),
    (re.compile(r"(?i)secretly"), "hidden_secret_keyword"),
    (re.compile(r"(?i)do\s+not\s+tell\s+the\s+user"), "hidden_concealment"),
    (re.compile(r"<\s*system[^>]*>", re.IGNORECASE), "hidden_system_tag"),
    (re.compile(r"​|‌|‍|⁠"), "invisible_unicode"),
)


@dataclass
class DescriptorScan:
    ok: bool
    findings: list[str]


def scan_descriptor(descriptor: str) -> DescriptorScan:
    if not descriptor:
        return DescriptorScan(True, [])
    findings: list[str] = []
    for pattern, label in _HIDDEN_INSTRUCTION_PATTERNS:
        if pattern.search(descriptor):
            findings.append(label)
    return DescriptorScan(ok=not findings, findings=findings)
