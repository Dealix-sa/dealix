"""Dealix 24/7 Growth Factory - daily runner.

Generates the daily CEO control surface: mission control, business score,
assurance, acquisition report, stoplight.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


CLI_TASKS = [
    ["-m", "dealix_cli", "mission-control"],
    ["-m", "dealix_cli", "business-score"],
    ["-m", "dealix_cli", "assurance"],
]

SCRIPT_TASKS = [
    ["scripts/generate_acquisition_daily_report.py"],
    ["scripts/generate_stoplight_report.py"],
]


def run(cmd: list[str]) -> int:
    print("+", " ".join(cmd))
    result = subprocess.run(cmd, check=False)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()

    root = Path(args.private_ops).resolve()
    root.mkdir(parents=True, exist_ok=True)

    failures = 0
    for task in CLI_TASKS:
        rc = run([sys.executable, *task, "--private-ops", str(root)])
        if rc != 0:
            failures += 1
    for task in SCRIPT_TASKS:
        script_path = Path(task[0])
        if not script_path.exists():
            print(f"skip (missing): {script_path}")
            continue
        rc = run([sys.executable, *task, "--private-ops", str(root)])
        if rc != 0:
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
