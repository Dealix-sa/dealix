"""
Claim guard.

Scans candidate public copy for unapproved claims and refuses to ship
text containing forbidden patterns.

Patterns are sourced from `dealix/registers/no_overclaim.yaml` and
covered by `tests/trust/test_no_overclaim.py`.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

REGISTER_PATH = Path(__file__).resolve().parent.parent / "registers" / "no_overclaim.yaml"

# Forbidden if not in the public_claims register. These are conservative
# defaults; the register adds project-specific patterns.
DEFAULT_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    r"\bguarantee[ds]?\b",
    r"\bbest[\s-]in[\s-]class\b",
    r"\bworld[\s-]?class\b",
    r"\b#1\b",
    r"\b(?:1000|10x|100x)\s*(?:roi|return)\b",
    r"\bunlimited\b",
    r"\b24/?7\s+support\b",
    r"\bcertified\s+by\b",
    r"\bpartner(?:ed)?\s+with\b",
    r"\baward[\s-]winning\b",
    r"\bproven\b",
)


@dataclass(frozen=True, slots=True)
class ClaimViolation:
    pattern: str
    matched: str
    context: str


class ClaimGuard:
    def __init__(self, forbidden: tuple[str, ...] | None = None) -> None:
        self._patterns = [re.compile(p, re.IGNORECASE) for p in (forbidden or DEFAULT_FORBIDDEN_PATTERNS)]

    @classmethod
    def from_register(cls, path: Path = REGISTER_PATH) -> "ClaimGuard":
        patterns: list[str] = list(DEFAULT_FORBIDDEN_PATTERNS)
        if path.exists():
            for raw in path.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if line.startswith("- ") and not line.startswith("- #"):
                    patterns.append(line[2:].strip().strip('"').strip("'"))
        return cls(tuple(patterns))

    def scan(self, text: str) -> list[ClaimViolation]:
        violations: list[ClaimViolation] = []
        for pattern in self._patterns:
            for match in pattern.finditer(text):
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 30)
                violations.append(ClaimViolation(
                    pattern=pattern.pattern,
                    matched=match.group(0),
                    context=text[start:end].replace("\n", " "),
                ))
        return violations

    def is_safe(self, text: str) -> bool:
        return not self.scan(text)
