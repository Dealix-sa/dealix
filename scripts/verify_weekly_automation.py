"""Verify weekly automation modules can be invoked.

Imports `ops_runtime.weekly_review_generator` and
`ops_runtime.weekly_metrics_writer`, invokes them against a temp directory,
and asserts the expected output files appear.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def main() -> int:
    failures: list[str] = []
    try:
        from ops_runtime.weekly_review_generator import generate_weekly_review
        from ops_runtime.weekly_metrics_writer import write_weekly_metrics
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL import — {exc!r}")
        print("\nverify_weekly_automation: FAIL (1 check)")
        return 1

    print("PASS imported ops_runtime.weekly_review_generator")
    print("PASS imported ops_runtime.weekly_metrics_writer")

    metrics: dict = {
        "as_of": "2026-05-23",
        "period": "2026-W21",
        "pipeline": {"leads_new": 0, "leads_qualified": 0, "dms_sent_with_consent": 0,
                     "samples_sent": 0, "proposals_out": 0, "estimated_acv_open_sar": 0},
        "revenue": {"booked_mtd_sar": 0},
        "delivery": {"sprints_in_flight": 0, "sprints_at_risk": 0},
        "learning": {"experiments_active": 0},
        "trust": {"incidents_open": 0, "approval_queue_depth": 0},
    }

    with tempfile.TemporaryDirectory() as tmp_str:
        tmp = Path(tmp_str)
        try:
            review_path = generate_weekly_review(metrics, tmp)
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL generate_weekly_review raised — {exc!r}")
            failures.append("review")
        else:
            if not review_path.exists():
                print(f"FAIL weekly review not written at {review_path}")
                failures.append("review_file")
            else:
                print(f"PASS generate_weekly_review wrote {review_path.relative_to(tmp)}")

        try:
            metrics_path = write_weekly_metrics(metrics, tmp)
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL write_weekly_metrics raised — {exc!r}")
            failures.append("metrics")
        else:
            if not metrics_path.exists():
                print(f"FAIL weekly metrics not written at {metrics_path}")
                failures.append("metrics_file")
            else:
                print(f"PASS write_weekly_metrics wrote {metrics_path.relative_to(tmp)}")

    if failures:
        print(f"\nverify_weekly_automation: FAIL ({len(failures)} checks)")
        return 1
    print("\nverify_weekly_automation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
