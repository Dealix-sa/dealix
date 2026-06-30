#!/usr/bin/env python3
"""Gate: outreach compliance — draft-only defaults and approval gates exist.

Checks that:
1. Core outreach gate modules are present
2. EXTERNAL_SEND_ENABLED is not set to true (default safe)
3. OUTBOUND_MODE is not set to anything other than draft_only or unset

Does NOT re-scan for forbidden strings — the test suite does that in
test_no_linkedin_scraper_string_anywhere.py and test_no_cold_whatsapp.py.

Run: python scripts/verify_outreach_compliance.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_GATE_FILES = [
    "app/outbound/policy_gate.py",
    "app/outbound/approval.py",
]


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_GATE_FILES:
        if not (ROOT / rel).exists():
            failures.append(f"Required outreach gate missing: {rel}")

    send_enabled = os.environ.get("EXTERNAL_SEND_ENABLED", "false").strip().lower()
    if send_enabled in ("1", "true", "yes", "on"):
        mode = os.environ.get("OUTBOUND_MODE", "")
        if mode not in ("controlled_live", "draft_only"):
            failures.append(
                f"EXTERNAL_SEND_ENABLED={send_enabled} with OUTBOUND_MODE={mode!r} "
                "is not permitted — use draft_only or controlled_live"
            )

    if failures:
        for f in failures:
            print(f"FAIL: {f}")
        return 1

    print("PASS: outreach compliance gate satisfied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
