"""Strip instruction-like content from messages originating from low-trust sources."""

from __future__ import annotations

import re
from dataclasses import dataclass

_INSTRUCTION_PATTERNS = [
    re.compile(r"(?i)\bignore (all )?previous instructions\b"),
    re.compile(r"(?i)\bdisregard (the )?system prompt\b"),
    re.compile(r"(?i)\byou are now\b"),
    re.compile(r"(?i)\boverride (the )?policy\b"),
    re.compile(r"(?i)\bact as (an? )?\w+"),
]


@dataclass(frozen=True)
class SanitizedMessage:
    text: str
    removed_patterns: tuple[str, ...]
    safe: bool


def sanitize(text: str, *, source_trust: str = "unknown") -> SanitizedMessage:
    """Strip instruction-style fragments from text when source_trust is not system-grade."""
    if source_trust == "system":
        return SanitizedMessage(text=text, removed_patterns=(), safe=True)

    removed: list[str] = []
    cleaned = text
    for pattern in _INSTRUCTION_PATTERNS:
        matches = pattern.findall(cleaned)
        if matches:
            removed.append(pattern.pattern)
            cleaned = pattern.sub("[redacted]", cleaned)
    return SanitizedMessage(text=cleaned, removed_patterns=tuple(removed), safe=not removed)
