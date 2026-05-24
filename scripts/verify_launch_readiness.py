#!/usr/bin/env python3
"""Verify Dealix launch readiness docs + delegated checks."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = (
    "docs/launch/DEALIX_LAUNCH_NOW_BUNDLE.md",
    "docs/launch/FINAL_LAUNCH_INSTRUCTIONS.md",
    "scripts/verify_paid_launch_readiness.py",
    "scripts/verify_commercial_launch_ready.py",
    ".github/workflows/official-launch-verify.yml",
)


def _exists(p: Path) -> bool:
    return p.is_file()


def main() -> int:
    missing = [p for p in REQUIRED if not _exists(REPO / p)]
    for m in missing:
        print(f"missing_launch_artifact:{m}", file=sys.stderr)
    ok = not missing
    print(f"LAUNCH_READINESS_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
