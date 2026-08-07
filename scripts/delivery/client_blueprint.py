#!/usr/bin/env python3
"""Client blueprint — verify the solution/blueprint phase and that acceptance criteria are signed.

Usage:
    python scripts/delivery/client_blueprint.py --client-slug acme
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLIENTS_DIR = REPO_ROOT / "clients"

SOLUTION_FILES = [
    "system_blueprint.md",
    "workflow_map.md",
    "data_model.md",
    "ai_policy.md",
    "acceptance_criteria.md",
]

# Markers that the acceptance-criteria file has been signed.
SIGNED_MARKERS = ["[x] Sponsor signature", "[x] Dealix delivery lead signature"]


def blueprint_status(slug: str) -> dict[str, object]:
    """Return blueprint completeness and acceptance-criteria signature status."""
    ws = CLIENTS_DIR / slug
    if not ws.exists():
        raise FileNotFoundError(f"client workspace not found: {ws}")

    phase_dir = ws / "02_solution"
    missing: list[str] = []
    for name in SOLUTION_FILES:
        if not (phase_dir / name).exists():
            missing.append(name)

    ac_file = phase_dir / "acceptance_criteria.md"
    signed = False
    if ac_file.exists():
        text = ac_file.read_text(encoding="utf-8")
        signed = all(marker in text for marker in SIGNED_MARKERS)

    ready = not missing and signed
    return {
        "client": slug,
        "ready_to_build": ready,
        "missing": missing,
        "acceptance_criteria_signed": signed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify client blueprint and acceptance criteria.")
    parser.add_argument("--client-slug", required=True)
    args = parser.parse_args()

    try:
        report = blueprint_status(args.client_slug)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"client: {report['client']}")
    print(f"ready to build: {report['ready_to_build']}")
    print(f"acceptance criteria signed: {report['acceptance_criteria_signed']}")
    if report["missing"]:
        print(f"missing files: {', '.join(report['missing'])}")
    return 0 if report["ready_to_build"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
