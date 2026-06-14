"""Umbrella verifier for the Dealix priority operating stack.

Runs the public verifiers that must pass before any change merges to main.
This script is intentionally minimal: each layer keeps its own verifier and
this file orchestrates them so CI has one entry point.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERIFIERS = [
    "scripts/verify_priority_operating_layer.py",
    "scripts/verify_priority_execution_sprint.py",
]


def run(script: str) -> int:
    path = ROOT / script
    if not path.exists():
        print(f"SKIP: {script} (not present)")
        return 0
    print(f"\n$ python {script}")
    result = subprocess.run([sys.executable, str(path)], cwd=str(ROOT), check=False)  # noqa: S603
    return result.returncode


def main() -> None:
    failures: list[str] = []
    for verifier in VERIFIERS:
        rc = run(verifier)
        if rc != 0:
            failures.append(verifier)

    if failures:
        print("\nverify_full_ops failed:")
        for f in failures:
            print("-", f)
        raise SystemExit(1)

    print("\nPASS: full ops priority stack verified.")


if __name__ == "__main__":
    main()
