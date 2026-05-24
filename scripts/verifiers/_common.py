"""Shared helpers for Dealix layer verifiers.

Every verifier:
  * imports this module
  * uses `report(name, passed)` to print exactly `<Name>: PASS|FAIL`
  * exits with `sys.exit(0 if passed else 1)`
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]


def report(layer_name: str, passed: bool, reasons: Iterable[str] = ()) -> None:
    """Emit verifier output and exit with appropriate code."""
    for reason in reasons:
        print(f"  - {reason}")
    print(f"{layer_name}: {'PASS' if passed else 'FAIL'}")
    sys.exit(0 if passed else 1)


def must_exist(*relpaths: str) -> list[str]:
    """Return a list of failure reasons for missing relpaths."""
    missing: list[str] = []
    for rel in relpaths:
        if not (REPO_ROOT / rel).exists():
            missing.append(f"missing: {rel}")
    return missing


def file_contains(relpath: str, *needles: str) -> list[str]:
    """Return failure reasons for needles missing from a file (case-insensitive)."""
    p = REPO_ROOT / relpath
    if not p.exists():
        return [f"missing: {relpath}"]
    try:
        text = p.read_text(encoding="utf-8", errors="replace").lower()
    except Exception as exc:  # noqa: BLE001
        return [f"unreadable {relpath}: {exc!s}"]
    return [f"{relpath} missing token {n!r}" for n in needles if n.lower() not in text]
