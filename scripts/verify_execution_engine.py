"""Verify the execution_engine smoke path.

Imports execution_engine, runs a smoke test against tests/fixtures/private_ops/,
asserts can_advance returns blockers for the current fixture state.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "private_ops"


def main() -> int:
    failures: list[str] = []
    try:
        from execution_engine import (
            can_advance,
            check_evidence_for_stage,
            read_current_stage,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL import execution_engine — {exc!r}")
        print("\nverify_execution_engine: FAIL (1 check)")
        return 1

    print("PASS import execution_engine")

    if not FIXTURE_PATH.exists():
        print(f"FAIL fixture missing — {FIXTURE_PATH}")
        print("\nverify_execution_engine: FAIL (1 check)")
        return 1
    print(f"PASS fixture present — {FIXTURE_PATH}")

    stage_info = read_current_stage(FIXTURE_PATH)
    stage_num = int(stage_info.get("stage", 0))
    print(f"PASS read_current_stage — stage={stage_num} status={stage_info.get('status')}")

    checks = check_evidence_for_stage(FIXTURE_PATH, stage_num)
    if not isinstance(checks, list) or not checks:
        print("FAIL check_evidence_for_stage returned no checks")
        failures.append("checks_empty")
    else:
        print(f"PASS check_evidence_for_stage — {len(checks)} criteria evaluated")

    advanceable, blockers = can_advance(checks)
    if advanceable:
        print("FAIL can_advance — fixture should not be advanceable in empty state")
        failures.append("advanceable_should_be_false")
    elif not blockers:
        print("FAIL can_advance — no blockers reported")
        failures.append("blockers_should_be_nonempty")
    else:
        print(f"PASS can_advance — blocked with {len(blockers)} blocker(s)")

    if failures:
        print(f"\nverify_execution_engine: FAIL ({len(failures)} checks)")
        return 1
    print("\nverify_execution_engine: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
