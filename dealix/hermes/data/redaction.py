"""
Redaction — strip or mask fields before they leave the data plane.
"""

from __future__ import annotations

import re
from typing import Any

from dealix.hermes.data.classification import DataClassification, classify_field


_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE_RE = re.compile(r"\+?\d[\d \-]{6,}\d")


def _mask_email(s: str) -> str:
    def repl(m: re.Match[str]) -> str:
        local, _, domain = m.group(0).partition("@")
        return f"{local[:2]}***@{domain}"

    return _EMAIL_RE.sub(repl, s)


def _mask_phone(s: str) -> str:
    return _PHONE_RE.sub(lambda m: m.group(0)[:3] + "***" + m.group(0)[-2:], s)


def redact(
    record: dict[str, Any],
    *,
    drop_above: DataClassification = DataClassification.CONFIDENTIAL,
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    levels = list(DataClassification)
    drop_idx = levels.index(drop_above)
    for key, value in record.items():
        cls = classify_field(key)
        if levels.index(cls) > drop_idx:
            continue
        if isinstance(value, str):
            value = _mask_email(_mask_phone(value))
        out[key] = value
    return out
