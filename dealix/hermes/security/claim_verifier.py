"""
Claim verifier — refuses to ship marketing or proposal text that makes
unsupported claims (the "agent washing" risk).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Phrases that are absolute and therefore almost always unsupportable.
_FORBIDDEN_CLAIMS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"(?i)\bguarantee(d|s)?\b"), "absolute_guarantee"),
    (re.compile(r"(?i)\b100\s*%\s*(secure|compliant|safe|accurate)\b"), "absolute_100"),
    (re.compile(r"(?i)\bzero\s+risk\b"), "absolute_zero_risk"),
    (re.compile(r"(?i)\bfully\s+(automat\w+|replace\w+)\b"), "full_automation_overclaim"),
    (re.compile(r"(?i)\bcompliant\s+with\s+(all|every)\b"), "blanket_compliance"),
    (re.compile(r"(?i)\bworld[-\s]*class\b"), "vague_superlative"),
    (re.compile(r"(?i)\bbest[-\s]*in[-\s]*class\b"), "vague_superlative"),
)


@dataclass
class ClaimVerification:
    safe: bool
    findings: list[str]
    flagged_phrases: list[str]


def verify_claims(text: str) -> ClaimVerification:
    if not text:
        return ClaimVerification(True, [], [])
    findings: list[str] = []
    flagged: list[str] = []
    for pattern, label in _FORBIDDEN_CLAIMS:
        for match in pattern.finditer(text):
            findings.append(label)
            flagged.append(match.group(0))
    return ClaimVerification(safe=not findings, findings=findings, flagged_phrases=flagged)
