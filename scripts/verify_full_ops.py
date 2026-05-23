#!/usr/bin/env python3
"""
verify_full_ops.py — orchestrator for the Master Tree verify scripts.

Runs the verify_* scripts that the Master Tree declares (under
scripts/generate_master_tree.py) and reports a single pass/fail.

Pre-existing legacy verify scripts under scripts/ are NOT executed here;
they live behind their own workflows and have their own dependency
requirements. Use `--all` to run every verify_*.py — primarily useful
on a developer machine with the full requirements installed.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
REPO = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from generate_master_tree import SCRIPTS as MASTER_TREE_SCRIPTS  # noqa: E402


SELF = Path(__file__).name


def master_tree_targets() -> list[Path]:
    """Return absolute paths to the verify_* scripts declared in the manifest."""
    names = MASTER_TREE_SCRIPTS["scripts"]
    out: list[Path] = []
    for name in names:
        if not name.startswith("verify_"):
            continue
        if name == SELF:
            continue
        target = SCRIPTS / name
        if target.exists():
            out.append(target)
    return sorted(out)


def all_verify_targets() -> list[Path]:
    return sorted(p for p in SCRIPTS.glob("verify_*.py") if p.name != SELF)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--all", action="store_true",
        help="Run every scripts/verify_*.py, not just the Master Tree ones.",
    )
    args = parser.parse_args(argv)

    targets = all_verify_targets() if args.all else master_tree_targets()

    failures: list[str] = []
    for script in targets:
        rel = script.relative_to(REPO)
        try:
            result = subprocess.run(
                [sys.executable, str(script)],
                cwd=REPO, capture_output=True, text=True, timeout=120,
            )
        except subprocess.TimeoutExpired:
            print(f"[FAIL] {rel}: timeout")
            failures.append(str(rel))
            continue
        status = "OK" if result.returncode == 0 else "FAIL"
        print(f"[{status}] {rel}")
        if result.returncode != 0:
            failures.append(str(rel))
            tail = result.stdout.strip().splitlines()[-5:] + result.stderr.strip().splitlines()[-5:]
            for line in tail:
                print(f"       {line}")

    print()
    if failures:
        print(f"[FAIL] {len(failures)} verify scripts failed:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"[OK] All {len(targets)} verify scripts passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
