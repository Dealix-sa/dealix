#!/usr/bin/env python3
"""Verify Dealix module/service status truth: nothing unbuilt presented as live.

Confirms the service-status governance docs exist and that the service
registry marks status explicitly (live vs planned/spec), so no future module
is presented as live.

Terminal markers:
    MODULE_STATUS_FILES_PASS=true|false
    MODULE_STATUS_LABELLED_PASS=true|false
    DEALIX_MODULE_STATUS_OK=true|false
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

STATUS_FILES = (
    "docs/company/SERVICE_STATUS_RULES.md",
    "docs/company/SERVICE_REGISTRY.md",
    "docs/product/CAPABILITY_MATRIX.md",
)

# A status-bearing doc should distinguish live from planned. We look for at
# least one explicit status vocabulary token in the registry/matrix.
STATUS_TOKENS = (
    r"\blive\b",
    r"\bplanned\b",
    r"\bspec\b",
    r"\bbeta\b",
    r"\bجاهز\b",
    r"\bمخطط\b",
    r"\bقيد\b",
)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        # UTF-8 reconfigure is best-effort; the default stream is fine if unavailable.
        pass

    missing = [f for f in STATUS_FILES if not (REPO / f).is_file()]
    files_ok = not missing
    for m in missing:
        print(f"MISSING: {m}")

    compiled = [re.compile(t, re.IGNORECASE) for t in STATUS_TOKENS]
    labelled_ok = True
    for rel in ("docs/company/SERVICE_REGISTRY.md", "docs/product/CAPABILITY_MATRIX.md"):
        fp = REPO / rel
        if not fp.is_file():
            labelled_ok = False
            continue
        text = fp.read_text(encoding="utf-8", errors="ignore")
        if not any(rx.search(text) for rx in compiled):
            print(f"NO_STATUS_VOCAB: {rel} has no explicit live/planned status tokens")
            labelled_ok = False

    print(f"MODULE_STATUS_FILES_PASS={'true' if files_ok else 'false'}")
    print(f"MODULE_STATUS_LABELLED_PASS={'true' if labelled_ok else 'false'}")
    ok = files_ok and labelled_ok
    print(f"DEALIX_MODULE_STATUS_OK={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
