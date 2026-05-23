"""
Claim Guard — block unsubstantiated claims before they reach external surfaces.

This module enforces the `docs/trust/NO_OVERCLAIM_POLICY.md` and
`docs/trust/CLAIMS_GUIDE.md` rules:

* banned phrases that signal hype or unsubstantiated claims
* unbacked numerical claims (percentages / multipliers without source)
* compliance words that require explicit evidence
* generic-superlative patterns

The guard returns a structured report. Callers decide whether to block,
warn, or rewrite. By convention any A3 publish path treats any blocking
flag as a hard stop.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import StrEnum


class FlagSeverity(StrEnum):
    BLOCK = "block"
    WARN = "warn"


@dataclass(frozen=True)
class ClaimFlag:
    severity: FlagSeverity
    rule: str
    excerpt: str
    suggestion: str = ""


@dataclass
class ClaimGuardReport:
    text: str
    flags: list[ClaimFlag] = field(default_factory=list)

    @property
    def is_blocking(self) -> bool:
        return any(f.severity == FlagSeverity.BLOCK for f in self.flags)

    @property
    def block_count(self) -> int:
        return sum(1 for f in self.flags if f.severity == FlagSeverity.BLOCK)

    @property
    def warn_count(self) -> int:
        return sum(1 for f in self.flags if f.severity == FlagSeverity.WARN)


# Banned phrases — always block.
# Surround patterns with word boundaries to avoid false positives.
_BANNED_PHRASES: list[tuple[str, str]] = [
    (r"\bindustry[- ]leading\b", "Use specific evidence instead of 'industry-leading'."),
    (r"\bbest[- ]in[- ]class\b", "Use specific evidence instead of 'best-in-class'."),
    (r"\brevolutionary\b", "Avoid 'revolutionary'; describe what specifically is new."),
    (r"\btransformational\b", "Avoid 'transformational'; describe the change in concrete terms."),
    (r"\bsynergy\b", "Avoid 'synergy'; describe the specific interaction."),
    (r"\bset and forget\b", "Avoid; specify the level of human oversight."),
    (r"\bguarantee(?:d|s)?\b(?!\s*(by|under|per)\s+(contract|sla))",
     "Use 'guarantee' only when contractually enforceable; otherwise rewrite."),
    (r"\bevangelize\b", "Avoid corporate-speak; describe the action instead."),
    (r"\bideate\b", "Use plain English."),
    # Only flag 'leverage' when used as a verb (-s, -d, -ing). Noun usage
    # ("founder leverage", "highest-leverage action") is acceptable and is
    # actively part of the Company OS vocabulary.
    (r"\bleverag(?:es|ed|ing)\b", "Avoid 'leverage' as a verb; use 'use'."),
]

# Multiplier-style numbers without citation context — block (these are signature overclaim patterns).
_UNBACKED_MULTIPLIER = re.compile(
    r"\b(?P<num>\d{1,4})x\b", re.IGNORECASE
)

# Percent claims need a citation cue nearby; warn if isolated.
_PERCENT_CLAIM = re.compile(r"\b\d{1,3}(?:\.\d+)?\s*%")

# Compliance words requiring explicit evidence linkage.
_COMPLIANCE_WORDS = re.compile(
    r"\b(PDPL|SDAIA|ZATCA|GDPR|SOC\s*2|HIPAA|ISO\s*\d+)\b\s*[- ]?\s*compliant\b",
    re.IGNORECASE,
)

# Citation cues — presence of these in the same text neutralizes percent/multiplier warnings.
_CITATION_CUES = re.compile(
    r"(source:|sources?:|per\s+|see\s+|aligned\s+with|n\s*=\s*\d+|"
    r"\[evidence|in our last|based on|typical range|range\s*\d|client[- ]reported)",
    re.IGNORECASE,
)


def _has_citation(text: str) -> bool:
    return bool(_CITATION_CUES.search(text))


def check(text: str) -> ClaimGuardReport:
    """Run all claim_guard rules on `text` and return a report.

    The report is structured: callers decide whether `is_blocking` triggers
    a hard refuse (default for A3 publish) or a soft warning.
    """
    report = ClaimGuardReport(text=text)

    for pattern, suggestion in _BANNED_PHRASES:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            report.flags.append(
                ClaimFlag(
                    severity=FlagSeverity.BLOCK,
                    rule="banned_phrase",
                    excerpt=m.group(0),
                    suggestion=suggestion,
                )
            )

    if not _has_citation(text):
        for m in _UNBACKED_MULTIPLIER.finditer(text):
            num = int(m.group("num"))
            if num >= 2:
                report.flags.append(
                    ClaimFlag(
                        severity=FlagSeverity.BLOCK,
                        rule="unbacked_multiplier",
                        excerpt=m.group(0),
                        suggestion="Add a source or qualifier (e.g., 'based on n=X engagements').",
                    )
                )
        for m in _PERCENT_CLAIM.finditer(text):
            report.flags.append(
                ClaimFlag(
                    severity=FlagSeverity.WARN,
                    rule="unbacked_percent",
                    excerpt=m.group(0),
                    suggestion="Add a source or label as client-reported.",
                )
            )

    for m in _COMPLIANCE_WORDS.finditer(text):
        report.flags.append(
            ClaimFlag(
                severity=FlagSeverity.BLOCK,
                rule="compliance_overclaim",
                excerpt=m.group(0),
                suggestion="Use 'aligned with' + specific clause instead of 'compliant'.",
            )
        )

    return report


def assert_passes(text: str) -> None:
    """Raise ValueError if the text would be blocked by claim_guard."""
    report = check(text)
    if report.is_blocking:
        details = "; ".join(
            f"{f.rule}:{f.excerpt}" for f in report.flags if f.severity == FlagSeverity.BLOCK
        )
        raise ValueError(f"claim_guard would block: {details}")


__all__ = [
    "ClaimFlag",
    "ClaimGuardReport",
    "FlagSeverity",
    "assert_passes",
    "check",
]
