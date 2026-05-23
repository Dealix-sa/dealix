"""Dealix full operations verifier.

Runs the full suite of Dealix operating verifiers in sequence and
collects failures.

Run:
    python scripts/verify_full_ops.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CHECKS = [
    ["python", "scripts/verify_master_tree.py"],
    ["python", "scripts/verify_document_quality.py"],
    ["python", "scripts/verify_company_os_deep.py"],
    ["python", "scripts/verify_public_safety.py"],
    ["python", "scripts/verify_private_boundary.py"],
]


def main() -> int:
    failed: list[str] = []

    for cmd in CHECKS:
        script_path = ROOT / cmd[1]
        if not script_path.exists():
            print(f"\n== Skipping (not present): {' '.join(cmd)} ==")
            continue

        print(f"\n== Running: {' '.join(cmd)} ==")
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            failed.append(" ".join(cmd))

    if failed:
        print("\nFAILED CHECKS:")
        for item in failed:
            print("-", item)
        return 1

    print("\nPASS: Dealix full ops verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
