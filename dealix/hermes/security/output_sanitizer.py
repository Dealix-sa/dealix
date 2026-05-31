"""
Output sanitization — strips dangerous content from model outputs before
they reach a downstream channel (UI, partner, customer).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_DANGEROUS_OUTPUT_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"<\s*script[^>]*>", re.IGNORECASE), "html_script"),
    (re.compile(r"javascript:", re.IGNORECASE), "javascript_uri"),
    (re.compile(r"data:text/html", re.IGNORECASE), "data_uri_html"),
    (re.compile(r"on\w+\s*=\s*\"[^\"]*\"", re.IGNORECASE), "html_event_handler"),
)

_PII_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    # Generic credit-card-like sequence (PCI surface — never emit)
    (re.compile(r"\b(?:\d[ -]?){13,16}\b"), "possible_pan"),
    # Saudi national ID (10 digits starting with 1 or 2)
    (re.compile(r"\b[12]\d{9}\b"), "possible_saudi_id"),
    # IBAN-ish: SA + 22 digits
    (re.compile(r"\bSA\d{22}\b"), "possible_iban"),
    # Email — flagged but not necessarily blocked
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "email"),
)


@dataclass
class OutputSanitization:
    safe: bool
    sanitized_text: str
    findings: list[str]


def sanitize_output(text: str, *, redact_pii: bool = True) -> OutputSanitization:
    if not text:
        return OutputSanitization(True, "", [])
    out = text
    findings: list[str] = []
    for pattern, label in _DANGEROUS_OUTPUT_PATTERNS:
        if pattern.search(out):
            findings.append(label)
            out = pattern.sub("[REMOVED]", out)
    if redact_pii:
        for pattern, label in _PII_PATTERNS:
            if pattern.search(out):
                findings.append(f"pii:{label}")
                if label != "email":
                    out = pattern.sub("[REDACTED]", out)
    return OutputSanitization(
        safe="html_script" not in findings
        and "javascript_uri" not in findings
        and not any(f.startswith("pii:possible") for f in findings),
        sanitized_text=out,
        findings=findings,
    )
