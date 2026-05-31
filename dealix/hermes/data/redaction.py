"""PII redaction — applied before any agent sees a context packet."""

from __future__ import annotations

import re

_PII_PATTERNS = [
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "[EMAIL]"),
    (re.compile(r"\+?\d[\d\s().-]{7,}\d"), "[PHONE]"),
    (re.compile(r"\b\d{10,}\b"), "[ID]"),
    (re.compile(r"SA\d{22}"), "[IBAN]"),  # Saudi IBAN
]


def redact_pii(text: str) -> str:
    redacted = text
    for pattern, placeholder in _PII_PATTERNS:
        redacted = pattern.sub(placeholder, redacted)
    return redacted
