#!/usr/bin/env python3
"""Verify execution-launch layer: launch workflows + daily-revenue machinery."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = (
    ".github/workflows/daily-revenue-machine.yml",
    ".github/workflows/official-launch-verify.yml",
    ".github/workflows/governed-full-ops-daily.yml",
    ".github/workflows/founder_strongest_ops_daily.yml",
    "scripts/post_redeploy_verify.sh",
)


def main() -> int:
    missing = [p for p in REQUIRED if not (REPO / p).is_file()]
    for m in missing:
        print(f"missing_execution_artifact:{m}", file=sys.stderr)
    ok = not missing
    print(f"EXECUTION_LAUNCH_LAYER_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
