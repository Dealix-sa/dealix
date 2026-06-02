#!/usr/bin/env python3
"""Generate the follow-up queue (Distribution OS).

Builds cadence-driven follow-ups from prospects, writes
``data/followups/followups.jsonl`` and ``reports/distribution/FOLLOWUP_QUEUE.md``.
Manual channels only; only due items are highlighted. Never sends anything.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auto_client_acquisition.distribution_os import build_followups, load_prospects  # noqa: E402
from auto_client_acquisition.distribution_os.report import render_followup_queue  # noqa: E402
from auto_client_acquisition.distribution_os.store import (  # noqa: E402
    followups_path,
    reports_dir,
    write_jsonl,
    write_text,
)


def main() -> int:
    prospects = load_prospects()
    followups = build_followups(prospects)

    out = write_jsonl(followups_path(), [f.to_dict() for f in followups])
    report = write_text(reports_dir() / "FOLLOWUP_QUEUE.md", render_followup_queue(followups))

    due = sum(1 for f in followups if f.status == "due")
    print(f"followups: {len(followups)} | due now: {due}")
    print(f"wrote: {out.relative_to(ROOT)}")
    print(f"wrote: {report.relative_to(ROOT)}")
    print("DEALIX_FOLLOWUP_QUEUE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
