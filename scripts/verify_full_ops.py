"""Orchestrator that runs every Dealix Company OS verifier in sequence.

Each step is independent — a failure in one step does not stop the
others. The final exit code is non-zero if any step failed, so CI
fails on any failure but you still see the full picture.

Scripts that don't yet exist in the repo (legacy stages) are skipped
with a warning rather than a hard failure.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent

CHECKS: list[list[str]] = [
    [sys.executable, "scripts/verify_document_quality.py"],
    [sys.executable, "scripts/verify_company_os_deep.py"],
    # Future stages — included when they land in the repo:
    [sys.executable, "scripts/verify_master_tree.py"],
    [sys.executable, "scripts/verify_public_safety.py"],
    [sys.executable, "scripts/verify_private_boundary.py"],
]


def main() -> int:
    failed: list[str] = []
    skipped: list[str] = []

    for cmd in CHECKS:
        script = cmd[1]
        if not (REPO_ROOT / script).exists():
            skipped.append(script)
            print(f"\n== Skipping (not present): {script} ==")
            continue

        print(f"\n== Running: {' '.join(cmd)} ==")
        result = subprocess.run(cmd, cwd=REPO_ROOT)
        if result.returncode != 0:
            failed.append(" ".join(cmd))

    if skipped:
        print("\nSKIPPED (not present yet):")
        for item in skipped:
            print(f"- {item}")

    if failed:
        print("\nFAILED CHECKS:")
        for item in failed:
            print(f"- {item}")
        return 1

    print("\nPASS: Dealix full ops verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
