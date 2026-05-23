"""Verify the execution_engine evidence automation.

Runs the checklist updater and report generator against the fixture and
asserts stage/stage_exit_checklist.csv and stage/evidence_report.md are
written.
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
        from execution_engine.evidence_checker import check_evidence_for_stage
        from execution_engine.evidence_report_generator import generate_evidence_report
        from execution_engine.stage_checklist_updater import update_checklist
        from execution_engine.stage_reader import read_current_stage
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL import — {exc!r}")
        print("\nverify_stage_evidence_automation: FAIL (1 check)")
        return 1

    stage_info = read_current_stage(FIXTURE_PATH)
    stage_num = int(stage_info.get("stage", 0))
    checks = check_evidence_for_stage(FIXTURE_PATH, stage_num)

    checklist_path = update_checklist(FIXTURE_PATH, checks)
    if not checklist_path.exists():
        print(f"FAIL checklist not written at {checklist_path}")
        failures.append("checklist_missing")
    else:
        content = checklist_path.read_text(encoding="utf-8")
        if "criterion" not in content or "status" not in content:
            print("FAIL checklist CSV header is malformed")
            failures.append("checklist_header")
        else:
            print(f"PASS checklist written — {checklist_path}")

    report_path = generate_evidence_report(FIXTURE_PATH, checks)
    if not report_path.exists():
        print(f"FAIL report not written at {report_path}")
        failures.append("report_missing")
    else:
        content = report_path.read_text(encoding="utf-8")
        if "Stage Evidence Report" not in content:
            print("FAIL evidence_report.md missing expected heading")
            failures.append("report_heading")
        else:
            print(f"PASS report written — {report_path}")

    if failures:
        print(f"\nverify_stage_evidence_automation: FAIL ({len(failures)} checks)")
        return 1
    print("\nverify_stage_evidence_automation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
