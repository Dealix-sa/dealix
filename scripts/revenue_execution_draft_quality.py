#!/usr/bin/env python3
"""Revenue Execution OS — draft quality gate.

Scores every stored draft and writes reports/distribution/DRAFT_QUEUE_REVIEW.md.
With --fail-on-issues, exits non-zero if any draft fails the gate (for CI).

    python3 scripts/revenue_execution_draft_quality.py [--output DIR] [--fail-on-issues]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from auto_client_acquisition.revenue_execution_os import stores
from auto_client_acquisition.revenue_execution_os.daily_report import (
    render_draft_quality_report,
)
from auto_client_acquisition.revenue_execution_os.draft_quality import review_drafts


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Score stored drafts (quality gate)")
    ap.add_argument("--output", default="reports/distribution", help="output directory")
    ap.add_argument("--fail-on-issues", action="store_true", help="exit 1 if any draft fails")
    args = ap.parse_args(argv)

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "DRAFT_QUEUE_REVIEW.md"
    path.write_text(render_draft_quality_report(), encoding="utf-8")
    print(f"wrote {path}")

    drafts = stores.DRAFTS.list(limit=1_000_000)
    prospects = {p.prospect_id: p for p in stores.PROSPECTS.list(limit=1_000_000)}
    report = review_drafts(drafts, prospects)
    print(
        f"drafts={report.total} passed={report.passed} failed={report.failed} pass_rate={report.pass_rate}"
    )
    if args.fail_on_issues and report.failed:
        print("FAIL: one or more drafts did not pass the quality gate")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
