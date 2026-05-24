#!/usr/bin/env python3
"""Verify Dealix marketing-system docs (copywriting rules, message library) exist."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = (
    "docs/marketing",
    "policies/dealix_control_policy.yaml",
    "auto_client_acquisition/governance_os/draft_gate.py",
    "dealix/registers/no_overclaim.yaml",
)


def _exists(p: Path) -> bool:
    return p.is_file() or p.is_dir()


def main() -> int:
    missing = [p for p in REQUIRED if not _exists(REPO / p)]
    for m in missing:
        print(f"missing_marketing_path:{m}", file=sys.stderr)
    ok = not missing
    print(f"MARKETING_SYSTEM_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
