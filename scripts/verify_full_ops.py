"""Dealix full-ops verifier.

Runs the suite of small, focused verifiers that guard the public/private
boundary, the CEO dashboard, and the weekly operating loop.  Each check is
a separate script so it can be wired into branch-protection independently.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CHECKS: list[list[str]] = [
    ["python", "scripts/verify_dashboard.py"],
    ["python", "scripts/verify_dashboard_targets.py"],
    ["python", "scripts/verify_weekly_playbook_rule.py"],
]


def run_check(cmd: list[str]) -> tuple[str, bool, str]:
    label = " ".join(cmd)
    try:
        result = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        return label, False, f"command not found: {exc}"

    output = result.stdout.strip()
    if result.stderr.strip():
        output = f"{output}\n{result.stderr.strip()}".strip()
    return label, result.returncode == 0, output


def main() -> int:
    failures: list[tuple[str, str]] = []

    for cmd in CHECKS:
        label, ok, output = run_check(cmd)
        if ok:
            print(f"PASS: {label}")
            if output:
                print(output)
        else:
            print(f"FAIL: {label}")
            if output:
                print(output)
            failures.append((label, output))

    if failures:
        print()
        print(f"Full-ops verification failed ({len(failures)} check(s)):")
        for label, _ in failures:
            print(f"- {label}")
        return 1

    print()
    print("PASS: full-ops verification clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
