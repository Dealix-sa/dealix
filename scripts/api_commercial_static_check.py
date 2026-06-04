#!/usr/bin/env python3
"""Static check for the commercial API surface contract (no server, no network).

The commercial/media-social API surface is documented as READ-ONLY. This check
verifies the QA doc exists and declares only GET endpoints, and that no
send/whatsapp/linkedin/smtp endpoint is declared. Read-only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QA_DOC = ROOT / "docs" / "ops" / "API_COMMERCIAL_LAUNCH_QA.md"

ALLOWED_READONLY = [
    "GET /api/v1/commercial/verticals",
    "GET /api/v1/commercial/offers",
    "GET /api/v1/commercial/readiness",
    "GET /api/v1/commercial/channel-policy",
    "GET /api/v1/commercial/metrics-schema",
    "GET /api/v1/media-social/calendar-schema",
]

FORBIDDEN = ["/send", "whatsapp", "smtp", "linkedin/post", "auto-submit", "POST /api/v1/commercial/send"]


def run() -> list[str]:
    errors: list[str] = []
    if not QA_DOC.exists():
        return [f"missing {QA_DOC.relative_to(ROOT)}"]
    text = QA_DOC.read_text(encoding="utf-8")
    low = text.lower()
    for ep in ALLOWED_READONLY:
        if ep not in text:
            errors.append(f"QA doc missing documented read-only endpoint: {ep}")
    for bad in FORBIDDEN:
        if bad.lower() in low and "forbidden" not in _context(low, bad.lower()):
            errors.append(f"QA doc references a forbidden send surface: {bad}")
    # Ensure no POST/PUT/DELETE mutation endpoint is declared as available.
    for m in re.finditer(r"\b(POST|PUT|DELETE|PATCH)\s+/api/v1/commercial/\S+", text):
        line = m.group(0)
        if "forbidden" not in _line_context(text, m.start()).lower():
            errors.append(f"QA doc declares mutating endpoint not marked forbidden: {line}")
    return errors


def _context(text: str, needle: str) -> str:
    i = text.find(needle)
    return text[max(0, i - 60): i + 60]


def _line_context(text: str, idx: int) -> str:
    start = text.rfind("\n", 0, idx)
    end = text.find("\n", idx)
    return text[start + 1: end if end != -1 else len(text)]


def main() -> int:
    errors = run()
    if not errors:
        print("API commercial static check PASS — read-only surface, no send endpoints.")
        return 0
    print("API commercial static check FAIL:")
    for e in errors:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
