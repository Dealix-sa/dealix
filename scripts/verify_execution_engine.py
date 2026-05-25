"""Verify execution_engine package imports cleanly and behaves correctly.

Runs a tiny smoke test against a temp private-ops directory so we know the
evidence scanner and checklist updater work end-to-end.
"""

from __future__ import annotations

import csv
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _smoke_test() -> list[str]:
    from execution_engine import scan_evidence, update_checklist

    failures: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        ops = Path(tmp)
        (ops / "stage").mkdir()
        (ops / "stage" / "current_stage.md").write_text(
            "# Current stage\n\nstage: pipeline\n",
            encoding="utf-8",
        )
        (ops / "pipeline").mkdir()
        (ops / "pipeline" / "pipeline_tracker.csv").write_text(
            "id,lead_name,stage,next_action\n",
            encoding="utf-8",
        )

        report = scan_evidence(ops)
        if report.stage != "pipeline":
            failures.append(f"scan_evidence returned wrong stage: {report.stage}")
        if report.passed:
            failures.append("scan_evidence passed against empty pipeline (should fail)")

        # Populate 25 rows, expect pass.
        with (ops / "pipeline" / "pipeline_tracker.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["id", "lead_name", "stage", "next_action"]
            )
            writer.writeheader()
            for i in range(1, 26):
                writer.writerow(
                    {
                        "id": str(i),
                        "lead_name": f"lead_{i}",
                        "stage": "new",
                        "next_action": "research",
                    }
                )

        report = scan_evidence(ops)
        if not report.passed:
            failures.append(
                f"scan_evidence failed against valid pipeline: {[r.detail for r in report.results]}"
            )

        checklist = ops / "stage" / "stage_exit_checklist.csv"
        update_checklist(checklist, report)
        if not checklist.exists():
            failures.append("update_checklist did not write the file")
        else:
            text = checklist.read_text(encoding="utf-8")
            if "done" not in text:
                failures.append("checklist did not mark passing checks as done")

    return failures


def main() -> None:
    print("== Execution Engine ==")
    failures = _smoke_test()
    if failures:
        print("FAIL:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    print("PASS: Execution engine import + smoke test green.")


if __name__ == "__main__":
    main()
