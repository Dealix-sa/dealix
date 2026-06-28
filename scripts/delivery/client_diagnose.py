#!/usr/bin/env python3
"""Client diagnosis — verify the diagnosis phase is complete enough to design against.

Usage:
    python scripts/delivery/client_diagnose.py --client-slug acme
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLIENTS_DIR = REPO_ROOT / "clients"

DIAGNOSIS_FILES = [
    "current_state.md",
    "pain_map.md",
    "bottlenecks.md",
    "opportunity_map.md",
    "risk_register.md",
]


def diagnose(slug: str) -> dict[str, object]:
    """Return a diagnosis report for the client workspace.

    The report lists missing files and a boolean `complete` flag.
    Diagnosis is considered complete only when every expected file exists
    and is non-empty beyond the template scaffolding (heuristic: >200 bytes).
    """
    ws = CLIENTS_DIR / slug
    if not ws.exists():
        raise FileNotFoundError(f"client workspace not found: {ws}")

    phase_dir = ws / "01_diagnosis"
    missing: list[str] = []
    empty: list[str] = []
    for name in DIAGNOSIS_FILES:
        f = phase_dir / name
        if not f.exists():
            missing.append(name)
        elif f.stat().st_size < 200:
            empty.append(name)

    complete = not missing and not empty
    return {
        "client": slug,
        "complete": complete,
        "missing": missing,
        "empty": empty,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify client diagnosis completeness.")
    parser.add_argument("--client-slug", required=True)
    args = parser.parse_args()

    try:
        report = diagnose(args.client_slug)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"client: {report['client']}")
    print(f"diagnosis complete: {report['complete']}")
    if report["missing"]:
        print(f"missing files: {', '.join(report['missing'])}")
    if report["empty"]:
        print(f"empty files: {', '.join(report['empty'])}")
    return 0 if report["complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
