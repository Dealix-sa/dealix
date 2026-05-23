"""Run every Dealix Company OS verifier in sequence.

A single command for "is the company operating system green?"
"""

import subprocess
import sys

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
        print(f"\n== Running: {' '.join(cmd)} ==")
        result = subprocess.run(cmd)
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
