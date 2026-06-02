#!/usr/bin/env python3
"""Compute distribution metrics over the draft + follow-up queues.

Reads the JSONL stores and prospects, writes
``reports/distribution/DISTRIBUTION_METRICS.md``. Revenue is never invented —
only paid evidence elsewhere in the platform counts as revenue.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auto_client_acquisition.distribution_os import compute_metrics, load_prospects  # noqa: E402
from auto_client_acquisition.distribution_os.models import Draft, Followup  # noqa: E402
from auto_client_acquisition.distribution_os.report import render_metrics  # noqa: E402
from auto_client_acquisition.distribution_os.store import (  # noqa: E402
    drafts_path,
    followups_path,
    read_jsonl,
    reports_dir,
    write_text,
)


def main() -> int:
    drafts = [Draft.from_dict(r) for r in read_jsonl(drafts_path())]
    followups = [Followup.from_dict(r) for r in read_jsonl(followups_path())]
    prospects = load_prospects()

    metrics = compute_metrics(drafts, followups, prospects)
    report = write_text(reports_dir() / "DISTRIBUTION_METRICS.md", render_metrics(metrics))

    print(
        f"drafts: {metrics['drafts_total']} | followups: {metrics['followups_total']} "
        f"| due: {metrics['followups_due']}"
    )
    print(f"wrote: {report.relative_to(ROOT)}")
    print("DEALIX_DISTRIBUTION_METRICS=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
