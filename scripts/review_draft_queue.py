#!/usr/bin/env python3
"""Render the draft queue review report from the current draft store.

Read-only over ``data/drafts/drafts.jsonl``; (re)writes
``reports/distribution/DRAFT_QUEUE_REVIEW.md`` for the founder's approval pass.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auto_client_acquisition.distribution_os.models import Draft  # noqa: E402
from auto_client_acquisition.distribution_os.report import render_draft_queue_review  # noqa: E402
from auto_client_acquisition.distribution_os.store import (  # noqa: E402
    drafts_path,
    read_jsonl,
    reports_dir,
    write_text,
)


def main() -> int:
    rows = read_jsonl(drafts_path())
    drafts = [Draft.from_dict(r) for r in rows]
    report = write_text(reports_dir() / "DRAFT_QUEUE_REVIEW.md", render_draft_queue_review(drafts))

    pending = sum(1 for d in drafts if d.status in {"pending_approval", "generated"})
    print(f"drafts in queue: {len(drafts)} | pending_approval: {pending}")
    print(f"wrote: {report.relative_to(ROOT)}")
    print("DEALIX_DRAFT_QUEUE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
