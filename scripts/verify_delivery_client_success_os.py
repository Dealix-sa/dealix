#!/usr/bin/env python3
"""Verify the Delivery & Client Success OS artifacts are in place."""
from __future__ import annotations

import sys
from pathlib import Path


REQUIRED = [
    "docs/client_success/DELIVERY_CLIENT_SUCCESS_OS.md",
    "docs/delivery/KICKOFF_PROTOCOL.md",
    "docs/delivery/LEAD_TABLE_STANDARD.md",
    "docs/delivery/DELIVERY_QA_SCORE.md",
    "docs/delivery/HANDOFF_PROTOCOL.md",
    "docs/client_success/FEEDBACK_RETENTION_SYSTEM.md",
    "docs/client_success/CLIENT_HEALTH_SCORE_V2.md",
    "docs/content/PROOF_APPROVAL_SYSTEM.md",
]


def main() -> int:
    failures: list[str] = []
    for rel in REQUIRED:
        p = Path(rel)
        if not p.exists():
            failures.append(f"Missing: {rel}")
        elif p.stat().st_size < 30:
            failures.append(f"Too short: {rel}")
    if failures:
        print("Delivery & Client Success OS verification FAILED:")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: Delivery & Client Success OS is in place.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
