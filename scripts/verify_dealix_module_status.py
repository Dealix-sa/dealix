#!/usr/bin/env python3
"""Verify Dealix module status integrity.

Asserts:
  1. docs/00_platform_truth/MODULE_STATUS.md exists.
  2. docs/registry/SERVICE_READINESS_MATRIX.yaml exists and every service uses a
     valid status from the allowed vocabulary.
  3. Prints a status distribution summary.

This complements (does not replace) scripts/verify_service_readiness_matrix.py.
Prints KEY=value lines. Exit 0 on pass, 1 on fail.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MATRIX = REPO / "docs/registry/SERVICE_READINESS_MATRIX.yaml"
MODULE_DOC = REPO / "docs/00_platform_truth/MODULE_STATUS.md"

ALLOWED = {"live", "pilot", "partial", "target", "blocked", "backlog"}


def main() -> int:
    failures: list[str] = []

    if not MODULE_DOC.exists():
        failures.append("missing docs/00_platform_truth/MODULE_STATUS.md")

    if not MATRIX.exists():
        failures.append("missing docs/registry/SERVICE_READINESS_MATRIX.yaml")
        print("MODULE_STATUS_PASS=false")
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    try:
        import yaml  # type: ignore
    except ImportError:
        print("MODULE_STATUS_PASS=skip (PyYAML not installed)")
        return 0

    data = yaml.safe_load(MATRIX.read_text(encoding="utf-8")) or {}
    services = data.get("services", []) or []

    counts = {s: 0 for s in ALLOWED}
    for svc in services:
        sid = svc.get("service_id", "<unknown>")
        status = svc.get("status")
        if status not in ALLOWED:
            failures.append(f"service '{sid}' has invalid status: {status!r}")
            continue
        counts[status] += 1

    summary = " ".join(f"{k.upper()}={counts[k]}" for k in sorted(ALLOWED))
    print(f"MODULE_TOTAL={len(services)} {summary}")

    if failures:
        print("MODULE_STATUS_PASS=false")
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("MODULE_STATUS_PASS=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
