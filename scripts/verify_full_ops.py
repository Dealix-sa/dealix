#!/usr/bin/env python3
"""
verify_full_ops.py — top-level orchestrator.

Runs every verify_* script under scripts/ and reports a single
pass/fail. The CI workflow `dealix-full-ops.yml` invokes this.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
REPO = SCRIPTS.parent

EXCLUDE = {
    Path(__file__).name,
}


def main() -> int:
    targets = sorted(
        p for p in SCRIPTS.glob("verify_*.py")
        if p.name not in EXCLUDE
    )

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
