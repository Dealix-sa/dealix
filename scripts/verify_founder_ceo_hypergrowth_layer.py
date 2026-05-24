#!/usr/bin/env python3
"""Aggregate founder + CEO + hypergrowth verifier."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

CHILDREN = (
    "verify_founder_management_system.py",
    "verify_hypergrowth_ceo_layer.py",
)


def _run(name: str) -> bool:
    proc = subprocess.run(  # noqa: S603
        [sys.executable, str(REPO / "scripts" / name)],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
    return proc.returncode == 0


def main() -> int:
    results = {name: _run(name) for name in CHILDREN}
    for name, ok in results.items():
        print(f"FOUNDER_CEO_CHILD_{name}={'true' if ok else 'false'}")
    overall = all(results.values())
    print(f"FOUNDER_CEO_HYPERGROWTH_LAYER_PASS={'true' if overall else 'false'}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
