#!/usr/bin/env python3
"""Generate the daily approval-first draft queue (Distribution OS).

Loads prospects, generates one governed "next best" draft per prospect, writes
the queue to ``data/drafts/drafts.jsonl`` and a review report to
``reports/distribution/DRAFT_QUEUE_REVIEW.md``. Never sends anything.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auto_client_acquisition.distribution_os import generate_drafts, load_prospects  # noqa: E402
from auto_client_acquisition.distribution_os.report import render_draft_queue_review  # noqa: E402
from auto_client_acquisition.distribution_os.store import (  # noqa: E402
    drafts_path,
    reports_dir,
    write_jsonl,
    write_text,
)


def main() -> int:
    prospects = load_prospects()
    drafts = generate_drafts(prospects)

    out = write_jsonl(drafts_path(), [d.to_dict() for d in drafts])
    report = write_text(reports_dir() / "DRAFT_QUEUE_REVIEW.md", render_draft_queue_review(drafts))

    pending = sum(1 for d in drafts if d.status in {"pending_approval", "generated"})
    print(f"prospects: {len(prospects)} | drafts: {len(drafts)} | pending_approval: {pending}")
    print(f"wrote: {out.relative_to(ROOT)}")
    print(f"wrote: {report.relative_to(ROOT)}")
    print("DEALIX_DISTRIBUTION_DRAFTS=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
