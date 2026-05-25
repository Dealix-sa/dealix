"""Verify the dealix_cli module.

Runs `python -m dealix_cli --help` and
`python -m dealix_cli stage --private-ops /tmp/fake` via subprocess. Both
should exit cleanly.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "dealix_cli", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return proc.returncode, proc.stdout, proc.stderr


def main() -> int:
    failures: list[str] = []

    rc, out, err = run(["--help"])
    if rc != 0:
        print(f"FAIL --help exited {rc} stderr={err.strip()}")
        failures.append("help")
    elif "Dealix Company OS" not in out and "usage" not in out.lower():
        print("FAIL --help output missing expected usage banner")
        failures.append("help_output")
    else:
        print("PASS python -m dealix_cli --help")

    rc, out, err = run(["stage", "--private-ops", "/tmp/fake"])
    if rc != 0:
        print(f"FAIL stage exited {rc} stderr={err.strip()}")
        failures.append("stage")
    else:
        print("PASS python -m dealix_cli stage --private-ops /tmp/fake")

    if failures:
        print(f"\nverify_cli: FAIL ({len(failures)} checks)")
        return 1
    print("\nverify_cli: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
