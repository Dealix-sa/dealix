#!/usr/bin/env python3
"""Verify Private Ops Runtime: bootstrap script + layout doc exist and the
runtime path is NEVER committed under the repo."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import REPO_ROOT, must_exist, report, file_contains  # noqa: E402

LAYER = "Private Ops Runtime"
RUNTIME_ROOT = Path("/opt/dealix-ops-private")


def main() -> None:
    reasons = must_exist(
        "scripts/bootstrap_private_ops_runtime.py",
        "docs/runtime/PRIVATE_OPS_LAYOUT.md",
    )
    reasons += file_contains(
        "docs/runtime/PRIVATE_OPS_LAYOUT.md",
        "/opt/dealix-ops-private",
        "never committed",
        "bootstrap_private_ops_runtime.py",
    )

    # Defensive: ensure no committed file pretends to live at the runtime path.
    leaked = list((REPO_ROOT).rglob("dealix-ops-private"))
    leaked = [p for p in leaked if "node_modules" not in p.parts]
    if leaked:
        reasons.append(f"runtime path leaked into repo: {leaked[0]}")

    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
