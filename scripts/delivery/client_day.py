#!/usr/bin/env python3
"""Client day — run the daily operating routine for a client engagement.

Prints a one-page daily command summary pulling from the workspace state.

Usage:
    python scripts/delivery/client_day.py --client-slug acme
"""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLIENTS_DIR = REPO_ROOT / "clients"

PHASE_LABELS = {
    "00_intake": "Map",
    "01_diagnosis": "Map",
    "02_solution": "Design",
    "03_delivery": "Build",
    "04_training": "Operate",
    "05_proof": "Scale",
}


def client_day(slug: str) -> dict[str, object]:
    """Return a daily command summary for the client workspace."""
    ws = CLIENTS_DIR / slug
    if not ws.exists():
        raise FileNotFoundError(f"client workspace not found: {ws}")

    today = _dt.date.today().isoformat()
    phase_status: list[dict[str, object]] = []
    for phase in PHASE_LABELS:
        pdir = ws / phase
        if not pdir.exists():
            phase_status.append({"phase": phase, "doctrine": PHASE_LABELS[phase], "exists": False, "file_count": 0})
            continue
        count = sum(1 for _ in pdir.glob("*.md"))
        phase_status.append({"phase": phase, "doctrine": PHASE_LABELS[phase], "exists": True, "file_count": count})

    # Open risks quick read
    risks_path = ws / "05_proof" / "open_risks.md"
    open_risks_count = 0
    if risks_path.exists():
        text = risks_path.read_text(encoding="utf-8")
        # Count table rows under "Open risks" (lines starting with '|' that are not headers)
        open_risks_count = sum(
            1 for line in text.splitlines()
            if line.startswith("|") and "open" in line.lower() and "---" not in line
        )

    return {
        "client": slug,
        "date": today,
        "phases": phase_status,
        "open_risks": open_risks_count,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Daily client command summary.")
    parser.add_argument("--client-slug", required=True)
    args = parser.parse_args()

    try:
        report = client_day(args.client_slug)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Client: {report['client']}  |  Date: {report['date']}")
    print("Doctrine: Map -> Design -> Build -> Operate -> Scale")
    print()
    for p in report["phases"]:
        flag = "ok" if p["exists"] and p["file_count"] else "--"
        print(f"  [{flag}] {p['phase']:<14} ({p['doctrine']:<7}) files={p['file_count']}")
    print()
    print(f"Open risks flagged: {report['open_risks']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
